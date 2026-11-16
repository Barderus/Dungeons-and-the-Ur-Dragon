import pygame
import pygame_menu
from characters import avatar_list
from colors import *

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640

class GameMenu:
    def __init__(self, start_game_callback):
        self.selected_characters = []
        self.start_game_callback = start_game_callback
        self.menu_theme = pygame_menu.themes.THEME_DARK.copy()
        self.menu_theme.title_font = pygame_menu.font.FONT_8BIT
        self.menu_theme.widget_font = pygame_menu.font.FONT_8BIT
        self.menu_theme.background_color = (0, 0, 0, 180)
        self.menu_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE

        # Preload specific characters
        self.preloaded_characters = []
        for character in avatar_list:
            if character.name in ["Aerith", "Gandalf", "Gimli", "Snape"]:
                self.preloaded_characters.append(character)
                if len(self.selected_characters) < 2:
                    self.selected_characters.append(character)

        # Create menus
        self.character_menu = self.create_character_menu()
        self.settings_menu = self.create_settings_menu()
        self.main_menu = self.create_main_menu()

    def create_main_menu(self):
        menu = pygame_menu.Menu(
            'Dungeons and the Ur-Dragon',
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            theme=self.menu_theme
        )

        menu.add.button('Start Game', self.start_game)
        menu.add.button('Character Selection', self.character_menu)
        menu.add.button('Settings', self.settings_menu)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        return menu

    def create_character_menu(self):
        menu = pygame_menu.Menu(
            'Character Selection',
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            theme=self.menu_theme
        )

        # Add character selection widgets only for preloaded characters
        for character in self.preloaded_characters:
            menu.add.toggle_switch(
                character.name,
                character in self.selected_characters,
                onchange=lambda value, char=character: self.toggle_character(char, value)
            )

        menu.add.button('Back', pygame_menu.events.BACK)
        return menu

    def create_settings_menu(self):
        menu = pygame_menu.Menu(
            'Settings',
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            theme=self.menu_theme
        )

        menu.add.range_slider(
            'Music Volume',
            50,
            (0, 100),
            1,
            onchange=self.set_music_volume
        )
        menu.add.range_slider(
            'Sound Volume',
            50,
            (0, 100),
            1,
            onchange=self.set_sound_volume
        )
        menu.add.button('Back', pygame_menu.events.BACK)

        return menu

    def toggle_character(self, character, selected):
        if selected:
            if len(self.selected_characters) < 3:
                self.selected_characters.append(character)
            else:
                return False
        else:
            if character in self.selected_characters:
                self.selected_characters.remove(character)
        return True

    def start_game(self):
        if len(self.selected_characters) >= 2:
            return self.start_game_callback(self.selected_characters)
        else:
            # Show error message
            self.main_menu.add.label('Please select at least 2 characters!', font_color=bcolors.RED)

    def set_music_volume(self, value):
        # Implement music volume control
        pass

    def set_sound_volume(self, value):
        # Implement sound volume control
        pass

    def update(self, events):
        self.main_menu.update(events)

    def draw(self, surface):
        self.main_menu.draw(surface)
