import pygame
import random
from player import Player, ALL_CARDS
from settings import CARDS_ENABLED, COLOR_TEXT_MAGIC, FONT_NAME, COLOR_UI_BACKGROUND
from ai_llm import get_ai_move
from ai_personalities import AI_PERSONALITIES, get_ai_phrase
from cards import apply_card_effect  # Import de la logique externe
from settings import (
    COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, COLOR_WATER_LIT, 
    COLOR_HIT, COLOR_SHIP, 
    CELL_SIZE, GRID_SIZE,
    GRID_OFFSET_X_PLAYER, GRID_OFFSET_X_ENEMY
)

# CHANGEMENT : GRID_OFFSET_Y réduit pour remonter les grilles
GRID_OFFSET_Y = 105
PROJECTILE_SPEED = 9  

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player("Joueur")
        self.enemy = Player("IA")
        self.turn_count = 1
        self.winner = None
        self.font = pygame.font.Font(FONT_NAME, 25)
        self.title_font = pygame.font.Font(FONT_NAME, 30)
        self.selected_card = None
        self.awaiting_target = False

        self.ai_personality = "Gentille"
        self.ai_phrase_to_display = ""
        self.extra_shot = 0
        self.projectile = None  
        self.ia_delay = 0
        self.ia_pending = False
        self.player_turn = True
        self.text_status = f"Tour de {self.player.name} !"

    def ship_positions_hit(self, player, row, col):
        for ship, positions in player.ship_positions.items():
            if (row, col) in positions:
                positions.remove((row, col))
                break

    def shoot(self, shooter, row, col):
        target = self.enemy if shooter == self.player else self.player
        
        # --- SÉCURITÉ BOUCLIER ---
        if shooter == self.enemy and "Bouclier_Actif" in target.reinforced_ships:
            target.reinforced_ships.remove("Bouclier_Actif")
            self.text_status = "BOUCLIER : Tir ennemi bloqué !"
            return "Bloqué"
            
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return "Invalid"
        
        val = target.board[row][col]

        # --- GESTION VISUELLE DES COULEURS ---
        start_x = GRID_OFFSET_X_PLAYER + CELL_SIZE*5 if shooter == self.player else GRID_OFFSET_X_ENEMY + CELL_SIZE*5
        start_y = GRID_OFFSET_Y + CELL_SIZE*5
        
        # Couleur par défaut (Rouge pour Joueur, Jaune pour IA)
        proj_color = (255, 0, 0) if shooter == self.player else (255, 255, 0)
        
        # Changement de couleur selon la carte active
        if self.selected_card == "Bombe":
            proj_color = (255, 165, 0)  # Orange
        elif self.selected_card == "Salve":
            proj_color = (255, 50, 50)   # Rouge vif / Flash
        elif self.selected_card == "Radar":
            proj_color = (0, 255, 255)   # Cyan / Électrique

        self.projectile = {"shooter": shooter, "target": (row, col), "pos": [start_x, start_y], "color": proj_color}

        # --- LOGIQUE DE TOUCHE ---
        if val == 1:
            for ship, pos in target.ship_positions.items():
                if (row, col) in pos and ship in target.reinforced_ships:
                    target.reinforced_ships.remove(ship)
                    return "Renforcé"
        
            target.board[row][col] = -1
            self.ship_positions_hit(target, row, col)
            shooter.hits += 1
            self.check_victory()
            return "Touché"

        elif val == 0:
            target.board[row][col] = -2
            return "Manqué"

        return "Déjà tiré"

    def check_victory(self):
        for p in [self.player, self.enemy]:
            if all(len(pos) == 0 for pos in p.ship_positions.values()):
                self.winner = self.enemy if p == self.player else self.player

    def ai_play(self):
        if self.winner:
            return
        personality_style = AI_PERSONALITIES[self.ai_personality]["style"]
        row, col = get_ai_move(self.player.board, personality_style)
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            available = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.player.board[r][c] in [0, 1]]
            if not available:
                return
            row, col = random.choice(available)

        result = self.shoot(self.enemy, row, col)
        if result in ("Touché", "Renforcé"):
            self.ai_phrase_to_display = get_ai_phrase(self.ai_personality, "hit")
        else:
            self.ai_phrase_to_display = get_ai_phrase(self.ai_personality, "miss")

        self.turn_count += 1
        self.player_turn = True
        self.text_status = f"Tour de {self.player.name} !"

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or self.winner:
            return
        x, y = event.pos

        # 1. Gestion de la sélection des cartes
        card_x, card_y = 50, 520
        for card in self.player.cards:
            rect = pygame.Rect(card_x, card_y, 120, 40)
            if rect.collidepoint(x, y):
                if CARDS_ENABLED:
                    self.selected_card = card
                    self.awaiting_target = True
                return # On arrête ici pour ne pas tirer en sélectionnant
            card_x += 130

        # 2. Utilisation de l'effet de la carte sélectionnée
        if self.selected_card and self.awaiting_target:
            col = (x - GRID_OFFSET_X_ENEMY) // CELL_SIZE
            row = (y - GRID_OFFSET_Y) // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                apply_card_effect(self, self.selected_card, row, col)
                if self.selected_card in self.player.cards:
                    self.player.cards.remove(self.selected_card)
                self.selected_card = None
                self.awaiting_target = False
                return # INDISPENSABLE : on ne tire pas après avoir utilisé une carte
            return

        # 3. Tir normal (seulement si aucune carte n'est en cours d'usage)
        if self.player_turn:
            col = (x - GRID_OFFSET_X_ENEMY) // CELL_SIZE
            row = (y - GRID_OFFSET_Y) // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                res = self.shoot(self.player, row, col)
                if res != "Déjà tiré":
                    if self.extra_shot > 0:
                        self.extra_shot -= 1
                        # On reste en player_turn = True
                    else:
                        self.player_turn = False
                        self.text_status = "Tour de l'IA..."
                        self.ia_delay = 250
                        self.ia_pending = True

    def update(self):
        if self.projectile:
            target_row, target_col = self.projectile["target"]
            target_x = GRID_OFFSET_X_ENEMY + target_col*CELL_SIZE if self.projectile["shooter"] == self.player else GRID_OFFSET_X_PLAYER + target_col*CELL_SIZE
            target_y = GRID_OFFSET_Y + target_row*CELL_SIZE
            dx = target_x - self.projectile["pos"][0]
            dy = target_y - self.projectile["pos"][1]
            dist = (dx**2 + dy**2)**0.5
            if dist < PROJECTILE_SPEED:
                self.projectile = None
            else:
                self.projectile["pos"][0] += PROJECTILE_SPEED * dx / dist
                self.projectile["pos"][1] += PROJECTILE_SPEED * dy / dist

        if self.ia_pending and not self.projectile:
            if self.ia_delay > 0:
                self.ia_delay -= 16
            else:
                self.ai_play()
                self.ia_pending = False

    def draw_grid(self, player, offset_x, show_ships=True):
        # 1. EFFET VISUEL BOUCLIER (Aura bleue)
        if player == self.player and "Bouclier_Actif" in player.reinforced_ships:
            shield_rect = pygame.Rect(offset_x - 5, GRID_OFFSET_Y - 5, (GRID_SIZE * CELL_SIZE) + 10, (GRID_SIZE * CELL_SIZE) + 10)
            pygame.draw.rect(self.screen, (0, 191, 255), shield_rect, 4, border_radius=5)

        # 2. DESSIN DES CASES
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(offset_x + col*CELL_SIZE, GRID_OFFSET_Y + row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                val = player.board[row][col]
                color = COLOR_OCEAN_DARK
                
                if val == 1:
                    color = COLOR_SHIP if show_ships else COLOR_OCEAN_DARK
                elif val == -1:
                    color = COLOR_HIT
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)

                # Croix pour les tirs manqués
                if val == -2:
                    pygame.draw.line(self.screen, (0,0,0), (rect.left+5, rect.top+5), (rect.right-5, rect.bottom-5), 2)
                    pygame.draw.line(self.screen, (0,0,0), (rect.left+5, rect.bottom-5), (rect.right-5, rect.top+5), 2)

        # 3. AFFICHAGE DES COORDONNÉES (Une seule fois)
        for i in range(GRID_SIZE):
            # Nombres (1 à 10) à gauche de la grille
            num_surf = self.font.render(str(i + 1), True, COLOR_TEXT_MAGIC)
            num_rect = num_surf.get_rect(center=(offset_x - 20, GRID_OFFSET_Y + i * CELL_SIZE + CELL_SIZE // 2))
            self.screen.blit(num_surf, num_rect)
            
            # Lettres (A à J) au-dessus de la grille
            let_surf = self.font.render(chr(65 + i), True, COLOR_TEXT_MAGIC)
            let_rect = let_surf.get_rect(center=(offset_x + i * CELL_SIZE + CELL_SIZE // 2, GRID_OFFSET_Y - 20))
            self.screen.blit(let_surf, let_rect)

    def draw_cards(self, player):
        if not CARDS_ENABLED:
            return
        x, y = 50, 520
        for card in player.cards:
            rect = pygame.Rect(x, y, 120, 40)
            color = (0,255,0) if card == self.selected_card else (255,215,0)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0,0,0), rect, 2)
            text = self.font.render(card, True, (0,0,0))
            self.screen.blit(text, (x+5, y+5))
            x += 130

    def draw(self):
        self.screen.fill(COLOR_UI_BACKGROUND)
        self.draw_grid(self.player, GRID_OFFSET_X_PLAYER, show_ships=True)
        self.draw_grid(self.enemy, GRID_OFFSET_X_ENEMY, show_ships=False)
        self.draw_cards(self.player)

        # Noms au-dessus des grilles
        name_player = self.title_font.render(self.player.name, True, (255,255,255))
        name_enemy = self.title_font.render(self.enemy.name, True, (255,255,255))
        self.screen.blit(name_player, (GRID_OFFSET_X_PLAYER, GRID_OFFSET_Y - 70))
        self.screen.blit(name_enemy, (GRID_OFFSET_X_ENEMY, GRID_OFFSET_Y - 70))

        if self.ai_phrase_to_display:
            phrase_surf = self.font.render(self.ai_phrase_to_display, True, (255,255,255))
            self.screen.blit(phrase_surf, (GRID_OFFSET_X_ENEMY + name_enemy.get_width() + 10, GRID_OFFSET_Y - 50))

        status_surf = self.font.render(self.text_status, True, (0,255,0) if self.player_turn else (255,0,0))
        self.screen.blit(status_surf, (80, 20))

        if self.projectile:
            pygame.draw.circle(self.screen, self.projectile["color"], (int(self.projectile["pos"][0]), int(self.projectile["pos"][1])), 8)

        if self.winner:
            msg = self.title_font.render(f"{self.winner.name} a gagné !", True, (255,255,0))
            self.screen.blit(msg, (200, 100))
