import csv
import re

from utils.dataclasses import Article, Dictionary


class MedisinskParser:
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Medisinsk lommeparlør",
            lang1="nob",
            lang2="sme",
            closed=True,
            is_ocr_read=True,
            author="Egil Utsi",
            date_published="1998",
            isbn="978-82-329-0564-5",
        )
        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []

        fieldnames = ["lemma", "entry"]
        with open(file, newline="") as fp:
            reader = csv.DictReader(fp, fieldnames=fieldnames)

            for index, row in enumerate(reader, start=1):
                lemma = re.sub(r"\([\)]+\)", "", row["lemma"])
                rendered = self.to_html(row["lemma"], row["entry"])

                a = Article(
                    dictionary=self.dictionary.id,
                    lemma=lemma,
                    rendered=rendered,
                    lang=self.dictionary.lang1,
                    article_number=index,
                )
                articles.append(a)

            return articles

    def to_html(self, lemma, translation):
        return f"<p><b>{lemma}</b>: {translation}</p>"
