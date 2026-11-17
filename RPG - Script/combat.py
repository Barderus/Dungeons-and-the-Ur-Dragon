import random
from collections import deque

from Colors import bcolors
from prompts import choose_numbered_option, display_numbered_targets


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
        living_enemies = [enemy for enemy in enemy_team if enemy.hp > 0]
        ally.cast_magic(living_enemies, chosen_spell)
        return

    if chosen_spell.effect_type == "revival":
        ally_targets = [obj for obj in ally_team if obj.hp <= 0]
    else:
        ally_targets = [obj for obj in ally_team if obj.hp > 0]

    target_groups = {
        "1": ally_targets if chosen_spell.effect_type != "damage" else [],
        "2": [obj for obj in enemy_team if obj.hp > 0] if chosen_spell.effect_type == "damage" else [],
    }

    if not any(target_groups.values()):
        print(f"\t{bcolors.YELLOW}{bcolors.BOLD}There are no valid targets for {chosen_spell.name}.{bcolors.ENDC}")
        return "c"

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

    if chosen_item.name == "Phoenix Down":
        all_targets = [obj for obj in ally_team if obj.hp <= 0]
    elif chosen_item.effect == "debuff":
        all_targets = [obj for obj in enemy_team if obj.hp > 0]
    else:
        all_targets = [obj for obj in ally_team if obj.hp > 0]

    if not all_targets:
        print(f"\t{bcolors.YELLOW}{bcolors.BOLD}There are no valid targets for {chosen_item.name}.{bcolors.ENDC}")
        return "c"

    display_numbered_targets(all_targets, "Choose a target:")
    target = choose_numbered_option(
        bcolors.RED + bcolors.BOLD + "    TARGET NUMBER: " + bcolors.ENDC,
        all_targets,
    )
    if target == "c":
        return "c"

    quantity_before = chosen_item.quantity
    chosen_item.use_item(target)
    if chosen_item.quantity == quantity_before:
        print(f"\t{bcolors.RED}{bcolors.BOLD}The item could not be used!{bcolors.ENDC}")
        return "c"

    if chosen_item.quantity == 0:
        ally.inventory.remove_item(chosen_item.name, 0)
    print(f"\t{ally.name} uses {chosen_item.name} on {target.name}!")


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
    spells = [spell for spell in enemy.spell_weights
              if spell in enemy.spells and spell.mp <= enemy.mp and spell.effect_type == "damage"]
    if not spells:
        return None
    weights = [enemy.spell_weights[spell] for spell in spells]
    return random.choices(spells, weights=weights, k=1)[0]


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
            if aoe_spell and enemy.mp >= aoe_spell.mp:
                enemy.cast_magic(alive_allies, aoe_spell)
                return  # After casting AoE, return to prevent further attacks

        # Revive, Heal or Attack Logic (after AoE check)
        for char in enemies_team:
            if char.hp <= 0:
                revive_spell = get_spell_by_name(enemy, "Revive")
                if revive_spell and enemy.mp >= revive_spell.mp:
                    enemy.cast_magic(char, revive_spell)
                    return
                else:
                    chosen_item = next((i for i in enemy.inventory.items.values() if i.name.lower() == "phoenix down"), None)
                    if chosen_item and chosen_item.quantity > 0:
                        chosen_item.use_item(char)
                        return

            elif char.hp < (char.maxhp // 2):
                curaga_spell = get_spell_by_name(enemy, "Curaga")
                if curaga_spell and enemy.mp >= curaga_spell.mp:
                    enemy.cast_magic(char, curaga_spell)
                    return
                else:
                    chosen_item = next((i for i in enemy.inventory.items.values() if i.name.lower() == "hi-potion"), None)
                    if chosen_item and chosen_item.quantity > 0:
                        chosen_item.use_item(char)
                        return

    # Check if enemy has spells and prioritize magic
    if enemy.spells:
        # Determine whether to cast magic or use physical attack
        magic_priority = enemy.mgk_atk / (enemy.mgk_atk + enemy.atk)  # Calculate a magic priority ratio
        if random.random() < magic_priority:  # Cast magic based on the priority ratio
            spell = select_enemy_spell(enemy)
            if spell:
                if spell.name in {"Meteor", "Quake", "Ultima", "Flare", "Breath of Fire", "Pandemonium"}:
                    enemy.cast_magic(alive_allies, spell)
                else:
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


def battle(ally_team, enemies_team):
    turn = 1
    char_q = deque()
    char_list = ally_team + enemies_team
    char_list = sorted(char_list, key=lambda chars: chars.speed if chars.hp > 0 else 0, reverse=True)
    for char in char_list:
        char_q.append(char)

    print()

    while char_q:
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
            return True
        if all(allies.hp <= 0 for allies in ally_team):
            print(bcolors.BOLD + bcolors.RED + "You failed. You and your allies perished in the hands of enemy." + bcolors.ENDC)
            return False

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
                return False
