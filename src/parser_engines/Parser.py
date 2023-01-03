from abc import ABC, abstractmethod


class Parser(ABC):
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

    @staticmethod
    @abstractmethod
    def parse_book_page(html, url):
        raise NotImplementedError
