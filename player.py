import random

# Liste de tous les sorts disponibles
ALL_CARDS = ["Double Tir", "Radar", "Bombe", "Bouclier", "Sabotage", "Salve"]

class Player:
    # ----------------------------------------------------------------------
    # A. INITIALISATION
    # ----------------------------------------------------------------------
    def __init__(self, name="Joueur"):
        # --- ATTRIBUTS D'IDENTIFICATION ET D'ÉTAT ---
        self.name = name
        self.tour = False
        self.hits = 0
        self.reinforced_ships = []

        # --- GRILLE DE JEU ET BATEAUX ---
        self.board = [[0]*10 for _ in range(10)]
        self.ships = [
            ("Destroyer", 2), 
            ("Sous-marin", 3), 
            ("Croiseur", 3),
            ("Bateau de bataille", 4), 
            ("Porte-avions", 5)
        ]
        self.ship_positions = {}

        # Distribution aléatoire des cartes : 3 cartes avec chance 1/6 chacune
        self.cards = []
        for card in ALL_CARDS:
            if len(self.cards) >= 3:
                break
            if random.randint(1,6) == 1:
                self.cards.append(card)
        # Compléter si moins de 3 cartes obtenues
        while len(self.cards) < 3:
            choice = random.choice(ALL_CARDS)
            if choice not in self.cards:
                self.cards.append(choice)

    def place_random_ships(self):
        """Place les navires de manière aléatoire sur la grille (utilisé par l'IA)."""
        for name, size in self.ships:
            placed = False
            while not placed:
                orientation = random.choice(["H","V"])
                row = random.randint(0,9)
                col = random.randint(0,9)
                positions = []

                # Vérification de la validité et collecte des positions
                for i in range(size):
                    r = row + i if orientation == "V" else row
                    c = col + i if orientation == "H" else col
                    if r >= 10 or c >= 10 or self.board[r][c] != 0:
                        break
                    positions.append((r,c))
                if len(positions) == size:
                    for r,c in positions:
                        self.board[r][c] = 1
                    self.ship_positions[name] = positions
                    placed = True
