from utils.dataclasses import Dictionary, Article
import re
import pandas as pd

class KonradParser:
    def __init__(self, dictionary_id, file):

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Lappisk ordbok",
            lang1="sme",
            lang2="eng",
            closed=True,
            is_ordered=True,
            author="Konrad Nielsen",
            date_published="1932-1938"
        )

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []
        
        df = pd.read_csv(file, sep=",", header=None)

        for i, row in df.iterrows():
            lemma = row[1]
            rendered = self.to_html(row[0], row[2], row[3], row[4])

            a = Article(
                lemma=lemma,
                dictionary=self.dictionary.id,
                rendered=rendered,
                lang=self.dictionary.lang1,
                article_number=i,
            )
            articles.append(a)

        return articles

    def to_html(self, lemma, eng, fin, deu):
        html = f"<p><b>{lemma}</b>"

        if not pd.isna(eng):
            html += f"<br>Eng: {eng}"
        if not pd.isna(fin):
            html += f"<br>Fin: {fin}"
        if not pd.isna(deu):
            html += f"<br>Deu: {deu}"

        html += "</p>"
        return html