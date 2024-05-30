from tkinter import Misc, Label, StringVar


class Combo(Label):
    """Wrapper for more convenient displaying of current combo value"""

    def __init__(self, master: Misc) -> None:
        """Creates combo widget and sets its attributes

        Args:
            master (Misc): Master window
        """

        self.value = 0
        self.__text = StringVar()
        self.max = 0

        self.set(0)

        super().__init__(master, textvariable=self.__text)

    def set(self, value: int | None = None):
        """Sets combo value to the widget

        Args:
            value (int | None): Set current combo value
        """
        if value is not None:
            self.value = value

        self.max = max(self.value, self.max)

        self.__text.set(f"COMBO: {self.value}x")

    def plus_one(self):
        """Increment current combo value by one"""
        self.value += 1
        self.set()
