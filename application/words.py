import functools
import random
from os.path import dirname, join
from typing import Dict, List, Tuple

_ROOT = dirname(dirname(__file__))
DEFAULT_WORD_FILE = join(_ROOT, "words", "nouns.txt")
DEFAULT_SELECT_RANGE = (5, 9)


@functools.cache
def create_word_select_dictionary(path: str) -> Dict:
    select_dictionary: Dict[int, List[str]] = {}
    with open(path, "r") as _:
        for word in set("".join(_.readlines()).split("\n")):
            word = word.strip()
            length = len(word)
            if length == 0:
                continue

            if length not in select_dictionary:
                select_dictionary[length] = []

            select_dictionary[length].append(word)

    return select_dictionary


@functools.cache
def get_word_list(length: Tuple[int, int], path: str) -> List[str]:
    select_dictionary = create_word_select_dictionary(path)
    candidates = []
    for index in range(length[0], length[1] + 1):
        candidates += select_dictionary[index]

    candidates.sort()
    return candidates


def get_random_word(
    length_from_to: Tuple[int, int] = DEFAULT_SELECT_RANGE,
    word_file: str = DEFAULT_WORD_FILE,
) -> str:
    word_list = get_word_list(length_from_to, word_file)
    return random.choice(word_list)
