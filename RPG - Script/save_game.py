import json
import os
from pathlib import Path

from characters import allies, avatars, bosses, enemies
from items import Items


SAVE_FILE = Path(__file__).resolve().parent.parent / "savegame.json"
CHARACTERS = {
    **{f"avatar:{name}": character for name, character in avatars.items()},
    **{f"ally:{name}": character for name, character in allies.items()},
    **{f"enemy:{name}": character for name, character in enemies.items()},
    **{f"boss:{name}": character for name, character in bosses.items()},
}
CHARACTER_IDS = {character: name for name, character in CHARACTERS.items()}
SAVED_STATS = ("hp", "mp", "atk", "df", "speed", "mgk_atk", "mgk_def")


def save_game(next_room, party, encounters):
    characters = {}
    for character_id, character in CHARACTERS.items():
        characters[character_id] = {
            "stats": {stat: getattr(character, stat) for stat in SAVED_STATS},
            "inventory": [
                {
                    "name": item.name,
                    "effect": item.effect,
                    "quantity": item.quantity,
                    "description": item.description,
                }
                for item in character.inventory.items.values()
            ],
        }

    data = {
        "version": 1,
        "next_room": next_room,
        "party": [CHARACTER_IDS[character] for character in party],
        "encounters": [
            [CHARACTER_IDS[character] for character in encounter]
            for encounter in encounters
        ],
        "characters": characters,
    }

    temporary_file = SAVE_FILE.with_suffix(".tmp")
    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        os.replace(temporary_file, SAVE_FILE)
    except OSError as error:
        print(f"Could not save the game: {error}")
        return False

    print(f"Game saved to {SAVE_FILE}.")
    return True


def load_game():
    try:
        with SAVE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if data["version"] != 1 or data["next_room"] not in (1, 2, 3):
            raise ValueError("unsupported save version or room")
        if len(data["party"]) != 4 or len(data["encounters"]) != 3:
            raise ValueError("incomplete party or encounter list")

        party = [CHARACTERS[character_id] for character_id in data["party"]]
        encounters = [
            [CHARACTERS[character_id] for character_id in encounter]
            for encounter in data["encounters"]
        ]

        saved_characters = data["characters"]
        restored_items = {}
        for character_id in CHARACTERS:
            saved = saved_characters[character_id]
            for stat in SAVED_STATS:
                if not isinstance(saved["stats"][stat], (int, float)):
                    raise ValueError(f"invalid {stat} for {character_id}")
            restored_items[character_id] = []
            for item in saved["inventory"]:
                if not isinstance(item["quantity"], int) or item["quantity"] < 0:
                    raise ValueError(f"invalid item quantity for {character_id}")
                restored_items[character_id].append(Items(**item))

        for character_id, character in CHARACTERS.items():
            saved = saved_characters[character_id]
            for stat in SAVED_STATS:
                setattr(character, stat, saved["stats"][stat])
            character.inventory.items.clear()
            for item in restored_items[character_id]:
                character.inventory.add_item(item)

    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Could not load the saved game: {error}")
        return None

    print(f"Game loaded from {SAVE_FILE}. Room {data['next_room']} is next.")
    return data["next_room"], party, encounters
