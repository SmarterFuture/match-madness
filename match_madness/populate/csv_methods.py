from match_madness.populate.base_methods import BasePopulator


class CsvPopulator(BasePopulator):
    """CSV based populator for populating GameFrame"""


    def __init__(self, file: str) -> None:
        """Creates Populator object used to populate GameFrame and provide additional
            information about loaded data

        Args:
            file (str): Path to the file with game data
        """
        self.data = {}
        with open(file, encoding="utf8") as raw_file:
            raw_data = raw_file.read().split("\n")

        for line in raw_data:
            line = line.split(",")
            if line == [""] or len(line) != 2:
                continue

            word, definition = line
            self.data[word] = definition
