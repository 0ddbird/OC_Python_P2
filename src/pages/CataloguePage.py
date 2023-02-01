import time
from pathlib import Path
import asyncio

from src.types.types import Book
from src.pages.BookPage import BookPage
from src.pages.Page import Page
from src.parser import Parser
from src.views.cli import log_progress, clr, AnsiClr


class CataloguePage(Page):
    def __init__(self, url: str, parser: Parser):
        super().__init__(url, parser)
        self.url = url
        self.parser = parser
        self.html = None
        self.completed = 0

    def get_books_urls(self) -> list[str]:
        if self.html is None:
            print("No HTML!")
        else:
            urls = self.parser.parse_books_urls(self.html)
            return urls

    async def async_get_books(self, path: Path) -> tuple[Book]:
        print(
            clr(AnsiClr.GREEN, f"Downloading {len(self.books_urls)} books...")
        )

        start_time = time.perf_counter()
        tasks = []
        for url in self.books_urls:
            tasks.append(asyncio.create_task(self._get_book(url, path)))
        books = await asyncio.gather(*tasks)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"\nDone in {total_time:.4f}s\n")
        return books

    async def _get_book(self, url: str, path: Path) -> Book:
        book_page = BookPage(url, self.parser, path)
        book_page.set_context(self.session)
        await book_page.async_request()
        book = book_page.get_book()
        book_page.set_context(self.session)
        await book_page.async_download_cover()
        self.completed += 1
        log_progress(self.completed, len(self.books_urls))
        return book
