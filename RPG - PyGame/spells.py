from magic import Magic

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
light_bolt = Magic("Light Bolt", "blue", 30, 45, 0, "damage",
                   "A light bolt pursues the enemy followed by a big explosion.")


# Bosses spells
firaga = Magic("Breath of Fire", "black", 50, 150, 0, "damage",
             "Ur-Dragon breathes a wall of fire towards the enemies")
pandemonium = Magic("Pandemonium", "black", 200, 300, 0, "damage",
               "Orcus bring hell upon all his enemies. Cursing every single enemy.")