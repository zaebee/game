import os
import time
import random
import pygame

from maze import Maze
from player import Player
from wall import Brick


class Game:
    """Implements maze game with player and enemies."""
    CAPTION = "Moving Platforms"
    WINDOW_WIDTH = 860
    WINDOW_HEIGHT = 720
    SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_GREEN = (163, 255, 180)

    def __init__(self):
        # TODO: connect to server listen (0.0.0.0)
        pygame.init()
        self._running = True
        self._clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.SIZE)
        self.maze = self.init_maze()
        self.maze_flat = list(self.maze.flat())

        # init player and add him into all sprites.
        self.player = Player()
        self.spawn(self.player)
        # self.player.set_start_position(self.maze_flat)
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.player)
        self.blocks = self.create_walls()
    
    def create_walls(self) -> pygame.sprite.Group:
        x = y = 0
        walls = pygame.sprite.Group()
        for index in range(0, self.maze.height * self.maze.width):
            if self.maze_flat[index] == 1:
                brick = Brick(x * Brick.WIDTH, y * Brick.HEIGHT)
                walls.add(brick)
            x += 1
            # x, y = 0, y + 1 if x > self.maze.width - 1 else x + 1, y
            if x > self.maze.width - 1:
                x = 0
                y += 1
        return walls
    
    def spawn(self, player: Player) -> None:
        """Set X, Y coords for player based on random empty cell."""
        result = []
        x = y = 0
        for index in range(self.maze.height * self.maze.width):
            if self.maze_flat[index] == 0:
                result.append((
                    x * Brick.WIDTH + Brick.WIDTH / 2, 
                    y * Brick.HEIGHT + Brick.HEIGHT / 2
                    ))
            x += 1
            if x > self.maze.width - 1:
                x = 0
                y += 1
        coords = random.choice(result)
        # player.rect.center = coords
                
    def init_maze(self) -> Maze:
        maze = Maze(15, 15)  # 720x720
        maze.get_directions(1, 1)
        return maze
    
    def on_cleanup(self):
        pygame.quit()

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self._running = False
        self.player.on_event(event)
        
    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(self.CAPTION, self._clock.get_fps())
        pygame.display.set_caption(caption)
       
    def on_render(self):
        """Renders sprite animations."""
        self.player.on_render()
        self.sprites.draw(self.screen)
        self.blocks.draw(self.screen)
            
    def on_execute(self):
        pygame.display.set_caption('Astro game')
        
        while self._running:
            self.on_render()
            self.display_fps()
            self.player.update(self.blocks)
            for event in pygame.event.get():
                self.on_event(event)
                # TODO: send event to server
            self._clock.tick(self.FPS)
            self.screen.fill(self.LIGHT_GREEN)
            self.on_render()
            pygame.display.flip()
        self.on_cleanup()


game = Game()
game.on_execute()
