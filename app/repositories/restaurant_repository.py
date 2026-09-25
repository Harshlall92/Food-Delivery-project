import json
from pathlib import Path

class RestaurantRepository:

    def __init__(self, filepath: str = "data/restaurants.json"):
        self.filepath = Path(filepath)

    async def get_restaurants(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                contents = json.load(file)
                return contents
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.filepath} not found.")
        return []