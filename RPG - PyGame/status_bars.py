import pygame
from colors import *

class StatusBar:
    def __init__(self, x, y, width, height, max_value, color, bg_color=bcolors.BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self.current_value = max_value
        self.color = color
        self.bg_color = bg_color

    def draw(self, surface, current_value):
        self.current_value = current_value
        # Draw background
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
        # Draw current value
        ratio = 0 if self.max_value <= 0 else self.current_value / self.max_value
        current_width = int(self.width * ratio)
        pygame.draw.rect(surface, self.color, (self.x, self.y, current_width, self.height))
        # Draw border
        pygame.draw.rect(surface, bcolors.WHITE, (self.x, self.y, self.width, self.height), 2)

class CharacterStatus:
    def __init__(self, character, x, y):
        self.character = character
        self.x = x
        self.y = y
        self.health_bar = StatusBar(x + 8, y + 2, 84, 10, character.max_hp, bcolors.RED)
        self.mana_bar = StatusBar(x + 8, y + 16, 84, 10, character.max_mp, bcolors.BLUE)
        self.font = pygame.font.SysFont('Arial', 11, bold=True)

    def draw(self, surface):
        # Draw character name
        name_text = self.font.render(self.character.name, True, bcolors.WHITE)
        surface.blit(name_text, (self.x, self.y - 14))
        
        # Draw status bars
        self.health_bar.draw(surface, self.character.hp)
        self.mana_bar.draw(surface, self.character.mp)
        
        # Draw values
        hp_text = self.font.render(f"HP: {self.character.hp}/{self.character.max_hp}", True, bcolors.WHITE)
        mp_text = self.font.render(f"MP: {self.character.mp}/{self.character.max_mp}", True, bcolors.WHITE)
        surface.blit(hp_text, (self.x + 98, self.y + 1))
        surface.blit(mp_text, (self.x + 98, self.y + 15))
