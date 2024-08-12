from xml.etree import ElementTree as ET
from utils.dataclasses import Dictionary, Article


class GTParser:
    def __init__(self, dictionary_id, file):
        name = file.name[3:-4]
        l1, l2 = name.split("-")

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Giellatekno",
            lang1=l1,
            lang2=l2,
        )

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []
        xml = ET.parse(file)

        for e in xml.iter("e"):
            rendered = ""

            l_node = e.find("lg/l")
            if l_node is None:
                # print("<e> node has no <lg><l>")
                continue

            lemma = l_node.text.strip("\n\t ").replace("\n", " ")
            pos = l_node.get("pos")

            rendered += f"<h3><b>{lemma}</b> ({pos})</h3><ul>"

            mgs = e.findall("mg")
            for mg in mgs:
                rendered += "<li>"
                tgs = mg.findall("tg")
                for tg in tgs:

                    re = tg.find("re")
                    if re is not None:
                        rendered += f"({re.text.strip()}) "

                    ts = tg.findall("t")
                    rendered += "; ".join(f'{t.text.strip()} ({t.get("pos")})' for t in ts)

                    xgs = tg.findall("xg")

                    for xg in xgs:
                        rendered += "<br/><br/>"

                        x = xg.find("x").text.strip().replace("\n", "").replace("\t", " ")
                        xt = xg.find("xt").text.strip().replace("\n", "").replace("\t", " ")

                        rendered += (f"{x}<br/>{xt}")

                rendered += "</li><br/>"

            a = Article(
                dictionary=self.dictionary.id,
                lemma=lemma,
                rendered=rendered,
                lang=self.dictionary.lang1,
                pos=pos
            )

            articles.append(a)

        articles.sort(lambda article: article.lemma)
        for i, article in enumerate(articles, start=1):
            article.article_number = i

        return articles
