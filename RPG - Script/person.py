import random

from Colors import bcolors
from inventory import Inventory


class Person:
    def __init__(self, name, hp, mp, atk, df, speed, mgk_atk, mgk_def, spells, descri,boss=False ):
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.mp = mp
        self.maxmp = mp
        self.atk = atk
        self.df = df
        self.speed = speed
        self.mgk_atk = mgk_atk
        self.mgk_def = mgk_def
        self.inventory = Inventory()
        self.spells = spells
        self.descri = descri
        self.boss = boss

        # For enemies: stores weights of each spell if needed
        self.spell_weights = {spell: 1 for spell in spells}

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def attacks(self, target):
        critical_chance = 0.2  # 20% chance for a critical hit
        critical_multiplier = 2  # Critical hits deal double damage

        # Define attack damage range
        min_attack = self.atk // 2  # Minimum attack damage
        max_attack = self.atk  # Maximum attack damage

        # Generate random damage within the specified range
        dmg = random.randint(min_attack, max_attack) - target.df

        # Determine if a critical hit occurs
        is_critical = random.random() < critical_chance
        if is_critical:
            dmg *= critical_multiplier
            print(bcolors.BOLD + bcolors.RED + "\nCRITICAL HIT! " + bcolors.ENDC)

        miss_messages = [
            f"{target.name} {bcolors.BOLD}evades{bcolors.ENDC} {self.name}'s attack!",
            f"{self.name} strikes, but {target.name} {bcolors.BOLD}dodges{bcolors.ENDC} it!",
            f"{target.name} deflects the blow with a {bcolors.BOLD}perfect parry!{bcolors.ENDC}",
            f"{self.name}'s attack is met with a {bcolors.BOLD}quick parry{bcolors.ENDC} from {target.name}!",
            f"{target.name} braces for the attack, {bcolors.BOLD}absorbing{bcolors.ENDC} {self.name}'s strike!",
            f"{self.name}'s attack, but {target.name} {bcolors.BOLD}blocks{bcolors.ENDC} it with a solid defense!"
        ]
        if dmg < 0:
            message = random.choice(miss_messages)
            print(message)
        elif target.hp - dmg <= 0:
            target.hp = 0

            kill_messages = [
                f"{self.name} lands a devastating strike, {bcolors.RED}{bcolors.BOLD}finishing off{bcolors.ENDC} {target.name}!",
                f"{target.name} falls as {self.name} delivers the {bcolors.RED}{bcolors.BOLD}final blow!{bcolors.ENDC}",
                f"{self.name} {bcolors.RED}{bcolors.BOLD}defeats{bcolors.ENDC} {target.name} with a powerful attack!",
                f"With a fierce attack, {self.name} {bcolors.RED}{bcolors.BOLD}vanquishes{bcolors.ENDC} {target.name}!",
                f"{self.name}'s strike overwhelms {target.name}, leaving them {bcolors.RED}{bcolors.BOLD}defeated!{bcolors.ENDC}",
            ]

            message = random.choice(kill_messages)
            print(message)

        else:
            target.hp -= dmg
            print(f"{self.name} attacks {target.name} for {bcolors.RED}{bcolors.BOLD}{dmg} points of damage{bcolors.ENDC}\n")

    def cast_magic(self, target, magic):
        magic.apply(caster=self, target=target)

    def get_stats(self):
        # Calculate the bar lengths and ticks
        hp_bar_length = 25
        mp_bar_length = 10

        # HP bar and MP bar generation with fixed lengths
        hp_bar = "█" * int((self.hp / self.maxhp) * hp_bar_length)
        hp_bar = hp_bar.ljust(hp_bar_length)

        mp_bar = "█" * int((self.mp / self.maxmp) * mp_bar_length)
        mp_bar = mp_bar.ljust(mp_bar_length)

        # Format HP and MP as strings with right-alignment within fixed widths
        current_hp = f"{int(self.hp)}/{self.maxhp}".rjust(9)
        current_mp = f"{self.mp}/{self.maxmp}".rjust(7)

        # Print the character stats line
        print("                     _________________________              __________ ")
        print(
            f"{bcolors.BOLD}{self.name:<20}{current_hp} |{bcolors.GREEN}{hp_bar}{bcolors.ENDC}|    {current_mp} |{bcolors.BLUE}{mp_bar}{bcolors.ENDC}|")

    def __str__(self):
        return (f"Name: {self.name}"
                f"\nHealth: {self.hp}"
                f"\tAtk: {self.atk}"
                f"\tDef: {self.df}"
                f"\nMP: {self.mp}"
                f"\tMagic Attack: {self.mgk_atk}"
                f"\tMagic Defence: {self.mgk_def}"
                f"\nSpells: {self.spells}")
