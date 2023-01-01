from typing import Set, Tuple, List
from enum import Enum


class MenuChoice(Enum):
    all = 1
    category = 2
    quit = 3


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
    user_selection = set(selected_categories.split(","))
    u_sel_cap = set(x.strip().lower() for x in user_selection)
    print(u_sel_cap)

    if u_sel_cap.issubset(category_names):
        selected_categories = [
            category
            for category in categories
            if category[0].lower() in u_sel_cap
        ]
        return selected_categories

    print(
        "I'm afraid you made a typo, or selected a category that "
        "doesn't exist. Mind to try again?"
    )
    prompt_category_selection(categories)
