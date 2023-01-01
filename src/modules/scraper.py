import asyncio
from aiohttp import ClientSession as Cs
import itertools
from pathlib import Path
from typing import List

from src.modules.export import download_cover
from src.modules.parser import parse_catalogue_page, build_book, Book


async def get_html(session: Cs, url: str) -> str:
    async with session.get(url) as resp:
        return await resp.text()


async def get_urls_in_page(session: Cs, url: str) -> List[str]:
    html = await get_html(session, url)
    books_urls = parse_catalogue_page(html)
    print(books_urls[0])
    return books_urls


async def get_books_urls(session: Cs, cat_pages_urls: List[str]) -> list[str]:
    tasks = []
    for url in cat_pages_urls:
        tasks.append(asyncio.create_task(get_urls_in_page(session, url)))
    url_lists = await asyncio.gather(*tasks)
    book_urls = list(itertools.chain(*url_lists))
    return book_urls


async def get_book(session: Cs, url: str, path: Path) -> Book:
    book_html = await get_html(session, url)
    book = build_book(book_html, url)
    await download_cover(
        session, path, book.cover_url, book.cover_name, book.category
    )
    print(f"downloaded {book.title}")

    return book


async def get_books(session: Cs, urls: List[str], path: Path) -> tuple[Book]:
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(get_book(session, url, path)))
        books = await asyncio.gather(*tasks)
    return books
