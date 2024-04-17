#!/usr/bin/env python3

"""This script appends Qvigstads dictionary to the init/data_dictionaries.txt file.

That file is a tab separated file, where one line is one row.
The columns are

NAME LANG1 LANG2 AUTHOR
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from utils.dataclasses import Dictionary, Article


def row_node_to_article(row_node, lang, article_id, article_number, dictionary_id):


    lemma = row_node[1].text.strip().replace("\n", " ")
    # print(lemma)
    pos = row_node[2].text.strip()

    # if not row_node[0].text.strip() and not row_node[3].text.strip():
    #     print(f"{article_number}: {lemma} - No translations!")
    # if row_node[0].text.strip() and row_node[3].text.strip():
    #     print(f"{article_number}: {lemma} - Two translations!")
    
    mgs = [row_node[0], row_node[3], row_node[4], row_node[5]]
    rendered = "<br>".join(ET.tostring(mg, encoding="unicode") for mg in mgs)
    rendered = rendered.replace("\n", "<br>").replace("\t", " ")

    return Article(
        id=article_id,
        dictionary=dictionary_id,
        lemma=lemma,
        rendered=rendered,
        lang=lang,
        pos=pos,
        article_number=article_number
    )



def main():
    dictionaries = []
    articles = []
    
    target = "../db/init"
    filename = 'qvigstad/Qvigstad Kalfjord_kopi.xml'
    name='Qvigstad-Kalfjord-sme-nob'

    with open(Path(target) / "data_dictionaries.txt", "r") as f:
        dictionary_id = len(f.readlines()) + 1
    
    with open(Path(target) / "data_articles.txt", "r") as f:
        article_id = len(f.readlines()) + 1
    
    d = Dictionary(
        id=dictionary_id,
        name=name,
        lang1='sme',
        lang2='nob',
        is_ordered=True,
        author='Just Qvigstad',
        date_published='1889', 
    )
    dictionaries.append(d)

    try:
        xml_file = ET.parse(filename)
    except Exception as e:
        print(e)
        exit(0)
    else:
        print(filename, "ok")

    for index, row in enumerate(xml_file.iter("row"), 1):
        
        try:
            article = row_node_to_article(row, 'sme', article_id, index, dictionary_id)
        except Exception as e:
            print(e)
            continue

        articles.append(article) 
        article_id += 1   
        
    lines = "\n".join(d.to_tsv_string() for d in dictionaries)
    with open(Path(target) / "data_dictionaries.txt", "a") as f:
        f.write("\n" + lines)

    article_lines = "\n".join(d.to_tsv_string() for d in articles)
    with open(Path(target) / "data_articles.txt", "a") as f:
        f.write("\n" + article_lines)


if __name__ == "__main__":
    raise SystemExit(main())
