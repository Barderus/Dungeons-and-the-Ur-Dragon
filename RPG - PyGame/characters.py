from Fighter import *
from spells import *

aerith_spells = [cura,curaga,revive,flare, blizzard]
snape_spells = [fire,thunder, dark, ultima, quake, tornado, drain]
gandalf_spells = [cura, protect, shell, holy, fire, speed]

# Avatar
knight = Fighter("Gimli", 1800, 30, 170, 105, 30, 30, 90, [], 10, 20)
warrior = Fighter("Aragorn", 900, 60, 200, 75, 70, 50, 50, [], 10, 20)
barbarian = Fighter("Eowyn", 850, 10, 250, 60, 80, 0, 50, [], 10, 20)
blue_witch = Fighter("Aerith", 700, 360, 30, 80, 45, 150, 100, aerith_spells, 10, 20)
fire_wizard = Fighter("Snape", 780, 440, 40, 70, 55, 220, 70, snape_spells, 10, 20)
mage_guardian = Fighter("Gandalf", 750, 400, 80, 75, 40, 200, 90, gandalf_spells, 10, 20)

avatar_list = [knight, warrior, barbarian, blue_witch, fire_wizard, mage_guardian]

faye_spells = [bio, blizzard, meteor, speed, protect]
dark_blade_spells = [dark, drain, speed, shell]
black_mage_spells = [fire, thunder, blizzard, quake, tornado]
liora_spells = [light_bolt, cure,cura, curaga, revive, protect, shell]
kobold_spells = [fire]

# NPC list
king = Fighter("Eldric", 650, 50, 150, 70, 90, 80, 60, [], 10, 20)
moonstone = Fighter("Faye", 530, 340, 50, 50, 75, 180, 75, faye_spells, 10, 20)
night_knight = Fighter("Thorne", 620, 300, 145, 65, 55, 100, 55, dark_blade_spells, 10, 20)
paladin = Fighter("Garrick", 850, 40, 130, 100, 40, 35, 50, None, 10, 20)
purple_wizard = Fighter("Zarek", 500, 400, 50, 65, 65, 220, 75, black_mage_spells, 10, 20)
#healing_wizard = Fighter("Liora", 600, 360, 55, 50, 35, 180, 100, liora_spells, 10, 20)
kobold = Fighter("Mikey", 550, 50, 155, 30, 100, 110, 20, kobold_spells, 10, 20)

npc_list = [king, moonstone, night_knight, paladin, purple_wizard, kobold]

necro_spells = [dark, drain, fire, quake]

# Enemies list
wraith = Fighter("Wraith", 1150, 50, 220, 100, 70, 10, 80, None, 10, 20)
troll = Fighter("Troll", 1550, 50, 200, 120, 70, 10, 80, None, 10, 20)
necromancer = Fighter("Necromancer", 650, 800, 75, 30, 60, 200, 90, necro_spells, 10, 20)
goblin = Fighter("Goblin", 450, 50, 120, 30, 100, 105, 20, kobold_spells, 10, 20 )
skeleton =Fighter("Skeleton Warrior", 640, 50, 125, 30, 60, 10, 20, None, 10, 20)
slime = Fighter("Slime", 750, 50, 145, 120, 10, 10, 75, None, 10, 20)
orc = Fighter("Orc", 900, 50, 175, 50, 75, 120, 20, None, 10, 20)
ghoul = Fighter("Ghoul", 550, 50, 130, 10, 0, 10, 20, None, 10, 20)
fire_worm = Fighter("Fire Worm", 870, 200, 100, 90, 70, 175, 50, kobold_spells, 10, 20)

enemies_list = [wraith, troll, necromancer, goblin, skeleton, slime, orc, ghoul, fire_worm]

dragon_spells = [firaga]
demon_spells = [pandemonium]
lich_spells = [meteor, dark, drain, quake, ultima, curaga, revive, fire]

#Boss List
dragon = Fighter("Ur-Dragon", 4000, 500, 300, 100, 100, 200, 100, dragon_spells, 10, 20)
demon =  Fighter("Orcus", 6666, 666, 333, 99, 99, 120, 99, demon_spells, 10, 20)
lich = Fighter("Lich", 2000, 1000, 100, 100, 300, 100, 120, lich_spells, 10, 20)

boss_list = [dragon, demon, lich]