import sys
import asyncio
import aiohttp

from src.pages.Catalogue import Catalogue
from src.scraper.Scraper import Scraper
from src.views.cli import pick_from_cli

FIRST_URL = "https://books.toscrape.com/catalogue/page-1.html"


async def main():

    scraper = Scraper()
    scraper.make_directories("../exports/")
    parser = pick_from_cli(sys.argv[1:])

    async with aiohttp.ClientSession() as session:

        catalogue = Catalogue(FIRST_URL, parser)
        catalogue.set_context(session)
        await catalogue.async_request_categories()
        scraper.set_categories(catalogue.categories)

        scraper.prompt_selection()
        await catalogue.async_get_categories_urls(scraper.user_selection)
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
    asyncio.run(main())
