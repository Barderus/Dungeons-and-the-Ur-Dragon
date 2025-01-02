from items import Items
from magic import Magic
from person import Person

# Black Spells
fire = Magic("Fire", "black", 25, 45, 0, "damage",
             "The mage emits a jolt of fire from their hands towards the enemy")
thunder = Magic("Thunder", "black", 25, 45, 25, "damage",
                "Lightning jolts from the mage's hand towards the enemy")
blizzard = Magic("Blizzard", "black", 25, 45, 0, "damage",
                 "A cold wind forms icicles that shoot towards the enemy")
meteor = Magic("Meteor", "black", 150, 150, 0, "damage",
               "A small meteor shower crashes down upon all enemies")
quake = Magic("Quake", "black", 100, 100, 0, "damage",
              "The ground trembles as fissures open beneath all enemies' feet")
tornado = Magic("Tornado", "black", 75, 65, 0, "damage",
                "A fierce whirlwind surrounds the enemy, slashing at them with violent winds")
ultima = Magic("Ultima", "black", 150, 150, 0, "damage",
               "The ultimate destructive spell, causing catastrophic damage to all enemies")
dark = Magic("Dark", "black", 30, 60, 0, "damage",
             "A shadowy force strikes the enemy, dealing damage and shrouding them in darkness.")
bio = Magic("Bio", "black", 30, 50, 0, "damage",
            "A poisonous wind that deals damage over time to the target.")
drain = Magic("Drain", "black", 25, 40, 0, "damage",
              "A sinister spell that drains the target's life force, restoring a portion of health to the caster.")

# White Spells
cure = Magic("Cure", "white", 25, 0, 75, "healing",
             "A gentle green light envelops the target, healing their wounds")
cura = Magic("Cura", "white", 35, 0, 100, "healing",
             "A stronger healing light mends the target's deeper wounds")
curaga = Magic("Curaga", "white", 50, 0, 150, "healing",
               "A powerful healing force that restores a huge amount of health")
revive = Magic("Revive", "white", 75, 0, 65, "revival",
               "A soft light envelops the fallen ally, reviving them with 10% of their maximum HP")

# Green Spells
protect = Magic("Protect", "green", 25, 0, 0, "buff",
                "A magical barrier surrounds the target, reducing physical damage taken")
shell = Magic("Shell", "green", 25, 0, 0, "buff",
              "A shimmering shield surrounds the target, reducing magical damage taken")
speed = Magic("Speed", "green", 25, 0, 0, "buff",
              "A spell that enhances the speed of all allies, allowing them to act more quickly in battle.")

# Blue Spell
holy = Magic("Holy", "blue", 100, 175, 0, "damage",
             "A blinding light descends from above, purging the enemy with divine power.")
flare = Magic("Flare", "blue", 110, 100, 0, "damage",
              "A concentrated burst of flames descends from the sky, engulfing the enemy and weakening everyone else..")


# Bosses spells
firaga = Magic("Breath of Fire", "black", 50, 150, 0, "damage",
             "Ur-Dragon breathes a wall of fire towards the enemies")
pandemonium = Magic("Pandemonium", "black", 200, 300, 0, "damage",
               "Orcus bring hell upon all his enemies. Cursing every single enemy.")

# Healing items
healing_pot = Items("Healing Potion", "heal", 1, "Restore 100 HP")
hi_pot = Items("HI-Potion", "heal", 1, "Restore 250 HP")
ether = Items("Ether", "heal", 1, "Restore 50MP")
hi_ether = Items("HI-Ether", "heal", 1, "Restore 100MP")
elixir = Items("Elixir", "heal", 1, "Restore 200 HP and 50 MP")
hi_elixir = Items("HI-Elixir", "heal", 1, "Restore to full Health and MP")
phoenix_down = Items("Phoenix Down", "heal", 1, "Revive target with 10% of HP")

