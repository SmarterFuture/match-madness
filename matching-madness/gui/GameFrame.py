import tkinter as tk
from tkinter import Misc, ttk
from typing import Iterator, List, Set, Tuple
from random import choice
from .Card import Card


class GameFrame(tk.Frame):
    DEFI_CLICKED = None
    WORD_CLICKED = None
    DELAY = 1000  # in ms

    def __init__(
        self, master: Misc, population_method: Iterator[Tuple[str, str]]
    ) -> None:
        super().__init__(master, height=600, width=300, bg="blue")
        self.pack(expand=1, fill="both")

        self.__population_method = population_method
        self.__population_lock = False

        fir_col = 0.2
        sec_col = 0.6
        height = 0.1
        width = 0.2

        ttk.Progressbar(self).place(
            relx=fir_col, rely=0.1, relwidth=sec_col, relheight=0.05
        )

        self.__defi_buttons: List[Card] = []
        self.__word_buttons: List[Card] = []
        self.__defi_vacant: Set[Card] = set()
        self.__word_vacant: Set[Card] = set()

        for i in range(5):
            rely = 0.2 + i * 0.15

            word = Card(self, "", "", lambda i=i: self.__card_hook(True, i))
            word.place(relx=fir_col, rely=rely, relheight=height, relwidth=width)

            defi = Card(self, "", "", lambda i=i: self.__card_hook(False, i))
            defi.place(relx=sec_col, rely=rely, relheight=height, relwidth=width)

            self.__defi_buttons.append(defi)
            self.__word_buttons.append(word)
            self.__defi_vacant.add(defi)
            self.__word_vacant.add(word)

    def __card_hook(self, is_word: bool, card_id: int) -> None:
        old_but = [self.DEFI_CLICKED, self.WORD_CLICKED][is_word]

        if old_but is not None:
            old_but.click(True)

        if is_word:
            self.WORD_CLICKED = self.__word_buttons[card_id]
        else:
            self.DEFI_CLICKED = self.__defi_buttons[card_id]

        self.__check_pair()

    def __check_pair(self) -> None:
        if self.DEFI_CLICKED is None or self.WORD_CLICKED is None:
            return

        defi_but = self.DEFI_CLICKED
        word_but = self.WORD_CLICKED

        self.DEFI_CLICKED = None
        self.WORD_CLICKED = None

        if defi_but == word_but:
            defi_but.correct()
            word_but.correct()
            self.__defi_vacant.add(defi_but)
            self.__word_vacant.add(word_but)
            self.after(self.DELAY, self.populate)

        else:
            defi_but.wrong()
            word_but.wrong()

            def normalise() -> None:
                defi_but.click(True)
                word_but.click(True)

            self.after(self.DELAY, normalise)

    def populate(self) -> None:
        if self.__population_lock:
            return
        if 2 > len(self.__word_vacant):
            return

        defi_vacant = list(self.__defi_vacant)
        for word_but in self.__word_vacant:
            defi_but = choice(defi_vacant)

            try:
                word, defi = next(self.__population_method)
            except StopIteration:
                self.__population_lock = True
                return
            else:
                word_but.change(word, defi)
                defi_but.change(defi, word)
