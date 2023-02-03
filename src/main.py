import sys
import asyncio
import aiohttp

from controller.Controller import Controller


async def main():
    async with aiohttp.ClientSession() as session:
        app = Controller(session, sys.argv[1:])
        app.make_directories("../exports/")
        await app.async_get_categories()
        app.prompt_selection()
        await app.async_get_books()
        app.export_categories_csv()
        print(f"Books data downloaded to {app.fs_controller.dir_base}")

if __name__ == "__main__":
    if (
        sys.version_info[0] == 3
        and sys.version_info[1] >= 8
        and sys.platform.startswith("win")
    ):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
