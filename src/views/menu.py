from typing import List
from enum import Enum

from src.modules.parser import T_category


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
    categories: List[T_category],
) -> List[T_category]:
    category_names = [category[0] for category in categories]
    for index, category_name in enumerate(category_names):
        print(f"{index + 1} : {category_name}")
    user_input = input(
        "Please type the category number "
        "you want to scrape separated by a comma\n"
        "ex: 1, 2, 30, 50, 8, 12\n"
    ).split(",")

    try:
        categories_input = [int(char_num.strip()) for char_num in user_input]
        if not all(1 <= num <= len(categories) for num in categories_input):
            print(f"Please enter numbers between 1 and {len(categories)}")
            input("Press Enter to try again")
            prompt_category_selection(categories)
    except ValueError:
        print("Please make sure you enter numbers only")
        input("Press Enter to try again")
        prompt_category_selection(categories)

    selected_categories = [
        category
        for category in categories
        if categories.index(category) + 1 in categories_input
    ]
    return selected_categories
