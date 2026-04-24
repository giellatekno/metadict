from abc import ABC, abstractmethod
from pathlib import Path

from utils.dataclasses import Article, Dictionary


class BaseParser(ABC):
    dictionary: Dictionary
    articles: list[Article]

    def get_parsed_data(self):
        return self.dictionary, self.articles

    def format_article(self, text: str) -> str:
        text = text.replace("$>", "<b>").replace("<$", "</b>")
        text = text.replace("%>", "<i>").replace("<%", "</i>")
        return text.strip()

    def clean_text(self, text: str) -> str:
        return text.strip().replace("\n", "").replace("\t", " ")

    @abstractmethod
    def parse_dict(self, file: Path) -> list[Article]: ...
