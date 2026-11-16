import random
import time
from pygame import mixer
from threading import Thread
from collections import deque

from Colors import bcolors
from characters import all_items, allies, avatars, bosses, enemies


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

def display_numbered_targets(targets, header):
    print(f"\n\t{header}")
    for index, target in enumerate(targets, start=1):
        print(f"\t{index}. {target.name}")
    print()


def choose_numbered_option(prompt_text, options, allow_cancel=True):
    while True:
        choice = input(prompt_text).strip().lower()
        if choice == "c" and allow_cancel:
            return "c"
        if choice.isdigit():
            option_index = int(choice) - 1
            if 0 <= option_index < len(options):
                return options[option_index]
        print(f"{bcolors.YELLOW}{bcolors.BOLD}Invalid choice. Please try again.{bcolors.ENDC}")


def treasure_table(main_team):
    items_per_ally = 3
    chest_contents = {}

    for ally in main_team:
        rewards = random.sample(all_items, items_per_ally)
        chest_contents[ally.name] = rewards

    print(f"\n{bcolors.BOLD}{bcolors.YELLOW}The chest contains:{bcolors.ENDC}")
    for ally_name, rewards in chest_contents.items():
        reward_names = ", ".join(reward.name for reward in rewards)
        print(f"\t{ally_name}: {reward_names}")

    for ally in main_team:
        rewards = chest_contents[ally.name]
        for reward in rewards:
            ally.inventory.add_item(reward)  # Add item to the inventory
        print(f"{ally.name} received: {[reward.name for reward in rewards]}")


def prompt_yes_no(prompt_text):
    while True:
        choice = input(prompt_text).strip().lower()
        if choice in {"yes", "y"}:
            return True
        if choice in {"no", "n"}:
            return False
        print(f"{bcolors.YELLOW}{bcolors.BOLD}Please enter Yes/No or Y/N.{bcolors.ENDC}")


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
        living_enemies = [enemy for enemy in enemy_team if enemy.hp > 0]
        if not living_enemies:
            return

        display_numbered_targets(living_enemies, "Choose a target:")
        target = choose_numbered_option(
            bcolors.RED + bcolors.BOLD + "    TARGET NUMBER: " + bcolors.ENDC,
            living_enemies,
        )
        if target == "c":
            return "c"

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
    for index, spell in enumerate(ally.spells, start=1):
        print(f"{index}. {spell.name} | MP cost: {spell.mp} \nDescription: {spell.descri}\n")

    # Get user input for choosing a spell
    chosen_spell = choose_numbered_option(
        f"\n\t{bcolors.BLUE}{bcolors.BOLD}SPELL NUMBER:{bcolors.ENDC} (c to cancel): ",
        ally.spells,
    )
    if chosen_spell == "c":
        return "c"

    if chosen_spell.name == "Meteor" or chosen_spell.name == "Quake" or chosen_spell.name == "Ultima" or chosen_spell.name == "Flare":
        ally.cast_magic(enemy_team, chosen_spell)
        return

    target_groups = {
        "1": [obj for obj in ally_team if obj.hp > 0 or chosen_spell.effect_type == "revival"],
        "2": [obj for obj in enemy_team if obj.hp > 0],
    }

    while True:
        target_group_choice = input(
            f"\n\t{bcolors.BLUE}{bcolors.BOLD}TARGET GROUP:{bcolors.ENDC}\n"
            "\t1. Allies\n"
            "\t2. Enemies\n"
            "\tChoose Group (c to cancel): "
        ).strip().lower()

        if target_group_choice == "c":
            return "c"

        valid_targets = target_groups.get(target_group_choice)
        if valid_targets:
            break
        print(f"\t\t{bcolors.YELLOW}{bcolors.BOLD}Invalid target group. Please try again.{bcolors.ENDC}")

    display_numbered_targets(valid_targets, "Choose a target:")
    target = choose_numbered_option(
        bcolors.RED + bcolors.BOLD + "    TARGET NUMBER: " + bcolors.ENDC,
        valid_targets,
    )
    if target == "c":
        return "c"

    ally.cast_magic(target, chosen_spell)


