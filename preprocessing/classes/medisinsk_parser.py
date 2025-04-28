from utils.dataclasses import Dictionary, Article
import pandas as pd
import re

class MedisinskParser:
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Medisinsk lommeparlør",
            lang1="nob",
            lang2="sme",
            closed=True,
            is_ordered=True,
            author="Egil Utsi",
            date_published="1998",
            isbn="978-82-329-0564-5",
        )
        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles
    
    def parse_dict(self, file):
        articles = []
        
        df = pd.read_csv(file, sep=",", header=None)
        
        for index, row in df.iterrows():
            lemma = re.sub(r"\([\)]+\)", "", row[0])
            rendered = self.to_html(row[0], row[1])

            a = Article(
                dictionary=self.dictionary.id,
                lemma=lemma,
                rendered=rendered,
                lang=self.dictionary.lang1,
                article_number=index
            )
            articles.append(a)



        return articles
        
    def to_html(self, lemma, translation):
        return f"<p><b>{lemma}</b>: {translation}</p>"
    