# Status inc items
hermes_shoes = Items("Hermes Shoes", "buff", 1, "Increases target speed in 10")
red_fang = Items("Red Fang", "buff", 1, "Increases Attack in 10")
protect_coat = Items("Protect Coat", "buff", 1, "Increase Defense in 10")
faerie_bless = Items("Faerie Bless", "buff", 1, "Increase Magik Attack in 10")
witch_hat = Items("Witch's Hat", "buff", 1, "Increase Magik Defence in 10")

# Status dec items
slug_bomb = Items("Slug Bomb", "debuff", 1, "Lowers target Attack in 10")
acid = Items("Acid", "debuff", 1, "Lowers target Defense in 10")
spider_silk = Items("Spider Silk", "debuff", 1, "Lowers target Speed in 10")
moonstone = Items("Moonstone", "debuff", 1, "Lowers target Magik Attack in 10")
dragon_spit = Items("Dragon Spit", "debuff", 1, "Lowers target Magik Defense in 10")

all_items = [healing_pot, hi_pot, ether, hi_ether, elixir, hi_elixir, phoenix_down, hermes_shoes, red_fang, protect_coat,
             faerie_bless, witch_hat, slug_bomb, acid, spider_silk, moonstone, dragon_spit]
initial_items = {
    "fighter": [red_fang, hermes_shoes, acid, healing_pot],
    "bruiser": [hi_pot, healing_pot, protect_coat, spider_silk],
    "healer": [hi_pot, ether, witch_hat, dragon_spit],
    "green mage": [elixir, faerie_bless, dragon_spit, healing_pot],
    "wizard": [elixir, faerie_bless, dragon_spit, healing_pot],
    "you": [hi_pot, hi_elixir, phoenix_down]
}

# Creating player avatar
avatars = {
    "fighter": Person(
        name="Aragorn", hp=900, mp=60, atk=200, df=70, speed=70, mgk_atk=50, mgk_def=50,
        spells=[],
        descri="A fearless and stalwart protector, the Warrior excels in close combat and defense.",
    ),
    "bruiser": Person(
        name="Gimli", hp=1800, mp=30, atk=180, df=100, speed=30, mgk_atk=30, mgk_def=60,
        spells=[],
        descri="A stout and resilient fighter, known for his unwavering strength and indomitable spirit",
    ),
    "healer": Person(
        name="Aerith", hp=700, mp=360, atk=30, df=80, speed=45, mgk_atk=150, mgk_def=100,
        spells=[cura, curaga, revive, flare],
        descri="A compassionate and wise protector, the Healer specializes in restoring hp and safeguarding allies.",
    ),
    "green mage": Person(
        name="Gandalf", hp=750, mp=400, atk=80, df=75, speed=40, mgk_atk=200, mgk_def=90,
        spells=[cura, protect, shell, holy, fire, blizzard, speed],
        descri="A versatile caster, the Green Mage blends healing magic with elemental attacks, balancing support and offense."
    ),
    "wizard": Person(
        name="Snape", hp=680, mp=440, atk=40, df=70, speed=50, mgk_atk=220, mgk_def=70,
        spells=[fire, thunder, dark, ultima, quake, tornado, drain],
        descri="A master of destructive magic, the Black Mage wields powerful spells to annihilate enemies from afar."
    ),
    "you": Person(
        name="You", hp=1250, mp=350, atk=175, df=65, speed=80, mgk_atk=155, mgk_def=80,
        spells=[fire, blizzard, thunder, dark, drain, quake, tornado, meteor, ultima],
        descri="The destined champion, the Hero embodies the player's choices, leading the charge against evil with courage and valor."
    )
}

for character, items in initial_items.items():
    for item in items:
        avatars[character].inventory.add_item(item)

initial_items_allies = {
    "liora": [healing_pot, hi_pot, elixir, phoenix_down, protect_coat],
    "zarek": [ether, healing_pot, faerie_bless, moonstone],
    "eldric": [healing_pot, hermes_shoes, acid, slug_bomb, red_fang],
    "thorn": [ether, moonstone, witch_hat, spider_silk, dragon_spit, healing_pot],
    "faye": [ether, faerie_bless, acid, spider_silk],
    "garrick": [healing_pot, hi_pot, protect_coat, red_fang],
    "talia": [healing_pot, ether, phoenix_down, acid, moonstone]
}

