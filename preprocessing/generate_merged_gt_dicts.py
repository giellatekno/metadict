import argparse
import os.path
import sys
import shutil
from pathlib import Path
from utils.utils import get_gut_root

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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--langs", nargs="+"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    gut_root = get_gut_root()
    p = Path(gut_root) / "giellalt"

    shutil.rmtree("merged/", ignore_errors=True)
    Path("merged/").mkdir(parents=True, exist_ok=True)

    for i, directory in enumerate(p.glob("dict-*"), start=1):
        # strip away the "dict-" prefix
        name = directory.name[5:]
        if len(name) != 7:
            # skip ...-x-private  and other such dicts
            continue
        l1, l2 = name.split("-")

        if args.langs:
            if l1 not in args.langs and l2 not in args.langs:
                continue

        output_filename = f"dicts/gt/gt-{l1}-{l2}.xml"
        try:
            n_entries = merge_giella_dicts(directory / "src", output_filename)
        except FileNotFoundError:
            print(f"no src files in dict {l1}-{l2}, skipping")
        except NotADirectoryError:
            print(f"no src directory in dict {l1}-{l2}, skipping")


if __name__ == "__main__":
    raise SystemExit(main())
