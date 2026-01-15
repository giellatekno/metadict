from xml.etree import ElementTree as ET

from utils.dataclasses import Article, Dictionary
from utils.utils import sort_by_sami_alphabet


class GTParser:
    def __init__(self, dictionary_id, file):
        langs = file.name[3:-4]
        l1, l2 = langs.split("-")
        if l2 == "mul":
            l2 = "nob"

        author = "Giellatekno"
        if langs == "sme-nob" or langs == "nob-sme":
            author = "Lene Antonsen, Trond Trosterud & Berit Merete Nystad Eskonsipo"
        elif langs == "sme-fin" or langs == "fin-sme":
            author = "Trond Trosterud"
        elif langs == "sma-mul" or langs == "nob-sma":
            author = "Lene Antonsen, Trond Trosterud, Maja Kappfjell, Sissel Jåma, Toini Bergström & Marit Fjellheim"

        name = "Neahttadigisánit"
        if l1 == "sma" or l2 == "sma":
            name = "Nedtedigibaakoeh"

        self.dictionary = Dictionary(
            id=dictionary_id, name=name, lang1=l1, lang2=l2, author=author
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
            pos = l_node.get("pos")

            rendered = self.to_html(lemma, pos, e)

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

        # Make each meaning group a list element
        mgs = e_node.findall("mg")
        for mg in mgs:
            # Find all translations
            tgs = mg.findall("tg")
            for tg in tgs:
                if self.dictionary.lang1 == "sma" and self.dictionary.lang2 == "nob":
                    if tg.get("{http://www.w3.org/XML/1998/namespace}lang") != "nob":
                        continue

                # Add restriction if any
                re = tg.find("re")
                if re:
                    html += f"({re.text.strip()}) "

                # Add all translations and POS if they have
                ts = tg.findall("t")
                html += (
                    "; ".join(
                        [
                            (
                                f"{self.clean_text(t.text)} ({t.get('pos')})"
                                if t.get("pos")
                                else f"{self.clean_text(t.text)}"
                            )
                            for t in ts
                        ]
                    )
                    + "<br/>"
                )

                for xg in tg.findall("xg"):
                    x = xg.find("x").text
                    xt = xg.find("xt").text
                    if x and xt:
                        html += f"<i>{self.clean_text(x)}</i> "
                        html += self.clean_text(xt) + "<br/><br/>"

            # Find and add all example scentences with translation
            for xg in mg.findall("xg"):
                x = xg.find("x").text
                xt = xg.find("xt").text
                if x and xt:
                    html += f"<i>{self.clean_text(x)}</i> "
                    html += self.clean_text(xt) + "<br/><br/>"

        # Remove excess linebreaks
        while html[-5:] == "<br/>":
            html = html.removesuffix("<br/>")

        return f"<p>{html}</p>"