# Create the NPC dictionary
allies = {
    "liora": Person(
        name="Liora the Healer", hp=600, mp=360, atk=55, df=50, speed=35, mgk_atk=180, mgk_def=100,
        spells=[blizzard, cure, cura, curaga, revive, protect, shell],
        descri="A compassionate healer from the White Lotus Order. Liora is known for her ability to mend even the most grievous wounds."
    ),
    "zarek": Person(
        name="Zarek the Black Mage", hp=500, mp=400, atk=50, df=65, speed=65, mgk_atk=220, mgk_def=75,
        spells=[fire, thunder, blizzard, quake, tornado],
        descri="A powerful black mage with mastery over the elements. Zarek's spells bring destruction to his foes."
    ),
    "eldric": Person(
        name="Eldric the Warrior", hp=650, mp=50, atk=150, df=70, speed=90, mgk_atk=80, mgk_def=60,
        spells=[],
        descri="A seasoned warrior known for his unshakable resolve and strength in battle. Eldric excels in close combat."
    ),
    "thorn": Person(
        name="Thorne the Dark Blade", hp=620, mp=300, atk=145, df=65, speed=55, mgk_atk=100, mgk_def=55,
        spells=[dark, drain, speed, shell],
        descri="A warrior with a mastery of dark magic, Thorne strikes fear into the hearts of his enemies with his cursed blade."
    ),
    "faye": Person(
        name="Faye the Mystic", hp=430, mp=340, atk=50, df=50, speed=75, mgk_atk=180, mgk_def=75,
        spells=[bio, blizzard, meteor, speed, protect],
        descri="A mysterious mage who wields unconventional magic. Faye uses forbidden spells to outsmart and debilitate her foes."
    ),
    "garrick": Person(
        name="Garrick the Guardian", hp=800, mp=40, atk=120, df=100, speed=40, mgk_atk=35, mgk_def=50,
        spells=[],
        descri="A stalwart warrior who prioritizes defense. Garrick’s immense strength and resilience make him a formidable protector."
    ),
    "talia": Person(
        name="Talia the Battle Cleric", hp=520, mp=240, atk=120, df=85, speed=45, mgk_atk=90, mgk_def=85,
        spells=[holy, flare, cure, protect, cura, shell],
        descri="A battle-hardened cleric who wields both a mace and holy magic. Talia can fight on the frontlines while supporting her allies."
    )
}

# Populate each ally's inventory from the initial_items_allies dictionary
for ally_name, items in initial_items_allies.items():
    for item in items:
        allies[ally_name].inventory.add_item(item)

initial_items_enemies = {
    "goblin": [healing_pot],
    "orc": [hi_pot],
    "kobold": [healing_pot],
    "knight": [hi_pot, protect_coat, hermes_shoes],
    "necro": [witch_hat, faerie_bless, ether, healing_pot],
    "troll": [red_fang],
}

