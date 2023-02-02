from collections import namedtuple
from typing import Tuple

Book = namedtuple(
    "Book",
    "url upc title itp etp stock description "
    "category rating cover_url cover_name",
)

# Type hints
Name = str
Url = str
Category = Tuple[Name, Url]
