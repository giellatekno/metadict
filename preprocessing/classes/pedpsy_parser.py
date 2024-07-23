from utils.dataclasses import Dictionary, Article
import re

class PedPsyParser:
    def __init__(self, dictionary_id, file):

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Pedagogalaš-psykologalaš sátnegirji",
            lang1="nob",
            lang2="sme",
            closed=True,
            is_ordered=True,
            author="Hans Petter Boyne, Arnulf Soleng",
            date_published="2006",
            isbn="82-7374-614-3",
        )

        # Consonant gradation
        self.gradation_pattern = re.compile(r"[^\s\d]{1,4}-[^\s\d,]{1,4}")

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []
        
        with open(file, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            if line.find("|") != -1:
                lemma = line.split("|")[0]                
            else:
                lemma = line.split("(")[0]

            lemma = lemma.replace("1", "").replace("2", "").replace("3", "").strip()

            rendered = self.to_html(line.strip(), lemma)
          
            a = Article(
                dictionary=self.dictionary.id,
                lemma=lemma,
                rendered=rendered,
                lang=self.dictionary.lang1,
                article_number=i
            )

            articles.append(a)   
        
        return articles
    
    def to_html(self, line: str, lemma):
        
        html = line.replace(lemma, f"<b>{lemma}</b>", 1)

        gradation = self.gradation_pattern.findall(line)
        if gradation:
            html = html.replace(gradation[0], f"<i>{gradation[0]}</i>")

        if html.find("omd.:") != -1:
            html = html.replace("omd.:", "omd.:<i>") + "</i>"

        return f"<p>{html}</p>"

