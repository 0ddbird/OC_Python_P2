import sys
import asyncio
import aiohttp

from src.modules.export import make_directory, export_csv
from src.modules.scraper import get_books_urls, get_books
from src.views.menu import main_menu


def get_all_books():
    pass


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        covers_path = make_directory("covers")
        csv_path = make_directory("csv")
        first_url = "https://books.toscrape.com/catalogue/page-1.html"
        selected_urls = await main_menu(session, first_url)
        books_urls = await get_books_urls(session, selected_urls)
        books = await get_books(session, books_urls, covers_path)

    export_csv(csv_path, books)


if __name__ == "__main__":
    if (
        sys.version_info[0] == 3
        and sys.version_info[1] >= 8
        and sys.platform.startswith("win")
    ):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
