from utils.dataclasses import Dictionary, Article
import re


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

        pattern = re.compile(r"((?:s\.|v\.|adj\.|adv\.|prep\.|pron\.|i\.|konj\.|postp\.|part\.)(?:\/(?:s\.|v\.|adj\.|adv\.|prep\.|pron\.|i\.|konj\.|postp\.|part\.))?)")
        
        with open(file, "r") as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            lemma, pos, text= pattern.split(line.strip(), maxsplit=1)
            rendered = self.to_html(lemma, pos, text)

            a = Article(
                dictionary=self.dictionary.id,
                lemma=lemma.strip(),
                pos=pos.strip(),
                rendered=rendered,
                lang=self.dictionary.lang1,
                article_number=i
            )
            articles.append(a)

        return articles
        
    def to_html(self, lemma, pos, text):
        return f"<p><b>{lemma}</b><i>{pos}</i>{text}</p>"