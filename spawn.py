import random

def get_empty(maze: list[int]) -> tuple[int, int]:
    """Returns X,Y coords for random empty cell."""
    result = []
    block_size = 48
    for index, value in enumerate(maze):
        if value == 0:
            result.append(index)
    cell_index = random.choice(result)
    x = y = block_size * cell_index * block_size / 2
    return (x, y)