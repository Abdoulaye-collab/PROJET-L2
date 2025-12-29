import random
from settings import GRID_SIZE

# ====================================================================
#  CONFIGURATION DES CARTES ET NAVIRES
# ====================================================================

# Liste de tous les sorts (Noms affichés dans le jeu)
# Doit correspondre aux noms gérés dans cards.py
ALL_CARDS = [" Double Tir", "Radar", "Bouclier", "Bombe", "Salve", "Sabotage"]

class Player:
    """
    Classe représentant un joueur (Humain ou IA).
    Gère sa grille (board), sa flotte (ships) et sa main de cartes.
    """
    def __init__(self, name="Joueur"):
        self.name = name

        # --- STATISTIQUES ---
        self.tour = False           # Est-ce à son tour de jouer ?
        self.hits = 0               # Nombre de tirs réussis
        self.reinforced_ships = []  # Liste des bonus actifs (ex: Bouclier)

        # --- GRILLE DE JEU ---
        # 0 = Eau, 1 = Bateau, -1 = Touché, -2 = Manqué
        self.board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]

        # --- FLOTTE ---
        # (Nom, Taille en cases)
        self.ships = [
            ("Destroyer", 2), 
            ("Sous-marin", 3), 
            ("Croiseur", 3),
            ("Bateau de bataille", 4), 
            ("Porte-avions", 5)
        ]

        # Dictionnaire stockant les positions exactes : {"Destroyer": [(0,1), (0,2)], ...}
        self.ship_positions = {}

        # --- CARTES SORTILÈGES ---
        self.cards = []
        self.hand_limit = 3 
        self.initialize_cards()

    # ====================================================================
    #  GESTION DES CARTES
    # ====================================================================
    def initialize_cards(self):
        """
        Distribue une main de départ (3 cartes aléatoires).
        Garantit qu'on n'a pas deux fois la même carte au départ.
        """
        
        self.cards = []
        attempts = 0
        while len(self.cards) < self.hand_limit:
            choice = random.choice(ALL_CARDS)
            if choice not in self.cards:
                self.cards.append(choice)
                attempts +=1

    # ====================================================================
    #  PLACEMENT DES NAVIRES (LOGIQUE IA)
    # ====================================================================
    def place_random_ships(self):
        """
        Place aléatoirement tous les navires sur la grille.
        Utilisé par l'IA au début de la partie.
        """
        # Reset complet avant placement
        self.board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.ship_positions = {}

        for name, size in self.ships:
            placed = False
            while not placed:
                # 1. Choix aléatoire position/orientation
                orientation = random.choice(["H", "V"])
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - 1)
                
                temp_positions = []
                is_possible = True

                # 2. Vérification case par case
                for i in range(size):
                    r = row + i if orientation == "V" else row
                    c = col + i if orientation == "H" else col
                    
                    # Hors limite ou case occupée ?
                    if r >= GRID_SIZE or c >= GRID_SIZE or self.board[r][c] != 0:
                        is_possible = False
                        break

                    temp_positions.append((r, c))

                # 3. Validation et Enregistrement
                if is_possible and len(temp_positions) == size:
                    for r, c in temp_positions:
                        self.board[r][c] = 1
                    self.ship_positions[name] = temp_positions
                    placed = True

    # ====================================================================
    #  LOGIQUE DE COMBAT
    # ====================================================================
    def receive_attack(self, row, col):
        """
        Traite un tir reçu à la position (row, col).
        Retourne True si touché, False sinon.
        """

        # Sécurité hors limites
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return False

        current_val = self.board[row][col]
        if current_val == 1:
            self.board[row][col] = -1 # On utilise -1 pour "Touché" par convention
            return True
        
        elif current_val == 0:
            self.board[row][col] = -2 # On utilise -2 pour "Manqué"
            return False
        
        return False

    def all_ships_sunk(self):
        """
        Vérifie si le joueur a perdu (plus aucun segment de bateau intact).
        Retourne True si Game Over.
        """
        # On parcourt toute la grille pour chercher un '1' (Bateau vivant)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 1:
                    return False # Il reste au moins un survivant
        return True
    
    def has_lost(self):
        """Alias pour all_ships_sunk"""
        return self.all_ships_sunk()