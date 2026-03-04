from dataclasses import dataclass, field

from spells import *


@dataclass(frozen=True)
class FighterTemplate:
    name: str
    hp: int
    mp: int
    atk: int
    df: int
    speed: int
    mgk_atk: int
    mgk_def: int
    spells: list = field(default_factory=list)
    boss: bool = False

    @property
    def max_hp(self):
        return self.hp

    @property
    def max_mp(self):
        return self.mp

    def create_fighter(self, xcoord=0, ycoord=0, flip=False):
        from Fighter import Fighter

        return Fighter(
            self.name,
            self.hp,
            self.mp,
            self.atk,
            self.df,
            self.speed,
            self.mgk_atk,
            self.mgk_def,
            list(self.spells),
            xcoord,
            ycoord,
            self.boss,
            flip=flip,
        )


aerith_spells = [cura, curaga, revive, flare, blizzard]
snape_spells = [fire, thunder, dark, ultima, quake, tornado, drain]
gandalf_spells = [cura, protect, shell, holy, fire, speed]

avatar_list = [
    FighterTemplate("Gimli", 1800, 30, 170, 105, 30, 30, 90, []),
    FighterTemplate("Aragorn", 900, 60, 200, 75, 70, 50, 50, []),
    FighterTemplate("Eowyn", 850, 10, 250, 60, 80, 0, 50, []),
    FighterTemplate("Aerith", 700, 360, 30, 80, 45, 150, 100, aerith_spells),
    FighterTemplate("Snape", 780, 440, 40, 70, 55, 220, 70, snape_spells),
    FighterTemplate("Gandalf", 750, 400, 80, 75, 40, 200, 90, gandalf_spells),
]

faye_spells = [bio, blizzard, meteor, speed, protect]
dark_blade_spells = [dark, drain, speed, shell]
black_mage_spells = [fire, thunder, blizzard, quake, tornado]
liora_spells = [light_bolt, cure, cura, curaga, revive, protect, shell]
kobold_spells = [fire]

npc_list = [
    FighterTemplate("Eldric", 650, 50, 150, 70, 90, 80, 60, []),
    FighterTemplate("Faye", 530, 340, 50, 50, 75, 180, 75, faye_spells),
    FighterTemplate("Thorne", 620, 300, 145, 65, 55, 100, 55, dark_blade_spells),
    FighterTemplate("Garrick", 850, 40, 130, 100, 40, 35, 50, []),
    FighterTemplate("Zarek", 500, 400, 50, 65, 65, 220, 75, black_mage_spells),
    FighterTemplate("Mikey", 550, 50, 155, 30, 100, 110, 20, kobold_spells),
]

necro_spells = [dark, drain, fire, quake]

enemies_list = [
    FighterTemplate("Wraith", 1150, 50, 220, 100, 70, 10, 80, []),
    FighterTemplate("Troll", 1550, 50, 200, 120, 70, 10, 80, []),
    FighterTemplate("Necromancer", 650, 800, 75, 30, 60, 200, 90, necro_spells),
    FighterTemplate("Goblin", 450, 50, 120, 30, 100, 105, 20, kobold_spells),
    FighterTemplate("Skeleton Warrior", 640, 50, 125, 30, 60, 10, 20, []),
    FighterTemplate("Slime", 750, 50, 145, 120, 10, 10, 75, []),
    FighterTemplate("Orc", 900, 50, 175, 50, 75, 120, 20, []),
    FighterTemplate("Ghoul", 550, 50, 130, 10, 0, 10, 20, []),
    FighterTemplate("Fire Worm", 870, 200, 100, 90, 70, 175, 50, kobold_spells),
]

dragon_spells = [firaga]
demon_spells = [pandemonium]
lich_spells = [meteor, dark, drain, quake, ultima, curaga, revive, fire]

boss_list = [
    FighterTemplate("Ur-Dragon", 4000, 500, 300, 100, 100, 200, 100, dragon_spells, True),
    FighterTemplate("Orcus", 6666, 666, 333, 99, 99, 120, 99, demon_spells, True),
    FighterTemplate("Lich", 2000, 1000, 100, 100, 300, 100, 120, lich_spells, True),
]
