from utils.dataclasses import Dictionary, Article
import pandas as pd


class SkoleordbokParser:
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Norsk-samisk skoleordbok",
            lang1="nob",
            lang2="sme",
            closed=True,
            is_ordered=True,
            author="Randi Romsdal Balto",
            date_published="2015",
            isbn="978-82-7374-735-8",
        )
        self.articles = self.parse_dict(file)

    
    def get_parsed_data(self):
        return self.dictionary, self.articles
    
    def parse_dict(self, file):
        articles = []

        df = pd.read_csv(file, sep=",", header=0, na_filter=False)

        for index, row in df.iterrows():
            lemma = row["lemma"]
            if type(lemma) == float:
                print(row)
            pos = row["pos"]
            translation = row["translation"]
            rendered = self.to_html(lemma, pos, translation)

            a = Article(
                dictionary=self.dictionary.id,
                lemma=lemma,
                pos=pos,
                rendered=rendered,
                lang=self.dictionary.lang1,
                article_number=index
            )
            articles.append(a)

        return articles
        
    def to_html(self, lemma, pos, translation):
        return f"<p><b>{lemma}</b> <i>{pos}</i> {translation}</p>"