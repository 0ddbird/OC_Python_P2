from pathlib import Path

import asyncio

from src.Models.BookPage import BookPage
from src.Models.Page import Page
from src.parser_engines.selectolax_parser import Book


class CataloguePage(Page):
    def __init__(self, url: str, parser):
        super().__init__(url, parser)
        self.url = url
        self.parser = parser
        self.html = None

    def get_books_urls(self):
        if self.html is None:
            print("No HTML!")
        else:
            urls = self.parser.parse_books_urls(self.html)
            return urls

    async def async_get_books(self, path: Path) -> tuple[Book]:
        tasks = []
        for index, url in enumerate(self.books_urls):
            tasks.append(asyncio.create_task(self._get_book(url, index, path)))
        books = await asyncio.gather(*tasks)
        return books

    async def _get_book(self, url: str, index: int, path: Path) -> Book:
        book_page = BookPage(url, self.parser, path)
        book_page.set_context(self.session)
        await book_page.async_request()
        book = book_page.get_book()
        book_page.set_context(self.session)
        await book_page.async_request_cover(index)
        print(f"downloaded {book.title}")
        return book
