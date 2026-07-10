import re

from utils.dataclasses import Article, Dictionary

from .base_parser import BaseParser


class RuoktumetParser(BaseParser):
    def __init__(self, dictionary_id, file):
        l1, l2 = file.stem.split("-")[-2:]

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Ruoktumet sátnegirjjáš",
            lang1=l1,
            lang2=l2,
            closed=True,
            is_ocr_read=True,
            author="Inga Laila Hætta, Inga Hætta Skarvik",
            date_published="1997",
            isbn="82-91047-77-4",
        )

        self.pattern = re.compile(r"^[^ ]+(?:(?: [~-] [^ ]+)?(?: \([^ ]+\.\))?)*")

        self.articles = self.parse_dict(file)

    def find_lemmas(self, lemma: str):
        lemma = re.sub(r" \([^)]*\)", "", lemma)
        lemma = re.sub(r"[¹²]", "", lemma)

        if "(" in lemma:
            return [re.sub(r"\([^)]*\)", "", lemma), re.sub("[()]", "", lemma)]
        return [lemma]

    def parse_dict(self, file):
        articles = []

        with open(file, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            lemmas = self.find_lemmas(line.split()[0])
            rendered = self.to_html(line.strip())

            for lemma in lemmas:
                a = Article(
                    dictionary=self.dictionary.id,
                    lemma=lemma,
                    rendered=rendered,
                    lang=self.dictionary.lang1,
                    article_number=i,
                )

                articles.append(a)

        return articles

    def to_html(self, line: str):
        if line.find("\\") == -1:
            bold = max(self.pattern.findall(line))
            html = line.replace(
                bold, f"<b>{bold.replace('(', '</b>(').replace(')', ')<b>')}</b>", 1
            )

        else:
            lines = [l.strip() for l in line.split("\\")]
            bold = max(self.pattern.findall(lines[0]))
            html = lines[0].replace(
                bold, f"<b>{bold.replace('(', '</b>(').replace(')', ')<b>')}</b>", 1
            )
            for l in lines[1:]:
                italic = max(self.pattern.findall(l))
                html += f"<br>&emsp;{l.replace(italic, f'<i>{italic.replace("(", "</i>(").replace(")", ")<i>")}</i>', 1)}"

        return f"<p>{html}</p>"
