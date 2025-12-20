import random
from settings import GRID_SIZE

# Liste de tous les sorts disponibles
ALL_CARDS = ["2-TIR", "RADAR", "BOUCLIER", "BOMBE", "SALVE", "SABOTAGE"]

class Player:
    def __init__(self, name="Joueur"):
        self.name = name
        self.tour = False
        self.hits = 0
        self.reinforced_ships = []

        self.board = [[0]*10 for _ in range(10)]
        self.ships = [
            ("Destroyer", 2), 
            ("Sous-marin", 3), 
            ("Croiseur", 3),
            ("Bateau de bataille", 4), 
            ("Porte-avions", 5)
        ]
        self.ship_positions = {}

        self.cards = []
        self.hand_limit = 3 
        self.initialize_cards()

    def initialize_cards(self):
        """Distribue exactement 3 cartes sans vider la liste."""
        self.cards = []
        while len(self.cards) < self.hand_limit:
            choice = random.choice(ALL_CARDS)
            if choice not in self.cards:
                self.cards.append(choice)

    def place_random_ships(self):
        """Place les navires en vérifiant strictement les collisions et les bords."""
        # On réinitialise au cas où
        self.board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.ship_positions = {}

        for name, size in self.ships:
            placed = False
            while not placed:
                orientation = random.choice(["H", "V"])
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - 1)
                
                temp_positions = []
                is_possible = True

                for i in range(size):
                    r = row + i if orientation == "V" else row
                    c = col + i if orientation == "H" else col
                    
                    # VERIFICATION : Hors grille ou case déjà occupée
                    if r >= GRID_SIZE or c >= GRID_SIZE or self.board[r][c] != 0:
                        is_possible = False
                        break
                    temp_positions.append((r, c))

                # Si tout le segment est valide et de la bonne taille
                if is_possible and len(temp_positions) == size:
                    for r, c in temp_positions:
                        self.board[r][c] = 1
                    self.ship_positions[name] = temp_positions
                    placed = True

    def receive_attack(self, row, col):
        """Traite un tir reçu."""
        if self.board[row][col] == 1:
            self.board[row][col] = -1 # On utilise -1 pour "Touché" par convention
            return True
        elif self.board[row][col] == 0:
            self.board[row][col] = -2 # On utilise -2 pour "Manqué"
            return False
        return False

    def all_ships_sunk(self):
        """Vérifie s'il reste des segments intacts (valeur 1)."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 1:
                    return False 
        return True
