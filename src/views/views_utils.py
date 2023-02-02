from strenum import StrEnum

SEPARATOR = f"{'=' * 54}"


class AnsiClr(StrEnum):
    GREEN = "38;2;26;188;156"
    YELLOW = "38;2;241;196;15"
    GREY = "38;2;236;240;241"


def ansi_esc(code):
    return f"\033[{code}m"


def clr(color: AnsiClr, string):
    return f"{ansi_esc(color)}{string}\033[m"

