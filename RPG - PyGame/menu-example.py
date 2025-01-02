# Source: https://coderslegacy.com/python/create-menu-screens-in-pygame-tutorial/

from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
from characters import *
pygame.init()
surface = pygame.display.set_mode((600, 400))

def start_game():
    pass

def choose_avatar_menu():
    main_menu._open(choose_avatar)

def set_avatar(avatar):
    print(avatar)

main_menu = pygame_menu.Menu("Dungeons and Ur-Dragon", 600, 400, theme = themes.THEME_SOLARIZED)
main_menu.add.text_input("Name: ", default="username", maxchar=15)
main_menu.add.button("Play", start_game)
main_menu.add.button("Choose Avatar", choose_avatar_menu)
main_menu.add.button("Quit", pygame_menu.events.EXIT)

choose_avatar = pygame_menu.Menu("Select Avatar", 600, 400, theme = themes.THEME_BLUE)
choose_avatar.add.selector("Avatars:", [knight, warrior, barbarian, blue_witch, fire_wizard, mage_guardian], onchange=set_avatar)



