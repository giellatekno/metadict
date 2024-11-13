from xml.etree import ElementTree as ET
from utils.dataclasses import Dictionary, Article


class GTParser:
    def __init__(self, dictionary_id, file):
        langs = file.name[3:-4]
        l1, l2 = langs.split("-")
        
        author = "Giellatekno"
        if langs == "sme-nob" or langs == "nob-sme":
            author = "Lene Antonsen, Trond Trosterud and Berit Merete Nystad Eskonsipo"
        elif langs == "sme-fin" or langs == "fin-sme":
            author = "Trond Trosterud"

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Neahttadigisánit",
            lang1=l1,
            lang2=l2,
            author=author
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
                pos=pos
            )

            articles.append(a)

        articles.sort(key=lambda article: article.lemma)
        for i, article in enumerate(articles, start=1):
            article.article_number = i

        return articles
    
    def to_html(self, lemma, pos, e_node: ET.Element):
        # Start html string
        html = f"<h3><b>{lemma}</b> ({pos})</h3><ul>"

        # Make each meaning group a list element
        mgs = e_node.findall("mg")
        for mg in mgs:
            html += "<li>"

            # Find all translations
            tgs = mg.findall("tg")
            for tg in tgs:

                # Add restriction if any                
                re = tg.find("re")
                if re != None:
                    html += f"({re.text.strip()}) "

                # Add all translations and POS if they have
                ts = tg.findall("t")
                html += "; ".join(f'{t.text.strip()} ({t.get("pos")})' if t.get("pos") else f'{t.text.strip()}' for t in ts)                  

                # Find and add all example scentences with translation
                xgs = tg.findall("xg")
                for xg in xgs:
                    html += "<br/><br/>"

                    x = xg.find("x").text.strip().replace("\n", "").replace("\t", " ")
                    xt = xg.find("xt").text.strip().replace("\n", "").replace("\t", " ")
                    
                    html += (f"{x}<br/>{xt}")

            # Close mg list element
            html += "</li><br/>"
        html += "</ul>"

        return html
