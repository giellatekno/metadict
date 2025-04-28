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

import gzip
from pathlib import Path
from utils.utils import articles_to_sql, dictionary_to_sql
from classes import *

parsers = {
    "gt": GTParser,
    "gtsme": GTSmeParser,
    "qvigstad": QvigstadParser,
    "sammallahti": SammallahtiParser,
    "fysihkka": FysihkkaParser,
    "girjjalasvuoda": GirjjalasvuodaParser,
    "algosatnegirji": AlgosatnegirjiParser,
    "ruoktumet": RuoktumetParser,
    "pedagogalas": PedPsyParser,
    "nettisanakirja": NettisanakirjaParser,
    "konrad_nielsen": KonradParser,
    "skoleordbok": SkoleordbokParser,
    "apotekordliste": ApotekordlisteParser,
    "medisinsk": MedisinskParser,
}


def parse_dictionary(file: Path, dictionary_id):
    try:
        parser = parsers[file.stem.split("-")[0]](dictionary_id, file)
    except KeyError:
        raise Exception("\033[93m" + f"Parsing of dictionary \"{file.stem}\" not implemented" + "\033[0m")
    except Exception as e:
        raise Exception("\033[91m" + f"Error parsing dictionary \"{file.stem}\": {e}" + "\033[0m")
    return parser.get_parsed_data()


def main():
    # dictionaries = []
    # articles = []

    # target = "../db/init"
    sql_folder = Path("sql_files")
    if not sql_folder.exists():
        sql_folder.mkdir()

    dicts_dir = Path("dicts")

    dictionary_id = 1
    
    for file in dicts_dir.iterdir():        
        print(f"Parsing {file}")
        try:
            d, a = parse_dictionary(file, dictionary_id)
        except Exception as e:
            print(e)
            continue

        dictionary_to_sql(d, file.stem)
        articles_to_sql(a, file.stem)

        # dictionaries.append(d)
        # articles.extend(a)    
        dictionary_id += 1

    # lines = "\n".join(d.to_tsv_string() for d in dictionaries)
    # with gzip.open(Path(target) / "data_dictionaries.txt.gz", "wb") as f:
    #     f.write(lines.encode())
    

    # article_lines = "\n".join(d.to_tsv_string() for d in articles)
    # with gzip.open(Path(target) / "data_articles.txt.gz", "wb") as f:
    #     f.write(article_lines.encode())


if __name__ == "__main__":
    raise SystemExit(main())
