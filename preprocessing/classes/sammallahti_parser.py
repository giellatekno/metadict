from utils.dataclasses import Dictionary, Article

"""
Letters to filter out of lemma:
    ĵḷṃṇṛṿ ọạẹ ēīōū ˣꞌ

$>duohta<$ - bold
%>duohta<$ - cursive
d@, g@, b@ - ḏ ḇ
"""


class SammallahtiParser:
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name=f"Sámi-Suoma Sátnegirji",
            lang1="sme",
            lang2="fin",
            closed=True,
            is_ordered=True,
            author="Pekka Sammallahti",
            date_published="2020",
        )

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def clean_lemma(self, lemma: str):
        lemma = lemma.replace("$>", "")
        lemma = lemma.replace("<$", "")
        lemma = lemma.replace("ˣ", "")
        lemma = lemma.replace("ꞌ", "")
        lemma = lemma.replace("|", "")
        lemma = lemma.replace("@", "")

        lemma = lemma.split(",")[0].split(":")[0]

        lemma = lemma.replace("ĵ", "j")
        lemma = lemma.replace("ḷ", "l")
        lemma = lemma.replace("ṃ", "m")
        lemma = lemma.replace("ṇ", "n")
        lemma = lemma.replace("ṛ", "r")
        lemma = lemma.replace("ṿ", "v")
        lemma = lemma.replace("ọ", "o")
        lemma = lemma.replace("ạ", "a")
        lemma = lemma.replace("ẹ", "e")
        lemma = lemma.replace("ē", "e")
        lemma = lemma.replace("ī", "i")
        lemma = lemma.replace("ō", "o")
        lemma = lemma.replace("ū", "u")

        return lemma

    def format_article(self, text: str):
        text = text.replace("$>", "<b>").replace("<$", "</b>")
        text = text.replace("%>", "<i>").replace("<%", "</i>")

        idx = text.find("@")
        while idx != -1:
            text = text[: idx - 1] + "<u>" + text[idx - 1] + "</u>" + text[idx + 1 :]
            idx = text.find("@")

        return text

    def parse_dict(self, file):
        articles = []

        with open(file, "r") as f:
            for i, line in enumerate(f.readlines(), 1):
                if line.strip() == "":
                    continue

                lemma = self.clean_lemma(line.split()[0])

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

    def to_html(self, line):
        return f"<p>{self.format_article(line)}</p>"
