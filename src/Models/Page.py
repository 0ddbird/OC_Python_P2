from abc import ABC
from aiohttp import ClientSession


class Page(ABC):
    def __init__(self, url: str, parser):
        self.url = url
        self.response = None
        self.status_code = None
        self.html = None
        self.session = None
        self.parser = parser
        self.books_urls = None

    def set_context(self, session: ClientSession):
        self.session = session

    async def async_request(self):
        async with self.session.get(self.url) as resp:
            self.html = await resp.text()
            return self.html
