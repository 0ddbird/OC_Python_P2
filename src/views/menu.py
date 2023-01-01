from typing import Set, Tuple, List
from enum import Enum

from src.modules.scrape_all import get_all_catalogue
from src.modules.scrape_categories import (
    request_categories,
    get_catalogue_selection,
)


class MenuChoice(Enum):
    all = 1
    category = 2
    quit = 3


async def main_menu(session, first_url):
    user_choice = prompt_scraping_mode()

    if user_choice == MenuChoice.quit:
        exit(0)
    if user_choice == MenuChoice.all:
        urls = await get_all_catalogue(session, first_url)
        return urls

    categories = await request_categories(session, first_url)
    selected_categories = prompt_category_selection(categories)
    sel_cat_urls = await get_catalogue_selection(session, selected_categories)
    return sel_cat_urls


def prompt_scraping_mode():
    choice = int(
        input(
            "Type [1] to get all books\nType [2] to select "
            "categories\nType [3] to exit\n_"
        )
    )
    if choice in [1, 2, 3]:
        return MenuChoice(choice)
    print("Please type 1, 2 or 3 to choose the scraping mode")
    prompt_scraping_mode()


def prompt_category_selection(
    categories: Set[Tuple[str, str]]
) -> List[Tuple[str, str]]:
    category_names = [category[0] for category in categories]
    for category_name in category_names:
        print(category_name)
    selected_categories = input(
        "Please type the category names "
        "you want to scrape separated by a comma\n"
        "ex: travel, default, romance\n"
    )
    user_selection = set(selected_categories.replace(' ', '').split(","))
    u_sel_cap = set(x.capitalize() for x in user_selection)

    if u_sel_cap.issubset(category_names):
        selected_categories_urls = [
            category
            for category in categories
            if category[0] in u_sel_cap
        ]
        return selected_categories_urls

    print(
        "I'm afraid you made a typo, or selected a category that "
        "doesn't exist. Mind to try again?"
    )
    prompt_category_selection(categories)
