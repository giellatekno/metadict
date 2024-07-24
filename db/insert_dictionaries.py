"""
This script loads dictionaries from .sql files into a running database,
using `psql`. If the --container (-c) argument is given, the `psql` command
will be run inside the running podman container named "metadict-db", otherwise
the hosts local `psql` will be used.
"""

import argparse
import shlex
import subprocess
import sys
from pathlib import Path

# command to use if inserting into a database running in a container,
# the container is assumed to have the `psql` command locally.
PODMAN_PSQL_CMD = "podman exec -i metadict-db psql -U postgres -f -"

# command to use if executing against database running locally,
# the psql command is assumed to exist locally
LOCAL_PSQL_CMD = "psql -U postgres -d postgres -f -"


def abort(msg, warn_inconsistent=False):
    msg = f"Error: {msg}\n"
    if warn_inconsistent:
        msg += (
            "WARNING: THE DATABASE WAS MODIFIED, AND IS PROBABLY LEFT\n"
            "IN AN INCONSISTENT STATE, DO A MANUAL INSPECTION\n"
        )
    msg += "Aborting due to errors"
    sys.exit(msg)


def execute_sql(sql, run_in_container=False):
    if run_in_container:
        cmd = shlex.split(PODMAN_PSQL_CMD)
    else:
        cmd = shlex.split(LOCAL_PSQL_CMD)
    proc = subprocess.run(
        cmd,
        input=sql,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "sql-scripts-folder",
        type=Path,
        help="path of the folder containing the \"[a|d]-*.sql\" files",
    )
    parser.add_argument(
        "-c",
        "--container",
        action="store_true",
        help="run psql inside podman image 'metadict-db'",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    args = vars(args)
    run_in_container = args["container"]
    path = args["sql-scripts-folder"]
    if not path.is_dir():
        exit(
            "Error: argument 'sql-scripts-folder': Not a directory "
            f"({path})"
        )

    data = []
    for dictionary_file in path.glob("d-*.sql"):
        article_file = dictionary_file.with_name("a-" + dictionary_file.name[2:])
        if not article_file.exists():
            exit(f"corresponding article file not found: {article_file}")
        articles_sql = article_file.read_text()

        data.append((dictionary_file.read_text(), articles_sql))

    for dictionary_sql, articles_sql in data:
        insert_dictionary(dictionary_sql, articles_sql, run_in_container)

    print("all done")


def insert_dictionary(dictionary_sql, articles_sql, run_in_container):
    dictionary_creation_proc = execute_sql(
        dictionary_sql,
        run_in_container=run_in_container,
    )

    if dictionary_creation_proc.returncode != 0:
        print("ERROR while running sql to create dictionary.")
        if dictionary_creation_proc.stderr:
            print("STDERR:")
            print(dictionary_creation_proc.stderr)
        return 1
    else:
        stderr = dictionary_creation_proc.stderr
        if stderr:
            abort("non-empty stderr when running psql")

        stdout = dictionary_creation_proc.stdout
        try:
            dict_id = _parse_id(stdout)
        except ValueError:
            abort("could not parse id of new dictionary")
        print(
            f"new dictionary created, it has id: {dict_id}, "
            "inserting articles..."
        )

    articles_sql = articles_sql.replace("$DICTIONARY$", str(dict_id))
    articles_creation_proc = execute_sql(
        articles_sql,
        run_in_container=run_in_container,
    )

    stdout = articles_creation_proc.stdout
    stderr = articles_creation_proc.stderr
    ret = articles_creation_proc.returncode
    if ret != 0:
        abort(
            "non-0 returncode from psql when inserting dictionaries",
            warn_inconsistent=True,
        )

    if stderr:
        abort(
            "non-empty stderr from psql when inserting dictionaries",
            warn_inconsistent=True,
        )

    print(stdout)


def _parse_id(stdout):
    for line in stdout.split("\n"):
        try:
            num = int(line.strip())
        except ValueError:
            pass
        else:
            return num
    raise ValueError


if __name__ == "__main__":
    raise SystemExit(main())
