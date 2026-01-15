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
"""

from pathlib import Path
from utils.utils import yellow, red
import classes

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
    "nettisanakirja": classes.NettisanakirjaParser,
    "konrad_nielsen": classes.KonradParser,
    "skoleordbok": classes.SkoleordbokParser,
    "apotekordliste": classes.ApotekordlisteParser,
    "medisinsk": classes.MedisinskParser,
    "gaerjiste": classes.GaerjisteParser,
}


def parse_dictionary(file: Path, dictionary_id):
    try:
        parser = parsers[file.stem.split("-")[0]](dictionary_id, file)
    except KeyError:
        raise Exception(yellow(f'Parsing of dictionary "{file.stem}" not implemented'))
    except Exception as e:
        raise Exception(red(f'Error parsing dictionary "{file.stem}": {e}'))
    return parser.get_parsed_data()


def main():
    sql_folder = Path("sql_files")
    if not sql_folder.exists():
        sql_folder.mkdir()

    dicts_dir = Path("dicts")

    for dictionary_id, file in enumerate(dicts_dir.iterdir(), start=1):
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


if __name__ == "__main__":
    raise SystemExit(main())
