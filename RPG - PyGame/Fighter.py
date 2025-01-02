import pygame
from SpriteSheet import *
pygame.init()

# fighter class
class Fighter:
    def __init__(self, name, hp, mp, atk, df, speed, mgk_atk, mgk_def, spells, xcoord, ycoord, boss=False):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.strength = atk
        self.mp = mp
        self.df = df
        self.speed = speed
        self.mgk_atk = mgk_atk
        self.mgk_def = mgk_def
        self.spells = spells
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.boss = boss
        self.alive = True
        self.animation_list = []
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead
        self.frame_index = 0
        self.animation_speed = 0.2  # Adjust for slower/faster animations

        # Common animation settings
        scale = 2
        color = (0, 0, 0)  # Black background for transparency

        # Load animations with validation
        for action in ['Idle', 'Attack', 'Hurt', 'Death']:
            path = f'../Images/Characters/{self.name}/{action}'
            sprite_sheet = SpriteSheet(path)
            frames = sprite_sheet.get_frames(scale, color)

            if not frames:  # If no frames are loaded
                print(f"Error: No frames found for action '{action}' in path {path}")
                self.animation_list.append([])  # Append an empty list to prevent indexing issues
            else:
                self.animation_list.append(frames)

        # Validate self.action and self.frame_index
        if self.action >= len(self.animation_list):
            print(f"Invalid action index: {self.action}. Defaulting to 0 (Idle).")
            self.action = 0  # Default to Idle

        if not self.animation_list[self.action]:
            print(f"No frames available for action {self.action}. Defaulting to first available action.")
            self.action = next((i for i, frames in enumerate(self.animation_list) if frames), 0)

        if self.frame_index >= len(self.animation_list[self.action]):
            print(f"Invalid frame index: {self.frame_index}. Defaulting to 0.")
            self.frame_index = 0

        # Set the first frame as the default
        if self.animation_list[self.action]:  # Ensure frames exist for the current action
            self.current_frame = self.animation_list[self.action][self.frame_index]
        else:
            print(f"Warning: No frames available for any action. Check sprite paths.")
            self.current_frame = None

    def update(self):
        """
        Update the current animation frame.
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0  # Loop back to the first frame
        self.current_frame = self.animation_list[self.action][int(self.frame_index)]

    def draw(self, surface):
        """
        Draw the current animation frame onto the given surface.
        """
        surface.blit(self.current_frame, (self.xcoord, self.ycoord))