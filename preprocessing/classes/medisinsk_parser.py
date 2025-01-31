from utils.dataclasses import Dictionary, Article

class MedisinskParser:
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="Medisinsk lommeparlør",
            lang1="nob",
            lang2="sme",
            closed=True,
            is_ordered=True,
            author="Egil Utsi",
            date_published="1998",
            isbn="978-82-329-0564-5",
        )
        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles
    
    def parse_dict(self, file):
        articles = []
        
        with open (file, "r") as f:
            lines = f.readlines()

        # Implement parsing logic here
        # Denne må jeg putte | inn i manuelt i filen
        return articles
        
    def to_html(self):
        # Implement HTML formatting logic here
        pass
    