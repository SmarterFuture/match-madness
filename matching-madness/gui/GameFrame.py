import tkinter as tk
from tkinter import Misc, ttk
from typing import Iterator, List, Set, Tuple
from .Card import Card
from random import choice


class GameFrame(tk.Frame):
    DEFI_CLICKED = None
    WORD_CLICKED = None
    DELAY = 1000 # in ms

    def __init__(self, master: Misc, populationMethod: Iterator[Tuple[str, str]]) -> None:
        super().__init__(master, height=600, width=300, bg="blue")
        self.pack(expand=1, fill="both")

        self.__populationMethod = populationMethod
        self.__populationLock = False

        xFirCol = 0.2
        xSecCol = 0.6
        height = 0.1
        width = 0.2
        
        ttk.Progressbar(self) \
            .place(relx=xFirCol,rely=0.1, relwidth=xSecCol, relheight=0.05)

        self.__defiButtons: List[Card] = []
        self.__wordButtons: List[Card] = []
        self.__defiVacant: Set[Card] = set()
        self.__wordVacant: Set[Card] = set()

        for i in range(5):
            rely = 0.2 + i * 0.15

            word = Card(self, "", "", lambda i=i: self.__cardHook(True, i))
            word.place(relx=xFirCol, rely=rely, relheight=height, relwidth=width)

            defi = Card(self, "", "", lambda i=i: self.__cardHook(False, i))
            defi.place(relx=xSecCol, rely=rely, relheight=height, relwidth=width)

            self.__defiButtons.append(defi)
            self.__wordButtons.append(word)
            self.__defiVacant.add(defi)
            self.__wordVacant.add(word)

    def __cardHook(self, is_word: bool, card_id: int):
        oldBut = [self.DEFI_CLICKED, self.WORD_CLICKED][is_word]

        if oldBut != None:
            oldBut.click(True)

        if is_word:
            self.WORD_CLICKED = self.__wordButtons[card_id]
        else:
            self.DEFI_CLICKED = self.__defiButtons[card_id]

        self.__checkPair()

    def __checkPair(self):
        if self.DEFI_CLICKED == None or self.WORD_CLICKED == None:
            return
        
        defiBut = self.DEFI_CLICKED
        wordBut = self.WORD_CLICKED

        self.DEFI_CLICKED = None
        self.WORD_CLICKED = None

        if defiBut == wordBut:
            defiBut.corrct()
            wordBut.corrct()
            self.__defiVacant.add(defiBut)
            self.__wordVacant.add(wordBut)
            self.after(self.DELAY, self.populate)

        else:
            defiBut.wrong()
            wordBut.wrong()
            
            def normalise():
                defiBut.click(True)
                wordBut.click(True)

            self.after(self.DELAY, normalise)


    def populate(self):
        if self.__populationLock:
            return
        if 2 > len(self.__wordVacant):
            return

        defiVacant = list(self.__defiVacant)
        for wordBut in self.__wordVacant:
            defiBut = choice(defiVacant)
            
            try:
                word, defi = next(self.__populationMethod)
            except StopIteration:
                self.__populationLock = True
                return
            else:
                wordBut.change(word, defi)
                defiBut.change(defi, word)

