import re

from utils.dataclasses import Article, Dictionary

from .base_parser import BaseParser

"""
Letters to filter out of lemma:
    ĵḷṇṛṿḥṃ ọạẹụ ēīōūӯ ˣꞌ

$>duohta<$ - bold
%>duohta<$ - cursive
d@, g@, b@ - ḏ ḇ
"""

outer_parenthesies = re.compile(
    r"\([^()]*(?:\([^()]*\)[^()]*)*\)|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]"
)


class SammallahtiParser(BaseParser):
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            slug=file.stem,
            name="Sámi–Suoma Sátnegirji",
            lang1="sme",
            lang2="fin",
            displayname="Sammallahti: Sámi-Suoma Sátnegirji",
            closed=True,
            author="Pekka Sammallahti",
            date_published="2020",
        )

        self.articles = self.parse_dict(file)

    def clean_lemma(self, lemma: str):
        # $>márska|eanan,-tn-:m<$ -> márska|eanan,-tn-:m
        lemma = re.sub(r"(\$>|<\$|jn[ae]\.|[’ꞌ'ˣ*@!?])", "", lemma)

        # maŋŋit:d#-is -> maŋŋit
        lemma = lemma.split(",")[0].split(":")[0].split("#")[0].split("→")[0]

        # miehtẹmūrrii -> miehtemurrii
        lemma = (
            lemma.replace("ạ", "a")
            .replace("ẹ", "e")
            .replace("ē", "e")
            .replace("ḥ", "h")
            .replace("ī", "i")
            .replace("ĵ", "j")
            .replace("ḷ", "l")
            .replace("ṃ", "m")
            .replace("ṇ", "n")
            .replace("ọ", "o")
            .replace("ō", "o")
            .replace("ṛ", "r")
            .replace("ū", "u")
            .replace("ü", "u")
            .replace("ụ", "u")
            .replace("ṿ", "v")
            .replace("ӯ", "y")
        )

        return lemma.strip()

    def fix_compunds(self, lemma_parts: list[str]):
        cmp_prefixes = []
        cmp_suffixes = []
        resolved = []
        for part in lemma_parts:
            if "|" in part:
                left, right = part.split("|", 1)
                cmp_prefixes.append(left)
                cmp_suffixes.append(right)
                resolved.append(left + right)
            else:
                resolved.append(part)

        if not cmp_prefixes and not cmp_suffixes:
            return resolved

        result = []
        for part in resolved:
            if part.startswith("-"):
                for prefix in cmp_prefixes:
                    result.append(prefix + part[1:])
            elif part.endswith("-"):
                for suffix in cmp_suffixes:
                    result.append(part[:-1] + suffix)
            else:
                result.append(part)

        return result

    def find_lemmas(self, line: str):

        # remove all parenthesies
        # NOTE: also removes some optional letters in words eg. "liidn(ẹ)oaivi"
        line = outer_parenthesies.sub("", line)

        # lemma is before pos (always in %><%) and before reference ("geahča")
        lemma_section = line.split("%>")[0].split(" gč. ")[0]

        # Split on variant mark ~ and clean each part
        lemma_parts = [
            v for l in lemma_section.split(" ~ ") for v in self.clean_lemma(l).split("/")
        ]

        return self.fix_compunds(lemma_parts)

    def format_article(self, text: str):
        text = super().format_article(text)
        idx = text.find("@")
        while idx != -1:
            text = text[: idx - 1] + "<u>" + text[idx - 1] + "</u>" + text[idx + 1 :]
            idx = text.find("@")

        return text

    def parse_dict(self, file):
        articles = []

        with open(file, "r") as f:
            for i, line in enumerate(f.readlines(), 1):
                if line.strip() == "" or " gč. " in line:
                    continue

                lemmas = self.find_lemmas(line)

                rendered = self.to_html(line.strip())

                for lemma in lemmas:
                    a = Article(
                        dictionary=self.dictionary.id,
                        lemma=lemma,
                        rendered=rendered,
                        lang=self.dictionary.lang1,
                        article_number=i,
                    )

                    articles.append(a)

        return articles

    def to_html(self, line):
        return f"<p>{self.format_article(line)}</p>"
