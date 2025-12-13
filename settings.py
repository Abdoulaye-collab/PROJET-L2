# --- PARAMÈTRES DE JEU ---
CARDS_ENABLED = True # Active/Désactive la mécanique des cartes de sortilège

# ==================================================================================
#                       COULEURS THÉMATIQUES
# ==================================================================================

# --- COULEURS D'INTERFACE (UI) ---
COLOR_UI_BACKGROUND = (50,60,90)  # Fond des éléments UI / Console ( Bleu Ardoise)
COLOR_TEXT_MAGIC = (255, 215, 0)      # Texte principal (Or/Jaune Vif)
COLOR_TEXT_BUTTON = (30,30,50)    # cadre d'interface ( Bleu Foncé) 

# --- COULEURS DE LA GRILLE / COMBAT ---
COLOR_OCEAN_DARK = (10, 25, 75)       # Eau de la Grille (Bleu Nuit/Saphir)
COLOR_SHIP = (120, 120, 120)             # Couleur des bateaux (Gris Moyen)
COLOR_WATER_LIT = (0, 150, 255)        # Eau touchée (Bleu Lumineux)
COLOR_HIT = (255, 0, 0)             # Bateau touché (Rouge Vif)

# --- COULEURS DE PRÉVISUALISATION (PLACEMENT) ---
COLOR_PREVIEW_VALID = (180,100,255) # Placement valide (Violet Clair)
COLOR_PREVIEW_INVALID = (255,50,50)  # Placement invalide (Rouge vif)

# ==================================================================================
#                           TYPOGRAPHIE
# ==================================================================================
FONT_NAME = 'CormorantUnicase-Regular.ttf'

# ==================================================================================
#                        DIMENSIONS DE L'ÉCRAN
# ==================================================================================

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
# ==================================================================================
#             PARAMÈTRES D'INTERFACE UTILISATEUR (MENU ET BOUTONS)
# ==================================================================================
BUTTON_WIDTH = 200 
BUTTON_HEIGHT = 50 
# Calcul de la position X pour centrer les boutons (en utilisant SCREEN_WIDTH)
BUTTON_CENTER_X = (SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2)

# ==================================================================================
#                 PARAMÈTRES DES GRILLES DE JEU
# ==================================================================================

# --- DIMENSIONS DE BASE ---
CELL_SIZE = 40  # Taille d'une cellule en pixels
GRID_SIZE = 10  # Nombre lignes/colonnes par grille (10x10)
GRID_WIDTH_TOTAL = GRID_SIZE * CELL_SIZE # Largeur totale de la grille (400 pixels)

# --- OFFSETS DE ET ALIGNEMENT ---
GAP_SIZE = 50 # Espace entre les deux grilles (game.py)
TOTAL_OCCUPIED_WIDTH = (GRID_WIDTH_TOTAL * 2) + GAP_SIZE # (850 pixels) largeur totale des grilles + l'espace 
MARGIN_X = (SCREEN_WIDTH - TOTAL_OCCUPIED_WIDTH) // 2 # (25 pixels) marge gauche/droite pour centrer les grilles

# --- Coordonnées des grilles ---
GRID_OFFSET_Y = 105 # Position Y commune des grilles
GRID_OFFSET_X_PLAYER = MARGIN_X # Position X de la grille du joueur (25)
GRID_OFFSET_X_ENEMY = MARGIN_X + GRID_WIDTH_TOTAL + GAP_SIZE # Position X de la grille de l'ennemi (475)

