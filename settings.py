# ==================================================================================
#                       SETTINGS.PY - CONFIGURATION GLOBALE
# ==================================================================================

# ----------------------------------------------------------------------------------
# 1. DIMENSIONS DE L'ÉCRAN
# ----------------------------------------------------------------------------------
SCREEN_WIDTH = 1400 
SCREEN_HEIGHT = 800 

# ----------------------------------------------------------------------------------
# 2. PARAMÈTRES DE JEU (GAMEPLAY)
# ----------------------------------------------------------------------------------
GRID_SIZE = 10       # Taille de la grille (10x10 cases)
CELL_SIZE = 35       # Taille standard (utilisée par défaut)
CARDS_ENABLED = True # Active la mécanique des cartes
PROJECTILE_SPEED = 80 # Vitesse des boules de feu (pixels par frame)

# ----------------------------------------------------------------------------------
# 3. DIMENSIONS DES GRILLES (INTERFACE DE JEU)
# ----------------------------------------------------------------------------------
# A. GRILLE JOUEUR (Plus petite, en bas à gauche)
CELL_SIZE_PLAYER = 35
START_X_PLAYER = 50
START_Y_PLAYER = 250 

# B. GRILLE IA (Plus grande, en haut à droite)
CELL_SIZE_IA = 55
START_X_IA = 800  
START_Y_IA = 150  

# C. GRILLE DE PLACEMENT (Pour la phase 1)
PLACEMENT_CELL_SIZE = 55
PLACEMENT_GRID_WIDTH_TOTAL = GRID_SIZE * PLACEMENT_CELL_SIZE

# --- CALCULS DE CENTRAGE (Nécessaires pour placement.py) ---
CENTER_HALF_X = SCREEN_WIDTH // 4   # Le centre de la moitié gauche de l'écran
PLACEMENT_GRID_OFFSET_X = CENTER_HALF_X - (PLACEMENT_GRID_WIDTH_TOTAL // 2)
PLACEMENT_GRID_OFFSET_Y = 150

# D. CARTES (INVENTAIRE)
CARD_WIDTH = 130   
CARD_HEIGHT = 150  
CARD_SPACING = 20  

# ----------------------------------------------------------------------------------
# 4. DIMENSIONS BOUTONS (MENU)
# ----------------------------------------------------------------------------------
BUTTON_WIDTH = 300 
BUTTON_HEIGHT = 60
BUTTONS_START_Y = 300
BUTTON_CENTER_X = (SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2)

# ----------------------------------------------------------------------------------
# 5. COULEURS (PALETTE GRAPHIQUE)
# ----------------------------------------------------------------------------------

# --- COULEURS UI & TEXTE ---
COLOR_UI_BACKGROUND = (50, 60, 90)   # Fond par défaut
COLOR_TEXT_MAGIC = (255, 215, 0)     # Or Magique (Titres importants)
COLOR_TEXT_BUTTON = (30, 30, 50)     # Texte Boutons (Foncé)
COLOR_TEXT_TITLE = (255, 255, 255)   # Blanc pur
COLOR_TEXT_NORMAL = (200, 240, 255)  # Blanc bleuté (Texte standard)

# --- COULEURS THÉMATIQUES (JOUEUR vs IA) ---
COLOR_MAGIC_PLAYER = (0, 180, 210)   # Cyan (Joueur)
COLOR_MAGIC_ENEMY = (160, 32, 240)   # Violet (IA)
COLOR_GRID_NEON = (0, 255, 255)      # Grille Joueur
COLOR_GRID_IA_PURPLE = (160, 32, 240)# Grille IA

# --- COULEURS ÉLÉMENTS DE JEU ---
COLOR_OCEAN_DARK = (10, 25, 75)      # Fond de l'eau
COLOR_SHIP = (120, 120, 120)         # Navire intact
COLOR_WATER_LIT = (0, 150, 255)      # Eau éclairée
COLOR_HIT = (255, 0, 0)              # Touché (Rouge)
COLOR_CELL_TINT = (0, 50, 100)       # Teinte des cases vides

# --- COULEURS PLACEMENT (PREVIEW) ---
COLOR_PREVIEW_VALID = (200, 255, 255) # Vert/Cyan clair (Valide)
COLOR_PREVIEW_INVALID = (255, 50, 50) # Rouge vif (Collision)

# --- COULEURS SPÉCIFIQUES (Grimoire / Placement) ---
COLOR_GRIMOIRE_INK = (90, 70, 50)   # Marron Encre (Utilisé pour l'ombre du texte)
COLOR_TEXT_NEON = (0, 200, 255)     # Cyan Lumineux

# --- COULEURS PANNEAUX (STATS) ---
COLOR_PANEL_BG_DARK = (5, 5, 30)     # Fond noir bleuté
PANEL_ALPHA_VALUE = 190              # Transparence (0-255)
COLOR_PANEL_BORDER = COLOR_GRID_NEON # Bordure cyan

# ----------------------------------------------------------------------------------
# 6. TYPOGRAPHIE (FONTS)
# ----------------------------------------------------------------------------------
# Assure-toi que ces fichiers existent dans assets/fonts/ !
FONT_NAME = 'assets/fonts/Sekuya-Regular.ttf'
FONT_NAME_2 = 'assets/fonts/DancingScript-Regular.ttf'
FONT_NAME_GRIMOIRE = 'assets/fonts/MagicSchoolOne.ttf'
FONT_NAME_GRIMOIRE2 = 'assets/fonts/MagicSchoolOne.ttf'