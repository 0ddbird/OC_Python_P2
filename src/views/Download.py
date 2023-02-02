from views.views_utils import AnsiClr, clr


def log_progress(done: int, total: int) -> None:
    progress = int(done / total * 100)
    block_char = "\u2588"

    # Bar % done
    progress_bar = block_char * progress
    green_bar = clr(AnsiClr.GREEN, progress_bar)

    # Bar % remaining
    empty_space = "\u2588" * (100 - progress)
    grey_bar = clr(AnsiClr.GREY, empty_space)
    print(f"\r0%-|{green_bar}{grey_bar}|-{progress}%", end="")
