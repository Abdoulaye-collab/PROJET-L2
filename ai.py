import random

class AI:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.played = set()
        self.grid = [[0]*grid_size for _ in range(grid_size)]

    def play(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.played:
                self.played.add((x, y))
                return x, y

    def receive_shot(self, x, y):
        # logique simplifiée
        return random.choice([True, False])
