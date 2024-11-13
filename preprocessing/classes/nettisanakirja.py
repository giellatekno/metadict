from utils.dataclasses import Dictionary, Article
import re

class NettisanakirjaParser:
    def __init__(self, dictionary_id, file):

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Nettisanakirja",
            lang1="fin",
            lang2="sme",
            closed=False,
            is_ordered=True,
            author="Jouni A. Vest",
            date_published="2024"
        )

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []
        
        with open(file, "r") as f:
            for i, line in enumerate(f.readlines(), 1):
                m = re.search(r"\$>[^<]+<\$", line)
                if not m:
                    print("line has no lemma")
                    continue
                lemma = m.group(0).replace("$>", "").replace("<$", "")

                rendered = self.to_html(line)

                a = Article(
                    dictionary=self.dictionary.id,
                    lemma=lemma,
                    rendered=rendered,
                    lang=self.dictionary.lang1,
                    article_number=i
                )

                articles.append(a)


        return articles

    def format_article(self, text):
        text = text.replace("$>", "<b>").replace("<$", "</b>")
        text = text.replace("%>", "<i>").replace("<%", "</i>")
        return text.strip()

    def to_html(self, line):
        return f"<p>{self.format_article(line)}</p>"
