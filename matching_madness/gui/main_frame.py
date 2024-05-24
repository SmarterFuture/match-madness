from os import listdir
from os.path import abspath, isfile, join
from re import search
from random import choice
from tkinter import Button, Frame, Misc
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from typing import Iterable

from matching_madness.gui.game_frame import GameFrame
from matching_madness.populate.base_methods import DATA_LIB, BasePopulator
from matching_madness.populate.csv_methods import CsvPopulator
from matching_madness.populate.json_methods import JsonPopulator


class MainFrame(Frame):
    __game_frame = None
    FILETYPES = [("JSON files", "*.json"), ("CSV files", "*.csv")]

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
            command=lambda: self.__gen_game(self.__eng_populator()),
        ).place(relx=col, rely=space, relheight=height, relwidth=width)

        Button(
            self,
            text="Spanish -> English",
            command=lambda: self.__gen_game(self.__esp_populator()),
        ).place(relx=col, rely=2 * space + height, relheight=height, relwidth=width)

        Button(self, text="Custom", command=self.__gen_custom_game).place(
            relx=col, rely=3 * space + 2 * height, relheight=height, relwidth=width
        )

    def put(self):
        if self.winfo_exists() == 0:
            return

        self.pack(expand=1, fill="both")
        self.update()

    def __get_data(self) -> Iterable[str]:
        dir_files = listdir(DATA_LIB)
        for file in dir_files:
            file = join(DATA_LIB, file)
            if isfile(file):
                yield file

    def __eng_populator(self) -> JsonPopulator:
        eng_files = list(
            filter(lambda x: search(r".*eng\d+\.json$", x), self.__get_data())
        )
        file = choice(eng_files)
        return JsonPopulator(file)

    def __esp_populator(self) -> JsonPopulator:
        esp_files = list(
            filter(lambda x: search(r".*esp\d+\.json$", x), self.__get_data())
        )
        file = choice(esp_files)
        return JsonPopulator(file)

    def __custom_populator(self, file: str) -> BasePopulator:
        if not isfile(file):
            raise FileNotFoundError("File does not exists")

        file_ext = file.split(".")[-1].lower()
        if file_ext == "json":
            return JsonPopulator(file)

        if file_ext == "csv":
            return CsvPopulator(file)

        raise NotImplementedError("File format is not supported")

    def __gen_game(self, populator: BasePopulator):
        self.pack_forget()
        self.__game_frame = GameFrame(self.__master, populator)
        self.__game_frame.bind("<Destroy>", lambda _: self.put())

    def __gen_custom_game(self):
        file = askopenfilename(
            title="Select custom file", initialdir="$HOME", filetypes=self.FILETYPES
        )
        file = abspath(file)
        if file is None:
            return

        try:
            self.__gen_game(self.__custom_populator(file))
        except FileNotFoundError:
            showerror(
                title="Not found",
                message="File you provided either was not found or it does not exist",
            )
        except NotImplementedError:
            showerror(
                title="Wrong filetype", message="File you provided is of wrong filetype"
            )
