from abc import ABC
from aiohttp import ClientSession


class Page(ABC):
    def __init__(self, url: str, parser):
        self.url = url
        self.html = None
        self.session = None
        self.parser = parser
        self.books_urls = None

    urls = {
        "base": "https://books.toscrape.com/catalogue",
        "first": "https://books.toscrape.com/catalogue/page-1.html",
        "page_frag": "https://books.toscrape.com/catalogue/page-",
    }

    def set_context(self, session: ClientSession) -> None:
        self.session = session

    async def async_request(self) -> str:
        async with self.session.get(self.url) as resp:
            self.html = await resp.text()
            return self.html
