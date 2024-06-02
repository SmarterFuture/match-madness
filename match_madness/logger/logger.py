from os import getcwd, makedirs
from os.path import join
from datetime import datetime


class Logger:
    """Tracks all the users mistakes"""

    def __init__(self):
        """Creates logs directory at current working directory (of whole module)"""
        timestamp = datetime.now().isoformat(timespec="minutes").replace(":", "_")
        now = f"log-{timestamp}.txt"

        path = join(getcwd(), "logs")
        makedirs(path, exist_ok=True)

        self.__path = join(path, now)
        self.__file = open(self.__path, "w", encoding="utf8")  # pylint: disable=R1732

    def write(self, word: str, defi: str, corr: str) -> None:
        """Creates log in file

        Args:
            word (str): Clicked card with word
            defi (str): Clicked card with definition
            corr (str): Correct definition for clicked word
        """
        log = f'You matched "{word}" with "{defi}" instead of "{corr}"\n'
        self.__file.write(log)

    def close(self) -> str:
        """Closes log file

        Returns:
            str: Path to log file
        """
        self.__file.close()
        return self.__path
