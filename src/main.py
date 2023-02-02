import sys
import asyncio
import aiohttp

from controllers.Controller import Controller

FIRST_URL = "https://books.toscrape.com/catalogue/page-1.html"


async def main():

    async with aiohttp.ClientSession() as session:

        app = Controller(FIRST_URL, session)
        app.select_parser(sys.argv[1:])
        app.make_directories("../exports/")
        app.init_catalogue()

        await app.async_get_categories()
        app.prompt_selection()
        await app.async_get_cat_urls()

        app.make_covers_subdirectories()

        await app.async_get_books_urls()
        await app.async_get_books()

    app.export_csv()
    print(f"Books data downloaded to {app.dir_base}")


if __name__ == "__main__":
    if (
        sys.version_info[0] == 3
        and sys.version_info[1] >= 8
        and sys.platform.startswith("win")
    ):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
