import json
from pathlib import Path


class JSONParser:
    """Parser for JSON input."""

    def __init__(self, source: str | Path):
        self.source = source

    def validate(self) -> bool:
        """Validate the JSON input.

        Raises:
            FileNotFoundError: If the input file does not exist.
            OSError: If the input file cannot be accessed for reading.

        Returns:
            True if the file contains valid JSON.
            False if the file content is not valid JSON.
        """
        try:
            with open(self.source, "r", encoding="utf-8") as file:
                json.load(file)
        except json.JSONDecodeError:
            return False

        return True
    
    def parse(self):
        """Parse the JSON file into Python objects."""
        with open(self.source, "r", encoding="utf-8") as file:
            return json.load(file)
