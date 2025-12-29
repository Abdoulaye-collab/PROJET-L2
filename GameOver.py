import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_NAME_GRIMOIRE,FONT_NAME

class GameOver:
    """
    Écran de fin de partie.
    Affiche le vainqueur, les statistiques et propose de revenir au menu.
    Adapte ses couleurs selon si c'est une Victoire (Cyan) ou une Défaite (Violet).
    """
    def __init__(self, screen, winner_name, loser_name, game_time_seconds, cards_count, is_player_victory):
        self.screen = screen
        self.game_time_seconds = game_time_seconds
        self.cards_count = cards_count
        self.is_player_victory = is_player_victory
        
        # --- GESTION DES NOMS (Objet Player ou String) ---
        if hasattr(winner_name, 'name'):
            self.winner_name = winner_name.name
        else:
            self.winner_name = str(winner_name)

        if hasattr(loser_name, 'name'):
            self.loser_name = loser_name.name
        else:
            self.loser_name = str(loser_name)
        
        # --- CHARGEMENT DES IMAGES DE FOND (Sécurisé) ---
        def load_bg(filename):
            try:
                img = pygame.image.load("assets/images/gagnant.png").convert()
                img = pygame.image.load("assets/images/perdant.png").convert()
                return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                print(f" Image manquante : {filename}")
                return None
            
        self.victory_img = load_bg("gagnant.png")
        self.defeat_img = load_bg("perdant.png")

        # --- POLICES ---
        self.title_font = pygame.font.Font(FONT_NAME_GRIMOIRE, 90) # Très gros titre
        self.stat_font = pygame.font.SysFont("Verdana", 24)

        # --- BOUTON "RETOUR" ---
        self.button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT - 120, 260, 60)
        self.button_text = "Retour au Menu"
        self.done = False

    def handle_event(self, event):
        """Gère le clic sur le bouton de retour."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.done = True

    def draw(self):
        """Affiche l'écran de fin."""
        center_x = SCREEN_WIDTH // 2

        # 1. CONFIGURATION DU THÈME (Couleurs & Textes)
        if self.is_player_victory:
            # --- THÈME VICTOIRE (CYAN / VICTOIRE) ---
            main_title = "VICTOIRE !"
            sub_title = "L'océan est sous votre contrôle."
            theme_color = (0, 255, 255)       
            shadow_color = (0, 100, 100)      
            bg_fallback = (0, 50, 50)         
            current_bg_img = self.victory_img
            
        else:
            # --- THÈME DEFAITE(VIOLET / DÉFAITE) ---
            main_title = "DÉFAITE..."
            sub_title = "Sombré dans les abysses..."
            theme_color = (180, 50, 255)      
            shadow_color = (50, 0, 80)        
            bg_fallback = (30, 0, 30)         
            current_bg_img = self.defeat_img

        # 2. DESSIN DU FOND
        if current_bg_img:
            self.screen.blit(current_bg_img, (0, 0))
            # Voile sombre pour lisibilité
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(100) # Transparence (0-255)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0,0))
        else:
            self.screen.fill(bg_fallback)

        # 3. TITRES
        # Ombre
        shadow_surf = self.title_font.render(main_title, True, shadow_color)
        self.screen.blit(shadow_surf, (center_x - shadow_surf.get_width()//2 + 5, 85))
        
        # Titre Principal
        title_surf = self.title_font.render(main_title, True, theme_color)
        self.screen.blit(title_surf, (center_x - title_surf.get_width()//2, 80))

        # Sous-titre
        sub_surf = self.stat_font.render(sub_title, True, (220, 220, 220))
        self.screen.blit(sub_surf, (center_x - sub_surf.get_width()//2, 210))
        
        # 4. PANNEAU DE STATISTIQUES
        PANEL_WIDTH = 450
        PANEL_Y = 290
        PANEL_HEIGHT = 250
        start_x = center_x - (PANEL_WIDTH // 2)
        PANEL_RECT = pygame.Rect(start_x, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT)
        
        # Fond du panneau (Noir semi-transparent)
        s = pygame.Surface((PANEL_RECT.width, PANEL_RECT.height))
        s.set_alpha(180) 
        s.fill((0, 0, 0))
        self.screen.blit(s, (PANEL_RECT.x, PANEL_RECT.y))
        
        # Bordure colorée
        pygame.draw.rect(self.screen, theme_color, PANEL_RECT, 2, border_radius=15)
        
        # Calcul temps (Minutes:Secondes)
        m = (self.game_time_seconds // 60) % 60
        s = self.game_time_seconds % 60
        time_str = f"{int(m)} min {int(s)} s"

        stats_list = [
            ("Vainqueur :", self.winner_name),
            ("Perdant :", self.loser_name),
            ("Sortilèges joués :", str(self.cards_count)),
            ("Durée :", time_str)
        ]
        
        current_y = PANEL_Y + 30
        line_spacing = 45
        side_margin = 30

        for label, value in stats_list:
            # Libellé (Gris clair)
            lbl = self.stat_font.render(label, True, (180, 180, 180))
            self.screen.blit(lbl, (PANEL_RECT.x + side_margin, current_y))
            
            # Valeur (Coloriée selon le thème)
            val = self.stat_font.render(value, True, theme_color) 
            val_rect = val.get_rect(right=PANEL_RECT.right - side_margin, top=current_y)
            self.screen.blit(val, val_rect)
            
            current_y += line_spacing
            
        # 5. BOUTON RETOUR
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