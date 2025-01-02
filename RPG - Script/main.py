import random
import time
from pygame import mixer
from threading import Thread
from collections import deque

from Colors import bcolors
from characters import *


def play_sound():
    # List of songs
    songs = [
        "../Music/AudioCoffee Band - Cinematic Galactic.mp3",
        "../Music/ArcSound - Dark Horror Nightmare.mp3",
        "../Music/BlackTrendMusic - Epic.mp3",
        "../Music/Lowtone Music - Cinematic Soundtrack.mp3",
        "../Music/Lowtone Music - Dark Trailer.mp3",
        "../Music/Lowtone Music - Epic Action.mp3",
        "../Music/Lowtone Music - Fantasy Teaser.mp3",
        "../Music/Lowtone Music - Get Up & Fight.mp3",
        "../Music/Lowtone Music - This is War - Cinematic Epic.mp3",
        "../Music/UNIVERSFIELD - Gloomy Depths.mp3"
    ]

    mixer.init()
    mixer.music.set_volume(0.8)

    def queue_songs(song_list):
        # Shuffle and queue all songs
        random.shuffle(song_list)
        first_song = song_list.pop(0)
        mixer.music.load(first_song)
        for song in song_list:
            mixer.music.queue(song)
        mixer.music.play()

    queue_songs(songs.copy())  # Queue initial songs

    # Loop to check if queue is empty
    while True:
        if not mixer.music.get_busy():
            #print("Queue empty, reloading songs...")
            queue_songs(songs.copy())  # Reload the songs
        time.sleep(5)

def target_list(enemy_team):
    print("\n\tChoose a target: \n"
          f"\t- {enemy_team[0].name}\n "
          f"\t- {enemy_team[1].name}\n"
          f"\t- {enemy_team[2].name}\n "
          f"\t- {enemy_team[3].name}\n ")


def treasure_table(main_team):

    items_per_ally = 3
    for ally in main_team:
        rewards = random.sample(all_items, items_per_ally)
        for reward in rewards:
            print(reward)
            ally.inventory.add_item(reward)  # Add item to the inventory
        print(f"{ally.name} received: {[reward.name for reward in rewards]}")


def battle_screen(ally_team, enemy_team):
    """ Display each character's health points and their names """
    # Display ally team
    for person in ally_team:
        person.get_stats()

    print()
    for bbeg in enemy_team:
        bbeg.get_stats()
    print()


def attack(ally, enemy_team):
    while True:
        target_list(enemy_team)
        char_name = input(bcolors.RED + bcolors.BOLD + "    TARGET: " + bcolors.ENDC)

        # Find the target in the enemy team
        target = None

        if char_name == "c":
            return "c"

        for enemy in enemy_team:
            if enemy.name.lower() == char_name.lower():  # Case-insensitive comparison
                target = enemy
                break


        if target is None:
            print(f"{bcolors.YELLOW}{bcolors.BOLD}Invalid target name. Please try again.{bcolors.ENDC}")
            continue

        if target.hp <= 0:
            print(f"{bcolors.YELLOW}{bcolors.BOLD}{target.name} is already dead. Choose another target.{bcolors.ENDC}")
        else:
            ally.attacks(target)  # Attack the selected target
            if target.hp == 0:
                print(f"{target.name} is {bcolors.RED}{bcolors.BOLD}dead{bcolors.ENDC}.")
            break


