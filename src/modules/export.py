from pathlib import Path
import re
import csv

from src.modules.parser import Book


def make_directory(dir_name: str) -> Path:
    target_path = Path.cwd() / ".." / "exports" / f"{dir_name}"
    target_path.mkdir(parents=True, exist_ok=True)
    return target_path


async def download_cover(
    session, path: Path, cov_url: str, cov_name: str
) -> None:
    async with session.get(cov_url) as resp:
        cover = await resp.read()
    letters_only_re = r"[^a-zA-Z0-9]"
    file_name = re.sub(letters_only_re, "_", cov_name)
    file_path = f"{path}/{file_name}.jpg"
    with open(file_path, "wb") as f:
        f.write(cover)


def export_csv(path: Path, books: tuple[Book]) -> None:
    with open(f"{path}/export.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(books[0]._fields)
        for book in books:
            writer.writerow(book)
