from tkinter import DoubleVar, Misc
from tkinter.ttk import Progressbar


class Progress(Progressbar):  # pylint: disable=R0901
    """Wrapper for more convenient working with ttk.Progressbar"""

    def __init__(self, master: Misc) -> None:
        """Creates Progressbar and sets up value attribute

        Args:
            master (Misc): Master window
        """
        self.value = 0
        self.__progress_var = DoubleVar(master, value=self.value)

        super().__init__(master, variable=self.__progress_var)

    def step(self, amount: float | None = 1) -> None:
        """Increment current value of Progressbar

        Args:
            amount (float | None): Amount by which it should be incremented
        """
        amount = amount or 1
        self.value = min(self.value + amount, 100)

        self.__progress_var.set(self.value)
