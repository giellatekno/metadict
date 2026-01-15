from utils.dataclasses import Dictionary, Article
import re


class RuoktumetParser:
    def __init__(self, dictionary_id, file):
        l1, l2 = file.stem.split("-")[-2:]

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Ruoktumet sátnegirjjáš",
            lang1=l1,
            lang2=l2,
            closed=True,
            is_ordered=True,
            author="Inga Laila Hætta, Inga Hætta Skarvik",
            date_published="1997",
            isbn="82-91047-77-4",
        )

        self.pattern = re.compile(r"^[^ ]+(?:(?: [~-] [^ ]+)?(?: \([^ ]+\.\))?)*")

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []

        with open(file, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            lemma = line.split()[0].replace("¹", "").replace("²", "")
            rendered = self.to_html(line.strip())

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
