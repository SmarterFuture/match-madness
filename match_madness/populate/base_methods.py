from os import path
from random import shuffle
from typing import Self, Tuple


DATA_LIB = path.join(path.dirname(__file__), "./data/")


class BasePopulator:
    """Base object for Populators"""

    data = {}
    __iterable = iter(())

    def normalised_step(self, max_value=100):
        """Returns value of unit in 100 point scale"""
        return max_value / max(0, len(self.data))

    def __iter__(self) -> Self:
        """Creates randomised iterator out of key-item pair dict"""
        items = list(self.data.items())
        shuffle(items)
        self.__iterable = iter(items)
        return self

    def __next__(self) -> Tuple[str, str]:
        """Handles JIT populating calls"""
        return next(self.__iterable)

    def __len__(self):
        """Returns length of data loaded from file"""
        return len(self.data)
