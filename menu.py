import pygame
import sys
import random

# --- MODULES DU PROJET ---
from settings import *
from effects import ParticleSystem

class Menu:
    """
    Gère l'affichage du menu principal, les animations et les interactions boutons.
    """
    # ====================================================================
    #  1. INITIALISATION
    # ====================================================================
    def __init__(self, screen):
        self.screen = screen
        self.selected = None

        # --- POLICES ---
        self.font_title = pygame.font.Font(FONT_NAME, 80)
        self.font_button = pygame.font.Font(FONT_NAME, 40)
        self.font_subtitle = pygame.font.Font(FONT_NAME, 20)
        
        # --- IMAGES ---
        self.background_image = pygame.image.load("assets/images/menu.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.sorcier_loaded = True

        # --- SYSTÈME DE PARTICULES ---
        self.particles = ParticleSystem()

        # --- TEXTES ---
        self.subtitle_text = "Un jeu de stratégie magique par Abdoulaye et Shelly !"  # Modifier ici pour changer le sous-titre
        
        # --- CONFIGURATION DES BOUTONS ---
        center_x = SCREEN_WIDTH // 2
        start_y = 350 # Hauteur du premier bouton
        gap_y = 120   # Espace entre les boutons
        
        self.buttons = [
            {"text": "Jouer",   "rect": pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT),"pos_y": start_y},
            {"text": "Quitter", "rect": pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT),"pos_y": start_y + gap_y},
        ]
        
        # Centrage des rectangles
        for btn in self.buttons:
            btn["rect"].center = (center_x, btn["pos_y"])
        
    # ====================================================================
    #  2. OUTILS GRAPHIQUES (HELPERS)
    # ====================================================================
    def draw_outlined_text(self, text, font, color, target_rect, thickness=2):
        """
        Dessine un texte avec un contour précis (outline) autour.
        """
        COLOR_CONTOUR = (255, 255, 255) # Contour Blanc
        
        surf_main = font.render(text, True, color)
        surf_outline = font.render(text, True, COLOR_CONTOUR)
        
        # On dessine le contour en décalant dans toutes les directions
        # (Technique plus propre que le double blit simple)
        offsets = [
            (-thickness, -thickness), (0, -thickness), (thickness, -thickness),
            (-thickness, 0),                           (thickness, 0),
            (-thickness, thickness),  (0, thickness),  (thickness, thickness)
        ]

        for dx, dy in offsets:
            # On centre le contour par rapport au rect cible
            outline_rect = surf_outline.get_rect(center=target_rect.center)
            self.screen.blit(surf_outline, outline_rect.move(dx, dy))
        
        # On dessine le texte principal par dessus
        main_rect = surf_main.get_rect(center=target_rect.center)
        self.screen.blit(surf_main, main_rect)

    # ====================================================================
    #  3. GESTION DES ÉVÉNEMENTS
    # ====================================================================
    def handle_event(self, event):
        """
        Détecte les clics sur les boutons.
        Retourne "JOUER" ou "QUITTER" si un bouton est cliqué.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        self.selected = button["text"]
                        return self.selected.upper()
        return None
    
    # ====================================================================
    #  4. AFFICHAGE GLOBAL
    # ====================================================================

    def draw(self):
        # A. Fond d'écran
        self.screen.blit(self.background_image, (0, 0))
    
        # B. Animation Particules (Magie en fond)
        if random.random() < 15: # % de chance par frame d'ajouter une particule
            px = random.randint(0, SCREEN_WIDTH)
            py = random.randint(0, SCREEN_HEIGHT)
            self.particles.add_particle(px, py, (0, 200, 255)) # Particules Cyan
        
        self.particles.update_and_draw(self.screen)

        center_x = SCREEN_WIDTH // 2

        # ---------------------------------------------------------
        # C. TITRE DU JEU
        # ---------------------------------------------------------
        title_text = "Wizard Battleships"

        # A. Préparation des surfaces
        COLOR_OMBRE = (COLOR_MAGIC_ENEMY)
        COLOR_CONTOUR = (255, 255, 255) 
        COLOR_INTERIEUR = (COLOR_MAGIC_PLAYER)   

        surf_ombre = self.font_title.render(title_text, True, COLOR_OMBRE)
        surf_main = self.font_title.render(title_text, True, COLOR_INTERIEUR)
        surf_outline = self.font_title.render(title_text, True, COLOR_CONTOUR)
        
        # B. Position 
        center_pos = (center_x, 150)
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
            self.screen.blit(surf_outline,base_rect.move(dx,dy))
            self.screen.blit(surf_outline, outline_rect)
            
        
        self.screen.blit(surf_main, base_rect)

        # ---------------------------------------------------------
        # D. SOUS-TITRE
        # ---------------------------------------------------------
        subtitle_surf = self.font_subtitle.render(self.subtitle_text, True, (200, 200, 200))
        subtitle_rect = subtitle_surf.get_rect(center=(center_x, SCREEN_HEIGHT - 30))
        self.screen.blit(subtitle_surf, subtitle_rect)

        # ---------------------------------------------------------
        # E. BOUTONS
        # ---------------------------------------------------------
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            rect = button["rect"]
            is_hovered = rect.collidepoint(mouse_pos)
            
            
            # Couleurs dynamiques
            fill_color = COLOR_MAGIC_ENEMY 
            border_color = (0, 0, 0) if not is_hovered else (0, 255, 255) # Cyan au survol
            text_color = (10, 25, 75) 
            
            # 1.Dessin du remplissage du bouton
            pygame.draw.rect(self.screen, fill_color, rect, border_radius=12)

            # 2. Bordure du bouton
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=12)

            # 2. On appelle la fonction 
            self.draw_outlined_text(
                text=button["text"],
                font=self.font_button,
                color=text_color,
                target_rect=rect,
                thickness=2
            )