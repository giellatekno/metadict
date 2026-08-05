import argparse
import csv
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Source .txt file")
    parser.add_argument("output", help="Target .csv file")
    args = parser.parse_args()

    with open(args.input, "r", newline="") as in_f, open(
        args.output, "w", newline=""
    ) as out_f:
        reader = csv.DictReader(in_f)
        writer = csv.writer(out_f)
        writer.writerow(["lemmas", "lemma_section", "translation_section"])

        for row in reader:
            lemmas = get_lemmas(row["lemma_section"])
            writer.writerow(
                [", ".join(lemmas), row["lemma_section"], row["translation_section"]]
            )


def get_lemmas(lemma_section: str):
    # Husk å fjerne:
    # * også
    # * eller
    # * mest
    # * essiv
    # * alm.
    # * og
    # * vanlig
    lemmas = []
    lemma_parts = re.split(r"[;]", lemma_section)
    for lemma_part in lemma_parts:
        lemma_part = re.sub(r"\[[^\]]+\]", "", lemma_part)
        lemma_part = re.sub(r"\([^\)]+\)", "", lemma_part)
        lemma_part = re.sub(r" (VI|IV|III|II|I|V)", " ", lemma_part)
        lemma_part = re.sub(r" -[^ -]+-", "", lemma_part)
        lemma_part = re.sub(r"nom\. ent\.", "", lemma_part)
        lemma_part = re.sub(r"også", "", lemma_part)
        lemma_part = re.sub(r"mest flt.", "", lemma_part)
        lemma_part = re.sub(r"essiv .+", "", lemma_part)
        lemma_part = re.sub(r"alm\. flt\.", "", lemma_part)
        lemma_part = re.sub(r"vanlig flt\.", "", lemma_part)
        lemma_part = re.sub(
            r"(attr|postp|prep|pred|adv)\.( og (attr|postp|prep|pred|adv)\.)*",
            "",
            lemma_part,
        )
        lemma_part = re.sub(r"[( ][^ ]+\.[^;]*", "", lemma_part)
        lemmas.extend([l.strip(" ,;:*1234") for l in lemma_part.split(",") if l != ""])
    return lemmas


if __name__ == "__main__":
    main()
