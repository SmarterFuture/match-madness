from os import listdir
from os.path import isfile, join
from re import search
from random import choice
from tkinter import Button, Frame, Misc
from typing import Iterable

from matching_madness.gui.game_frame import GameFrame
from matching_madness.populate.base_methods import DATA_LIB, BasePopulator
from matching_madness.populate.json_methods import Populator


class MainFrame(Frame):
    __game_frame = None

    def __init__(self, master: Misc) -> None:
        super().__init__(master, height=600, width=400)
        self.put()

        self.__master = master

        col = 0.3
        space = 0.1
        height = 0.2
        width = 0.4

        Button(
            self,
            text="English -> Slovak",
            command=lambda: self.__gen_game(self.__random_eng()),
        ).place(relx=col, rely=space, relheight=height, relwidth=width)

        Button(
            self,
            text="Spanish -> English",
            command=lambda: self.__gen_game(self.__random_esp()),
        ).place(relx=col, rely=2 * space + height, relheight=height, relwidth=width)

        Button(self, text="Custom").place(
            relx=col, rely=3 * space + 2 * height, relheight=height, relwidth=width
        )

    def put(self):
        self.pack(expand=1, fill="both")
        self.update()

    def __get_data(self) -> Iterable[str]:
        dir_files = listdir(DATA_LIB)
        for file in dir_files:
            file = join(DATA_LIB, file)
            if isfile(file):
                yield file

    def __random_eng(self) -> Populator:
        eng_files = list(
            filter(lambda x: search(r".*eng\d+\.json$", x), self.__get_data())
        )
        file = choice(eng_files)
        return Populator(file)

    def __random_esp(self) -> Populator:
        esp_files = list(
            filter(lambda x: search(r".*esp\d+\.json$", x), self.__get_data())
        )
        file = choice(esp_files)
        return Populator(file)

    def __gen_game(self, populator: BasePopulator):
        self.pack_forget()
        self.__game_frame = GameFrame(self.__master, populator)
        self.__game_frame.bind("<Destroy>", lambda _: self.put())
