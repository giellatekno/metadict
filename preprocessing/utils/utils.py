import os.path
import re

from utils.dataclasses import Article


def yellow(s):
    """Return the string 's' with ansi terminal escapes to make it yellow."""
    return f"\033[93m{s}\033[0m"


def red(s):
    """Return the string 's' with ansi terminal escapes to make it red."""
    return f"\033[91m{s}\033[0m"


def get_gut_root():
    app_toml_path = os.path.expanduser("~/.config/gut/app.toml")
    with open(app_toml_path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            try:
                k, v = line.split("=", maxsplit=1)
            except ValueError:
                continue
            k = k.strip()
            v = v.strip()
            if k != "root":
                continue

            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]

            return v


def sort_alphabetically(input_list: list[Article], saami=False):
    nordic_alphabet = (
        " !\"«»#$%&'()*+,-./0123456789:;<=>?@[\\]^_`abcdefghijklmnopqrsštuvwxyzžæäøöå{|}~"
    )
    saami_alphabet = " !\"«»#$%&'()*+,-./0123456789:;<=>?@[\\]^_`aáâäbcčdđefghiïjklmnŋopqrsštŧuvwxyzžæøöå{|}~"

    alphabet = saami_alphabet if saami else nordic_alphabet

    def clean_lemma(article: Article):
        lemma = article.lemma.lower()
        lemma = re.sub(r"[ç]", "c", lemma)
        lemma = re.sub(r"[ð]", "đ", lemma)
        lemma = re.sub(r"[í]", "i", lemma)
        lemma = re.sub(r"[ñ]", "n", lemma)
        lemma = re.sub(r"[àã]", "a", lemma)
        lemma = re.sub(r"[éèê]", "e", lemma)
        lemma = re.sub(r"[üúû]", "u", lemma)
        lemma = re.sub(r"[ôõóò]", "o", lemma)
        lemma = re.sub(r"[ʼ´ˈ’ʻ]", "'", lemma)

        # Debug if you get ValueError: substring not found
        for c in lemma:
            if c not in alphabet:
                print(
                    yellow(
                        f"Found unknown character \"{c}\" with unicode '{hex(ord(c))}' in lemma: '{lemma}'"
                    )
                )
                lemma = lemma.replace(c, "~", 1)
        return lemma

    return sorted(
        input_list,
        key=lambda article: [alphabet.index(c) for c in clean_lemma(article)],
    )
