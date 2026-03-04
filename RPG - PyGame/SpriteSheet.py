import os
import pygame
pygame.init()

"""
    Parameter:
    image: A single sprite sheet image (optional). This would typically be a pygame.Surface object.
    images_folder: A folder containing separate images (optional), in case the animations aren't in a single sprite sheet.

    Attributes:
        self.sheet: Stores the provided sprite sheet image (or None if not given).
        self.images_folder: Stores the path to a folder containing individual images (if applicable).
        self.is_sprite_sheet: A boolean indicating if a sprite sheet is provided (True if image is not None).
        self.frames: An empty list intended to store individual frames extracted from the sprite sheet.
"""
class SpriteSheet:
    def __init__(self, character_name, animation_type="Idle"):
        """
        Initialize the SpriteSheet class.
        :param character_name: Name of the character (must match folder name)
        :param animation_type: Type of animation (Idle, Attack, Hurt, Death)
        """
        base_dir = os.path.dirname(__file__)
        self.images_folder = os.path.join(base_dir, "Images", "Characters", character_name, animation_type)
        if not os.path.exists(self.images_folder):
            raise FileNotFoundError(f"Animation folder '{self.images_folder}' does not exist.")

    def get_frames(self, scale=1.0, color=(0, 0, 0), flip=False):
        """
        Load all frames from the animation folder.
        :param scale: Scaling factor for resizing.
        :param color: Transparency color (colorkey).
        :param flip: Whether to flip the frame horizontally.
        :return: List of pygame.Surface frames.
        """
        frames = []
        try:
            # Get all image files and sort them numerically
            images = [f for f in os.listdir(self.images_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
            images.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
            
            if not images:
                print(f"No images found in {self.images_folder}")
                return frames

            # Load each image
            for image_file in images:
                img_path = os.path.join(self.images_folder, image_file)
                try:
                    img = pygame.image.load(img_path).convert_alpha()
                    width, height = img.get_size()
                    img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
                    img.set_colorkey(color)
                    if flip:
                        img = pygame.transform.flip(img, True, False)
                    frames.append(img)
                except pygame.error as e:
                    print(f"Error loading image '{image_file}': {e}")
        except Exception as e:
            print(f"Error loading images from '{self.images_folder}': {e}")

        return frames

    @staticmethod
    def get_character_sprite(character_name, animation_type="Idle", scale=1.0, flip=False):
        """
        Static method to quickly get a character's sprite frames.
        :param character_name: Name of the character
        :param animation_type: Type of animation
        :param scale: Scaling factor
        :param flip: Whether to flip the sprite
        :return: List of pygame.Surface frames
        """
        try:
            sprite_sheet = SpriteSheet(character_name, animation_type)
            return sprite_sheet.get_frames(scale, (0, 0, 0), flip)
        except FileNotFoundError as e:
            print(f"Warning: {e}")
            return []
