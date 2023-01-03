import sys
import asyncio
import aiohttp

from src.Models.FirstCataloguePage import FirstCataloguePage
from src.Models.Scraper import Scraper, MenuChoice
from src.parser_engines.bs_parser import BSParser
from src.parser_engines.selectolax_parser import SelectolaxParser

FIRST_URL = "https://books.toscrape.com/catalogue/page-1.html"


async def main():
    scraper = Scraper()
    parser = SelectolaxParser()
    # parser = BSParser()

    user_choice = scraper.prompt_scraping_mode()

    if user_choice == MenuChoice.quit:
        exit(0)

    dir_covers = scraper.make_directory("../exports/covers")
    dir_csv = scraper.make_directory("../exports/csv")

    async with aiohttp.ClientSession() as session:

        page = FirstCataloguePage(FIRST_URL, parser)
        page.set_context(session)
        await page.async_request_categories()
        scraper.set_categories(page.all_categories)

        if user_choice == MenuChoice.all:
            await page.get_all_categories_urls()
            scraper.set_selected_categories(page.all_categories)

        elif user_choice == MenuChoice.category:
            selected_categories = scraper.prompt_selection()
            scraper.set_selected_categories(selected_categories)
            await page.get_categories_urls(scraper.selected_categories)

        for category_name, _ in scraper.selected_categories:
            scraper.make_directory(category_name, dir_covers)

        await page.get_books_urls()
        books = await page.async_get_books(dir_covers)

    scraper.export_csv(dir_csv, books)


if __name__ == "__main__":
    if (
        sys.version_info[0] == 3
        and sys.version_info[1] >= 8
        and sys.platform.startswith("win")
    ):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
