from matching_madness.populate.base_methods import BasePopulator


class CsvPopulator(BasePopulator):

    def __init__(self, file: str) -> None:
        self.data = {}
        with open(file, encoding="utf8") as raw_file:
            raw_data = raw_file.read().split("\n")

        for line in raw_data:
            if line == "":
                continue
            word, definition = line.split(",")
            self.data[word] = definition
