from pathlib import Path
import re
import csv

from src.modules.parser import Book


def make_directory(dir_name: str, base_path=None) -> Path:
    if base_path:
        target_path = base_path / f"{dir_name}"
    else:
        target_path = Path.cwd() / f"{dir_name}"
    target_path.mkdir(parents=True, exist_ok=True)
    return target_path


async def download_cover(
    session, covers_path: Path, cov_url: str, cov_name: str, category: str
) -> None:
    async with session.get(cov_url) as resp:
        cover = await resp.read()
    letters_only_re = r"[^a-zA-Z0-9]"
    file_name = re.sub(letters_only_re, "_", cov_name)
    target_path = covers_path / f"{category}"
    target_path.mkdir(parents=True, exist_ok=True)
    with open(f"{target_path}/{file_name}.jpg", "wb") as f:
        f.write(cover)


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