def cast_spell(ally, enemy_team, ally_team):
    # Check if the ally has any spells
    if not ally.spells:
        print(f"\n\t{bcolors.YELLOW}{bcolors.BOLD}{ally.name} is not adept with the arts of Magik.{bcolors.ENDC}\n")
        return "c"

    # Display available spells
    print(f"\n{bcolors.BOLD}{bcolors.BLUE} SPELLS: {bcolors.ENDC}")
    for spell in ally.spells:
        print(f"Spell Name: {spell.name} | MP cost: {spell.mp} \nDescription: {spell.descri}\n")

    # Get user input for choosing a spell
    choose_spell = input(f"\n\t{bcolors.BLUE}{bcolors.BOLD}SPELL:{bcolors.ENDC} (c to cancel): ").strip().lower()
    if choose_spell == "c":
        return "c"

    # Find the chosen spell
    chosen_spell = next((spell for spell in ally.spells if spell.name.lower() == choose_spell), None)
    if not chosen_spell:
        print("Spell not found.")
        return "c"

    if chosen_spell.name == "Meteor" or chosen_spell.name == "Quake" or chosen_spell.name == "Ultima" or chosen_spell.name == "Flare":
        ally.cast_magic(enemy_team, chosen_spell)
        return

    # Create a list of valid targets (enemies and allies)
    all_targets = [obj for obj in enemy_team if obj.hp > 0] + [obj for obj in ally_team]

    # Target selection loop
    while True:
        char_name = input(bcolors.RED + bcolors.BOLD + "    TARGET: " + bcolors.ENDC).strip().lower()

        if char_name == "c":
            return "c"
        # Find target by name
        target = next((person for person in all_targets if person.name.lower() == char_name), None)

        if target:
            break
        else:
            print(f"\t\t{bcolors.YELLOW}{bcolors.BOLD}Invalid target. Please try again.{bcolors.ENDC}")

    ally.cast_magic(target, chosen_spell)


def items(ally, enemy_team, ally_team):
    print(f"\n{bcolors.BOLD}{bcolors.BLUE}INVENTORY:{bcolors.ENDC}")

    # Display available items with their descriptions
    for item in ally.inventory.items.values():
        print(f"- {item.name}: {item.description} x{item.quantity} ")

    choose_item = input(f"\n\t{bcolors.BLUE}{bcolors.BOLD}ITEM{bcolors.ENDC} (c to cancel): ").strip().lower()

    if choose_item == "c":
        return "c"

    # Find the chosen item
    chosen_item = next((item for item in ally.inventory.items.values() if item.name.lower() == choose_item), None)
    if chosen_item is None:
        print(f"\t{bcolors.YELLOW}{bcolors.BOLD}You don't have this item. Try again.{bcolors.ENDC}")
        return "c"

    # Create a list of valid targets (both allies and enemies)
    all_targets = [obj for obj in enemy_team if obj.hp > 0] + [obj for obj in ally_team]

    # Target selection loop
    while True:
        target_name = input(bcolors.RED + bcolors.BOLD + "    TARGET: " + bcolors.ENDC).strip().lower()
        if target_name == "c":
            return "c"

        # Find target by name
        target = next((person for person in all_targets if person.name.lower() == target_name), None)

        if target:
            break
        else:
            print("\tThat's not a valid target. Please try again.")

    chosen_item.use_item(target)
    if chosen_item.quantity == 0:
        ally.inventory.remove_item(chosen_item.name, chosen_item.quantity)  # Remove item from inventory if quantity is 0
        print(f"\t{ally.name} uses {chosen_item.name} on {target.name}!")
    else:
        print(f"\t{bcolors.RED}{bcolors.BOLD}The item could not be used!{bcolors.ENDC}")


def actions(ally, enemy_team, ally_team):
    while True:
        action = input(f"\n{ally.name}'s action:"
                       f"{bcolors.BOLD}{bcolors.BLUE}\nACTIONS:{bcolors.ENDC}"
                       "\n1. Attack"
                       "\n2. Magic"
                       "\n3. Items"
                       "\nChoose Action: ").strip()
        if action == "1":
            result = attack(ally, enemy_team)
            if result == "c":
                continue
            break
        elif action == "2":
            result = cast_spell(ally, enemy_team, ally_team)
            if result == "c":
                continue
            break
        elif action == "3":
            item = items(ally, enemy_team, ally_team)
            if item == "c":
                continue
            break
        else:
            print(f"\t\t{bcolors.YELLOW}{bcolors.BOLD}Invalid action. Please choose 1, 2, or 3.{bcolors.ENDC}")


