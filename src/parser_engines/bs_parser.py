from collections import namedtuple
from bs4 import BeautifulSoup
import re

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

Book = namedtuple(
    "Book",
    "url upc title itp etp stock description "
    "category rating cover_url cover_name",
)


def bs4_parse(book_html: str, book_url: str) -> Book:
    html = BeautifulSoup(book_html, "lxml").select("div.page_inner")[1]
    num_count = slice(10, -10)

    menu = html.select("ul.breadcrumb > li")
    title = menu[-1].text
    category = menu[-2].find("a").get_text()
    description_block = html.find("#product_description + p")
    description = (
        description_block.get_text() if description_block else "No description"
    )
    table_rows = html.select("tr > td")
    upc = table_rows[0].get_text()
    itp = float(table_rows[2].get_text()[1:])
    etp = float(table_rows[3].get_text()[1:])
    stock = table_rows[5].get_text()[num_count]
    rating_class = html.find(
        "p", attrs={"class": re.compile("^star-rating.*")}
    ).attrs["class"][-1]
    rating = RATINGS[rating_class]
    cover = html.select_one("#product_gallery img")
    cover_url = cover.attrs["src"].replace(
        "../..", "https://books.toscrape.com/"
    )
    cover_name = cover["alt"]
    return Book(
        book_url,
        upc,
        title,
        itp,
        etp,
        stock,
        description,
        category,
        rating,
        cover_url,
        cover_name,
    )
