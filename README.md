# 🐉 Dungeons and the Ur-Dragon

A text-based RPG battle simulator written in Python, where players can engage in strategic, turn-based combat with procedurally generated enemies and iconic characters from pop culture.

---

##  Overview

This game simulates classic RPG-style battles through a terminal-based interface. Players can create characters, cast spells, use items, and take on legendary enemies — including the mythical **Ur-Dragon**. The gameplay revolves around turn-based strategy, where thoughtful use of spells, stats, and inventory items determines victory.

---

## ✨ Features

- **Character Selection**: Choose from customizable characters inspired by various pop culture universes.
- **Spells**: Use powerful offensive, defensive, and support spells (e.g., Fire, Thunder, Meteor, Heal, Ultima).
- **Inventory System**: Store and use items like potions and buffs during battle.
- **Turn-Based Battle System**: Control character actions or simulate enemy AI decisions each round.
- **Mana System**: Manage MP strategically to time attacks, buffs, and heals.
- **Procedural Generation**: Enemies and stats are generated dynamically for each encounter.
- **Team Composition**: Simulate full-party combat with allies, healers, and damage dealers.

---

##  Game Classes & Components

- **Person Class**: Core entity for characters and enemies. Manages HP, MP, stats, available spells/items, and decision logic.
- **Magic Class**: Defines spells, costs, and behavior (healing, buffing, damage).
- **Inventory Class**: Manages and tracks consumable items across all characters.
- **Items Class**: Represents usable items with effects like healing or stat buffs.
- **Battle Class**: Handles turn order, damage application, spell effects, and battle resolution logic.

---

##  Skills Demonstrated

- Object-Oriented Programming (OOP)
- Modular code organization
- Procedural logic and combat simulations
- State management and turn-based mechanics
- Expandability (e.g., plug-and-play spells, enemies, items)

---
##  Next Steps

This project is actively being developed into a GUI-based RPG using **Pygame**, with the following upcoming features:

- Visual sprites and character animations
- Mouse-driven turn selection and real-time updates
- Save/load mechanics for persistent characters and campaigns
---
## Contributing
Feel free to fork the repository and submit pull requests for improvements, bug fixes, or new features. Contributions are welcome!

---
## License
This project is licensed under the MIT License - see the LICENSE file for details.

---
## Acknowledgements
* Inspired by classic RPG games.
* Uses Python's object-oriented programming principles to structure the game.