import sys
import time
import asyncio
import aiohttp

from src.modules.export import make_directory, export_csv
from src.modules.scraper import get_catalogue_pages_urls, get_books_urls, \
    get_all_books


async def main():
    async with aiohttp.ClientSession() as session:
        covers_path = make_directory("covers")
        csv_path = make_directory("csv")
        first_url = "https://books.toscrape.com/catalogue/page-1.html"
        cat_pages_urls = await get_catalogue_pages_urls(session, first_url)
        books_urls = await get_books_urls(session, cat_pages_urls)
        books = await get_all_books(session, books_urls, covers_path)
    export_csv(csv_path, books)


if __name__ == "__main__":
    if (
        sys.version_info[0] == 3
        and sys.version_info[1] >= 8
        and sys.platform.startswith("win")
    ):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
