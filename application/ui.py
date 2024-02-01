from enum import StrEnum
from typing import Type

from rich.console import RenderableType
from textual import events
from textual.app import App, ComposeResult
from textual.driver import Driver
from textual.widgets import Button, Footer, Header, Label, Rule, Select, Static

from . import logic


class STRINGS(StrEnum):
    TITLE = "Hangman"
    TITLE_SUB = "The classic Hangman game."
    TITLE_TEXT = (
        "\n    All words are English (UK) Nouns, using the letters a to z, "
        "\n    no hyphen or spaces. Exit anytime with ctrl+c."
    )
    LENGTH_MIN = "Minimum word length:"
    LENGTH_MAX = "Maximum word length:"
    BUTTON = "Start"
    GAME_TEXT = "Type a letter"
    WRONG = "Wrong letters: {}"
    REMAINING = "You have {} lives remaining."
    WON = "You won!"
    LOST = "You lost, the word was '{}'."
    MENU = "MENU"


LENGTH_MIN = logic.create_number_choices_range(4, 17)
LENGTH_MAX = logic.create_number_choices_range(4, 17)


class ViewStart(Static):
    def compose(self) -> ComposeResult:
        self.composites = {
            "title_sub": Label(STRINGS.TITLE_SUB),
            "title_text": Label(STRINGS.TITLE_TEXT),
            "rule_1": Rule(orientation="horizontal", line_style="dashed"),
            "label_min": Label(STRINGS.LENGTH_MIN),
            "select_min": Select(LENGTH_MIN, value=4, name=STRINGS.LENGTH_MIN),
            "label_max": Label(STRINGS.LENGTH_MAX),
            "select_max": Select(LENGTH_MAX, value=8, name=STRINGS.LENGTH_MAX),
            "rule_2": Rule(orientation="horizontal", line_style="dashed"),
            "button": Button(label=STRINGS.BUTTON, id=STRINGS.BUTTON),
        }

        for entry in self.composites.values():
            yield entry


class ViewGame(Static):
    def __init__(
        self,
        min_word_length: int,
        max_word_length: int,
        renderable: RenderableType = "",
        *,
        expand: bool = False,
        shrink: bool = False,
        markup: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(
            renderable,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.game = logic.Logic()
        self.game.set_word_random((min_word_length, max_word_length))

    def compose(self) -> ComposeResult:
        self.composites = {
            "info": Static(STRINGS.GAME_TEXT),
            "rule_1": Rule(orientation="horizontal", line_style="dashed"),
            "art": Static(self.game.art),
            "word": Static(self.game.word),
            "wrong": Static(STRINGS.WRONG.format(self.game.wrong)),
        }
        for entry in self.composites.values():
            yield entry

    def input(self, key: str) -> None:
        if self.game.state == logic.STATES.DEAD:
            return

        try:
            results = self.game.set_letter(key)
        except ValueError:
            return

        self.composites["info"].update(
            renderable=STRINGS.REMAINING.format(self.game.lives)
        )
        self.composites["art"].update(renderable=self.game.art)
        self.composites["word"].update(renderable=self.game.word)
        self.composites["wrong"].update(
            renderable=STRINGS.WRONG.format(", ".join(self.game.wrong))
        )

        if self.game.state == logic.STATES.DEAD:
            self.composites["info"].update(
                renderable=STRINGS.LOST.format(self.game._word)
            )
        elif self.game.state == logic.STATES.WON:
            self.composites["info"].update(renderable=STRINGS.WON)

        if self.game.state in [logic.STATES.DEAD, logic.STATES.WON]:
            self.mount(Rule(orientation="horizontal", line_style="dashed"))
            self.mount(Button(STRINGS.MENU, id=STRINGS.MENU))


class MainView(Static):
    def compose(self) -> ComposeResult:
        self.composites = {
            "view": ViewStart(),
        }
        for entry in self.composites.values():
            yield entry


class HangmanUI(App):
    """Hangman CLI UI."""

    TITLE = STRINGS.TITLE

    def compose(self) -> ComposeResult:
        self.composites = {
            "header": Header(),
            "main": MainView(),
            "footer": Footer(),
        }

        for entry in self.composites.values():
            yield entry

    def on_select_changed(self, event: Select.Changed) -> None:
        composites = self.composites["main"].composites["view"].composites

        if event.select.name == STRINGS.LENGTH_MIN:
            if event.value > composites["select_max"].value:
                composites["select_max"].value = event.value

        elif event.select.name == STRINGS.LENGTH_MAX:
            if event.value < composites["select_min"].value:
                composites["select_min"].value = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == STRINGS.BUTTON:
            self.composites["main"].composites["view"].remove()
            self.composites["main"].composites["view"] = ViewGame(
                self.composites["main"]
                .composites["view"]
                .composites["select_min"]
                .value,
                self.composites["main"]
                .composites["view"]
                .composites["select_max"]
                .value,
            )
            self.composites["main"].mount(self.composites["main"].composites["view"])

        elif event.button.id == STRINGS.MENU:
            self.composites["main"].composites["view"].remove()
            self.composites["main"].composites["view"] = ViewStart()
            self.composites["main"].mount(self.composites["main"].composites["view"])

    def on_key(self, event: events.Key) -> None:
        if isinstance(self.composites["main"].composites["view"], ViewGame):
            if event.is_printable:
                self.composites["main"].composites["view"].input(str(event.character))
