from tkinter import Button, Frame, messagebox, Misc
from typing import List
from random import shuffle

from match_madness.gui.progress import Progress
from match_madness.populate.base_methods import BasePopulator
from match_madness.gui.card import Card


class GameFrame(Frame):  # pylint: disable=R0902
    """Simplifies game creation and its process"""

    DELAY = 1000  # in ms
    defi_clicked = None
    word_clicked = None

    def __init__(self, master: Misc, populator: BasePopulator) -> None:
        """Creates and places new GameFrame onto master window. Handling whole
            game process

        Args:
            master (Misc): Master window
            populator (BasePopulator): Populator object used for populating cards
                on GameFrame
        """
        super().__init__(master, height=600, width=400)
        self.pack(expand=1, fill="both")

        self.__matched = 0
        self.__correct = 0

        self.__step = populator.normalised_step()
        self.__population_method = iter(populator)
        self.__population_lock = False

        fir_col = 0.2
        sec_col = 0.6
        height = 0.1
        width = 0.2
        but_height = 20

        self.__progress = Progress(self)
        self.__progress.place(relx=fir_col, rely=0.1, relwidth=sec_col, relheight=0.05)

        Button(self, text="X", command=self.kill).place(
            relx=1, rely=0, width=but_height, height=but_height, anchor="ne"
        )

        self.__defi_buttons: List[Card] = []
        self.__word_buttons: List[Card] = []
        self.__defi_vacant: List[Card] = []
        self.__word_vacant: List[Card] = []

        for i in range(5):
            rely = 0.2 + i * 0.15

            word = Card(self, "", "", lambda i=i: self.__card_hook(True, i))
            word.place(relx=fir_col, rely=rely, relheight=height, relwidth=width)

            defi = Card(self, "", "", lambda i=i: self.__card_hook(False, i))
            defi.place(relx=sec_col, rely=rely, relheight=height, relwidth=width)

            self.__defi_buttons.append(defi)
            self.__word_buttons.append(word)
            self.__defi_vacant.append(defi)
            self.__word_vacant.append(word)

        self.populate()

    def __card_hook(self, is_word: bool, card_id: int) -> None:
        """Hook used by Card objects to trigger pair handler

        Args:
            is_word (bool): Whether given card is considered "word" or "definition"
            card_id (int): Card position in "__defi_buttons" or "__word_buttons"
        """
        old_but = [self.defi_clicked, self.word_clicked][is_word]

        if old_but is not None:
            old_but.click(True)

        if is_word:
            self.word_clicked = self.__word_buttons[card_id]
        else:
            self.defi_clicked = self.__defi_buttons[card_id]

        self.__check_pair()

    def __check_pair(self) -> None:
        """Check and handles pairs"""
        if self.defi_clicked is None or self.word_clicked is None:
            return

        self.__matched += 1
        defi_but = self.defi_clicked
        word_but = self.word_clicked

        self.defi_clicked = None
        self.word_clicked = None

        if defi_but == word_but:
            self.__correct += 1

            defi_but.correct()
            word_but.correct()

            self.__defi_vacant.append(defi_but)
            self.__word_vacant.append(word_but)

            self.__progress.step(self.__step)
            if self.__progress.value == 100:
                self.kill(False)

            self.after(self.DELAY, self.populate)

        else:
            defi_but.wrong()
            word_but.wrong()

            def normalise() -> None:
                """Auxiliary function to revert buttons back to normal"""
                defi_but.click(True)
                word_but.click(True)

            self.after(self.DELAY, normalise)

    def populate(self) -> None:
        """Populates cards and randomization of "word" "definition" positions"""
        if self.__population_lock or 2 > len(self.__word_vacant):
            return

        defi_vacant = list(self.__defi_vacant)
        shuffle(defi_vacant)
        for word_but in self.__word_vacant:
            defi_but = defi_vacant.pop()

            try:
                word, defi = next(self.__population_method)
            except StopIteration:
                self.__population_lock = True
                return

            word_but.change(word, defi)
            defi_but.change(defi, word)

        self.__defi_vacant = []
        self.__word_vacant = []

    def kill(self, silent: bool = True) -> None:
        """Closes of current GameFrame object

        Args:
            silent (bool): Whether informative dialog will be displayed
        """
        if not silent:
            percent = round(self.__correct / self.__matched * 100, 2)
            messagebox.showinfo("Information", f"You finished with {percent}%")
        self.destroy()
