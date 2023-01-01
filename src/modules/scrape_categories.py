import asyncio
import itertools

from aiohttp import ClientSession as Cs

from src.modules.parser import parse_category_urls, get_page_count, T_category
from src.modules.scraper import get_html
from typing import List, Tuple

BASE_URL = "https://books.toscrape.com/catalogue/category/books/"


async def request_categories(session, first_url) -> List[T_category]:
    homepage_html = await get_html(session, first_url)
    categories = parse_category_urls(homepage_html)
    return categories


async def get_category_urls(session, category, url):
    cat_home_html = await get_html(session, url)
    page_count = get_page_count(cat_home_html)
    if page_count > 1:
        category_urls = [
            f"{url}page-{page_num}.html"
            for page_num in range(1, page_count + 1)
        ]
    else:
        category_urls = [f"{url}index.html"]
    return category_urls


async def get_catalogue_selection(
    session: Cs, category_urls: List[Tuple]
) -> List[str]:
    tasks = []
    for category, url in category_urls:
        full_url = f"https://books.toscrape.com/catalogue/{url}".replace(
            "index.html", ""
        )

        tasks.append(
            asyncio.create_task(get_category_urls(session, category, full_url))
        )
    url_list = await asyncio.gather(*tasks)

    unpacked_urls = [*itertools.chain(*url_list)]
    formatted_urls = [
        u.replace("../../..", "https://books.toscrape.com/catalogue")
        for u in unpacked_urls
    ]
    return formatted_urls
