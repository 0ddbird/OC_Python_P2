from pathlib import Path

import asyncio

from src.Typing.types import Book
from src.Pages.BookPage import BookPage
from src.Pages.Page import Page
from src.Parser import Parser


class CataloguePage(Page):
    def __init__(self, url: str, parser: Parser):
        super().__init__(url, parser)
        self.url = url
        self.parser = parser
        self.html = None

    def get_books_urls(self) -> list[str]:
        if self.html is None:
            print("No HTML!")
        else:
            urls = self.parser.parse_books_urls(self.html)
            return urls

    async def async_get_books(self, path: Path) -> tuple[Book]:
        tasks = []
        for url in self.books_urls:
            tasks.append(asyncio.create_task(self._get_book(url, path)))
        books = await asyncio.gather(*tasks)
        return books

    async def _get_book(self, url: str, path: Path) -> Book:
        book_page = BookPage(url, self.parser, path)
        book_page.set_context(self.session)
        await book_page.async_request()
        book = book_page.get_book()
        book_page.set_context(self.session)
        await book_page.async_download_cover()
        return book
