import tkinter as tk
from tkinter import Misc, Button
from typing import Callable


class Card(Button):
    """Abstraction class for consistent UI/UX presentation. Main UI/UX building element
        of GameFrame class
    """

    IS_TOGGLED = False
    COLORS = ["SystemButtonFace", "green"]
    
    def __init__(self, master: Misc, text: str, other: str, hook: Callable[[], None] ) -> None:
        """Creates new Card object with hook to master class. Handling both pair values
            and UI/UX

        Args:
            master (Misc): Master window
            text (str): What will be displayed on the Card
            other (str): The pair value to the "text" value
            hook (Callable[[], None]): Hook function to GameFrame class to handle pair
                triggers
        """
        self.__master = master
        self.__other = other
        self.value = text
        self.__hook = hook
        super().__init__(self.__master, text=text, command=self.click)
    
    def __eq__(self, other: object) -> bool:
        """Checks whether two Cards are pair, by compering their value "text" value
            (either "word" or "defi") with the "other" value of the other object

        Args:
            other (object): Card to compare against

        Returns:
            bool: True if the cards are a pair
        """
        if not isinstance(other, Card):
            return False
        return self.__other == other.value # type: ignore

    def click(self, silent=False) -> None:
        """Handles clicks on the Card

        Args:
            silent: Whether or not hook function will be triggered
        """
        self.IS_TOGGLED = not self.IS_TOGGLED
        color = self.COLORS[self.IS_TOGGLED]
        self.config(bg=color)

        if not silent:
            self.__hook()

    def correct(self) -> None:
        """Handles UI/UX of correctly matched card"""
        self.click(True)
        self.config(state=tk.DISABLED)

    def wrong(self) -> None:
        """Handles UI/UX of incorrectly matched card"""
        self.config(bg="red")
    
    def change(self, text: str, other: str) -> None:
        """In place rebuilds Card object, same as __init__(), with exception of using old
            "master" and "hook" values

        Args:
            text (str): What will be displayed on the Card
            other (str): The pair value to the "text" value
        """
        self = self.__init__(self.master, text, other, self.__hook)

