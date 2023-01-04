import sys
import asyncio
import aiohttp

from src.Models.Catalogue import Catalogue
from src.Models.Scraper import Scraper, MenuChoice
from src.parser_engines.selectolax_parser import SelectolaxParser


FIRST_URL = "https://books.toscrape.com/catalogue/page-1.html"


async def main():

    scraper = Scraper()
    user_choice = scraper.prompt_scraping_mode()

    if user_choice == MenuChoice.quit:
        exit(0)

    parser = SelectolaxParser()
    scraper.make_directories("../exports/")

    async with aiohttp.ClientSession() as session:

        catalogue = Catalogue(FIRST_URL, parser)
        catalogue.set_context(session)
        await catalogue.async_request_categories()
        scraper.set_categories(catalogue.all_categories)

        if user_choice == MenuChoice.category:
            scraper.prompt_selection()
            await catalogue.async_get_categories_urls(scraper.categories)
        else:
            scraper.set_selected_categories(catalogue.all_categories)
            await catalogue.async_get_all_categories_urls()

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
