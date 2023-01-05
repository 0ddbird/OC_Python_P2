import re
from bs4 import BeautifulSoup
from src.Typing.types import Book
from src.Parser.Parser import Parser


class BSParser(Parser):
    @staticmethod
    def parse_category_urls(html):
        categories = []
        anchors = BeautifulSoup(html, "lxml").select(
            ".nav-list > li > ul > li " "> a"
        )
        for anchor in anchors:
            cat_name = anchor.get_text().strip()
            url = anchor.attrs["href"]
            if not url:
                return []
            categories.append((cat_name, url))
        return categories

    @staticmethod
    def parse_page_count(html):
        dom_count = (
            BeautifulSoup(html, "lxml")
            .select_one("form.form-horizontal")
            .select("strong")
        )
        if len(dom_count) < 3:
            return 1
        page_books_count = int(dom_count[-1].get_text())
        all_books_count = int(dom_count[0].get_text())
        pages_count, rest = divmod(all_books_count, page_books_count)
        return pages_count if rest == 0 else pages_count + 1

    @staticmethod
    def parse_books_urls(html):
        lis = (
            BeautifulSoup(html, "lxml")
            .select_one("section " "ol")
            .select("li")
        )

        return [
            "https://books.toscrape.com/catalogue/"
            + li.select_one("a").attrs["href"].replace("../../../", "")
            for li in lis
        ]

    def parse_book_page(self, book_html: str, book_url: str) -> Book:
        html = BeautifulSoup(book_html, "lxml").select("div.page_inner")[1]
        num_count = slice(10, -10)

        menu = html.select("ul.breadcrumb > li")
        title = menu[-1].text.replace("'", "'")
        category = menu[-2].find("a").get_text()
        description_block = html.find("#product_description + p")
        description = (
            description_block.get_text().replace("'", "'")
            if description_block
            else "No description"
        )
        table_rows = html.select("tr > td")
        upc = table_rows[0].get_text()
        itp = float(table_rows[2].get_text()[1:])
        etp = float(table_rows[3].get_text()[1:])
        stock = table_rows[5].get_text()[num_count]
        rating_class = html.find(
            "p", attrs={"class": re.compile("^star-rating.*")}
        ).attrs["class"][-1]
        rating = self._ratings[rating_class]
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
