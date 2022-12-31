from src.modules.parser import get_page_count
from src.modules.scraper import get_html
from typing import List
from aiohttp import ClientSession as Cs

BASE_URL = "https://books.toscrape.com/catalogue/page-"


async def get_all_catalogue(session: Cs, first_url: str) -> List[str]:

    first_page_html = await get_html(session, first_url)
    last_page_num = get_page_count(first_page_html) + 1
    urls = [
        f"{BASE_URL}{page_num}.html" for page_num in range(1, last_page_num)
    ]
    return urls
