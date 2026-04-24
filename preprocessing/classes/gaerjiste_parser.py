import re

from utils.dataclasses import Article, Dictionary

from .base_parser import BaseParser


class GaerjisteParser(BaseParser):
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Norsk-sydsamisk ordliste. Gærjiste vaalteme.",
            lang1="nob",
            lang2="sma",
            closed=True,
            author="Albert Jåma",
            date_published="2001",
        )
        self.articles = self.parse_dict(file)

    def parse_dict(self, file):
        articles = []

        with open(file, "r") as f:
            for i, line in enumerate(f.readlines(), 1):
                if line.startswith("#"):
                    continue
                m = re.search(r"^\$>[^<]+<\$", line)
                if not m:
                    print("line has no lemma:")
                    print(line)
                    continue
                lemmas = self.extract_lemmas(m)
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

    def extract_lemmas(self, text):
        lemmas = re.sub(r"(\$>)|(<\$)|(\(.+\))|(\[.+\])", "", text.group(0)).split(",")
        return [lemma.strip() for lemma in lemmas]

    def to_html(self, line):
        return f"<p>{self.format_article(line)}</p>"
