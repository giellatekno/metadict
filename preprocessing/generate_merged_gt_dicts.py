import os.path
import shutil
import sys
from pathlib import Path

from utils.utils import get_gut_root

try:
    # if GUTHOME (the gut directory) environment variable is set...
    GUTROOT = get_gut_root()
    script_directory = os.path.join(
        GUTROOT, "giellalt", "giella-core", "dicts", "scripts"
    )
    # ...and the scripts directory have been moved to git ...
    if not os.path.isdir(script_directory):
        raise KeyError
finally:
    sys.path.append(script_directory)
    from merge_giella_dicts import merge_giella_dicts


WANTED_DICTS = [
    "sme-nob",
    "nob-sme",
    "sme-fin",
    "fin-sme",
    "sma-mul",
    "nob-sma",
]


def main():
    gut_root = get_gut_root()
    p = Path(gut_root) / "giellalt"

    for directory in p.glob("dict-*"):
        # strip away the "dict-" prefix
        name = directory.name[5:]
        if len(name) != 7:
            # skip ...-x-private  and other such dicts
            continue
        l1, l2 = name.split("-")

        if name not in WANTED_DICTS:
            continue

        output_filename = f"dicts/gt-{l1}-{l2}.xml"
        try:
            n_entries = merge_giella_dicts(directory / "src", output_filename)
        except FileNotFoundError:
            print(f"no src files in dict {l1}-{l2}, skipping")
        except NotADirectoryError:
            print(f"no src directory in dict {l1}-{l2}, skipping")

    # create a copy of the gt-sme-nob dictionary for the sme-sme dictionary
    if Path("dicts/gt-sme-nob.xml").exists():
        shutil.copy("dicts/gt-sme-nob.xml", "dicts/gtsme.xml")


if __name__ == "__main__":
    raise SystemExit(main())
