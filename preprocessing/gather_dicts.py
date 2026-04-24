#!/usr/bin/env python3
"""Populate dicts/ with dictionary source files.

Sources:
  closed   gut_root/giellatekno/dictionaries-closed/text
  gt       gut_root/giellalt/dict-* (merged via merge_giella_dicts)

By default both sources are gathered. Use --closed-only or --gt-only to
restrict to one. Use --purge to wipe dicts/ before gathering.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

from utils.utils import get_gut_root

WANTED_GT_DICTS = [
    "sme-nob",
    "sme-fin",
    "sme-smn",
    "sma-mul",
    "smn-sme",
    "smn-fin",
    "nob-sma",
    "nob-sme",
    "fin-sme",
    "fin-smn",
]


def gather_closed_dicts(gut_root: str, dicts_dir: Path):
    source = Path(gut_root) / "giellatekno" / "dictionaries-closed" / "text"
    if not source.exists():
        raise FileNotFoundError(f"dictionaries-closed/text not found: {source}")

    wip = source / "ocr" / "work-in-progress"

    for file in source.rglob("*"):
        if not file.is_file():
            continue
        if file.is_relative_to(wip):
            continue
        dest = dicts_dir / file.name
        if dest.is_symlink() and dest.resolve() == file.resolve():
            continue
        if dest.exists() or dest.is_symlink():
            dest.unlink()
        dest.symlink_to(file.resolve())
        print(f"Linked {file.name}")


def gather_gt_dicts(gut_root: str, dicts_dir: Path):
    scripts_dir = os.path.join(gut_root, "giellalt", "giella-core", "dicts", "scripts")
    if not os.path.isdir(scripts_dir):
        raise FileNotFoundError(f"giella-core scripts not found: {scripts_dir}")

    sys.path.append(scripts_dir)
    from merge_giella_dicts import merge_giella_dicts

    p = Path(gut_root) / "giellalt"
    for directory in p.glob("dict-*"):
        name = directory.name[5:]
        if name not in WANTED_GT_DICTS:
            continue

        l1, l2 = name.split("-")
        output_filename = str(dicts_dir / f"gt-{l1}-{l2}.xml")
        try:
            merge_giella_dicts(directory / "src", output_filename)
        except FileNotFoundError:
            print(f"no src files in dict-{l1}-{l2}, skipping")
        except NotADirectoryError:
            print(f"no src directory in dict-{l1}-{l2}, skipping")

    sme_nob = dicts_dir / "gt-sme-nob.xml"
    if sme_nob.exists():
        shutil.copy(sme_nob, dicts_dir / "gtsme.xml")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--purge", action="store_true", help="delete dicts/ before gathering"
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--closed-only", action="store_true", help="only gather closed dicts"
    )
    source.add_argument("--gt-only", action="store_true", help="only gather GT dicts")
    return parser.parse_args()


def main():
    args = parse_args()

    gut_root = get_gut_root()
    if gut_root is None:
        raise RuntimeError("gut root not found in ~/.config/gut/app.toml")

    dicts_dir = Path("dicts")
    if args.purge and dicts_dir.exists():
        shutil.rmtree(dicts_dir)
        print("Purged dicts/")
    dicts_dir.mkdir(exist_ok=True)

    if not args.gt_only:
        print("Gathering closed dictionaries...")
        gather_closed_dicts(gut_root, dicts_dir)

    if not args.closed_only:
        print("Gathering GT dictionaries...")
        gather_gt_dicts(gut_root, dicts_dir)


if __name__ == "__main__":
    raise SystemExit(main())