def items(ally, enemy_team, ally_team):
    print(f"\n{bcolors.BOLD}{bcolors.BLUE}INVENTORY:{bcolors.ENDC}")

    # Display available items with their descriptions
    inventory_items = list(ally.inventory.items.values())
    for index, item in enumerate(inventory_items, start=1):
        print(f"{index}. {item.name}: {item.description} x{item.quantity} ")

    chosen_item = choose_numbered_option(
        f"\n\t{bcolors.BLUE}{bcolors.BOLD}ITEM NUMBER{bcolors.ENDC} (c to cancel): ",
        inventory_items,
    )
    if chosen_item == "c":
        return "c"

    # Create a list of valid targets (both allies and enemies)
    all_targets = [obj for obj in enemy_team if obj.hp > 0] + [obj for obj in ally_team]

    display_numbered_targets(all_targets, "Choose a target:")
    target = choose_numbered_option(
        bcolors.RED + bcolors.BOLD + "    TARGET NUMBER: " + bcolors.ENDC,
        all_targets,
    )
    if target == "c":
        return "c"

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


def get_spell_by_name(caster, spell_name):
    return next((spell for spell in caster.spells if spell.name == spell_name), None)


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
        boss_aoe_spell_name = {
            "Lich": "Meteor",
            "Ur-Dragon": "Breath of Fire",
            "Orcus": "Pandemonium",
        }.get(enemy.name)

        if any(ally.hp == ally.maxhp for ally in ally_team):  # Check if any ally is at full HP
            aoe_spell = get_spell_by_name(enemy, boss_aoe_spell_name) if boss_aoe_spell_name else None
            if aoe_spell:
                enemy.cast_magic(ally_team, aoe_spell)
                return  # After casting AoE, return to prevent further attacks

        # Revive, Heal or Attack Logic (after AoE check)
        for char in enemies_team:
            if char.hp <= 0:
                revive_spell = get_spell_by_name(enemy, "Revive")
                if revive_spell:
                    enemy.cast_magic(char, revive_spell)
                else:
                    chosen_item = next((i for i in enemy.inventory.items.values() if i.name.lower() == "phoenix down"), None)
                    if chosen_item:
                        chosen_item.use_item(char)

            elif char.hp < (char.maxhp // 2):
                curaga_spell = get_spell_by_name(enemy, "Curaga")
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
        low_mgk_ally = sorted_by_mgk_def[0]
        high_atk_ally = sorted_by_atk[0]

        ally_list = [low_mgk_ally] if low_mgk_ally == high_atk_ally else [low_mgk_ally, high_atk_ally]
        target_ally = random.choice(ally_list)

    enemy.attacks(target_ally)

    if target_ally.hp == 0:
        print(f"{target_ally.name} is " + bcolors.BOLD + bcolors.RED + "dead" + bcolors.ENDC)



def prompt():
    """
        This function displays a welcoming message and prompts the user for their characters.
    """
    print(fr"""
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

    avatar_options = list(avatars.values())

    # Display the names with a dash and style, followed by the hero's description.
    for index, avatar_obj in enumerate(avatar_options, start=1):
        print(f"{bcolors.BOLD}\t\t{index}. {avatar_obj.name}{bcolors.ENDC}")
        print(f"\t\t{avatar_obj.descri}\n")

    selected_hero = choose_numbered_option("Enter the hero's number: ", avatar_options, allow_cancel=False)
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

    thread = Thread(target=play_sound, daemon=True)
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
    if prompt_yes_no("Do you wish to open the chest? [Yes] [No]"):
        treasure_table(main_team)

    for char in enemies_fight2:
        char.hp=char.maxhp
        char.mp=char.maxmp

    battle(main_team, enemies_fight2)

    print("You stumble upon an stylish, golden-covered treasure chest hidden in the corner of the room. What secrets, or dangers, might lie within?")
    if prompt_yes_no("Do you wish to open the chest? [Yes] [No]"):
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
