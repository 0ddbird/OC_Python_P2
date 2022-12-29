import asyncio
import itertools

from src.modules.export import download_cover
from src.modules.parser import get_page_count, parse_books_urls, build_book


async def async_get_page_html(session, url):
    async with session.get(url) as resp:
        return await resp.text()


async def get_catalogue_pages_urls(session, first_url):
    base_url = "https://books.toscrape.com/catalogue/page-"
    first_page_html = await async_get_page_html(session, first_url)
    last_page = get_page_count(first_page_html) + 1
    urls = [f"{base_url}{page_num}.html" for page_num in range(1, last_page)]
    return urls


async def get_urls_in_page(session, url):
    html = await async_get_page_html(session, url)
    return parse_books_urls(html)


async def get_books_urls(session, catalogue_pages_urls):
    tasks = []
    for url in catalogue_pages_urls:
        tasks.append(asyncio.create_task(get_urls_in_page(session, url)))
    url_lists = await asyncio.gather(*tasks)
    book_urls = list(itertools.chain(*url_lists))
    return [f"https://books.toscrape.com/catalogue/{u}" for u in book_urls]


async def get_book(session, book_url, cover_path):
    book_html = await async_get_page_html(session, book_url)
    book = build_book(book_html, book_url)
    await download_cover(session, cover_path, book.cover_url, book.cover_name)
    return book


async def get_all_books(session, books_urls, covers_path):
    tasks = []
    for url in books_urls:
        tasks.append(asyncio.create_task(get_book(session, url, covers_path)))
    return await asyncio.gather(*tasks)
