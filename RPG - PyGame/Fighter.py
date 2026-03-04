import pygame
from SpriteSheet import SpriteSheet
pygame.init()

# fighter class
class Fighter:
    def __init__(self, name, hp, mp, atk, df, speed, mgk_atk, mgk_def, spells, xcoord, ycoord, boss=False, flip=False):
        self.name = name
        self.max_hp = hp
        self.maxhp = hp
        self.hp = hp
        self.max_mp = mp
        self.maxmp = mp
        self.strength = atk
        self.atk = atk
        self.mp = mp
        self.df = df
        self.speed = speed
        self.mgk_atk = mgk_atk
        self.mgk_def = mgk_def
        self.spells = spells if spells else []
        self.spell_weights = {spell: 1 for spell in self.spells}
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.boss = boss
        self.flip = flip
        self.alive = True
        self.animation_list = []
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead
        self.frame_index = 0
        self.animation_speed = 0.2  # Adjust for slower/faster animations
        self.update_time = pygame.time.get_ticks()

        # Common animation settings
        scale = 1.2 if boss else 1.0

        # Load animations with validation
        animation_types = ['Idle', 'Attack', 'Hurt', 'Death']
        for action in animation_types:
            try:
                frames = SpriteSheet.get_character_sprite(self.name, action, scale, self.flip)
                if not frames:
                    print(f"Warning: No frames found for {self.name}'s {action} animation")
                    self.animation_list.append([])
                else:
                    self.animation_list.append(frames)
            except Exception as e:
                print(f"Error loading {self.name}'s {action} animation: {e}")
                self.animation_list.append([])

        self._apply_animation_fallbacks()

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

    def _apply_animation_fallbacks(self):
        idle_frames = self.animation_list[0] if self.animation_list else []
        fallback_labels = {1: "Attack", 2: "Hurt", 3: "Death"}

        if not idle_frames:
            return

        for index, label in fallback_labels.items():
            if index < len(self.animation_list) and not self.animation_list[index]:
                self.animation_list[index] = idle_frames
                print(f"Warning: Falling back to Idle frames for {self.name}'s {label} animation.")

    def update(self):
        """
        Update the current animation frame.
        """
        if not self.animation_list[self.action]:
            return

        # Update animation
        animation_cooldown = 100  # milliseconds
        self.current_frame = self.animation_list[self.action][int(self.frame_index)]
        
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += self.animation_speed
            self.update_time = pygame.time.get_ticks()
            
        # If the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            # If it was an attack animation, return to idle
            if self.action == 1:  # Attack
                self.action = 0  # Idle

    def draw(self, surface):
        """
        Draw the current animation frame onto the given surface.
        """
        if self.current_frame:
            surface.blit(self.current_frame, (self.xcoord, self.ycoord))

    def cast_magic(self, target, magic):
        magic.apply(caster=self, target=target)

    def clone(self, flip=None):
        return Fighter(
            self.name,
            self.max_hp,
            self.max_mp,
            self.atk,
            self.df,
            self.speed,
            self.mgk_atk,
            self.mgk_def,
            list(self.spells) if self.spells else [],
            self.xcoord,
            self.ycoord,
            self.boss,
            self.flip if flip is None else flip,
        )

    def create_fighter(self, flip=None):
        return self.clone(flip=flip)
