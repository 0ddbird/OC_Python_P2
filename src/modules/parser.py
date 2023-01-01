from typing import Set, Tuple
from collections import namedtuple
from selectolax.parser import HTMLParser

from src.parser_engines.bs_parser import bs4_parse
from src.parser_engines.selectolax_parser import selectolax_parse

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

Book = namedtuple(
    "Book",
    "url upc title itp etp stock description "
    "category rating cover_url cover_name",
)


def get_page_count(html_str: str) -> int:
    dom_count = (
        HTMLParser(html_str).css_first("form.form-horizontal").css("strong")
    )
    if len(dom_count) < 3:
        return 1
    page_books_count = int(dom_count[-1].text())
    all_books_count = int(dom_count[0].text())
    pages_count, rest = divmod(all_books_count, page_books_count)
    if rest == 0:
        return pages_count
    return pages_count + 1


def parse_category_urls(html_str: str) -> Set[Tuple[str, str]] or None:
    categories = set()

    cat_anchor_tags = HTMLParser(html_str).css(
        ".nav-list > li > ul > li " "> a"
    )
    for anchor_tag in cat_anchor_tags:
        cat_name = anchor_tag.text().strip()
        first_page_url = anchor_tag.attributes["href"]
        if not first_page_url:
            return None
        categories.add((cat_name, first_page_url))
    return categories


def parse_catalogue_page(html_str: str) -> list[str]:
    li_elements = HTMLParser(html_str).css_first("section ol").css("li")

    return [
        f"https://books.toscrape.com/catalogue/"
        + li.css_first("a").attributes["href"].replace("../../../", "")
        for li in li_elements
    ]


def build_book(book_html: str, book_url: str) -> Book:
    return selectolax_parse(book_html, book_url)
    # return bs4_parse(book_html, book_url)
