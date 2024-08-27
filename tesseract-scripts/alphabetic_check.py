"""Checks if lines in a given file are sorted alphabetically.
Prints lines that are not alphabetically sorted"""

import argparse
from pathlib import Path
import re

alphabet = "aábcčdđeéfghijklmnŋopqrsštŧuvwxyzžæäøöå"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=str, help="File to sort")

    return parser.parse_args()


def acmp(a, b):
    la = len(a)
    lb = len(b)
    lm = min(la, lb)
    p = 0
    while p < lm:
        pa = alphabet.index(a[p])
        pb = alphabet.index(b[p])
        if pa > pb:
            return 1
        if pb > pa:
            return -1
        p = p + 1
    if la > lb:
        return 1
    if lb > la:
        return -1
    return 0


def main():
    args = parse_args()

    input_file = Path(args.file)

    if not input_file.exists() or not input_file.is_file():
        print(f"Invalid input file: {input_file}")
        exit(1)

    with open(input_file, "r") as input_f:
        words = [
            re.sub(r"[,:-]", "", line.strip().split()[0].lower())
            for line in input_f.readlines()
        ]

    for i in range(1, len(words)):
        prev = words[i-1]
        cur = words[i]

        try:
            if acmp(prev, cur) == 1:
                print(f"{i}: {prev}")
                print(f"{i+1}: {cur}")
                print()
        except:
            # anders: Which exception can happen here?
            print("Couldn't compare following words")
            print(prev, cur)
            exit()


if __name__ == "__main__":
    raise SystemExit(main())
