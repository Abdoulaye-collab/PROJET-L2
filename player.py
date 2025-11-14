import random
from constants import GRID_SIZE

class Player:
    def __init__(self, name):
        self.name = name
        self.grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]

    def receive_shot(self, x, y):
        # 1 = bateau, 0 = vide
        if self.grid[y][x] == 1:
            self.grid[y][x] = -1
            return True
        else:
            self.grid[y][x] = -2
            return False

    def place_random_ships(self):
        # exemple simple : placer 5 bateaux aléatoirement
        for _ in range(5):
            x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            self.grid[y][x] = 1
