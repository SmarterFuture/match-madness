import tkinter as tk
from .gui.game_frame import GameFrame
from .populate.json_methods import Populator


def main():
    """This is main function, that runs whole application"""
    root = tk.Tk()
    root.title("Matching Madness")

    population_method = iter(Populator("eng1.json"))
    _main_gui = GameFrame(root, population_method)

    root.mainloop()
