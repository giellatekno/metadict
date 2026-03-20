import csv
import re

from utils.dataclasses import Article, Dictionary


class KintelParser:
    def __init__(self, dictionary_id, file):
        l1, l2 = file.stem.split("-")[-2:]
        self.dictionary = Dictionary(
            id=dictionary_id,
            name=(
                "Norsk-lulesamisk Ordbok" if l1 == "nob" else "Lulesamisk-norsk Ordbok"
            ),
            lang1=l1,
            lang2=l2,
            closed=False,
            author="Anders Kintel",
            date_published="2012",
            isbn="",
        )
        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []

        with open(file, "r", newline="") as fp:
            reader = csv.DictReader(fp)
            for i, row in enumerate(reader):
                lemmas = self.get_lemmas(row["lemma"])
                rendered = self.to_html(row["lemma"], row["translation"])
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

    def get_lemmas(self, lemma: str):
        lemma = lemma.replace("$>", "").replace("<$", "")
        lemma = lemma.replace("%>", "").replace("<%", "")
        return [lemma.split()[0]]

    def to_html(self, lemma: str, translation: str):
        lemma = lemma.replace("$>", "<b>").replace("<$", "</b>")
        lemma = lemma.replace("%>", "<i>").replace("<%", "</i>")
        translation = translation.replace("$>", "<b>").replace("<$", "</b>")
        translation = translation.replace("%>", "<i>").replace("<%", "</i>")

        if translation == "":
            return f"<p>{lemma}</p>"
        return f"<p>{lemma}<br>{translation}</p>"

