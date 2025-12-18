import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_UI_BACKGROUND, COLOR_TEXT_MAGIC, FONT_NAME

class GameOver:
    def __init__(self, screen, winner_name, loser_name, game_time_seconds):
        print("--- DEBUG GAMEOVER INIT ---")
        print(f"Reçu Winner: {winner_name}")
        print(f"Reçu Loser: {loser_name}")
        # ----------------
        self.screen = screen
        self.game_time_seconds = game_time_seconds
        if hasattr(winner_name, 'name'):
            self.winner_name = winner_name.name
        else:
            self.winner_name = str(winner_name)

        if hasattr(loser_name, 'name'):
            self.loser_name = loser_name.name
        else:
            self.loser_name = str(loser_name)
        
        print(f"FINAL self.winner_name = {self.winner_name}")
        print(f"FINAL self.loser_name = {self.loser_name}")
        print("---------------------------")
        # ----------------
        
        # --- POLICES ---
        self.title_font = pygame.font.Font(FONT_NAME, 70)
        self.stat_font = pygame.font.SysFont("Verdana", 25)
        self.info_font = pygame.font.SysFont("Verdana", 20)

    # --- BOUTONS (pour revenir au menu) ---
        self.button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT - 100, 
            200, 
            50
        )
        self.button_text = "Retour au Menu"
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.done = True # Signal pour revenir au menu

    def draw(self):
        self.screen.fill(COLOR_UI_BACKGROUND)
        center_x = SCREEN_WIDTH // 2
        
        # --------------------- 1. TITRE DE VICTOIRE ---------------------
        
        title_text = f"Victoire de {self.winner_name} !"
        title_surf = self.title_font.render(title_text, True, COLOR_TEXT_MAGIC)
        title_rect = title_surf.get_rect(center=(center_x, 80))
        
        # Ajout d'une ombre (effet magique)
        SHADOW_COLOR = (150, 0, 200) 
        shadow_rect = title_surf.get_rect(center=(center_x + 3, 83))
        self.screen.blit(self.title_font.render(title_text, True, SHADOW_COLOR), shadow_rect)
        
        self.screen.blit(title_surf, title_rect)
        
        # --------------------- 2. PANNEAU DE STATISTIQUES ---------------------
        
        PANEL_Y = 150
        PANEL_HEIGHT = 250
        PANEL_RECT = pygame.Rect(
            center_x - 300, 
            PANEL_Y, 
            600, 
            PANEL_HEIGHT
        )
        
        # Dessin du panneau (Fond différent pour le contraste)
        pygame.draw.rect(self.screen, (70, 80, 110), PANEL_RECT)
        pygame.draw.rect(self.screen, COLOR_TEXT_MAGIC, PANEL_RECT, 3) # Bordure dorée
        
        stat_y = PANEL_Y + 30
        
        # Conversion du temps de jeu en format lisible H:MM:SS
        seconds = self.game_time_seconds % 60
        minutes = (self.game_time_seconds // 60) % 60
        hours = self.game_time_seconds // 3600
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

        # --- Affichage des Statistiques ---
        stats = [
            ("Décret Arcanique :", f" {self.winner_name} a vaincu !"),
            ("Adversaire Vaincu :", self.loser_name),
            ("Durée du Conflit :", time_str),
            # Ajoutez ici d'autres stats futures (ex: Tirs Manqués, Cartes Utilisées)
        ]
        
        for label, value in stats:
            label_surf = self.stat_font.render(label, True, COLOR_TEXT_MAGIC)
            value_surf = self.stat_font.render(value, True, (255, 255, 255))
            
            # Affichage de la colonne de gauche (Label)
            self.screen.blit(label_surf, (PANEL_RECT.x + 20, stat_y))
            
            # Affichage de la colonne de droite (Valeur)
            value_rect = value_surf.get_rect(right=PANEL_RECT.right - 20, y=stat_y)
            self.screen.blit(value_surf, value_rect)
            
            stat_y += 50
            
        # --------------------- 3. BOUTON RETOUR AU MENU ---------------------
        
        mouse_pos = pygame.mouse.get_pos()
        COLOR_BUTTON_FILL = (180, 180, 180)
        COLOR_BUTTON_HOVER = COLOR_TEXT_MAGIC
        
        pygame.draw.rect(self.screen, COLOR_BUTTON_FILL, self.button_rect)
        
        # Effet de survol
        border_color = COLOR_BUTTON_HOVER if self.button_rect.collidepoint(mouse_pos) else (0, 0, 0)
        pygame.draw.rect(self.screen, border_color, self.button_rect, 3)
        
        # Texte du bouton
        text_surf = self.stat_font.render(self.button_text, True, (10, 25, 75)) # Texte en Bleu Nuit
        text_rect = text_surf.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surf, text_rect)

        pygame.display.flip()