import random
import os
from typing import Optional, Generator

WALL = u'\u2588'
EMPTY = ' '

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


class Maze:

    def __repr__(self) -> str:
        return f'Maze:{self.width}x{self.height}'

    def __init__(self, height: int = 11, width: int = 31):
        """Initialize maze with size height and width."""
        self.height = height
        self.width = width
        self.maze = {}
        for y in range(height):
            for x in range(width):
                self.maze[(x, y)] = WALL
        self.generate_rooms()

    def generate_rooms(self):
        """Creates empty cells for each odd index."""
        for x in range(1, self.width, 2):
            for y in range(1, self.height, 2):
                self.maze[(x, y)] = EMPTY

    def flat(self) -> Generator[int, None, None]:
        """Returns flat list, for example 
        [['W', ' ', 'W'], ['W', 'W', 'W']] -> [1, 0, 1, 1, 1, 1, 0, 1, 0]."""
        for v in self.maze.values():
            yield 1 if v == WALL else 0

    def _print(self):
        height, width = self.height, self.width
        for y in range(height):
            for x in range(width):
                print(self.maze[(x, y)], end='')
            print()

    def get_directions(
            self, x: int, y: int, has_visited: Optional[list] = None) -> None:
        """Gets direction to next cells from current (x, y)."""
        while True:
            unvisited = []
            has_visited = has_visited or [(x, y)]
            if y > 1 and (x, y - 2) not in has_visited:
                unvisited.append('up')
            if y < self.height - 2 and (x, y + 2) not in has_visited:
                unvisited.append('down')
            if x < self.width - 2 and (x + 2, y) not in has_visited:
                unvisited.append('right')
            if x > 1 and (x - 2, y) not in has_visited:
                unvisited.append('left')
            if not unvisited:
                # BASE CASE
                return
            else:
                next_direction = random.choice(unvisited)
                next_coords = self.destroy_wall(x, y, next_direction)
                has_visited.append(next_coords)
                self.get_directions(*next_coords, has_visited=has_visited)

    def destroy_wall(
            self, x: int, y: int, next_direction: str) -> tuple[int, int]:
        if next_direction == 'up':
            next_coords = (x, y - 2)
            self.maze[(x, y - 1)] = EMPTY
        elif next_direction == 'down':
            next_coords = (x, y + 2)
            self.maze[(x, y + 1)] = EMPTY
        elif next_direction == 'right':
            next_coords = (x + 2, y)
            self.maze[(x + 1, y)] = EMPTY
        elif next_direction == 'left':
            next_coords = (x - 2, y)
            self.maze[(x - 1, y)] = EMPTY
        return next_coords
