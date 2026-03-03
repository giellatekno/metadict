import csv

from utils.dataclasses import Article, Dictionary


class GirjjalasvuodaParser:
    def __init__(self, dictionary_id, file):
        l1, l2 = file.stem.split("-")[-2:]

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Girjjálašvuođa tearpmat",
            lang1=l1,
            lang2=l2,
            closed=True,
            is_ocr_read=True,
            author="Harald Gaski, Vuokko Hirvonen, Ellen Näkkäläjärvi",
            date_published="1992",
            isbn="82-91047-10-3",
        )

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []

        with open(file, newline="") as fp:
            if self.dictionary.lang1 != "sme":
                fieldnames = ["lemma", "entry"]
                reader = csv.DictReader(fp, fieldnames=fieldnames)
                for index, row in enumerate(reader, start=1):
                    lemma = row["lemma"]
                    entry = row["entry"]

                    rendered = self.to_html(lemma, entry)

                    a = Article(
                        dictionary=self.dictionary.id,
                        lemma=lemma,
                        rendered=rendered,
                        lang=self.dictionary.lang1,
                        article_number=index,
                    )
                    articles.append(a)
            else:
                fieldnames = ["lemma", "entry", "translation"]
                reader = csv.DictReader(fp, fieldnames=fieldnames)
                for index, row in enumerate(reader, start=1):
                    lemma = row["lemma"]
                    entry = row["entry"]
                    translation = row["translation"]

                    rendered = self.to_html(lemma, entry, translation)

                    a = Article(
                        dictionary=self.dictionary.id,
                        lemma=lemma,
                        rendered=rendered,
                        lang=self.dictionary.lang1,
                        article_number=index,
                    )
                    articles.append(a)

        return articles

    def to_html(self, lemma, entry, translation=None):
        if translation:
            return f"<p><b>{lemma}</b><br>{entry}<br>{translation}</p>"
        else:
            return f"<p><b>{lemma}</b><br>{entry}</p>"
