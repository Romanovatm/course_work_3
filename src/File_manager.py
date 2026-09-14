import json
from typing import Any


def file_manager(path: str) -> Any:
    """
    Функция, читающая файл json формата.
    """

    with open(path) as file:
        data = json.load(file)
        return data
