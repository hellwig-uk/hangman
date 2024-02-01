import functools
from enum import StrEnum
from os.path import dirname, join
from typing import Tuple

from . import words

_ROOT = dirname(dirname(__file__))
ART = join(_ROOT, "ascii_art", "{}.txt")


# Use gettext or similar to provide localisation.
class STATES(StrEnum):
    STARTED = "Started"
    ALIVE = "Alive"
    DEAD = "Game Over"
    WON = "Won"


class STRINGS(StrEnum):
    WORD_EMPTY = "Word must not be empty"
    LETTER_ONLY_ONE = "Must be 1 letter only."
    LETTER_ALREADY_SET = "Letter already set."


@functools.cache
def cached_art(value: int) -> str:
    path = ART.format(value)
    with open(path, "r") as file_read:
        return "".join(file_read.readlines())


class Logic:
    def __init__(self):
        self._lives = 7
        self._word = str
        self._word_test = str
        self._length = int
        self._letters = list
        self._correct = int
        self._incorrect = int

    def set_word(self, word: str) -> None:
        self._word = word.strip()
        self._length = len(self._word)
        if self._length == 0:
            raise ValueError(STRINGS.WORD_EMPTY)
        self._word_test = word.lower()
        self._letters = []
        self._correct = 0
        self._incorrect = 0

    def set_word_random(
        self,
        length_from_to: Tuple[int, int] = words.DEFAULT_SELECT_RANGE,
        word_file: str = words.DEFAULT_WORD_FILE,
    ) -> None:
        word = words.get_random_word(length_from_to, word_file)
        self.set_word(word.capitalize())

    def set_letter(self, letter: str) -> bool:
        letter = letter.lower().strip()
        if len(letter) != 1:
            raise ValueError(STRINGS.LETTER_ONLY_ONE)

        if letter in self._letters:
            raise ValueError(STRINGS.LETTER_ALREADY_SET)

        self._letters.append(letter)

        if letter in self._word_test:
            self._correct += 1
            return True

        self._incorrect += 1
        return False

    @property
    def wrong(self) -> str:
        out = []
        for letter in self._letters:
            if letter not in self._word_test:
                out.append(letter)
        return "".join(out)

    @property
    def word(self) -> str:
        out = []
        for index, letter in enumerate(self._word_test):
            if letter in self._letters:
                out.append(self._word[index])
            else:
                out.append("⎵")
        return "".join(out)

    @property
    def state(self) -> STATES:
        if self._correct == self._incorrect == 0:
            return STATES.STARTED
        elif self.lives <= 0:
            return STATES.DEAD
        elif "⎵" not in self.word:
            return STATES.WON

        return STATES.ALIVE

    @property
    def lives(self) -> int:
        return 6 - self._incorrect

    @property
    def art(self) -> str:
        return cached_art(7 - self.lives)


def create_number_choices_range(
    started: int, stopped: int
) -> Tuple[Tuple[str, int], ...]:
    tuples = tuple([(str(number), number) for number in range(started, stopped + 1)])
    return tuples
