# Dungeons and the Ur-Dragon

A Python-based, turn-based RPG battle simulator inspired by classic fantasy games. Players assemble a party of characters, manage spells and inventory, and battle increasingly challenging enemies through a series of encounters.

The project began as an exploration of **object-oriented programming and game development**, eventually expanding into combat mechanics, enemy decision-making, and an experimental graphical implementation using Pygame.

## Project Overview

Dungeons and the Ur-Dragon is a terminal-based RPG that combines character attributes, turn-based combat, magic, consumable items, and enemy AI.

The game features a three-room encounter structure, where players fight enemies, collect rewards, and progress toward a final boss battle.

Characters and enemies have individual attributes, including health, mana, physical and magical attack, defense, and speed.

## Game Features

### Turn-Based Combat

Players control a party of characters and choose their actions during combat.

The battle system includes:

- Physical attacks with randomized damage and critical hits.
- Offensive, defensive, healing, and support magic.
- Mana management and spell costs.
- Target selection for individual and area-of-effect abilities.
- Consumable items that restore health, revive characters, or apply status effects.

### Enemy AI

Enemies use rule-based decision-making to select actions during combat.

Their behavior includes prioritizing vulnerable targets based on health and defensive attributes and selecting spells during encounters.

### Character & Inventory Systems

The game uses object-oriented components to manage individual characters, available spells, item inventories, and combat interactions.

Each character maintains their own statistics and resources, while the inventory system tracks consumable items and their effects.

### Dungeon Progression

The terminal game includes three encounters, with item rewards between battles and a final boss encounter.

This introduces progression and resource management beyond individual battles.

### Saving and Loading

The terminal game automatically saves at the beginning of each fight. A save keeps the party, character stats, inventories, and enemy lineup. If the party falls, you can reload that checkpoint and retry immediately. You can also load it when starting the game. The single save slot is `savegame.json` in the project root; battles in progress are not saved.

## Pygame Development

Alongside the terminal version, I began experimenting with a graphical implementation using **Pygame**.

The graphical prototype explores:

- Character sprite rendering and animation.
- Idle, attack, damage, and death animations.
- Backgrounds and graphical interface elements.
- Keyboard-controlled animation states.
- Frame-based updates and sprite sheet handling.

The Pygame implementation is an experimental prototype and does not yet include the complete combat mechanics of the terminal version.

## Future Development

Possible extensions include:

- Integrating the terminal combat mechanics into the graphical interface.
- Expanding enemy decision-making and combat strategies.
- Implementing additional dungeons, encounters, and boss mechanics.
- Adding persistent character progression.
