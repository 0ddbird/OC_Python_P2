import re

from typehints.types import Book, Url
from models.Page import Page


class BookPage(Page):
    def __init__(self, url: Url, parser, path, **kwargs):
        super().__init__(url, parser)
        self.url = url
        self.parser = parser
        self.cov_path = path
        self.session = None
        self.book = None
        self.verbose = "verbose" in kwargs.values()

    def get_book(self) -> Book:
        if self.book is None:
            book = self.parser.parse_book_page(self.html, self.url)
            self.book = book
        return self.book

    @staticmethod
    def incr_gen():
        first = True
        inc = 1
        while True:
            if first:
                first = False
                yield ""
            else:
                yield f"({inc})"
                inc += 1

    async def async_download_cover(self) -> None:
        async with self.session.get(self.book.image_url) as resp:
            cover = await resp.read()
        letters_only_re = r"[^a-zA-Z0-9 ]"
        f_name = re.sub(letters_only_re, "_", self.book.cover_name)
        base_path = self.cov_path / f"{self.book.category}/"
        incr_gen = self.incr_gen()
        while True:
            incr = next(incr_gen)
            f_path = base_path / f"_{f_name}{incr}.jpg"
            try:
                with open(f_path, "xb") as f:
                    f.write(cover)
                    self.incr_gen().close()
                    return
            except FileExistsError:
                pass
