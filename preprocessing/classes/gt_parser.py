from xml.etree import ElementTree as ET
from utils.dataclasses import Dictionary, Article

class GTParser:
    def __init__(self, dictionary_id, file):
        name = file.name[3:-4]
        l1, l2 = name.split("-")
        
        self.dictionary = Dictionary(
            id=dictionary_id,
            name=f"gt-{name}",
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
        
            l_node = e.find("lg/l")
            if l_node is None:
                print("<e> node has no <lg><l>")
                continue    
            
            lemma = l_node.text.strip("\n\t ").replace("\n", " ")
            pos = l_node.get("pos")

            mgs = e.findall("mg")

            for mg in mgs:
                tg = mg.find("tg")
                ts = tg.findall("t")
                
                #TODO all translations
                translation = f", ".join(f"{t.text} ({t.get('pos')})" for t in ts)
        
            # TODO add examples

            rendered = self.to_html(lemma, translation, pos)

            a = Article(
                dictionary=self.dictionary.id,
                lemma=lemma,
                rendered=rendered,
                lang=self.dictionary.lang1,
                pos=pos
            )

            articles.append(a)    
            
        return articles

    

    def to_html(self, lemma, translation, pos, examples=""):
        return f"""
                <div class="article">
                    <p>
                        <b>{lemma}</b> {pos} : {translation} <br>
                        {examples} 
                    </p>
                </div>
            """.replace("\n", "")