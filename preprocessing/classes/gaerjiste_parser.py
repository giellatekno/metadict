import re

from utils.dataclasses import Article, Dictionary


class GaerjisteParser:
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Norsk-sydsamisk ordliste. Gærjiste vaalteme.",
            lang1="nob",
            lang2="sma",
            closed=True,
            author="Albert Jåma",
            date_published="2001",
            isbn="",
        )
        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []

        # Implement parsing logic here
        with open(file, "r") as f:
            for i, line in enumerate(f.readlines(), 1):
                if line.startswith("#"):
                    continue
                m = re.search(r"^\$>[^<]+<\$", line)
                if not m:
                    print("line has no lemma:")
                    print(line)
                    continue
                lemmas = self.extract_lemmas(m)
                rendered = self.to_html(line)

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

    def extract_lemmas(self, text):
        lemmas = re.sub(r"(\$>)|(<\$)|(\(.+\))|(\[.+\])", "", text.group(0)).split(",")
        return [lemma.strip() for lemma in lemmas]

    def format_article(self, text):
        text = text.replace("$>", "<b>").replace("<$", "</b>")
        text = text.replace("%>", "<i>").replace("<%", "</i>")
        return text.strip()

    def to_html(self, line):
        return f"<p>{self.format_article(line)}</p>"
