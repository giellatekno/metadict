from utils.dataclasses import Dictionary, Article

class AlgosatnegirjiParser:
    def __init__(self, dictionary_id, file):

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Álgosátnegirji",
            lang1="sme",
            lang2="nob",
            # closed=True,
            is_ordered=True,
            author="Nils Jernsletten",
            date_published="2007",
            isbn="82-7374-221-0",
        )

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def clean_lemma(self, lemma: str):
        lemma = lemma.replace(":", "")
        lemma = lemma.replace(",", "")
        return lemma.strip()

    def format_article(self, line):
        words = line.split()


        if words[0][-1] == ":":
            return f"<b>{line}</b>"
        
        bold = ""
        for word in words:
            bold += word 
            if not (word[-1] == "," or word[-1] == ")" or word[-1] == ";"):
                # print(word,"\t\t", line)
                break
            bold += " "

        text = line.replace(bold, f"<b>{bold.replace("(", "</b>(").replace(")", ")<b>")}</b>")

        if text.find("(=") != -1:
            text = text.replace("(=", "<b>(=") + "</b>"

        return text


    def parse_dict(self, file):
        articles = []
        
        with open(file, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            
            lemma = self.clean_lemma(line.split()[0])            

            rendered = self.to_html(line.strip())
        

            a = Article(
                dictionary=self.dictionary.id,
                lemma=lemma,
                rendered=rendered,
                lang=self.dictionary.lang1,
                article_number=i
            )

            articles.append(a)   
        
        return articles
    
    def to_html(self, line: str):
        return f"<div class=\"article\"><p>{self.format_article(line)}</p></div>"

