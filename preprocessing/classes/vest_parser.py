import re

from utils.dataclasses import Article, Dictionary

from .base_parser import BaseParser


class VestParser(BaseParser):
    def __init__(self, dictionary_id, file):
        l1, l2 = file.stem.split("-")[-2:]
        name = "Nettisanakirja" if l1 == "fin" else "Neahttasátnegirji"
        self.dictionary = Dictionary(
            id=dictionary_id,
            name=name,
            lang1=l1,
            lang2=l2,
            displayname=(f"Vest: {name}"),
            closed=False,
            author="Jovnna-Ánde Vest",
            date_published="2024" if l1 == "fin" else "2026",
        )

        self.articles = self.parse_dict(file)

    def parse_dict(self, file):
        articles = []

        with open(file, "r") as f:
            for i, line in enumerate(f.readlines(), 1):
                lemmas = self.find_lemmas(line)
                rendered = self.to_html(line)

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

    def find_lemmas(self, line: str):
        lemmas = []
        lemma_section = line.split("  ")[0]
        lemma_parts = re.split(r"~(?![^()]*\))", lemma_section)
        for lemma_part in lemma_parts:
            lemma = re.sub(r"(\$>|<\$|%>|<%)", "", lemma_part)
            lemma = re.sub(r" \([^\)]+\)?", "", lemma)
            lemma = re.sub(r";.*", "", lemma)
            lemma = re.sub(r"[´/!]", "", lemma)
            lemma = lemma.split(",")[0].strip().replace("´", "")

            if "(" in lemma:
                lemmas.append(re.sub(r"\([^\)]*\)", "", lemma))
                lemmas.append(re.sub(r"[\(\)]", "", lemma))
            else:
                lemmas.append(lemma)

        return lemmas

    def to_html(self, line):
        return f"<p>{self.format_article(line)}</p>"
