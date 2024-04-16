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
from dataclasses import dataclass, fields
from pathlib import Path
from tempfile import NamedTemporaryFile


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
        v = []
        for field in fields(self):
            value = getattr(self, field.name)
            stringified = pyobj_to_psql_data(value)
            v.append(stringified)

        return "\t".join(v)


@dataclass
class Article:
    id: int
    lemma: str
    dictionary: id
    rendered: str
    pos: str | None = None
    lang: str | None = None
    article_number: int | None = None
    additional_properties: str | None = None


def pyobj_to_psql_data(obj):
    if obj is None:
        return "\\N"
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, int):
        return str(obj)
    else:
        raise TypeError("unhandled type of obj", type(obj))


def main():
    gut_root = get_gut_root()
    p = Path(gut_root) / "giellalt"

    dictionaries = []
    articles = []
    for i, directory in enumerate(p.glob("dict-*"), start=1):
        # strip away the "dict-" prefix
        name = directory.name[5:]
        if len(name) != 7:
            # skip ...-x-private  and other such dicts
            continue
        l1, l2 = name.split("-")
        d = Dictionary(id=i, name=f"gt-{name}", lang1=l1, lang2=l2)
        dictionaries.append(d)

        with NamedTemporaryFile() as f:
            try:
                n_entries = merge_giella_dicts(directory / "src", f.name)
            except FileNotFoundError:
                print(f"no src files in dict {l1}-{l2}, skipping")
            except NotADirectoryError:
                print(f"no src directory in dict {l1}-{l2}, skipping")
            else:
                print(f"{l1}-{l2}: {n_entries}")

    lines = "\n".join(d.to_tsv_string() for d in dictionaries)
    with open("init/data_dictionaries.txt", "w") as f:
        f.write(lines)


if __name__ == "__main__":
    raise SystemExit(main())
