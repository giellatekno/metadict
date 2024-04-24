from xml.etree import ElementTree as ET
from utils.dataclasses import Dictionary, Article

class QvigstadParser:
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Qvigstad-Kalfjord-sme-nob",
            lang1="sme",
            lang2="nob",
            is_ordered=True,
            author="Just Qvigstad",
            date_published="1889", 
        )

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles


    def parse_dict(self, file):
        articles = []
        
        xml_file = ET.parse(file)

        for index, row in enumerate(xml_file.iter("row"), 1):

            full_lemma = row[1].text.strip().replace("\n", " ")

            for lemma in full_lemma.split(", "):
                if lemma == "pl.":
                    continue

                pos = row[2].text.strip()
                translation = f"{row[0].text+row[3].text}".strip()

                explanation = f"{row[4].text.strip()}\n{row[5].text.strip()}"

                rendered = self.to_html(full_lemma, translation, pos, explanation)

                a = Article(
                    dictionary=self.dictionary.id,
                    lemma=lemma,
                    rendered=rendered,
                    lang=self.dictionary.lang1,
                    pos=pos,
                    article_number=index
                )

                articles.append(a)

        return articles


    def to_html(self, lemma, translation, pos, explanation):
        explanation = explanation.replace('\n', '<br/>')

        return f"<div class=\"article\"><p><b>{lemma}</b> {pos} : {translation} <br/> {explanation}</p></div>"