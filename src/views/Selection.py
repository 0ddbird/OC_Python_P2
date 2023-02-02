from views.views_utils import SEPARATOR, AnsiClr, clr


def display_categories(categories, grid=False) -> None:
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


def prompt_selection() -> str:
    return input(
        "Please type the category number for each category "
        "you want to select, separated by commas.\n"
        "You can also select one or multiple range(s) with '-'\nex: "
        f"{clr(AnsiClr.YELLOW, '1, 4-8, 10, 30-45')}\n>_"
    )
