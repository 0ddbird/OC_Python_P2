from src.parser.BeautifulSoup_ import BeautifulSoupParser
from src.parser.Selectolax_ import SelectolaxParser
from strenum import StrEnum


def pick_parser_from_cli(args: list):
    # if "-bs4" in args:
    return BeautifulSoupParser()
    # return SelectolaxParser()


# ANSI constants and functions
MARGIN = 20 * " "
SEPARATOR = f"{'=' * 54}"
LOGO = (
    f"{MARGIN + '    _______'}\n"
    f"{MARGIN + '   / Book //'}\n"
    f"{MARGIN + '  / Worm //'}\n"
    f"{MARGIN + ' /______//'}\n"
    f"{MARGIN + '(______(/'}\n"
)


class AnsiClr(StrEnum):
    GREEN = "38;2;26;188;156"
    YELLOW = "38;2;241;196;15"
    GREY = "38;2;236;240;241"


def ansi_esc(code):
    return f"\033[{code}m"


def clr(color: AnsiClr, string):
    return f"{ansi_esc(color)}{string}\033[m"


# CLI menu
def print_welcome():
    print(
        f"{SEPARATOR}"
        f"\n{LOGO}\nWelcome to BookWorm, a scraper for books.toscrape.com!\n"
        f"{SEPARATOR}"
    )
    input(
        f"Press {clr(AnsiClr.YELLOW, 'Enter')} to see the "
        f"catalogue.\n{SEPARATOR}"
    )


def print_categories(categories, grid=False):

    if grid:
        # Adding index prefix to each category and grouping them into columns
        column_number = 5
        table = zip(*[iter(categories)] * column_number)

        # Calculating the padding base on the length of the longest string
        padding = max(len(category) for category in categories) + 20

        # Keeping track of last category number from previous array
        i = 0

        for rows in table:
            # Create constant spaced entry "i. Category     "
            column = [
                f"\033[1m\033[33m{i + 1}\033[39m. {category}\033[0m".ljust(
                    padding
                )
                for i, category in enumerate(rows, start=i)
            ]

            # Building a row with tabs between columns
            print("\t".join(column))

            # Incrementing i new value for the first item of next column
            i += len(column)
    else:
        for index, category_name in enumerate(categories):
            print(f"{index + 1}. {category_name}")
    print(f"\n{SEPARATOR}")


def get_selection_input():
    return input(
        "Please type the category number for each category "
        "you want to select, separated by commas.\n"
        "You can also select one or multiple range(s) with '-'\nex: "
        f"{clr(AnsiClr.YELLOW, '1, 4-8, 10, 30-45')}\n>_"
    )


# Progress bar
def log_progress(done: int, total: int):
    progress = int(done / total * 100)
    block_char = "\u2588"

    # Bar % done
    progress_bar = block_char * progress
    green_bar = clr(AnsiClr.GREEN, progress_bar)

    # Bar % remaining
    empty_space = "\u2588" * (100 - progress)
    grey_bar = clr(AnsiClr.GREY, empty_space)
    print(f"\r0%-|{green_bar}{grey_bar}|-{progress}%", end="")
