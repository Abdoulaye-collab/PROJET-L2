import pygame
from settings import COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, BUTTON_WIDTH, BUTTON_CENTER_X as CENTER_X,FONT_NAME

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(FONT_NAME, 40)
        self.title_font = pygame.font.Font(FONT_NAME, 60)
        self.subtitle_font = pygame.font.Font(FONT_NAME, 20)
        self.subtitle_text = "Un jeu de stratégie magique par Abdoulaye et Shelly !"  # Modifier ici pour changer le sous-titre
        self.buttons = [
            {"text": "Jouer", "rect": pygame.Rect(CENTER_X, 200, BUTTON_WIDTH, 50)},
            {"text": "Options", "rect": pygame.Rect(CENTER_X, 300, BUTTON_WIDTH, 50)},
            {"text": "Quitter", "rect": pygame.Rect(CENTER_X, 400, BUTTON_WIDTH, 50)},
        ]
        self.selected = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    self.selected = button["text"]

    def draw(self):
        self.screen.fill(COLOR_OCEAN_DARK)

        # Titre du jeu
        title_surf = self.title_font.render("Wizards Battleship", True, COLOR_TEXT_MAGIC)
        title_rect = title_surf.get_rect(center=(self.screen.get_width()//2, 100))
         # Ajout d'une ombre (effet magique)
        SHADOW_COLOR = (150, 0, 200) 
        shadow_rect = title_surf.get_rect(center=(self.screen.get_width()//2 + 3, 103))
        self.screen.blit(self.title_font.render("Wizards Battleship", True, SHADOW_COLOR), shadow_rect)
        
        self.screen.blit(title_surf, title_rect)

        # Sous-titre en bas à gauche
        subtitle_surf = self.subtitle_font.render(self.subtitle_text, True, (255, 255, 255))
        self.screen.blit(subtitle_surf, (10, self.screen.get_height() - 30))

        # Boutons
        mouse_pos = pygame.mouse.get_pos()

        # Définition des couleurs thématiques pour les boutons
        COLOR_BUTTON_FILL = (180, 180, 180)
        COLOR_BUTTON_INACTIVE = (0, 0, 0) # Gris neutre / Pierre
        COLOR_BUTTON_HOVER = COLOR_TEXT_MAGIC   # Or Magique (au survol)
        COLOR_TEXT_BUTTON = (10, 25, 75)        # Texte en Bleu Nuit (pour contraster)

        for button in self.buttons:
            rect = button["rect"]
            pygame.draw.rect(self.screen, COLOR_BUTTON_FILL, rect)
            if rect.collidepoint(mouse_pos):
                border_color = COLOR_BUTTON_HOVER
            else:
                border_color = COLOR_BUTTON_INACTIVE
            pygame.draw.rect(self.screen, border_color, rect, 3)

            
            text_surf = self.font.render(button["text"], True, COLOR_TEXT_BUTTON) # Texte en Bleu Nuit
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
   
