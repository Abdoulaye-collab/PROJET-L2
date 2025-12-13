import pygame
from settings import COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, BUTTON_WIDTH, BUTTON_CENTER_X as CENTER_X,FONT_NAME

# ====================================================================
#  CLASSE MENU : GESTION DE L'ÉCRAN D'ACCUEIL
# ====================================================================
class Menu:
    # ----------------------------------------------------------------------
    # A. INITIALISATION ET ATTRIBUTS
    # ----------------------------------------------------------------------
    def __init__(self, screen):
        self.screen = screen
        self.selected = None

        # --- POLICES ET TEXTES ---
        self.font = pygame.font.Font(FONT_NAME, 40)
        self.title_font = pygame.font.Font(FONT_NAME, 60)
        self.subtitle_font = pygame.font.Font(FONT_NAME, 20)
        
        self.subtitle_text = "Un jeu de stratégie magique par Abdoulaye et Shelly !"  # Modifier ici pour changer le sous-titre
        
        # --- BOUTONS ---
        # Coordonnées des boutons centrés
        self.buttons = [
            {"text": "Jouer", "rect": pygame.Rect(CENTER_X, 200, BUTTON_WIDTH, 50)},
            {"text": "Options", "rect": pygame.Rect(CENTER_X, 300, BUTTON_WIDTH, 50)},
            {"text": "Quitter", "rect": pygame.Rect(CENTER_X, 400, BUTTON_WIDTH, 50)},
        ]
        
    # ----------------------------------------------------------------------
    # B. GESTION DES ÉVÉNEMENTS
    # ----------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    self.selected = button["text"]
    # ----------------------------------------------------------------------
    # C. AFFICHAGE DE L'ÉCRAN
    # ----------------------------------------------------------------------
    def draw(self):
        self.screen.fill(COLOR_OCEAN_DARK)

        # ------------------- 1. Titre et Sous-titre -------------------
        
        # Titre du jeu (Wizards Battleship)
        title_surf = self.title_font.render("Wizards Battleship", True, COLOR_TEXT_MAGIC)
        title_rect = title_surf.get_rect(center=(self.screen.get_width()//2, 100))
        
        # Ombre magique pour le titre
        SHADOW_COLOR = (150, 0, 200) 
        shadow_rect = title_surf.get_rect(center=(self.screen.get_width()//2 + 3, 103))
        self.screen.blit(self.title_font.render("Wizards Battleship", True, SHADOW_COLOR), shadow_rect)
        
        self.screen.blit(title_surf, title_rect)

        # Sous-titre (Crédits)
        subtitle_surf = self.subtitle_font.render(self.subtitle_text, True, (255, 255, 255))
        self.screen.blit(subtitle_surf, (10, self.screen.get_height() - 30))

        # ------------------- 2.Affichage des Boutons -------------------
        
        mouse_pos = pygame.mouse.get_pos()

        # Définition des couleurs thématiques pour les boutons
        COLOR_BUTTON_FILL = (180, 180, 180)
        COLOR_BUTTON_INACTIVE = (0, 0, 0)       # Gris neutre / Pierre
        COLOR_BUTTON_HOVER = COLOR_TEXT_MAGIC   # Or Magique (au survol)
        COLOR_TEXT_BUTTON = (10, 25, 75)        # Texte en Bleu Nuit (pour contraster)

        for button in self.buttons:
            rect = button["rect"]

            # Dessin du remplissage du bouton
            pygame.draw.rect(self.screen, COLOR_BUTTON_FILL, rect)

            # Définition de la couleur de la bordure (effet de survol)
            if rect.collidepoint(mouse_pos):
                border_color = COLOR_BUTTON_HOVER
            else:
                border_color = COLOR_BUTTON_INACTIVE
            
            # Dessin de la bordure
            pygame.draw.rect(self.screen, border_color, rect, 3)

            # Dessin du texte
            text_surf = self.font.render(button["text"], True, COLOR_TEXT_BUTTON) # Texte en Bleu Nuit
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)

