from os import listdir
from os.path import abspath, isfile, join
from re import search
from random import choice
from tkinter import Button, Frame, Misc
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from typing import Iterable

from match_madness.gui.game_frame import GameFrame
from match_madness.populate.base_methods import DATA_LIB, BasePopulator
from match_madness.populate.csv_methods import CsvPopulator
from match_madness.populate.json_methods import JsonPopulator


class MainFrame(Frame):
    """Main game object that handles anything within it"""

    __game_frame = None
    FILETYPES = [("JSON files", "*.json"), ("CSV files", "*.csv")]

    def __init__(self, master: Misc) -> None:
        """Creates MainFrame and places it onto master

        Args:
            master (Misc): Master window
        """
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

    def __custom_populator(self, file: str) -> BasePopulator:
        """Creates custom Populator from provided file

        Args:
            file (str): Absolute path to custom game file

        Returns:
            BasePopulator: Custom Populator from either .csv or .json file

        Raises:
            FileNotFoundError: Specified file does not exist
            NotImplementedError: File format is not supported
        """
        if not isfile(file):
            raise FileNotFoundError

        file_ext = file.split(".")[-1].lower()
        if file_ext == "json":
            return JsonPopulator(file)

        if file_ext == "csv":
            return CsvPopulator(file)

        raise NotImplementedError

    def __eng_populator(self) -> JsonPopulator:
        """Creates populator from random file within ../populate/data/ directory

        Returns:
            JsonPopulator: Created Populator for English -> Slovak game
        """
        eng_files = list(filter(lambda x: search(r".*eng\d+\.json$", x), self.__get_data()))
        file = choice(eng_files)
        return JsonPopulator(file)

    def __esp_populator(self) -> JsonPopulator:
        """Creates populator from random file within ../populate/data/ directory

        Returns:
            JsonPopulator: Created Populator for Spanish -> English game
        """
        esp_files = list(filter(lambda x: search(r".*esp\d+\.json$", x), self.__get_data()))
        file = choice(esp_files)
        return JsonPopulator(file)

    def __gen_custom_game(self):
        """Generates custom game or provides information for user about how it failed"""
        file = askopenfilename(title="Select custom file", initialdir="$HOME", filetypes=self.FILETYPES)
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
            showerror(title="Wrong filetype", message="File you provided is of wrong filetype")

    def __get_data(self) -> Iterable[str]:
        """Looks into ../populate/data/

        Returns:
            Iterable[str]: Full path to file within ../populate/data/ location
        """
        dir_files = listdir(DATA_LIB)
        for file in dir_files:
            file = join(DATA_LIB, file)
            if isfile(file):
                yield file

    def __gen_game(self, populator: BasePopulator):
        """Generates game populated by Populator

        Args:
            populator (BasePopulator): Used to populate game
        """
        self.pack_forget()
        self.__game_frame = GameFrame(self.__master, populator)
        self.__game_frame.bind("<Destroy>", lambda _: self.put())

    def put(self):
        """Places / unhides MainFrame onto master"""
        if self.winfo_exists() == 0:
            return

        self.pack(expand=1, fill="both")
        self.update()
