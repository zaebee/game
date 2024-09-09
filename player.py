import pygame
import random
from maze import Maze
from animator import SpriteStripAnim

DIRECT_DICT = {pygame.K_a: (-1, 0),
               pygame.K_d: (1, 0),
               pygame.K_w: (0, -1),
               pygame.K_s: (0, 1)}


class Player(pygame.sprite.Sprite):
    SIZE = 78, 58

    def __init__(self, fps: int = 60, state: str = 'idle'):
        super().__init__()
        frames = fps / 12
        # x start position for player
        self.centerx = self.SIZE[0] + self.SIZE[0] // 2
        self.centery = self.SIZE[1] + self.SIZE[1] // 2
        self.animations = {
            'idle':
                SpriteStripAnim(
                    'images/idle_(78x58).png', (0, 0, *self.SIZE), 11, 1, True, frames),
            'run':
                SpriteStripAnim(
                    'images/run_(78x58).png', (0, 0, *self.SIZE), 8, 1, True, frames),
        }
        self.state = state
        self.animator = self.animations[state]
        self.speed = 3  # start speed for player
        self.direction = None
        self.direction_stack = []  # Held keys in the order they were pressed
        # self._active_state = self.STATE[]
        self.image = self.animator.next()
        self.rect = self.image.get_rect()

    def add_direction(self, key):
        """
        Add a pressed direction key on the direction stack.
        """
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            self.direction_stack.append(key)
            self.direction = self.direction_stack[-1]

    def pop_direction(self, key):
        """
        Pop a released key from the direction stack.
        """
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]

    def on_event(self, event):
        """
        Handle events pertaining to player control.
        """
        if event.type == pygame.KEYDOWN:
            self.state = 'run'
            self.add_direction(event.key)
            print(f'direction ADD: {self.direction_stack}')
        elif event.type == pygame.KEYUP:
            self.state = 'idle'
            self.pop_direction(event.key)
            print(f'direction POP: {self.direction_stack}')

    def update(self, blocks):
        """
        We have added some logic here for collision detection against the
        sprite.Group, blocks.
        """
        # Increase the value of the index by 1
        # so that we can change the sprite images
        # self.image = self.images[self.index]
        # self.next_image('idle')
        if self.direction_stack:
            print('Player moving')
            self.movement(blocks, 0)
            self.movement(blocks, 1)

    def on_render(self):
        self.animator = self.animations[self.state]
        self.image = self.animator.next()
        # self.next_image('idle')

    def shoot(self):
        # TODO: spawn bullet.
        pass

    def movement(self, blocks: pygame.sprite.Group, axis: int):
        """
        Move player and then check for collisions; adjust as necessary.
        """
        direction_vector = DIRECT_DICT[self.direction]
        self.rect[axis] += self.speed * direction_vector[axis]
        collision = pygame.sprite.spritecollideany(self, blocks)
        collision = False
        while collision:
            self.adjust_on_collision(collision, axis)
            collision = pygame.sprite.spritecollideany(self, blocks)

    def adjust_on_collision(self, collide: pygame.sprite.Sprite, axis: int):
        """
        Adjust player's position if colliding with a solid block.
        """
        if self.rect[axis] < collide.rect[axis]:
            self.rect[axis] = collide.rect[axis] - self.rect.size[axis]
        else:
            self.rect[axis] = collide.rect[axis] + collide.rect.size[axis]
