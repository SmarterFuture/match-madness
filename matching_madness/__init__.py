import tkinter as tk

from matching_madness.gui.main_frame import MainFrame


def main():
    """This is main function, that runs whole application"""
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Matching Madness")

    MainFrame(root)

    root.mainloop()
