#!/usr/bin/env python3

"""This script creates the init/data_dictionaries.txt file.
Data about dictionaries is read from gut.

That file is a tab separated file, where one line is one row.
The columns are

NAME LANG1 LANG2 AUTHOR
"""

import os
import os.path
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, fields
from pathlib import Path


def get_gut_root():
    app_toml_path = os.path.expanduser("~/.config/gut/app.toml")
    with open(app_toml_path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            try:
                k, v = line.split("=", maxsplit=1)
            except IndexError:
                continue
            k = k.strip()
            v = v.strip()
            if k != "root":
                continue

            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]

            return v


try:
    # if GUTHOME (the gut directory) environment variable is set...
    GUTROOT = get_gut_root()
    script_directory = os.path.join(GUTROOT, "giellalt", "giella-core", "dicts", "scripts")
    # ...and the scripts directory have been moved to git ...
    if not os.path.isdir(script_directory):
        raise KeyError
finally:
    sys.path.append(script_directory)
    from merge_giella_dicts import merge_giella_dicts


def pyobj_to_psql_data(obj):
    if obj is None:
        return "\\N"
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, int):
        return str(obj)
    else:
        raise TypeError("unhandled type of obj", type(obj))


def dataclass_to_tsv_string(dcls_inst):
    strings = []
    for field in fields(dcls_inst):
        value = getattr(dcls_inst, field.name)
        stringified = pyobj_to_psql_data(value)
        strings.append(stringified)

    return "\t".join(strings)


@dataclass
class Dictionary:
    id: int
    name: str
    lang1: str
    lang2: str
    is_ordered: bool = False
    author: str | None = None
    date_published: str | None = None
    isbn: str | None = None
    source: str | None = None

    def to_tsv_string(self):
        return dataclass_to_tsv_string(self)


@dataclass
class Article:
    id: int
    lemma: str
    dictionary: int
    rendered: str
    pos: str | None = None
    lang: str | None = None
    article_number: int | None = None
    additional_properties: str | None = None

    def to_tsv_string(self):
        return dataclass_to_tsv_string(self)


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
    gut_root = get_gut_root()
    p = Path(gut_root) / "giellalt"

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
    with open("init/data_dictionaries.txt", "w") as f:
        f.write(lines)

    article_lines = "\n".join(d.to_tsv_string() for d in articles)
    with open("init/data_articles.txt", "w") as f:
        f.write(article_lines)


if __name__ == "__main__":
    raise SystemExit(main())
