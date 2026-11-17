from threading import Thread

from Colors import bcolors
from audio import play_sound
from dungeon import (battle_with_checkpoint, clear, first_room_treasure,
                     gen_allies, gen_enemies, prepare_enemies, prompt,
                     second_room_treasure)
from prompts import prompt_yes_no
from save_game import SAVE_FILE, load_game


def main():

    thread = Thread(target=play_sound, daemon=True)
    thread.start()

    saved_game = None
    if SAVE_FILE.exists() and prompt_yes_no("Load your saved game? [Yes] [No] "):
        saved_game = load_game()

    if saved_game:
        next_room, main_team, encounters = saved_game
    else:
        allies_team = gen_allies()
        encounters = list(gen_enemies())
        selected_hero = prompt()
        main_team = [selected_hero] + allies_team
        next_room = 1

    # Display the team roster with access to object attributes
    print(bcolors.BOLD + bcolors.PURPLE + "\nYour team roster: " + bcolors.ENDC)
    for ally in main_team:
        print(f"\t- {ally.name}")

    if next_room == 1:
        clear()
        if not battle_with_checkpoint(1, main_team, encounters):
            return
        first_room_treasure(main_team)

    if next_room <= 2:
        prepare_enemies(encounters[1])

        if not battle_with_checkpoint(2, main_team, encounters):
            return

        second_room_treasure(main_team)

    clear()
    print(
        f"{bcolors.RED}{bcolors.BOLD}Prepare yourself, for this battle will test your strength, strategy, and resolve. "
        f"\nThe fate of your party rests in your hands...{bcolors.ENDC}")
    prepare_enemies(encounters[2])
    battle_with_checkpoint(3, main_team, encounters)


if "__main__" == __name__:
    main()
