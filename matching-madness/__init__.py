import tkinter as tk
from .gui.GameFrame import GameFrame


def main():
    root = tk.Tk()
    root.title("Matching Madness")
    
    main_gui = GameFrame(root)

    root.mainloop()
