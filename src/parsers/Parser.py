from abc import ABC, abstractmethod
from typehints.types import Book


class Parser(ABC):
    _ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    def __repr__(self):
        return "Parser(ABC)"

    @staticmethod
    @abstractmethod
    def parse_category_urls(html):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def parse_page_count(html):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def parse_books_urls(html):
        raise NotImplementedError

    @abstractmethod
    def parse_book_page(self, html, url) -> Book:
        raise NotImplementedError