def select_enemy_spell(enemy):
    spells = list(enemy.spell_weights.keys())
    weights = list(enemy.spell_weights.values())
    chosen_spell = random.choices(spells, weights=weights, k=1)[0]
    return chosen_spell


def enemy_attack(ally_team, enemy, enemies_team):
    # Select only alive allies
    alive_allies = [ally for ally in ally_team if ally.hp > 0]

    if not alive_allies:
        print(f"All allies are down. {enemy.name} has no one to attack.")
        return

    # Sort allies by attributes
    sorted_by_hp = sorted(alive_allies, key=lambda obj: obj.hp)
    sorted_by_mgk_def = sorted(alive_allies, key=lambda obj: obj.mgk_def)
    sorted_by_atk = sorted(alive_allies, key=lambda obj: obj.atk, reverse=True)

    # Ally with lowest HP
    low_hp_ally = sorted_by_hp[0]
    target_ally = low_hp_ally

    # Boss logic for AoE attack if any ally is at full HP
    if enemy.boss:
        if any(ally.hp == ally.maxhp for ally in ally_team):  # Check if any ally is at full HP
            if enemy.name == "Lich":
                meteor_spell = next((spell for spell in enemy.spells if spell.name == "Meteor"), None)
                if meteor_spell:
                    enemy.cast_magic(ally_team, meteor_spell)
                    return  # After casting AoE, return to prevent further attacks
            elif enemy.name == "Dragon":
                firaga_spell = next((spell for spell in enemy.spells if spell.name == "Breath of Fire"), None)
                if firaga_spell:
                    enemy.cast_magic(ally_team, firaga_spell)
                    return  # After casting AoE, return to prevent further attacks
            elif enemy.name == "Orcus":
                hell_spell = next((spell for spell in enemy.spells if spell.name == "Pandemonium"), None)
                if hell_spell:
                    enemy.cast_magic(ally_team, hell_spell)
                    return  # After casting AoE, return to prevent further attacks

        # Revive, Heal or Attack Logic (after AoE check)
        for char in enemies_team:
            if char.hp <= 0:
                revive_spell = next((spell for spell in enemy.spells if spell.name == "Revive"), None)
                if revive_spell:
                    enemy.cast_magic(char, revive_spell)
                else:
                    chosen_item = next((i for i in enemy.inventory.items.values() if i.name.lower() == "phoenix down"), None)
                    if chosen_item:
                        chosen_item.use_item(char)

            elif char.hp < (char.maxhp // 2):
                curaga_spell = next((spell for spell in enemy.spells if spell.name == "Curaga"), None)
                if curaga_spell:
                    enemy.cast_magic(char, curaga_spell)
                else:
                    chosen_item = next((i for i in enemy.inventory.items.values() if i.name.lower() == "hi-potion"), None)
                    if chosen_item:
                        chosen_item.use_item(char)

    # Check if enemy has spells and prioritize magic
    if enemy.spells:
        # Determine whether to cast magic or use physical attack
        magic_priority = enemy.mgk_atk / (enemy.mgk_atk + enemy.atk)  # Calculate a magic priority ratio
        if random.random() < magic_priority:  # Cast magic based on the priority ratio
            spell = select_enemy_spell(enemy)
            if spell:
                enemy.cast_magic(low_hp_ally, spell)
                return

    # Fallback to physical attack if no spells or insufficient MP
    if low_hp_ally.hp < (low_hp_ally.maxhp // 2) and low_hp_ally.mgk_def < low_hp_ally.df:
        target_ally = low_hp_ally
    else:
        # Select from weaker defense and stronger attack allies
        random_low_mgk = random.choice(sorted_by_mgk_def)
        random_high_atk = random.choice(sorted_by_atk)

        ally_list = [random_low_mgk] if random_low_mgk == random_high_atk else [random_low_mgk, random_high_atk]
        target_ally = random.choice(ally_list)

    enemy.attacks(target_ally)

    if target_ally.hp == 0:
        print(f"{target_ally.name} is " + bcolors.BOLD + bcolors.RED + "dead" + bcolors.ENDC)



def prompt():
    """
        This function displays a welcoming message and prompts the user for their characters.
    """
    print(f"""
                                {bcolors.YELLOW
    }{bcolors.BOLD}Dungeons and the Ur-Dragon{bcolors.ENDC}
                                ~~~~~~~~~~~~~~~~~~~~~~~~~~

                               __====-_  _-====__
                          _--^^^#####//      \\#####^^^--_
                       _-^##########// (    ) \\##########^-_
                      -############//  |\^^/|  \\############-
                    _/############//   (@::@)   \\############\_
                   /#############((     \\//     ))#############\
                   
                  -###############\\    (oo)    //###############-
                 -#################\\  / ** \  //#################-
                -###################\\/      \//###################-
               _#/|##########/\######(   /\   )######/\##########|\#_
               |/ |#/\#/\#/\/  \#/\#\ \ |  | / /\#/\#/\  \/\#/\#| \|
               |/   |/   |/      |/     |||     |/      |/   |/  \|
                \_____________________|||_____________________/
                  |_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|

    """)
    print(
        f"\tAre you ready to embark on an {bcolors.BOLD}epic adventure{bcolors.ENDC}, defeat the forces of {bcolors.RED}evil{bcolors.ENDC},")
    print(f"\tand become a {bcolors.GREEN}legendary hero{bcolors.ENDC}?\n\n{bcolors.ENDC}")
    input(f"{bcolors.BLUE}\t\t\t\tPress any key to begin...\n > {bcolors.ENDC}")
    print(f"{bcolors.RED}{bcolors.BOLD}\t\t\t\t\t\tLet the quest begin!{bcolors.ENDC}")
    print(f"{bcolors.GREEN}\n\t\tChoose your hero: {bcolors.ENDC}")

    # List of all the character names to be chosen from
    avatar_names = [avatar.name for avatar in avatars.values()]

    # Display the names with a dash and style, followed by the hero's description.
    for name in avatar_names:
        print(f"{bcolors.BOLD}\t\t- {name}{bcolors.ENDC}")
        avatar_obj = next(avatar for avatar in avatars.values() if avatar.name == name)
        print(f"\t\t{avatar_obj.descri}\n")

    # Control loop to check if the name entered by the user is valid
    while True:
        hero_choice = input("Enter the hero's name: ").capitalize()
        if hero_choice in avatar_names:
            name_to_avatar = {avatar.name: avatar for avatar in avatars.values()}
            selected_hero = name_to_avatar[hero_choice]  # Now this is the object
            break
        else:
            print(f"{bcolors.BOLD}{bcolors.YELLOW}{hero_choice}{bcolors.ENDC} is not a playable character.\n")

    # Returns the name of the hero
    return selected_hero


def gen_enemies():
    """
        This function generates a random list of enemies for the player to fight
    """
    # Enemies for room1
    enemy_list = list(enemies.values())

    # Enemies for room2
    enemy_list2 = list(enemies.values())

    # enemies for room3
    boss_list = list(bosses.values())

    enemy_fight_set = set()
    enemy_fight_set2 = set()
    boss_fight_set = set()

    #  Select the enemies
    while len(enemy_fight_set) < 4:
        enemy_fight_set.add(random.choice(enemy_list))

    while len(enemy_fight_set2) < 4:
        enemy_fight_set2.add(random.choice(enemy_list))

    # Select the enemies for the boss fight
    for x in range(1, 4):
        boss_fight_set.add(random.choice(enemy_list))
    boss_fight_set.add(random.choice(boss_list))

    return list(enemy_fight_set), list(enemy_fight_set2), list(boss_fight_set)


def gen_allies():
    """
        This function generates a random list of allies to join the player to fight
    """
    allies_list = list(allies.values())

    allies_team = set()
    while len(allies_team) < 3:
        allies_team.add(random.choice(allies_list))
    return list(allies_team)


def clear():
    """
        This function clears the screen
            os.system('cls' if os.name == 'nt' else 'clear') << Not working
    """
    time.sleep(2)
    print("\n" * 100)


def battle(ally_team, enemies_team):
    running = True
    turn = 1
    char_q = deque()
    char_list = ally_team + enemies_team
    char_list = sorted(char_list, key=lambda chars: chars.speed if chars.hp > 0 else 0, reverse=True)
    for char in char_list:
        char_q.append(char)

    print()
    while running and char_q:
        print(
            f"\n############################## {bcolors.BOLD}{bcolors.GREEN}TURN {turn}{bcolors.ENDC} ##############################")
        battle_screen(ally_team, enemies_team)
        current_char = char_q.popleft()

        if current_char.hp > 0:
            if current_char in ally_team:
                actions(current_char, enemies_team, ally_team)
            elif current_char in enemies_team:
                enemy_attack(ally_team, current_char, enemies_team)
        turn += 1

        if all(enemy.hp <= 0 for enemy in enemies_team):
            print(f"\n{bcolors.GREEN}{bcolors.BOLD} All enemies are defeated!{bcolors.ENDC}")
            running = False
            break
        if all(allies.hp <= 0 for allies in ally_team):
            print(
                + bcolors.BOLD + bcolors.RED + "You failed. You and your allies perished in the hands of enemy." + bcolors.ENDC)
            running = False
            break

        if not char_q:
            #print("Refilling the queue...")
            char_list = [char for char in ally_team + enemies_team if char.hp > 0]
            if char_list:  # Refill the queue if there are still characters alive
                char_list = sorted(char_list, key=lambda chars: chars.speed if chars.hp > 0 else 0, reverse=True)
                for char in char_list:
                    char_q.append(char)
                    #print(char.name)
            else:
                print("Battle is over!")
                running = False


def main():

    thread = Thread(target=play_sound)
    thread.start()

    # Generate allies, enemies
    allies_team = gen_allies()
    enemies_fight, enemies_fight2, boss_fight = gen_enemies()

    # Prompt the user for their hero
    selected_hero = prompt()

    # Create the main team
    main_team = [selected_hero] + allies_team

    # Display the team roster with access to object attributes
    print(bcolors.BOLD + bcolors.PURPLE + "\nYour team roster: " + bcolors.ENDC)
    for ally in main_team:
        print(f"\t- {ally.name}")

    clear()
    battle(main_team, enemies_fight)
    print("You stumble upon an ancient, dust-covered treasure chest hidden in the corner of the room. What secrets, or dangers, might lie within?")
    user_choice = input("Do you wish to open the chest? [Yes] [No]").lower()

    if user_choice == "yes":
        treasure_table(main_team)

    for char in enemies_fight2:
        char.hp=char.maxhp
        char.mp=char.maxmp

    battle(main_team, enemies_fight2)

    print("You stumble upon an stylish, golden-covered treasure chest hidden in the corner of the room. What secrets, or dangers, might lie within?")
    user_choice = input("Do you wish to open the chest? [Yes] [No]").lower()

    if user_choice == "yes":
        rand_num = random.randint(1, 2)
        if rand_num == 1:
            treasure_table(main_team)
        elif rand_num == 2:
            for ally in allies_team:
                ally.hp = ally.maxhp
                ally.mgk_def += 10
    clear()
    print(
        f"{bcolors.RED}{bcolors.BOLD}Prepare yourself, for this battle will test your strength, strategy, and resolve. "
        f"\nThe fate of your party rests in your hands...{bcolors.ENDC}")
    for char in boss_fight:
        char.hp=char.maxhp
        char.mp=char.maxmp
    battle(main_team, boss_fight)


if "__main__" == __name__:
    main()
