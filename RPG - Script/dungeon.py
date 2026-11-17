import random
import time

from Colors import bcolors
from characters import all_items, allies, avatars, bosses, enemies
from combat import battle
from prompts import choose_numbered_option, prompt_yes_no
from save_game import load_game, save_game


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


def first_room_treasure(main_team):
    print("You stumble upon an ancient, dust-covered treasure chest hidden in the corner of the room. What secrets, or dangers, might lie within?")
    if prompt_yes_no("Do you wish to open the chest? [Yes] [No]"):
        treasure_table(main_team)


def second_room_treasure(main_team):
    print("You stumble upon an stylish, golden-covered treasure chest hidden in the corner of the room. What secrets, or dangers might lie within?")
    if prompt_yes_no("Do you wish to open the chest? [Yes] [No]"):
        rand_num = random.randint(1, 2)
        if rand_num == 1:
            treasure_table(main_team)
        else:
            for ally in main_team[1:]:
                ally.hp = ally.maxhp
                ally.mgk_def += 10


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


def prepare_enemies(enemy_team):
    for char in enemy_team:
        char.hp = char.maxhp
        char.mp = char.maxmp


def battle_with_checkpoint(room, party, encounters):
    if not save_game(room, party, encounters):
        return False

    while True:
        if battle(party, encounters[room - 1]):
            return True

        if not prompt_yes_no("Load the checkpoint and retry this fight? [Yes] [No] "):
            return False

        saved_game = load_game()
        if saved_game is None or saved_game[0] != room:
            print("The checkpoint could not be loaded.")
            return False

        party[:] = saved_game[1]
        encounters[:] = saved_game[2]
