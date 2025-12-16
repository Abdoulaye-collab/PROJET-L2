import pygame
from settings import COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, BUTTON_WIDTH,BUTTON_HEIGHT, BUTTONS_START_Y, BUTTON_CENTER_X as CENTER_X,FONT_NAME,SCREEN_WIDTH, SCREEN_HEIGHT

# ====================================================================
#  CLASSE MENU : GESTION DE L'ÉCRAN D'ACCUEIL
# ====================================================================
class Menu:
    # ----------------------------------------------------------------------
    # FONCTION UTILITAIRE : DESSINER TEXTE AVEC CONTOUR
    # ----------------------------------------------------------------------
    def draw_outlined_text(self, text, font, color, center_pos):
        """
        Dessine un texte avec un contour blanc automatique.
        """
        COLOR_CONTOUR = (255, 255, 255) # Blanc
        EPAISSEUR = 2 # Épaisseur du contour (2 est bon pour les petits textes)
        
        surf_main = font.render(text, True, color)
        surf_outline = font.render(text, True, COLOR_CONTOUR)
        rect = surf_main.get_rect(center=center_pos)
        
        # Dessiner le contour (8 directions)
        offsets = [
            (-EPAISSEUR, -EPAISSEUR), (0, -EPAISSEUR), (EPAISSEUR, -EPAISSEUR),
            (-EPAISSEUR, 0),                           (EPAISSEUR, 0),
            (-EPAISSEUR, EPAISSEUR),  (0, EPAISSEUR),  (EPAISSEUR, EPAISSEUR)
        ]
        
        for dx, dy in offsets:
            self.screen.blit(surf_outline, rect.move(dx, dy))
            
        # Dessiner le texte principal
        self.screen.blit(surf_main, rect)
    # ----------------------------------------------------------------------
    # A. INITIALISATION ET ATTRIBUTS
    # ----------------------------------------------------------------------
    def __init__(self, screen):
        self.screen = screen
        self.selected = None
        self.DECO_WIDTH = 400 
        self.DECO_HEIGHT = 400
        # --- POLICES ET TEXTES ---
        self.font = pygame.font.Font(FONT_NAME, 40)
        self.title_font = pygame.font.Font(FONT_NAME, 60)
        self.subtitle_font = pygame.font.Font(FONT_NAME, 20)

        sorcier_img = pygame.image.load('images/sorcier.png').convert_alpha() 
        self.sorcier_image = pygame.transform.scale(sorcier_img, (self.DECO_WIDTH, self.DECO_HEIGHT))
        self.sorcier_loaded = True
        
        self.subtitle_text = "Un jeu de stratégie magique par Abdoulaye et Shelly !"  # Modifier ici pour changer le sous-titre
        
        # --- BOUTONS ---
        # Coordonnées des boutons centrés
        button_center_x = SCREEN_WIDTH // 2
        
        # Hauteurs Y des boutons
        Y1 = 300 # Jouer
        Y2 = 400 # Options
        Y3 = 500 # Quitter (Ajusté pour plus d'espace)
        
        self.buttons = [
            {"text": "Jouer",   "rect": pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)},
            {"text": "Options", "rect": pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)},
            {"text": "Quitter", "rect": pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)},
        ]
        
        # Centrer les rectangles (Ceci assure que les boutons sont au milieu de l'écran)
        self.buttons[0]["rect"].center = (button_center_x, Y1)
        self.buttons[1]["rect"].center = (button_center_x, Y2)
        self.buttons[2]["rect"].center = (button_center_x, Y3)
        
        # Déterminer la zone de travail des boutons pour le centrage des images :
        self.BUTTONS_START_Y = self.buttons[0]["rect"].top
        self.BUTTONS_END_Y = self.buttons[-1]["rect"].bottom
        self.TOTAL_BUTTON_SPAN_Y = self.BUTTONS_END_Y - BUTTONS_START_Y
        self.CENTER_Y_BUTTONS = self.BUTTONS_START_Y + (self.TOTAL_BUTTON_SPAN_Y // 2)

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
        center_x = SCREEN_WIDTH // 2
        
        

        # ------------------- 1. Titre et Sous-titre -------------------
        
        title_text = "Wizard Battleships"
        # A. Préparation des surfaces
        COLOR_OMBRE = (COLOR_TEXT_MAGIC)
        COLOR_CONTOUR = (255, 255, 255) # Blanc pour le contour
        COLOR_INTERIEUR = (148,0,211)   # Couleur Magique pour l'intérieur

        surf_ombre = self.title_font.render(title_text, True, COLOR_OMBRE)
        surf_outline = self.title_font.render(title_text, True, COLOR_CONTOUR)
        surf_main = self.title_font.render(title_text, True, COLOR_INTERIEUR)

        # B. Position centrale
        center_pos = (center_x, 100)
        base_rect = surf_main.get_rect(center=center_pos)

        rect_ombre = base_rect.move(6, 6)

        self.screen.blit(surf_ombre, rect_ombre)

        # C. Dessin du Contour (remplace l'ancienne ombre simple)
        OUTLINE_THICKNESS = 1 
        offsets = [
            (-OUTLINE_THICKNESS, -OUTLINE_THICKNESS), (0, -OUTLINE_THICKNESS), (OUTLINE_THICKNESS, -OUTLINE_THICKNESS),
            (-OUTLINE_THICKNESS, 0),                                           (OUTLINE_THICKNESS, 0),
            (-OUTLINE_THICKNESS, OUTLINE_THICKNESS),  (0, OUTLINE_THICKNESS),  (OUTLINE_THICKNESS, OUTLINE_THICKNESS)
        ]
        
        for dx, dy in offsets:
            outline_rect = base_rect.move(dx, dy)
            self.screen.blit(surf_outline, outline_rect)
            self.screen.blit(surf_outline,base_rect.move(dx,dy))
        
        self.screen.blit(surf_main, base_rect)

        # Sous-titre
        subtitle_surf = self.subtitle_font.render(self.subtitle_text, True, (255, 255, 255))
        Y_POSITION = 750
        subtitle_rect = subtitle_surf.get_rect(center=(center_x, Y_POSITION)) 
        self.screen.blit(subtitle_surf, subtitle_rect)

        # ------------------- 2.Affichage des Boutons -------------------
        
        mouse_pos = pygame.mouse.get_pos()

        # Définition des couleurs thématiques pour les boutons
        COLOR_BUTTON_FILL = COLOR_TEXT_MAGIC
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

            self.draw_outlined_text(
                text=button["text"],
                font=self.font,
                color=(0,255,240),
                center_pos=rect.center
            )

            # Dessin du texte
            text_surf = self.font.render(button["text"], True, COLOR_TEXT_BUTTON) # Texte en Bleu Nuit
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
        
        # ------------------- 3. Affichage des Images Décoratives -------------------
        
        MARGIN_FROM_BUTTON = 50 # Espace entre le bouton et l'image
        
        # Position Y : Centrée sur la zone des boutons
        deco_y = self.CENTER_Y_BUTTONS - (self.DECO_HEIGHT // 2)
        
        # Position X : 
        # L'extrémité droite de la zone des boutons est au centre_x + (BUTTON_WIDTH / 2)
        button_edge_x_right = center_x + (BUTTON_WIDTH // 2)
        button_edge_x_left = center_x - (BUTTON_WIDTH // 2)
        
        # # a. Bateau (à droite)
        # bateau_x = button_edge_x_right + MARGIN_FROM_BUTTON 
        
        # if self.bateau_loaded and self.bateau_image:
        #     self.screen.blit(self.bateau_image, (bateau_x, deco_y))
            
        # b. Sorcier (à gauche)
        # On recule de la largeur de l'image + la marge
        sorcier_x = button_edge_x_right + MARGIN_FROM_BUTTON
        
        if self.sorcier_loaded and self.sorcier_image:
            self.screen.blit(self.sorcier_image, (sorcier_x, deco_y))
            

        pygame.display.flip()
