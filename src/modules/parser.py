from collections import namedtuple
from selectolax.parser import HTMLParser

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_page_count(html_str):
    dom_count = (
        HTMLParser(html_str).css_first("form.form-horizontal").css("strong")
    )
    all_books_count = int(dom_count[0].text())
    page_books_count = int(dom_count[-1].text())
    pages_count = all_books_count // page_books_count
    return pages_count


def parse_books_urls(html_str):
    li = HTMLParser(html_str).css_first("section ol").css("li")
    return [item.css_first("a").attributes["href"] for item in li]


def build_book(book_html, book_url):
    html = HTMLParser(book_html).css("div.page_inner")[1]
    num_count = slice(10, -10)

    menu = html.css("ul.breadcrumb > li")
    title = menu[-1].text()
    category = menu[-2].css_first("a").text()
    description_block = html.css_first("#product_description + p")
    description = (
        html.css_first("#product_description + p").text()
        if description_block
        else "No description"
    )
    table_rows = html.css("tr > td")
    upc = table_rows[0].text()
    etp = table_rows[2].text()[1:]
    itp = table_rows[3].text()[1:]
    stock = table_rows[5].text()[num_count]
    rating_class = (
        html.css_first(".star-rating")
        .attributes["class"]
        .replace("star-rating ", "")
    )
    rating = RATINGS[rating_class]
    cover = html.css_first("#product_gallery img")
    cover_url = cover.attributes["src"].replace(
        "../..", "https://books.toscrape.com/"
    )
    cover_name = cover.attributes["alt"]

    Book = namedtuple(
        "Book",
        "url upc title itp etp stock description "
        "category rating cover_url cover_name",
    )

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
