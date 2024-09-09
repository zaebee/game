import pygame


class Brick(pygame.sprite.Sprite):
    WIDTH = 48
    HEIGHT = 48
    
    def __init__(self, x: int, y: int, is_door: bool = False) -> None:
        super().__init__()
        self.image = pygame.image.load('images/brick.png').convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_door = is_door
        
    def spawn_coords(self):
        pass