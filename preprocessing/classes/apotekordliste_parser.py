from utils.dataclasses import Dictionary, Article
import re


class ApotekordlisteParser:
    def __init__(self, dictionary_id, file):
        langs = file.stem.split("-")[-3:]
        l1, l2 = langs[0], langs[1]

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Apotekordliste / Apotehkasátnelistu / Apteekkisanasto",
            lang1=l1,
            lang2=l2,
            closed=True,
            is_ordered=True,
            author="Egil Utsi, Håkon Jenssen",
            date_published="2006",
            isbn="82-7374-595-3",
        )
        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []

        with open(file, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            lemma = line.split(":")[0].split("(")[0].strip()
            rendered = self.to_html(lemma, line.strip())
            a = Article(
                dictionary=self.dictionary.id,
                lemma=lemma,
                rendered=rendered,
                lang=self.dictionary.lang1,
                article_number=i,
            )
            articles.append(a)
        return articles

    def to_html(self, lemma, line):
        formatted = re.sub(lemma, f"<b>{lemma}</b>", line, 1)
        formatted = re.sub(r"(\((lat\.[^)]*)\))", r"<i>\1</i>", formatted)
        formatted = re.sub(r"(\d(?=:))", r"<b>\1</b>", formatted)

        return f"<p>{formatted}</p>"
