from pathlib import Path
import argparse
import os
import re
import hfst
from multiprocessing import Pool
from functools import partial

pm_lang1 = None
pm_lang2 = None
pm_lang3 = None

unknowns = re.compile(r'\t"[^"]*" \?|(?<!.)"[^"]*"(?!\n\t)')
words = re.compile(r'"<?([^\s"<>]+)>?"')


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Verify text",
        description="Uses fst tokenisers to check for spelling mistakes in a given text file. Outputs a \"mistakes-{filename}.txt file\""
    )
    parser.add_argument("file", type=str, help="Textfile to be analysed.")
    parser.add_argument("-l1", type=str, nargs="?", help="Langcode of language with compiled hfst-tokeniser. Default: \"sme\"", default="sme")
    parser.add_argument("-l2", type=str, nargs="?", help="Langcode of language with compiled hfst-tokeniser. Default: \"nob\"", default="nob")
    parser.add_argument("--latin", action="store_true", help="Input text contains latin words")
    parser.add_argument("-o", "--one", action="store_true", help="One lang only (l1)")


    return parser.parse_args()

def mark_word(word):
    return f"<{word}>"

def find_unknown_words(line, pm):
    tokenized = pm.get_tokenized_output(line, output_format="giellacg")
    res = "".join(unknowns.findall(tokenized))
    return set(words.findall(res)) 


def verify_line(args, latin, latin_words, one_lang):
    idx = args[0]
    line = args[1]

    assert(pm_lang1 != None and pm_lang2 != None)
    # assert(pm_lang1 != None and pm_lang2 != None and pm_lang3 != None)

    line = line.replace(":", " ")

    set1 = find_unknown_words(line, pm_lang1)
    set2 = find_unknown_words(line, pm_lang2)
    # set3 = find_unknown_words(line, pm_lang3)

    if one_lang:
        unknown_words = set1
    else:
        unknown_words = set1.intersection(set2)
        # unknown_words = set1.intersection(set2).intersection(set3)

    if latin:
        unknown_words.difference_update(latin_words)


    if unknown_words:
        # print(unknown_words)
        # for word in unknown_words:
        #     pattern = r'\b' + re.escape(word) + r'\b'
        #     line = re.sub(pattern, mark_word(word), line)
        # print(line)
        return [(idx, f"{idx:<4} | {word:25} | {line}") for word in unknown_words]


def main():
    ENV = os.environ.copy()
    args = parse_args()
    global pm_lang1, pm_lang2, pm_lang3

    try:
        pm_lang1 = hfst.PmatchContainer(f'{ENV["GTLANGS"]}/lang-{args.l1}/tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst')
        pm_lang2 = hfst.PmatchContainer(f'{ENV["GTLANGS"]}/lang-{args.l2}/tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst')
        # pm_lang3 = hfst.PmatchContainer(f'{ENV["GTLANGS"]}/lang-fin/tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst')
    except Exception as e:
        print(e)
        exit(1)

    input_file = Path(args.file)

    latin_words = set()
    if args.latin:
        with open("latin.txt") as f:
            words = f.read().split()

        for word in words:
            latin_words.add(word.lower())
            latin_words.add(word.capitalize())

    if not input_file.exists() or not input_file.is_file():
        print(f"Invalid input file: {input_file}")
        exit(1)

    with open(input_file, "r") as input_f:
        lines = input_f.readlines()


    output_list = []

    with Pool() as pool:
        res = pool.map(partial(verify_line, latin=args.latin, latin_words=latin_words, one_lang=args.one), enumerate(lines, 1))

    for r in res:
        if r:
            output_list.extend(r)
    output_list = [o[1] for o in sorted(output_list, key=lambda x: x[0])]

    with open(f"mistakes-{input_file.name}", "w") as output_f:
        output_f.writelines(output_list)



if __name__ == "__main__":
    raise SystemExit(main())