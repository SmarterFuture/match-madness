import json
from matching_madness.populate.base_methods import BasePopulator


class Populator(BasePopulator):
    """JSON based populator for populating GameFrame"""

    def __init__(self, file: str, custom_path: str | None = None) -> None:
        """Creates Populator object used to populate GameFrame and provide additional
            information about loaded data

        Args:
            file (str): Name of the file in ./data/ directory or in directory provided
                by "custom_path"
            custom_path (str | None): Path to directory in which "file" is located
        """
        file = custom_path or self.PWD + file
        with open(file, encoding="utf8") as raw_json:
            self.data = json.load(raw_json)
