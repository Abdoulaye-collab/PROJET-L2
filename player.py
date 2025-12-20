import random
from settings import GRID_SIZE

# Liste de tous les sorts disponibles
ALL_CARDS = ["2-TIR", "RADAR", "BOUCLIER", "BOMBE", "SALVE", "SABOTAGE"]

# ====================================================================
# CLASSE PLAYER : GESTION DU JOUEUR, DE LA GRILLE ET DE LA MAGIE
# ====================================================================
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

        # --- MECANIQUE MAGIQUE
        self.cards = []
        self.hand_limit = 3 
        self.initialize_cards()

    def initialize_cards(self):
        """Distribue aléatoirement 3 cartes magiques au joueur au début du jeu ."""

        temp_cards = []
        # Distribution initiale avec une chance 1/6 pour chaque carte
        for card in ALL_CARDS:
            if random.randint(1,6) == 1:
                self.cards.append(card)

        # S'assurer que le joueur a au plus la limite de cartes (3)
        self.cards = temp_cards[:self.hand_limit]

        # Compléter si moins de 3 cartes obtenues
        while len(self.cards) < 3:
            choice = random.choice(ALL_CARDS)
            if choice not in self.cards:
                self.cards.append(choice)

    # ----------------------------------------------------------------------
    # B. GESTION DU PLACEMENT DES BATEAUX (IA)
    def place_random_ships(self):
        """Place les navires de manière aléatoire sur la grille (utilisé par l'IA)."""
        
        for name, size in self.ships:
            placed = False
            while not placed:
                orientation = random.choice(["H","V"])
                row = random.randint(0,GRID_SIZE-1)
                col = random.randint(0,GRID_SIZE-1)
                positions = []

                # Vérification de la validité et collecte des positions
                is_valid = True
                for i in range(size):
                    r = row + i if orientation == "V" else row
                    c = col + i if orientation == "H" else col
                    
                    if r >= 10 or c >= 10 or self.board[r][c] != 0:
                        break
                    positions.append((r,c))

                if is_valid:
                    for r,c in positions:
                        self.board[r][c] = 1
                    self.ship_positions[name] = positions
                    placed = True

# ----------------------------------------------------------------------
    # D. GESTION DU COMBAT (Correction de l'AttributeError)
    # ----------------------------------------------------------------------
    
    def receive_attack(self, row, col):
        """Traite un tir reçu sur cette grille."""
        
        # Logique simplifiée : 
        if self.board[row][col] == 1:
            # Touché (Hit)
            self.board[row][col] = 3 # 3 représente une case touchée
            # Une implémentation complète vérifierait si le navire est coulé ici
            return True
        elif self.board[row][col] == 0:
            # Manqué (Miss)
            self.board[row][col] = 2 # 2 représente un tir manqué
            return False
        
        return False # Si la case a déjà été touchée (2 ou 3)

    def all_ships_sunk(self):
        """
        Vérifie si le joueur a perdu en cherchant s'il reste une seule case 
        de bateau intacte (valeur 1) sur le plateau.
        """
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 1:
                    # Trouvé un segment de navire intact
                    return False 
        
        # Si aucun '1' n'est trouvé, la flotte est détruite
        return True