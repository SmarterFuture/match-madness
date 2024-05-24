import json
from matching_madness.populate.base_methods import BasePopulator


class JsonPopulator(BasePopulator):
    """JSON based populator for populating GameFrame"""

    def __init__(self, file: str) -> None:
        """Creates Populator object used to populate GameFrame and provide additional
            information about loaded data

        Args:
            file (str): Path to the file with game data
        """
        self.data = {}
        with open(file, encoding="utf8") as raw_json:
            self.data = json.load(raw_json)

        items = list(self.data.items())
        for key, item in items:
            if not isinstance(item, str):
                self.data.pop(key)
