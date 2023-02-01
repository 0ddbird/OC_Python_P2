import asyncio
import itertools

from src.types.types import Category, Url
from src.pages.CataloguePage import CataloguePage
from src.parser.Parser import Parser


class Catalogue(CataloguePage):
    def __init__(self, url: Url, parser: Parser):
        super().__init__(url, parser)
        self.url = url
        self.parser = parser
        self.html = None
        self.categories = None
        self.categories_urls = None
        self.books_urls = None
        self.size = None

    async def async_request_categories(self) -> None:
        if self.html is None:
            self.html = await self.async_request()
        categories = self.parser.parse_category_urls(self.html)
        self.categories = categories
        self.size = len(categories)

    async def async_get_categories_urls(
        self, category_urls: list[Category]
    ) -> None:
        if len(category_urls) == self.size:
            await self.async_get_all_categories_urls()
        else:
            await self.async_get_selected_categories_urls(category_urls)

    async def async_get_all_categories_urls(self) -> None:
        if self.html is None:
            self.html = await self.async_request()
        last_page_num = self.parser.parse_page_count(self.html)
        urls = [
            f"{self.urls['page_frag']}{page_num}.html"
            for page_num in range(1, last_page_num + 1)
        ]
        self.categories_urls = urls

    async def async_get_selected_categories_urls(
        self, category_urls: list[Category]
    ) -> None:
        coros = []
        for _, url in category_urls:
            url = f"{self.urls['base']}/{url}".replace("index.html", "")
            coros.append(asyncio.create_task(self._get_category_urls(url)))
        url_lists = await asyncio.gather(*coros)
        urls = [*itertools.chain(*url_lists)]
        f_urls = [u.replace("../../..", self.urls["base"]) for u in urls]
        self.categories_urls = f_urls

    async def _get_category_urls(self, url: Url) -> list[Url]:
        page = CataloguePage(url, self.parser)
        page.set_context(self.session)
        html = await page.async_request()
        page_count = page.parser.parse_page_count(html)
        if page_count == 1:
            return [f"{url}index.html"]
        return [
            f"{url}page-{page_num}.html"
            for page_num in range(1, page_count + 1)
        ]

    async def async_get_books_urls(self) -> None:
        coros = []
        for url in self.categories_urls:
            coros.append(asyncio.create_task(self._get_urls_in_page(url)))
        url_lists = await asyncio.gather(*coros)
        books_urls = list(itertools.chain(*url_lists))
        self.books_urls = books_urls

    async def _get_urls_in_page(self, url: Url) -> list[Url]:
        page = CataloguePage(url, self.parser)
        page.set_context(self.session)
        await page.async_request()
        books_urls = page.get_books_urls()
        return books_urls
