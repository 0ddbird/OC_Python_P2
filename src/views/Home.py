from views.views_utils import SEPARATOR, AnsiClr, clr

MARGIN = 20 * " "
LOGO = (
    f"{MARGIN + '    _______'}\n"
    f"{MARGIN + '   / Book //'}\n"
    f"{MARGIN + '  / Worm //'}\n"
    f"{MARGIN + ' /______//'}\n"
    f"{MARGIN + '(______(/'}\n"
)


def display_home() -> None:
    print(
        f"{SEPARATOR}"
        f"\n{LOGO}\nWelcome to BookWorm, a scraper for books.toscrape.com!\n"
        f"{SEPARATOR}"
    )
    input(
        f"Press {clr(AnsiClr.YELLOW, 'Enter')} to see the "
        f"catalogue.\n{SEPARATOR}"
    )
