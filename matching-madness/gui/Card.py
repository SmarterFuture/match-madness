import tkinter as tk
from tkinter import Misc, Button
from typing import Callable


class Card(Button):
    IS_TOGGLED = False
    COLORS = ["SystemButtonFace", "green"]
    
    def __init__(self, master: Misc, text: str, other: str, hook: Callable[[], None] ) -> None:
        self.__master = master
        self.__other = other
        self.value = text
        self.__hook = hook
        super().__init__(self.__master, text=text, command=self.click)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return False
        return self.__other == other.value # type: ignore

    def click(self, silent=False):
        self.IS_TOGGLED = not self.IS_TOGGLED
        color = self.COLORS[self.IS_TOGGLED]
        self.config(bg=color)

        if not silent:
            self.__hook()

    def corrct(self):
        self.click(True)
        self.config(state=tk.DISABLED)

    def wrong(self):
        self.config(bg="red")
    
    def change(self, text: str, other: str):
        self = self.__init__(self.master, text, other, self.__hook)

