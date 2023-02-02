from itertools import groupby
from operator import attrgetter
from parsers.Selectolax_ import SelectolaxParser
from parsers.BeautifulSoup_ import BeautifulSoupParser
from controller.FileSystemController import FileSystemController
from middleware.InputValidationMiddleware import InputValidationMiddleware
from views.Home import display_home
from views.Selection import display_categories, prompt_selection
from models.Catalogue import Catalogue


class Controller:
    def __init__(self, first_url, session):
        self.fs_controller = FileSystemController()
        self.categories = None
        self.user_selection = None
        self.categories_urls = None
        self.input_result = {"value": set(), "valid": False, "message": ""}
        self.first_url = first_url
        self.parser = None
        self.catalogue = None
        self.session = session
        self.books = None
        self.book_lists = None

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
        self.books = await self.catalogue.async_get_books(
            self.fs_controller.dir_covers
        )

    def split_books_by_category(self):
        sorted_books = sorted(self.books, key=attrgetter("category"))
        self.book_lists = [
            list(group)
            for _, group in groupby(sorted_books, key=attrgetter("category"))
        ]

    def export_categories_csv(self) -> None:
        self.split_books_by_category()
        for book_list in self.book_lists:
            self.fs_controller.export_csv(book_list)

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
                self.fs_controller.make_covers_subdirectories(
                    self.user_selection
                )
                break
