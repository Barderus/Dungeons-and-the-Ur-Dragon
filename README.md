# RPG Battle Script Game

## Overview
This is a text-based RPG battle game written in Python, where players can create characters, cast spells, use items, and engage in battles with enemies. The game features a variety of spells, including offensive, defensive, and healing abilities, as well as an inventory system for using items during combat. The application is designed to simulate turn-based battles between characters (players or enemies), where the player's strategic use of spells, items, and stats will determine the outcome.

## Features
- **Character Selection**: Players can select characters with customizable stats from many different pop culture sources.
- **Spells**: A variety of spells are available, including Fire, Thunder, Blizzard, Meteor, Quake, Tornado, Ultima, healing, revival, and stat-boosting spells.
- **Inventory System**: Each character can hold a list of items (e.g., health potions, buffs), and use items during battle.
- **Battle System**: Characters can fight enemies with randomized behavior, including the use of items and spells.
- **Mana System**: Characters and enemies have mana points (MP), which are required to cast spells.
- **Turn-based Gameplay**: Players and enemies take turns attacking, using spells, and using items until one side is defeated.

## Game Classes & Components

- **Person Class**
Represents a character (player or enemy) in the game. Includes attributes like name, HP, MP, attack, defense, speed, items, and spells. The class has methods for physical attacks, casting spells, and using items.

- **Magic Class**
Handles the different types of magic spells (fire, thunder, healing, etc.). The class includes methods to cast spells, check MP, and apply spell effects.

- **Inventory Class**
Manages the character's inventory, allowing items to be added, removed, or used during battle. Items can have various effects, such as healing or stat boosts.

- **Items Class**
Represents individual items in the game, including properties and effects like healing or buffing. Each item can be used to apply a specific effect to the character.

- **Battle Class**
Handles the mechanics of turn-based combat. Manages player and enemy turns, checks for victory conditions, and applies spell and item effects.


## Contributing
Feel free to fork the repository and submit pull requests for improvements, bug fixes, or new features. Contributions are welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
* Inspired by classic RPG games.
* Uses Python's object-oriented programming principles to structure the game.


