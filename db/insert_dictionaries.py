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


def abort(msg, stderr=None, warn_inconsistent=False):
    msg = f"Error: {msg}\n"
    if warn_inconsistent:
        msg += (
            "WARNING: THE DATABASE WAS MODIFIED, AND IS PROBABLY LEFT\n"
            "IN AN INCONSISTENT STATE, DO A MANUAL INSPECTION\n"
        )
    if stderr is not None:
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8")
        assert isinstance(stderr, str)
        msg += "\n10 last lines of stderr:"
        msg += "\n".join(stderr.split("\n")[-10:])
    msg += "\ninsert_dictionaries.py: Aborting due to errors"
    sys.exit(msg)


def execute_sql(sql, run_in_container=False):
    if isinstance(sql, str):
        sql = sql.encode("utf-8")
    assert isinstance(sql, bytes)
    if run_in_container:
        cmd = shlex.split(PODMAN_PSQL_CMD)
    else:
        cmd = shlex.split(LOCAL_PSQL_CMD)
    proc = subprocess.run(
        cmd,
        input=sql,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "sql-scripts-folder",
        type=Path,
        help='path of the folder containing the "[a|d]-*.sql" files',
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
        exit(f"Error: argument 'sql-scripts-folder': Not a directory ({path})")

    data = []
    for dictionary_file in sorted(path.glob("d-*.sql*")):
        dict_name = dictionary_file.name[2:]
        article_file = dictionary_file.with_name("a-" + dictionary_file.name[2:])
        if not article_file.exists():
            abort(f"corresponding article file not found: {article_file}")
        articles_sql = article_file.read_bytes()

        data.append((dict_name, dictionary_file.read_bytes(), articles_sql))

    for dict_name, dictionary_sql, articles_sql in data:
        insert_dictionary(
            dict_name,
            dictionary_sql,
            articles_sql,
            run_in_container=run_in_container,
        )

    print("all done")


def insert_dictionary(dict_name, dictionary_sql, articles_sql, run_in_container):
    print(f"inserting dictionary '{dict_name}'")
    dictionary_creation_proc = execute_sql(
        dictionary_sql,
        run_in_container=run_in_container,
    )

    if dictionary_creation_proc.returncode != 0:
        abort("non-0 returncode from psql")

    stderr = dictionary_creation_proc.stderr
    if stderr:
        abort("non-empty stderr when running psql", stderr=stderr)

    stdout = dictionary_creation_proc.stdout
    try:
        dict_id = _parse_id(stdout.decode("utf-8"))
    except ValueError:
        abort("could not parse id of new dictionary")
    print(f"new dictionary created, it has id: {dict_id}, inserting articles...")

    articles_sql = articles_sql.replace(
        b"$DICTIONARY$",
        str(dict_id).encode("utf-8"),
    )
    articles_creation_proc = execute_sql(
        articles_sql,
        run_in_container=run_in_container,
    )

    stdout = articles_creation_proc.stdout.decode("utf-8")
    stderr = articles_creation_proc.stderr.decode("utf-8")
    ret = articles_creation_proc.returncode
    if ret != 0:
        abort(
            "non-0 returncode from psql when inserting dictionaries",
            stderr=stderr,
            warn_inconsistent=True,
        )

    if stderr:
        if stderr.startswith("psql:<stdin>:"):
            try:
                err_char_pos = int(stderr[13 : stderr.index(":", 13)])
            except ValueError:
                pass
            else:
                # show input around this position, for debugging
                print(articles_sql[err_char_pos - 50 : err_char_pos + 50])
        abort(
            "non-empty stderr from psql when inserting dictionaries",
            stderr=stderr,
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
