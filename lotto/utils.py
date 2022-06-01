import collections
import os
import random
from collections.abc import Iterable, Mapping

# fix to use PyInquirer in python>=3.10
collections.Mapping = Mapping

from PyInquirer import prompt


def clear_screen():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')


def simple_choice(message: str, choices: list[str]) -> str:
    questions = [
        {
            "type": "list",
            "name": "name",
            "message": message,
            "choices": choices,
        },
    ]
    return prompt(questions)["name"]


def sorted_random_subarray(array: Iterable[int], length: int) -> list[int]:
    array = list(array)
    assert -1 < length <= len(array), f"Length ({length}) must be less or equal then array."
    random.shuffle(array)
    array = array[:length]
    array.sort()
    return array
