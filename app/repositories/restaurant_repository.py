import json
from pathlib import Path
from anyio import open_file

class RestaurantRepository:

    def __init__(self, filepath: str = "data/restaurants.json"):
        self.filepath = Path(filepath)

    async def get_restaurants(self):
        try:
            async with await open_file(self.filepath, "r", encoding="utf-8") as file:
                contents = await file.read()
                return json.loads(contents)
        except FileNotFoundError:
            print(f"File not found: {self.filepath}")
        return []