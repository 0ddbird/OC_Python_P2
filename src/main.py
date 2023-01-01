import sys
import asyncio
import aiohttp


from src.modules.export import make_directory, export_csv
from src.modules.scrape_all import get_all_catalogue
from src.modules.scrape_categories import (
    request_categories,
    get_catalogue_selection,
)
from src.modules.scraper import get_books_urls, get_books
from src.views.menu import (
    prompt_scraping_mode,
    prompt_category_selection,
    MenuChoice,
)


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        covers_path = make_directory("../exports/covers")
        csv_path = make_directory("../exports/csv")
        first_url = "https://books.toscrape.com/catalogue/page-1.html"

        user_choice = prompt_scraping_mode()
        if user_choice == MenuChoice.quit:
            exit(0)
        if user_choice == MenuChoice.all:
            urls = await get_all_catalogue(session, first_url)
        else:
            all_categories = await request_categories(session, first_url)
            selected_categories = prompt_category_selection(all_categories)
            for cat_name, _ in selected_categories:
                make_directory(cat_name, covers_path)
            urls = await get_catalogue_selection(session, selected_categories)

        books_urls = await get_books_urls(session, urls)
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
