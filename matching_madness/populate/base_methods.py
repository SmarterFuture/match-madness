from typing import Self, Tuple


class BasePopulator:
    """Base class for all Populate objects"""

    PWD = "./matching_madness/populate/data/"
    data = {}
    __iterable = iter(())

    def normalised_step(self, max_value=100):
        """Returns value of unit in 100 point scale"""
        return max_value / len(self.data)

    def __iter__(self) -> Self:
        """Creates iterator out of key-item pair dict"""
        self.__iterable = iter(self.data.items())
        return self

    def __next__(self) -> Tuple[str, str]:
        """Handles JIT populating calls"""
        return next(self.__iterable)

    def __len__(self):
        """Returns length of data loaded from file"""
        return len(self.data)
