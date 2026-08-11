import csv
import re

from utils.dataclasses import Article, Dictionary

from .base_parser import BaseParser


class QvigstadParser(BaseParser):
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            slug=file.stem,
            name="Just Qvigstads lappiske ordbok fra Kaldfjorden og Vesterålen",
            lang1="sme",
            lang2="nob",
            is_historic=True,
            author="Just Qvigstad",
            date_published="1889",
        )

        self.articles = self.parse_dict(file)

    def find_lemmas(self, lemma_string: str):
        lemmas = []
        for lemma in lemma_string.split(", "):
            lemma = lemma.strip()
            if lemma == "pl.":
                continue
            if "(" in lemma:
                lemmas.extend(
                    [re.sub(r"\([^)]*\)", "", lemma), re.sub("[()]", "", lemma)]
                )
            else:
                lemmas.append(lemma)
        return lemmas

    def parse_dict(self, file):
        articles = []

        with open(file, newline="") as fp:
            reader = csv.DictReader(fp)
            for index, row in enumerate(reader, start=1):
                full_lemma = row["lemma"]
                pos = row["pos"]
                translation = row["translation"]
                entry = row["dictionary_entry"]
                ref = row["refrence"]

                rendered = self.to_html(full_lemma, translation, pos, entry, ref)

                for lemma in self.find_lemmas(full_lemma):
                    a = Article(
                        dictionary=self.dictionary.id,
                        lemma=lemma,
                        rendered=rendered,
                        lang=self.dictionary.lang1,
                        pos=pos,
                        article_number=index,
                    )
                    articles.append(a)
        return articles

    def to_html(self, lemma, translation, pos, entry, ref):
        return f"<p><b>{lemma}</b> {pos} : {translation} <br>{entry} <br>{ref}</p>"
