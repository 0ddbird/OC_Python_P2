import sys
import asyncio
import aiohttp

from src.Pages.Catalogue import Catalogue
from src.Scraper.Scraper import Scraper
from src.Parser.Selectolax_ import SelectolaxParser


FIRST_URL = "https://books.toscrape.com/catalogue/page-1.html"


async def main(*args):
    scraper = Scraper()
    parser = SelectolaxParser()
    scraper.make_directories("../exports/")

    async with aiohttp.ClientSession() as session:
        catalogue = Catalogue(FIRST_URL, parser)
        catalogue.set_context(session)
        await catalogue.async_request_categories()
        scraper.set_categories(catalogue.all_categories)
        scraper.prompt_selection()
        await catalogue.async_get_categories_urls(scraper.categories)
        scraper.make_covers_subdirectories()
        await catalogue.async_get_books_urls()
        books = await catalogue.async_get_books(scraper.dir_covers)

    scraper.export_csv(books)


if __name__ == "__main__":
    if (
        sys.version_info[0] == 3
        and sys.version_info[1] >= 8
        and sys.platform.startswith("win")
    ):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(*sys.argv[1:]))
