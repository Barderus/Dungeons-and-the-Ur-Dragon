from Colors import bcolors


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


def prompt_yes_no(prompt_text):
    while True:
        choice = input(prompt_text).strip().lower()
        if choice in {"yes", "y"}:
            return True
        if choice in {"no", "n"}:
            return False
        print(f"{bcolors.YELLOW}{bcolors.BOLD}Please enter Yes/No or Y/N.{bcolors.ENDC}")
