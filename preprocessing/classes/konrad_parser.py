import csv

from utils.dataclasses import Article, Dictionary


class KonradParser:
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Lappisk ordbok",
            lang1="sme",
            lang2="eng",
            is_historic=True,
            author="Konrad Nielsen",
            date_published="1932–1938",
        )

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []

        with open(file, newline="") as fp:
            fieldnames = ["old_lemma", "lemma", "eng", "fin", "deu"]
            reader = csv.DictReader(fp, fieldnames=fieldnames)

            for i, row in enumerate(reader, start=1):
                rendered = self.to_html(
                    row["old_lemma"], row["eng"], row["fin"], row["deu"])

                a = Article(
                    lemma=row["lemma"],
                    dictionary=self.dictionary.id,
                    rendered=rendered,
                    lang=self.dictionary.lang1,
                    article_number=i,
                )
                articles.append(a)

        return articles

    def to_html(self, old_lemma, eng, fin, deu):
        html = f"<p><b>{old_lemma}</b>"

        if eng:
            html += f"<br>Eng: {eng}"
        if fin:
            html += f"<br>Fin: {fin}"
        if deu:
            html += f"<br>Deu: {deu}"

        html += "</p>"
        return html
