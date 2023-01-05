import csv
from pathlib import Path

from src.typing.types import Category, Url, Book

ERROR_MESSAGES = {
    "char": "Forbidden character",
    "boundaries": "Category number is out of boundaries",
    "range_format": "Select a range between 2 numbers separated by a '-'",
}

margin = 20
ASCII = (
    f"{' ' * margin + '    _______'}\n"
    f"{' ' * margin + '   /      /,'}\n"
    f"{' ' * margin + '  / B.W. //'}\n"
    f"{' ' * margin + ' /______//'}\n"
    f"{' ' * margin + '(______(/'}\n"
)


class Scraper:
    def __init__(self):
        self.dir_csv = None
        self.dir_covers = None
        self.catalogue = None
        self.user_selection = None
        self.categories_urls = None
        self.input_result = {"value": set(), "valid": False, "message": ""}

    def set_categories(self, categories: list[Category]) -> None:
        self.catalogue = categories

    def set_selected_category_urls(self, urls: list[Url]):
        self.categories_urls = urls

    @staticmethod
    def make_directory(dir_name: str, base_path=None) -> Path:
        if base_path:
            target_path = base_path / f"{dir_name}"
        else:
            target_path = Path.cwd() / f"{dir_name}"
        target_path.mkdir(parents=True, exist_ok=True)
        return target_path

    def make_directories(self, rel_path: str):
        self.dir_covers = self.make_directory(f"{rel_path}covers")
        self.dir_csv = self.make_directory(f"{rel_path}csv")

    def make_covers_subdirectories(self):
        for category_name, _ in self.user_selection:
            self.make_directory(category_name, self.dir_covers)

    @staticmethod
    def _can_conv_to_int(num_str: str):
        try:
            int(num_str)
            return True
        except ValueError:
            return False

    def _is_valid_str(self, num_str: str, last: int) -> bool:
        if not self._can_conv_to_int(num_str):
            self.input_result["message"] = ERROR_MESSAGES["char"]
            return False
        if int(num_str) < 1 or int(num_str) > last:
            self.input_result["message"] = ERROR_MESSAGES["boundaries"]
            return False
        return True

    def _is_valid_range(self, range_str: str, last: int) -> bool:
        range_fragment = range_str.split("-")
        if not len(range_fragment) == 2:
            self.input_result["message"] = ERROR_MESSAGES["range_format"]
            return False

        left_str, right_str = range_fragment
        if not self._is_valid_str(left_str, last) or not self._is_valid_str(
            right_str, last
        ):
            return False

        return True

    def decode_input(self, user_input: str, last: int):
        segments = [sub_str.strip() for sub_str in user_input.split(",")]
        for segment in segments:
            if len(segment) < 3:
                if not self._is_valid_str(segment, last):
                    return self.input_result
                else:
                    self.input_result["value"].add(int(segment))

            elif len(segment) < 6 and "-" in segment:
                if not self._is_valid_range(segment, last):
                    return self.input_result
                else:
                    left_str, right_str = [int(x) for x in segment.split("-")]
                    cat_range = sorted([left_str, right_str])
                    categories = [
                        x for x in range(cat_range[0], cat_range[1] + 1)
                    ]
                    for category_num in categories:
                        self.input_result["value"].add(category_num)

        if len(self.input_result["value"]) > 0:
            self.input_result["valid"] = True
        return self.input_result

    @staticmethod
    def split_list_evenly(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    def prompt_selection(self):
        def ansi(s):
            return f"\033[{s}m"

        clr = ansi("38;2;241;196;15")
        reset = ansi("")
        while True:
            catalogue = self.catalogue
            last = len(catalogue)
            category_names = [category[0] for category in catalogue]
            print(
                f"{'_' * 54}\n"
                f"{ASCII}"
                "Welcome to BookWorm, a scraper for books.toscrape.com!\n"
                f"{'_' * 54}\n"
            )
            input(f"Press{clr} Enter{reset} to see the " "catalogue...")
            for index, category_name in enumerate(category_names):
                print(f"{clr}{index + 1}{reset}: {category_name}")
            user_input = input(
                "Please type each category number "
                "you want to select separated by a comma.\n"
                "you can also set one or multiple range(s) with '-' \n"
                f"ex: {clr}1, 4-8, 10, 30-45{reset}\n>_"
            )
            selected, valid, msg = self.decode_input(user_input, last).values()

            if not valid:
                print(msg)
                input("Press Enter to try again")
            else:
                self.user_selection = [
                    category
                    for category in catalogue
                    if catalogue.index(category) + 1 in selected
                ]
                break

    def export_csv(self, books: tuple[Book]) -> None:
        target_path = Path.cwd() / ".." / "exports" / f"{self.dir_csv}"
        target_path.mkdir(parents=True, exist_ok=True)
        with open(
            target_path / "export.csv", "w", encoding="utf-8", newline=""
        ) as f:
            writer = csv.writer(f)
            writer.writerow(books[0]._fields)
            for book in books:
                writer.writerow(book)