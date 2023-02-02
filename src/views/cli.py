from parsers.BeautifulSoup_ import BeautifulSoupParser
from parsers.Selectolax_ import SelectolaxParser


def pick_parser_from_cli(args: list):
    print(args)
    if "-bs4" in args:
        print('Selected parser: Beautiful Soup')
        return BeautifulSoupParser()
    print('Selected parser: Selectolax')
    return SelectolaxParser()
