from selectolax.parser import HTMLParser

from typehints.types import Book
from parsers.Parser import Parser


class SelectolaxParser(Parser):
    @staticmethod
    def parse_category_urls(html):
        categories = []
        anchors = HTMLParser(html).css(".nav-list > li > ul > li > a")
        for anchor in anchors:
            cat_name = anchor.text().strip()
            url = anchor.attributes["href"]
            if not url:
                return []
            categories.append((cat_name, url))
        return categories

    @staticmethod
    def parse_page_count(html) -> int:
        dom_count = (
            HTMLParser(html).css_first("form.form-horizontal").css("strong")
        )
        if len(dom_count) < 3:
            return 1
        page_books_count = int(dom_count[-1].text())
        all_books_count = int(dom_count[0].text())
        pages_count, rest = divmod(all_books_count, page_books_count)
        return pages_count if rest == 0 else pages_count + 1

    @staticmethod
    def parse_books_urls(html_str: str) -> list[str]:
        lis = HTMLParser(html_str).css_first("section ol").css("li")

        return [
            "https://books.toscrape.com/catalogue/"
            + li.css_first("a").attributes["href"].replace("../../../", "")
            for li in lis
        ]

    def parse_book_page(self, book_html: str, book_url: str) -> Book:
        html = HTMLParser(book_html).css("div.page_inner")[1]
        num_count = slice(10, -10)

        menu = html.css("ul.breadcrumb > li")
        title = menu[-1].text().replace("'", "")
        category = menu[-2].css_first("a").text()
        description_block = html.css_first("#product_description + p")
        description = (
            description_block.text().replace("'", "")
            if description_block
            else "No description"
        )
        table_rows = html.css("tr > td")
        upc = table_rows[0].text()
        etp = table_rows[2].text()[1:]
        itp = table_rows[3].text()[1:]
        stock = table_rows[5].text()[num_count].strip()
        rating_class = (
            html.css_first(".star-rating")
            .attributes["class"]
            .replace("star-rating ", "")
        )
        rating = self._ratings[rating_class]
        cover = html.css_first("#product_gallery img")
        cover_url = cover.attributes["src"].replace(
            "../..", "https://books.toscrape.com"
        )
        cover_name = cover.attributes["alt"].replace("'", "")

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
