from collections import namedtuple
from typing import Tuple

Book = namedtuple(
    "Book",
    "product_page_url "
    "universal_product_code "
    "title "
    "price_including_tax "
    "price_excluding_tax "
    "number_available "
    "product_description "
    "category review_rating "
    "image_url "
    "cover_name",
)

# Type hints
Name = str
Url = str
Category = Tuple[Name, Url]
