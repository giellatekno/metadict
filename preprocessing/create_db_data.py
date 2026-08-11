#!/usr/bin/env python3
"""
This script takes as input all files in the dicts/ folder, and creates
output files in the sql_files/.
Two types of .sql files will be created, one with a prefix of "a-", and
one with a prefix of "d-". The "-d" files is the sql for inserting a row
in the "dictionaries" table of the database, and the "a-"-.sql file is
the sql for inserting all the articles. The articles needs to know which
dictionary they belong to, and inserting data into the database is done
in 2 steps, first create the dictionary entry, to get the id, and then
replace "$DICTIONARY$" in the "a-" files in the fly while executing the
sql.

Use the script "db/insert_dictionary.py" to insert these .sql files
into a live database. Refer to that script for further information.

Use --only to regenerate a subset, e.g. --only 'gt*' when only the
giellatekno dictionaries have been updated. The other .sql files are then
left alone, and the dictionaries they came from need not be present in
dicts/.
"""

import argparse
import fnmatch
import shutil
from pathlib import Path

import classes
from utils.utils import red, yellow

parsers = {
    "gt": classes.GTParser,
    "gtsme": classes.GTSmeParser,
    "qvigstad": classes.QvigstadParser,
    "sammallahti": classes.SammallahtiParser,
    "fysihkka": classes.FysihkkaParser,
    "girjjalasvuoda": classes.GirjjalasvuodaParser,
    "algosatnegirji": classes.AlgosatnegirjiParser,
    "ruoktumet": classes.RuoktumetParser,
    "pedagogalas": classes.PedPsyParser,
    "vest": classes.VestParser,
    "konrad_nielsen": classes.KonradParser,
    "skoleordbok": classes.SkoleordbokParser,
    "apotekordliste": classes.ApotekordlisteParser,
    "medisinsk": classes.MedisinskParser,
    "gaerjiste": classes.GaerjisteParser,
    "bergsland_magga": classes.BergslandMaggaParser,
    # "kintel": classes.KintelParser,
}


def parse_dictionary(file: Path, dictionary_id):
    try:
        parser = parsers[file.stem.split("-")[0]](dictionary_id, file)
    except KeyError:
        raise Exception(yellow(f'Parsing of dictionary "{file.stem}" not implemented'))
    except Exception as e:
        raise Exception(red(f'Error parsing dictionary "{file.stem}": {e}'))
    return parser.get_parsed_data()


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--only",
        metavar="GLOB",
        default="*",
        help="only parse dictionaries whose name matches GLOB, e.g. 'gt*'. "
        "sql_files/ is then left in place, and only the matching files in it "
        "are overwritten (default: parse everything, and wipe sql_files/ "
        "first)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    parse_everything = args.only == "*"

    sql_folder = Path("sql_files")
    if parse_everything and sql_folder.exists():
        shutil.rmtree(sql_folder)
    sql_folder.mkdir(exist_ok=True)

    dicts_dir = Path("dicts")

    parsed = 0
    # sorted, so that a filtered run gives the same ids as a full one
    for dictionary_id, file in enumerate(sorted(dicts_dir.iterdir()), start=1):
        if not fnmatch.fnmatch(file.stem, args.only):
            continue

        print(f"Parsing {file}")
        try:
            d, a = parse_dictionary(file, dictionary_id)
        except Exception as e:
            print(e)
            continue

        with open(f"sql_files/d-{file.stem}.sql", "w") as f:
            f.write(d.to_sql())

        with open(f"sql_files/a-{file.stem}.sql", "w") as f:
            sql = "INSERT INTO articles (lemma, dictionary, rendered, pos, \
                    lang, article_number, additional_properties ) VALUES"
            f.write(sql)

            last_i = len(a) - 1
            for i, article in enumerate(a):
                f.write(article.to_sql())
                f.write(";\n" if i == last_i else ",\n")

        parsed += 1

    if parsed == 0:
        exit(red(f'Error: no dictionaries in dicts/ matched "{args.only}"'))


if __name__ == "__main__":
    raise SystemExit(main())
