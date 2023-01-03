import asyncio
import itertools

from src.Models.CataloguePage import CataloguePage


class FirstCataloguePage(CataloguePage):
    def __init__(self, url: str, parser):
        super().__init__(url, parser)
        self.url = url
        self.parser = parser
        self.html = None
        self.all_categories = None
        self.categories_urls = None
        self.books_urls = None

    BASE_URL = "https://books.toscrape.com/catalogue/page-"

    async def async_request_categories(self):
        if self.html is None:
            self.html = await self.async_request()
        categories = self.parser.parse_category_urls(self.html)
        self.all_categories = categories

    async def get_all_categories_urls(self):
        if self.html is None:
            self.html = await self.async_request()
        last_page_num = self.parser.parse_page_count(self.html)
        urls = [
            f"{self.BASE_URL}{page_num}.html"
            for page_num in range(1, last_page_num + 1)
        ]
        self.categories_urls = urls

    async def get_categories_urls(self, category_urls):
        tasks = []
        for _, url in category_urls:
            url = f"https://books.toscrape.com/catalogue/{url}".replace(
                "index.html", ""
            )
            tasks.append(asyncio.create_task(self._get_category_urls(url)))
        url_list = await asyncio.gather(*tasks)

        unpacked_urls = [*itertools.chain(*url_list)]
        formatted_urls = [
            u.replace("../../..", "https://books.toscrape.com/catalogue")
            for u in unpacked_urls
        ]
        self.categories_urls = formatted_urls

    async def _get_category_urls(self, url):
        page = CataloguePage(url, self.parser)
        page.set_context(self.session)
        html = await page.async_request()
        page_count = page.parser.parse_page_count(html)
        if page_count > 1:
            categories_urls = [
                f"{url}page-{page_num}.html"
                for page_num in range(1, page_count + 1)
            ]
        else:
            categories_urls = [f"{url}index.html"]
        return categories_urls

    async def get_books_urls(self):
        tasks = []
        for url in self.categories_urls:
            tasks.append(asyncio.create_task(self._get_urls_in_page(url)))
        url_lists = await asyncio.gather(*tasks)
        books_urls = list(itertools.chain(*url_lists))
        self.books_urls = books_urls

    async def _get_urls_in_page(self, url):
        page = CataloguePage(url, self.parser)
        page.set_context(self.session)
        await page.async_request()
        books_urls = page.get_books_urls()
        return books_urls
