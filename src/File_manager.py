import json
from typing import Any


def open_file_manager(path: str) -> Any:
    """
    Функция, читающая файл json формата.
    """

    with open(path, "r", encoding="UTF-8") as file:
        data = json.load(file)
        return data
