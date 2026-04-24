import csv

from utils.dataclasses import Article, Dictionary

from .base_parser import BaseParser


class SkoleordbokParser(BaseParser):
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Norsk-samisk skoleordbok",
            lang1="nob",
            lang2="sme",
            closed=True,
            is_ocr_read=True,
            author="Randi Romsdal Balto",
            date_published="2015",
            isbn="978-82-7374-735-8",
        )
        self.articles = self.parse_dict(file)

    def parse_dict(self, file):
        articles = []

        with open(file, newline="") as fp:
            reader = csv.DictReader(fp)

            for index, row in enumerate(reader, start=1):
                lemma = row["lemma"]
                pos = row["pos"]
                translation = row["translation"]
                rendered = self.to_html(lemma, pos, translation)

                a = Article(
                    dictionary=self.dictionary.id,
                    lemma=lemma,
                    pos=pos,
                    rendered=rendered,
                    lang=self.dictionary.lang1,
                    article_number=index,
                )
                articles.append(a)

        return articles

    def to_html(self, lemma, pos, translation):
        return f"<p><b>{lemma}</b> <i>{pos}</i> {translation}</p>"
