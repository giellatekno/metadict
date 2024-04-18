#!/usr/bin/env python3

from pathlib import Path
from utils.parsers import parse_dictionary

def main():
    dictionaries = []
    articles = []

    target = "../db/init"
    dicts_dir = Path("dicts")

    dictionary_id = 1

    for dir in dicts_dir.iterdir():
        
        if not dir.is_dir():
            continue
        
        for file in dir.iterdir():
            print(f"Parsing {file}")
            try:
                d, a = parse_dictionary(dir.name, file, dictionary_id)
            except Exception as e:
                print(e)
                continue
            
            dictionaries.append(d)
            articles.extend(a)    
            dictionary_id += 1



    lines = "\n".join(d.to_tsv_string() for d in dictionaries)
    with open(Path(target) / "data_dictionaries.txt", "w") as f:
        f.write(lines)

    article_lines = "\n".join(d.to_tsv_string() for d in articles)
    with open(Path(target) / "data_articles.txt", "w") as f:
        f.write(article_lines)


if __name__ == "__main__":
    raise SystemExit(main())