# Creating enemies
enemies = {
    # Enemies
    "goblin": Person(
        name="Goblin", hp=450, mp=50, atk=120, df=30, speed=100, mgk_atk=105, mgk_def=20,
        spells=[fire],
        descri=""
    ),
    "orc": Person(
        name="Orc", hp=800, mp=50, atk=175, df=50, speed=75, mgk_atk=120, mgk_def=20,
        spells=[drain, blizzard],
        descri=""
    ),
    "kobold": Person(
        name="Kobold", hp=600, mp=50, atk=115, df=30, speed=90, mgk_atk=110, mgk_def=20,
        spells=[fire],
        descri=""
    ),
    "skeleton": Person(
        name="Skeleton Warrior", hp=640, mp=50, atk=125, df=30, speed=60, mgk_atk=10, mgk_def=20,
        spells=[],
        descri=""
    ),
    "knight": Person(
        name="Dark Knight", hp=900, mp=50, atk=180, df=70, speed=70, mgk_atk=10, mgk_def=20,
        spells=[drain, dark],
        descri=""
    ),
    "ghoul": Person(
        name="Ghoul", hp=550, mp=50, atk=130, df=10, speed=0, mgk_atk=10, mgk_def=20,
        spells=[],
        descri=""
    ),
    "slime": Person(
        name="Slime", hp=750, mp=50, atk=145, df=120, speed=10, mgk_atk=10, mgk_def=75,
        spells=[],
        descri=""
    ),
    "necro": Person(
        name="Necromancer", hp=500, mp=800, atk=75, df=30, speed=60, mgk_atk=180, mgk_def=80,
        spells=[dark, drain, fire, quake],
        descri=""
    ),
    "ghost": Person(
        name="Wraith", hp=1150, mp=50, atk=200, df=120, speed=70, mgk_atk=10, mgk_def=80,
        spells=[],
        descri=""
    ),
    "troll": Person(
        name="Troll", hp=1550, mp=50, atk=215, df=100, speed=30, mgk_atk=10, mgk_def=70,
        spells=[],
        descri=""
    ),

    "hydra": Person(
        name="Hydra", hp=1700, mp= 10, atk=200, df=100, speed=50, mgk_atk = 0, mgk_def= 50,
        spells=[],
        descri=""
    ),
    "worm":Person(
        name="Fire Worm", hp=870, mp=200, atk=100, df=90, speed=70, mgk_atk=175, mgk_def=50,
        spells=[fire],
        descri=""
    ),
    "floating_wizard":Person(
        name="Floating Wizard", hp=630, mp=800, atk=50, df=45, speed=70, mgk_atk=250, mgk_def=150,
        spells=[fire, blizzard, thunder, tornado, meteor, bio],
        descri=""
    )
}

# Populate each enemy's inventory from the initial_items_enemies dictionary
for enemy_name, items in initial_items_enemies.items():
    for item in items:
        enemies[enemy_name].inventory.add_item(item)

enemies["orc"].spell_weights = {
    drain: 2,  # Medium likelihood of using Drain
    blizzard: 5  # Higher likelihood of using Blizzard
}

enemies["knight"].spell_weights = {
    drain: 3,  # Medium chance
    protect: 4,  # Slightly higher chance to use Protect
    speed: 2  # Lower chance
}

enemies["necro"].spell_weights = {
    dark: 4,  # High chance of using Dark
    drain: 3,  # Medium chance
    fire: 2,  # Lower chance
    quake: 5,  # Highest likelihood
}

# Bosses

initial_items_bossess = {
    "lich": [hi_elixir, hi_pot, phoenix_down],
    "demon": [hi_elixir, hi_pot, phoenix_down],
}

bosses = {
    "dragon": Person(
        name="Ur-Dragon", hp=4000, mp=500, atk=300, df=100, speed=100, mgk_atk=200, mgk_def=100,
        spells=[firaga],
        descri="",
        boss = True

),
    "lich": Person(
        name="Lich", hp=2000, mp=1000, atk=100, df=100, mgk_atk=300, speed=100, mgk_def=120,
        spells=[meteor, dark, drain, quake, ultima, curaga, revive, fire],
        descri="",
        boss=True

    ),
    "demon": Person(
        name="Orcus", hp=6666, mp=666, atk=333, df=99, mgk_atk=99, speed=120, mgk_def=99,
        spells=[pandemonium ],
        descri="",
        boss=True

    )
}

bosses["lich"].spell_weights = {
    meteor: 3,
    dark: 4,  # High chance of using Dark
    drain: 3,  # Medium chance
    fire: 4,  # Lower chance
    quake: 5,  # Highest likelihood
    ultima:3,
    curaga:0,
    revive:0,
}
bosses["dragon"].spell_weights = {
    firaga: 5
}

bosses["demon"].spell_weights = {
    pandemonium: 5
}