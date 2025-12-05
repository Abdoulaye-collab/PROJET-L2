import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)
        self.title_font = pygame.font.SysFont("Arial", 60)
        self.subtitle_font = pygame.font.SysFont("Arial", 20)
        self.subtitle_text = "Un jeu de stratégie magique par Abdoulaye et Shelly !"  # Modifier ici pour changer le sous-titre
        self.buttons = [
            {"text": "Jouer", "rect": pygame.Rect(300, 200, 200, 50)},
            {"text": "Options", "rect": pygame.Rect(300, 300, 200, 50)},
            {"text": "Quitter", "rect": pygame.Rect(300, 400, 200, 50)},
        ]
        self.selected = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    self.selected = button["text"]

    def draw(self):
        self.screen.fill((0, 105, 148))

        # Titre du jeu
        title_surf = self.title_font.render("WIZARDS BATTLESHIP", True, (255, 255, 0))
        title_rect = title_surf.get_rect(center=(self.screen.get_width()//2, 100))
        self.screen.blit(title_surf, title_rect)

        # Sous-titre en bas à gauche
        subtitle_surf = self.subtitle_font.render(self.subtitle_text, True, (255, 255, 255))
        self.screen.blit(subtitle_surf, (10, self.screen.get_height() - 30))

        # Boutons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            rect = button["rect"]
            color = (200,200,255) if rect.collidepoint(mouse_pos) else (255,255,255)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0,0,0), rect, 3)
            text_surf = self.font.render(button["text"], True, (0,0,0))
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
