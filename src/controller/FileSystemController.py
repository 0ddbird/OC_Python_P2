import csv
from pathlib import Path

from typehints.types import Book


class FileSystemController:
    def __init__(self):
        self.dir_base = None
        self.dir_covers = None
        self.dir_csv = None

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

    def make_covers_subdirectories(self, user_selection) -> None:
        for category_name, _ in user_selection:
            self.make_directory(category_name, self.dir_covers)

    def export_csv(self, book_list: list[Book]) -> None:
        category_name = book_list[0].category
        target_path = Path.cwd() / ".." / "exports" / f"{self.dir_csv}"
        target_path.mkdir(parents=True, exist_ok=True)
        with open(
            target_path / f"{category_name}.csv",
            "w",
            encoding="utf-8",
            newline="",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(book_list[0]._fields)
            for book in book_list:
                writer.writerow(book)
