# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

# Additional notes
# - Further adaptations from https://www.pygame.org/wiki/Spritesheet
# - Cleaned up overall formatting.
# - Updated from Python 2 -> Python 3.

from typing import Optional
import pygame


class SpriteSheet:

    def __init__(self, filename: str):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load sprite sheet image: {filename}")
            raise SystemExit(e)


    def image_at(self, rectangle, color_key: Optional[int] = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        area = pygame.Rect(rectangle)
        image = pygame.Surface(area.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), area)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0,0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        return image

    def images_at(self, areas, color_key = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(area, color_key) for area in areas]

    def load_strip(self, area, image_count: int, color_key = None):
        """Load a whole strip of images, and return them as a list."""
        tuples = [(area[0] + area[2] * x, area[1], area[2], area[3])
                for x in range(image_count)]
        return self.images_at(tuples, color_key)