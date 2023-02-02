import csv
from pathlib import Path

from parsers.Selectolax_ import SelectolaxParser
from parsers.BeautifulSoup_ import BeautifulSoupParser
from middleware.InputValidationMiddleware import InputValidationMiddleware
from views.Home import display_home
from views.Selection import display_categories, prompt_selection
from models.Catalogue import Catalogue


class Controller:
    def __init__(self, first_url, session):
        self.dir_base = None
        self.dir_csv = None
        self.dir_covers = None
        self.categories = None
        self.user_selection = None
        self.categories_urls = None
        self.input_result = {"value": set(), "valid": False, "message": ""}
        self.first_url = first_url
        self.parser = None
        self.catalogue = None
        self.session = session
        self.books = None

    def select_parser(self, args: list) -> None:
        self.parser = (
            BeautifulSoupParser() if "-bs4" in args else SelectolaxParser()
        )

    def init_catalogue(self) -> None:
        self.catalogue = Catalogue(self.first_url, self.parser)
        self.catalogue.session = self.session

    async def async_get_categories(self) -> None:
        self.categories = await self.catalogue.async_request_categories()

    async def async_get_cat_urls(self) -> None:
        await self.catalogue.async_get_categories_urls(self.user_selection)

    async def async_get_books_urls(self) -> None:
        await self.catalogue.async_get_books_urls()

    async def async_get_books(self) -> None:
        self.books = await self.catalogue.async_get_books(self.dir_covers)

    def prompt_selection(self) -> None:
        while True:
            categories = self.categories
            category_names = [category[0] for category in categories]

            display_home()
            display_categories(category_names, True)

            user_input = prompt_selection()
            input_validator = InputValidationMiddleware()
            sel, valid, msg = input_validator.decode_input(
                user_input, len(categories)
            ).values()

            if not valid:
                print(msg)
                input("Press Enter to try again")
            else:
                self.user_selection = [
                    category
                    for category in categories
                    if categories.index(category) + 1 in sel
                ]
                break

    @staticmethod
    def make_directory(dir_name: str, base_path=None) -> Path:
        if base_path:
            target_path = base_path / f"{dir_name}"
        else:
            target_path = Path.cwd() / f"{dir_name}"
        target_path.mkdir(parents=True, exist_ok=True)
        return target_path.resolve()

    def make_directories(self, rel_path: str) -> None:
        self.dir_base = self.make_directory(rel_path)
        self.dir_covers = self.make_directory(f"{rel_path}covers")
        self.dir_csv = self.make_directory(f"{rel_path}csv")

    def make_covers_subdirectories(self) -> None:
        for category_name, _ in self.user_selection:
            self.make_directory(category_name, self.dir_covers)

    def export_csv(self) -> None:
        target_path = Path.cwd() / ".." / "exports" / f"{self.dir_csv}"
        target_path.mkdir(parents=True, exist_ok=True)
        with open(
            target_path / "export.csv", "w", encoding="utf-8", newline=""
        ) as f:
            writer = csv.writer(f)
            writer.writerow(self.books[0]._fields)
            for book in self.books:
                writer.writerow(book)
