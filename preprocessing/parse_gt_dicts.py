#!/usr/bin/env python3

"""This script creates the init/data_dictionaries.txt file.
Data about dictionaries is read from gut.

That file is a tab separated file, where one line is one row.
The columns are

NAME LANG1 LANG2 AUTHOR
"""

import os.path
import xml.etree.ElementTree as ET
from pathlib import Path
from utils.utils import get_gut_root
from utils.dataclasses import Dictionary, Article

def e_node_to_article(e_node, lang, article_id, dictionary_id):
    l_node = e_node.find("lg/l")
    if l_node is None:
        raise Exception("<e> node has no <lg><l>")

    lemma = l_node.text.strip("\n\t ").replace("\n", " ")
    mgs = e_node.findall("mg")
    rendered = "<br>".join(ET.tostring(mg, encoding="unicode") for mg in mgs)
    rendered = rendered.replace("\n", "<br>").replace("\t", " ")

    return Article(
        id=article_id,
        dictionary=dictionary_id,
        lemma=lemma,
        rendered=rendered,
        lang=lang,
    )


def main():

    target = "../db/init"

    dictionaries = []
    articles = []
    merged_dir = Path("merged")
    for dictionary_id, dictionary in enumerate(merged_dir.iterdir(), start=1):
        # strip away the "gt-" prefix and ".xml" suffix
        name = dictionary.name[3:-4]
        l1, l2 = name.split("-")
        d = Dictionary(
            id=dictionary_id,
            name=f"gt-{name}",
            lang1=l1,
            lang2=l2,
        )
        dictionaries.append(d)

        try:
            merged_xml = ET.parse(dictionary)
        except Exception as e:
            print(e)
            continue
        else:
            print(dictionary, "ok")

        for e in merged_xml.iter("e"):
            article_id = len(articles) + 1
            try:
                article = e_node_to_article(e, l1, article_id, dictionary_id)
            except Exception as e:
                print(e)
                continue
            articles.append(article)

    lines = "\n".join(d.to_tsv_string() for d in dictionaries)
    with open(Path(target) / "data_dictionaries.txt", "w") as f:
        f.write(lines)

    article_lines = "\n".join(d.to_tsv_string() for d in articles)
    with open(Path(target) / "data_articles.txt", "w") as f:
        f.write(article_lines)


if __name__ == "__main__":
    raise SystemExit(main())
