import pygame
import os # Pour gérer les fichiers images
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_NAME

class GameOver:
    def __init__(self, screen, winner_name, loser_name, game_time_seconds, cards_count):
        self.screen = screen
        self.game_time_seconds = game_time_seconds
        self.cards_count = cards_count
        
        # --- GESTION DES NOMS ---
        if hasattr(winner_name, 'name'):
            self.winner_name = winner_name.name
        else:
            self.winner_name = str(winner_name)

        if hasattr(loser_name, 'name'):
            self.loser_name = loser_name.name
        else:
            self.loser_name = str(loser_name)
        
        # --- CHARGEMENT DES IMAGES DE FOND (Sécurisé) ---
        # On essaie de charger les images. Si elles n'existent pas, on met None.
        try:
            # Assure-toi que les images sont dans le même dossier ou dans assets/
            self.victory_img = pygame.image.load("victory_bg.png").convert()
            self.victory_img = pygame.transform.scale(self.victory_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.victory_img = None
            print("Image victory_bg.png non trouvée (Fond couleur par défaut)")

        try:
            self.defeat_img = pygame.image.load("defeat_bg.png").convert()
            self.defeat_img = pygame.transform.scale(self.defeat_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.defeat_img = None
            print("Image defeat_bg.png non trouvée (Fond couleur par défaut)")

        # --- POLICES ---
        self.title_font = pygame.font.Font(FONT_NAME, 90) # Très gros titre
        self.stat_font = pygame.font.SysFont("Verdana", 24)

        # --- BOUTON ---
        self.button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT - 120, 260, 60)
        self.button_text = "Retour au Menu"
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.done = True

    def draw(self):
        center_x = SCREEN_WIDTH // 2
        
        # 1. DÉTECTION DU GAGNANT (Pour choisir le thème)
        is_player_winner = True
        if "IA" in self.winner_name or "ia" in self.winner_name or "Enemy" in self.winner_name:
            is_player_winner = False

        # 2. CONFIGURATION DU THÈME (Couleurs & Textes)
        if is_player_winner:
            # --- THÈME JOUEUR (CYAN / VICTOIRE) ---
            main_title = "VICTOIRE !"
            sub_title = "L'océan est sous votre contrôle."
            
            # Couleurs Cyan
            theme_color = (0, 255, 255)       # Cyan pur
            shadow_color = (0, 100, 100)      # Cyan foncé
            bg_fallback = (0, 50, 50)         # Fond si pas d'image
            current_bg_img = self.victory_img
            
        else:
            # --- THÈME IA (VIOLET / DÉFAITE) ---
            main_title = "DÉFAITE..."
            sub_title = "Sombré dans les abysses..."
            
            # Couleurs Violettes
            theme_color = (180, 50, 255)      # Violet Néon
            shadow_color = (50, 0, 80)        # Violet très sombre
            bg_fallback = (30, 0, 30)         # Fond si pas d'image
            current_bg_img = self.defeat_img

        # 3. DESSIN DU FOND
        if current_bg_img:
            # Si l'image existe, on l'affiche
            self.screen.blit(current_bg_img, (0, 0))
            # On ajoute un voile sombre semi-transparent pour que le texte reste lisible
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(100) # Transparence (0-255)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0,0))
        else:
            # Sinon fond uni
            self.screen.fill(bg_fallback)

        # 4. TITRES
        # Ombre du titre
        shadow_surf = self.title_font.render(main_title, True, shadow_color)
        self.screen.blit(shadow_surf, (center_x - shadow_surf.get_width()//2 + 5, 85))
        
        # Titre Principal
        title_surf = self.title_font.render(main_title, True, theme_color)
        self.screen.blit(title_surf, (center_x - title_surf.get_width()//2, 80))

        # Sous-titre
        sub_surf = self.stat_font.render(sub_title, True, (220, 220, 220))
        self.screen.blit(sub_surf, (center_x - sub_surf.get_width()//2, 170))
        
        # 5. PANNEAU DE STATS
        PANEL_Y = 230
        PANEL_HEIGHT = 280
        PANEL_RECT = pygame.Rect(center_x - 300, PANEL_Y, 600, PANEL_HEIGHT)
        
        # Fond du panneau (Noir semi-transparent)
        s = pygame.Surface((PANEL_RECT.width, PANEL_RECT.height))
        s.set_alpha(180) 
        s.fill((0, 0, 0))
        self.screen.blit(s, (PANEL_RECT.x, PANEL_RECT.y))
        
        # Bordure du panneau (Couleur du thème : Cyan ou Violet)
        pygame.draw.rect(self.screen, theme_color, PANEL_RECT, 2, border_radius=15)
        
        # Calcul temps
        m = (self.game_time_seconds // 60) % 60
        s = self.game_time_seconds % 60
        time_str = f"{int(m)} min {int(s)} s"

        stats_list = [
            ("Vainqueur :", self.winner_name),
            ("Perdant :", self.loser_name),
            ("Sortilèges joués :", str(self.cards_count)),
            ("Durée :", time_str)
        ]
        
        current_y = PANEL_Y + 40
        for label, value in stats_list:
            lbl = self.stat_font.render(label, True, (180, 180, 180))
            self.screen.blit(lbl, (PANEL_RECT.x + 40, current_y))
            
            # La valeur est coloriée selon le thème pour faire joli
            val = self.stat_font.render(value, True, theme_color) 
            val_rect = val.get_rect(right=PANEL_RECT.right - 40, top=current_y)
            self.screen.blit(val, val_rect)
            
            current_y += 55
            
        # 6. BOUTON
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            btn_bg = theme_color # Le bouton s'allume en Cyan ou Violet au survol
            btn_txt_col = (0, 0, 0)
        else:
            btn_bg = (50, 50, 50)
            btn_txt_col = (255, 255, 255)
        
        pygame.draw.rect(self.screen, btn_bg, self.button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.button_rect, 2, border_radius=10)
        
        btn_txt = self.stat_font.render(self.button_text, True, btn_txt_col)
        btn_rect = btn_txt.get_rect(center=self.button_rect.center)
        self.screen.blit(btn_txt, btn_rect)

        pygame.display.flip()