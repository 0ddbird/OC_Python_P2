from src.parser.BeautifulSoup_ import BeautifulSoupParser
from src.parser.Selectolax_ import SelectolaxParser


def pick_from_cli(args: list):
    if "-bs4" in args:
        return BeautifulSoupParser()
    return SelectolaxParser()


async def log_progress(func):
    await func
