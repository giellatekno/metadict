#!/usr/bin/env python3

"""This script creates the init/data_dictionaries.txt file.
Data about dictionaries is read from gut.

That file is a tab separated file, where one line is one row.
The columns are

NAME LANG1 LANG2 AUTHOR
"""

import os
import os.path
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


if __name__ == "__main__":
    gut_root = get_gut_root()
    p = Path(gut_root) / "giellalt"
    lines = []
    for directory in p.glob("dict-*"):
        # strip away the "dict-" prefix
        name = directory.name[5:]
        if len(name) != 7:
            # skip ...-x-private  and other such dicts
            continue
        l1, l2 = name.split("-")
        lines.append(f"gt-{l1}-{l2}\t{l1}\t{l2}\tGiellatekno")

    lines = "\n".join(lines)
    with open("init/data_dictionaries.txt", "w") as f:
        f.write(lines)
