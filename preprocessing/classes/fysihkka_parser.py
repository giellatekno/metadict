from utils.dataclasses import Dictionary, Article

class FysihkkaParser:
    def __init__(self, dictionary_id, file):
        l1, l2 = file.stem.split("-")[-2:]

        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Fysihkka- ja kemiijatearpmat",
            lang1=l1,
            lang2=l2,
            closed=True,
            is_ordered=True,
            author="Arne Nystad, Nils Henrik Valkeapää",
            date_published="1993",
            isbn="82-91047-15-4",
        )

        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def parse_dict(self, file):
        articles = []
        
        with open(file, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            
            lemma = line.split("|")[0].split("(")[0].strip()                

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
        # single line
        if line.find("\\") == -1:
            return f"<p><b>{line.split("|")[0].strip()} </b>{line.split("|")[1].strip()}</p>"

        # multi line
        lines = line.split("\\")
        html = f"<b>{lines[0].split("|")[0].strip()} </b>{lines[0].split("|")[1].strip()}"
        for l in lines[1:]:
            html += f"<br>&emsp;<b>{l.split("|")[0].strip()} </b>{l.split("|")[1].strip()}"

        return f"<p>{html}</p>"

