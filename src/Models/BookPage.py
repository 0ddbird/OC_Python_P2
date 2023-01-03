import re

from src.Models.Page import Page


class BookPage(Page):
    def __init__(self, url, parser, path):
        super().__init__(url, parser)
        self.url = url
        self.parser = parser
        self.cover_path = path
        self.session = None
        self.book = None

    def get_book(self):
        if self.book is None:
            book = self.parser.parse_book_page(self.html, self.url)
            self.book = book
        return self.book

    async def async_request_cover(self):
        async with self.session.get(self.book.cover_url) as resp:
            cover = await resp.read()
        letters_only_re = r"[^a-zA-Z0-9]"
        file_name = re.sub(letters_only_re, "_", self.book.cover_name)
        file_path = self.cover_path / f"{self.book.category}/{file_name}.jpg"
        with open(file_path, "wb") as f:
            f.write(cover)
