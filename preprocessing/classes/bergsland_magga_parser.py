import csv

from utils.dataclasses import Article, Dictionary

from .base_parser import BaseParser


class BergslandMaggaParser(BaseParser):
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Åarjelsaemien-daaroen baakoegærja",
            lang1="sma",
            lang2="nob",
            closed=True,
            author="Knut Bergsland & Lajla Mattsson Magga",
            date_published="1993",
            isbn="978-82-7601-010-5",
        )
        self.articles = self.parse_dict(file)

    def parse_dict(self, file):
        articles = []

        with open(file, newline="") as fp:
            reader = csv.DictReader(fp)
            for i, row in enumerate(reader, start=1):
                lemmas = row["lemmas"]
                lemma_section = row["lemma_section"]
                translation = row["translation_section"]

                rendered = self.to_html(lemma_section, translation)

                for lemma in lemmas.split(", "):
                    a = Article(
                        dictionary=self.dictionary.id,
                        lemma=lemma,
                        rendered=rendered,
                        lang=self.dictionary.lang1,
                        article_number=i,
                    )
                    articles.append(a)

        return articles

    def to_html(self, lemma_section: str, translation_section: str):
        rendered_lemma = f"<b>{lemma_section}</b>"
        # rendered_lemma = re.sub(
        #     r"(pred\.|attr\.|komp\.|superl\.|gen\.|akk\.)", r"<i>\1</i>", rendered_lemma
        # )
        rendered = rendered_lemma
        if translation_section.startswith("="):
            rendered += f"<b> {translation_section}</b>"
        else:
            rendered += f" {translation_section}"

        return f"<p>{rendered}</p>"
