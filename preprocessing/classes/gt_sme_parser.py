from xml.etree import ElementTree as ET

from utils.dataclasses import Article, Dictionary
from utils.utils import sort_by_sami_alphabet


class GTSmeParser:
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Neahttadigisánit",
            lang1="sme",
            lang2="sme",
            author="Risten West, Lene Antonsen, Trond Trosterud & Berit Merete Nystad Eskonsipo",
        )

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []
        xml = ET.parse(file)

        for e in xml.iter("e"):
            l_node = e.find("lg/l")

            if l_node is None:
                # print("<e> node has no <lg><l>")
                continue

            lemma = l_node.text.strip("\n\t ").replace("\n", " ")

            if e.find("mg/dg") == None:
                continue

            pos = l_node.get("pos")

            try:
                rendered = self.to_html(lemma, pos, e)
            except Exception as e:
                print(lemma, e)
                continue

            a = Article(
                dictionary=self.dictionary.id,
                lemma=lemma,
                rendered=rendered,
                lang=self.dictionary.lang1,
                pos=pos,
            )

            articles.append(a)

        # articles.sort(key=lambda article: article.lemma)
        articles = sort_by_sami_alphabet(articles)
        for i, article in enumerate(articles, start=1):
            article.article_number = i

        return articles

    def clean_text(self, text: str):
        return text.strip().replace("\n", "").replace("\t", " ")

    def to_html(self, lemma, pos, e_node: ET.Element):
        # Start html string
        html = f"<b>{lemma}</b> ({pos}): "

        # Iterate meaning groups
        mgs = e_node.findall("mg")
        for mg in mgs:
            # Find and add all definitions
            ds = [
                self.clean_text(d.text)
                for d in mg.findall("dg/d")
                if d.text and d.text.strip()
            ]
            if ds:
                html += "; ".join(ds) + "<br/>"

            # Find and add all example sentences
            xs = [self.clean_text(x.text) for x in mg.findall("xg/x") if x.text]
            tgxs = [
                self.clean_text(x.text)
                for x in mg.findall("tg/xg/x")
                if x.text and self.clean_text(x.text) not in xs
            ]
            if xs or tgxs:
                for x in xs:
                    html += f"<i>{x}</i>" + "<br/>"
                for x in tgxs:
                    html += f"<i>{x}</i>" + "<br/>"

                html += "<br/>"

        # Remove excess linebreaks
        while html[-5:] == "<br/>":
            html = html.removesuffix("<br/>")

        # if lemma == "fierbmi":
        #     print(html)
        return f"<p>{html}</p>"
