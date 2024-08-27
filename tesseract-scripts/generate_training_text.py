"""
Short script for turning a wordfrequency list into training_text for tesseract.
Wordlist found at: https://giellatekno.uit.no/lists/sme/sme_wf.freq
"""

import random
import argparse

START_PUNC = list("([{«“")
END_PUNC = list(".,:;])}”»’'?!%´\"-_")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input",
        type=argparse.FileType("r", encoding="utf-8"),
    )
    parser.add_argument(
        "output",
        type=argparse.FileType("w", encoding="utf-8"),
    )
    return parser.parse_args()


def main():
    args = parse_args()
    lines = [line.strip() for line in args.input.readlines()]

    words = []

    for line in lines:
        freq = int(line.split()[0])
        try:
            word = line.split()[1].strip()
        except Exception:
            continue
        for _ in range(freq):
            words.append(word)

    random.shuffle(words)

    output_lines = []
    line = ""
    for word in words:
        word = word.strip()
        if len(word) > 81:
            continue

        if len(line) + len(word) > 81:
            output_lines.append(line + "\n")
            line = ""

        if word in END_PUNC:
            if line and line.rstrip()[-1:] not in END_PUNC:
                # print(line)
                line = line.rstrip() + word + " "
        elif word in START_PUNC:
            line = line + word
        else:
            if random.randint(0, 50) == 0:
                word = word.upper()
            line = line + word + " "

    args.output.writelines(output_lines)


if __name__ == "__main__":
    raise SystemExit(main())
