# player.py
import random

class Player:
    def __init__(self, name="Joueur"):
        self.name = name
        self.grid = [[0]*10 for _ in range(10)]
        self.cards = ["Double Tir", "Radar", "Bouclier"]  # Exemple
        self.tour = False

    def place_random_ships(self, n=5):
        """Place n navires aléatoirement"""
        count = 0
        while count < n:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if self.grid[row][col] == 0:
                self.grid[row][col] = 1
                count += 1
