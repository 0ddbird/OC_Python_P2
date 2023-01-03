import csv
from pathlib import Path
from enum import Enum
from typing import List, Tuple
from src.parser_engines.selectolax_parser import Book

Name = str
Url = str
Category = Tuple[Name, Url]


class MenuChoice(Enum):
    all = 1
    category = 2
    quit = 3


class Scraper:
    def __init__(self):
        self.categories = None
        self.selected_categories = None
        self.selected_cat_urls = None

    @staticmethod
    def prompt_scraping_mode() -> MenuChoice:
        while True:
            choice = input(
                "Type [1] to get all books\nType [2] to select "
                "categories\nType [3] to exit\n_"
            )
            switch = {
                "1": MenuChoice.all,
                "2": MenuChoice.category,
                "3": MenuChoice.quit,
            }
            if choice in switch:
                return switch[choice]
            else:
                print("Please type 1, 2 or 3 to choose the scraping mode")
                input("Type enter to select categories")

    def set_categories(self, categories) -> None:
        self.categories = categories

    def set_selected_categories(self, categories) -> None:
        self.selected_categories = categories

    def set_selected_category_urls(self, urls: List[Url]):
        self.selected_cat_urls = urls

    @staticmethod
    def make_directory(dir_name: str, base_path=None) -> Path:
        if base_path:
            target_path = base_path / f"{dir_name}"
        else:
            target_path = Path.cwd() / f"{dir_name}"
        target_path.mkdir(parents=True, exist_ok=True)
        return target_path

    def prompt_selection(self) -> List[Category]:
        while True:
            categories = self.categories
            category_names = [category[0] for category in categories]
            for index, category_name in enumerate(category_names):
                print(f"{index + 1} : {category_name}")
            user_input = input(
                "Please type the category number "
                "you want to scrape separated by a comma\n"
                "ex: 1, 2, 30, 50, 8, 12\n"
            ).split(",")

            try:
                cat_input = [int(char_num.strip()) for char_num in user_input]
                if not all(1 <= num <= len(categories) for num in cat_input):
                    print(f"Numbers must be between 1 and {len(categories)}")
                    input("Press Enter to try again")
                else:
                    selected_categories = [
                        category
                        for category in categories
                        if categories.index(category) + 1 in cat_input
                    ]
                    return selected_categories
            except ValueError:
                print("Please make sure you enter numbers only")
                input("Press Enter to try again")

    @staticmethod
    def export_csv(path: Path, books: tuple[Book]) -> None:
        target_path = Path.cwd() / ".." / "exports" / f"{path}"
        target_path.mkdir(parents=True, exist_ok=True)
        with open(
            target_path / f"export.csv", "w", encoding="utf-8", newline=""
        ) as f:
            writer = csv.writer(f)
            writer.writerow(books[0]._fields)
            for book in books:
                writer.writerow(book)
