from utils.dataclasses import Article, Dictionary

from .base_parser import BaseParser

"""
Letters to filter out of lemma:
    ĵḷṃṇṛṿ ọạẹ ēīōū ˣꞌ

$>duohta<$ - bold
%>duohta<$ - cursive
d@, g@, b@ - ḏ ḇ
"""


class SammallahtiParser(BaseParser):
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
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
        lemma = (
            lemma.replace("$>", "")
            .replace("<$", "")
            .replace("ˣ", "")
            .replace("ꞌ", "")
            .replace("|", "")
            .replace("@", "")
        )

        lemma = lemma.split(",")[0].split(":")[0]

        lemma = (
            lemma.replace("ĵ", "j")
            .replace("ḷ", "l")
            .replace("ṃ", "m")
            .replace("ṇ", "n")
            .replace("ṛ", "r")
            .replace("ṿ", "v")
            .replace("ọ", "o")
            .replace("ạ", "a")
            .replace("ẹ", "e")
            .replace("ē", "e")
            .replace("ī", "i")
            .replace("ō", "o")
            .replace("ū", "u")
        )

        return lemma

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
                if line.strip() == "":
                    continue

                lemma = self.clean_lemma(line.split()[0])

                rendered = self.to_html(line.strip())

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
