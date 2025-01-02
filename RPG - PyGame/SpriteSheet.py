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
    def __init__(self, images_folder):
        """
                Initialize the SpriteSheet class.
                :param images_folder: Folder containing individual frames for animations.
        """
        self.images_folder = images_folder
        if not os.path.exists(self.images_folder):
            raise FileNotFoundError(f"Folder '{self.images_folder}' does not exist.")

    def get_frames(self, scale, color, flip=False):
        """
        Load all frames from the folder.
        :param scale: Scaling factor for resizing.
        :param color: Transparency color (colorkey).
        :param flip: Whether to flip the frame horizontally.
        :return: List of pygame.Surface frames.
        """
        frames = []
        images = os.listdir(self.images_folder)

        if not images:
            print(f"No images found in {self.images_folder}")
            return frames

        # Load each image
        for image_file in images:
            try:
                img_path = os.path.join(self.images_folder, image_file)
                img = pygame.image.load(img_path).convert_alpha()
                width, height = img.get_size()
                img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
                img.set_colorkey(color)
                if flip:
                    img = pygame.transform.flip(img, True, False)
                frames.append(img)
            except Exception as e:
                print(f"Error loading image '{image_file}': {e}")

        return frames