import asyncio

from aiohttp import ClientSession as Cs

from src.modules.parser import parse_category_urls, get_page_count
from src.modules.scraper import get_html
from typing import List, Tuple, Set

BASE_URL = "https://books.toscrape.com/catalogue/category/books/"


async def request_categories(session, first_url) -> Set[Tuple[str, str]]:
    homepage_html = await get_html(session, first_url)
    categories = parse_category_urls(homepage_html)
    return categories


async def get_category_urls(session, category, url):
    # For one category index url
    cat_home_html = await get_html(session, url)
    page_count = get_page_count(cat_home_html)
    category_urls = [
        f"{BASE_URL}{category}_{page_count}.html" in range(1, page_count)
    ]
    return category_urls


async def get_catalogue_selection(
    session: Cs, category_urls: List[Tuple]
) -> List[str]:
    tasks = []

    for category, url in category_urls:
        tasks.append(
            asyncio.create_task(get_category_urls(session, category, url))
        )
    url_list = await asyncio.gather(*tasks)

    return url_list
