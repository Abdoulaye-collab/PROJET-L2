import pygame
import random
from player import Player, ALL_CARDS
from settings import CARDS_ENABLED
from ai_llm import get_ai_move
from ai_personalities import AI_PERSONALITIES, get_ai_phrase

CELL_SIZE = 40
GRID_SIZE = 10
GRID_OFFSET_X_PLAYER = 50
GRID_OFFSET_X_ENEMY = 500
GRID_OFFSET_Y = 100

PROJECTILE_SPEED = 15  # vitesse de la boule pour animation tir

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player("Joueur")
        self.enemy = Player("IA")
        self.turn_count = 1
        self.winner = None
        self.font = pygame.font.SysFont("Arial", 25)
        self.title_font = pygame.font.SysFont("Arial", 30)
        self.selected_card = None
        self.awaiting_target = False

        # IA personnalité
        self.ai_personality = "Gentille"
        self.ai_phrase_to_display = ""

        # tirs supplémentaires (Double Tir)
        self.extra_shot = 0

        # Animation de tir
        self.projectile = None  # dict : {"shooter": player, "target": (row, col), "pos": (x,y), "color": (r,g,b)}

        # Timer IA
        self.ia_delay = 0
        self.ia_pending = False

        # Tour du joueur ou de l'IA
        self.player_turn = True
        self.text_status = f"Tour de {self.player.name} !"

    # ------------------------ CARTES ------------------------
    def ship_positions_hit(self, player, row, col):
        for ship, positions in player.ship_positions.items():
            if (row, col) in positions:
                positions.remove((row, col))
                break

    def play_card(self, player, card_name, target_row=None, target_col=None):
        if not CARDS_ENABLED or target_row is None or target_col is None:
            return

        enemy = self.enemy if player == self.player else self.player

        if card_name == "50:50":
            chance = random.random()
            target = enemy if chance < 0.5 else player
            if target.grid[target_row][target_col] == 1:
                target.grid[target_row][target_col] = -1
                self.ship_positions_hit(target, target_row, target_col)
                if target == enemy:
                    player.hits += 1
                else:
                    enemy.hits += 1

        elif card_name == "Juge":
            if player.hits >= enemy.hits:
                if enemy.grid[target_row][target_col] == 1:
                    enemy.grid[target_row][target_col] = -1
                    self.ship_positions_hit(enemy, target_row, target_col)
                    player.hits += 1
            else:
                for ship, positions in player.ship_positions.items():
                    if positions:
                        r, c = positions[0]
                        if player.grid[r][c] == 1:
                            player.grid[r][c] = -1
                            self.ship_positions_hit(player, r, c)
                        break

        elif card_name == "END":
            if self.turn_count <= 2 and player.hits >= 3:
                self.winner = player
            else:
                for ship, positions in player.ship_positions.items():
                    if ship not in player.reinforced_ships and positions:
                        player.reinforced_ships.append(ship)
                        break

        elif card_name == "Double Tir":
            self.extra_shot = max(self.extra_shot, 1)
            self.shoot(player, target_row, target_col)

    # ------------------------ TIRS ------------------------
    def shoot(self, shooter, row, col):
        target = self.enemy if shooter == self.player else self.player
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return "Invalid"

        val = target.grid[row][col]

        # Init animation projectile
        start_x = GRID_OFFSET_X_PLAYER + CELL_SIZE*5 if shooter == self.player else GRID_OFFSET_X_ENEMY + CELL_SIZE*5
        start_y = GRID_OFFSET_Y + CELL_SIZE*5
        proj_color = (255, 0, 0) if shooter == self.player else (255, 255, 0)
        self.projectile = {"shooter": shooter, "target": (row, col), "pos": [start_x, start_y], "color": proj_color}

        if val == 1:
            for ship, pos in target.ship_positions.items():
                if (row, col) in pos and ship in target.reinforced_ships:
                    target.reinforced_ships.remove(ship)
                    return "Renforcé"

            target.grid[row][col] = -1
            self.ship_positions_hit(target, row, col)
            shooter.hits += 1
            self.check_victory()
            return "Touché"

        elif val == 0:
            target.grid[row][col] = -2
            return "Manqué"

        return "Déjà tiré"

    def check_victory(self):
        for p in [self.player, self.enemy]:
            if all(len(pos) == 0 for pos in p.ship_positions.values()):
                self.winner = self.enemy if p == self.player else self.player

    # ------------------------ IA ------------------------
    def ai_play(self):
        if self.winner:
            return
        personality_style = AI_PERSONALITIES[self.ai_personality]["style"]
        row, col = get_ai_move(self.player.grid, personality_style)
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            available = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.player.grid[r][c] in [0, 1]]
            if not available:
                return
            row, col = random.choice(available)

        result = self.shoot(self.enemy, row, col)
        # Phrase IA selon résultat
        if result in ("Touché", "Renforcé"):
            self.ai_phrase_to_display = get_ai_phrase(self.ai_personality, "hit")
        else:
            self.ai_phrase_to_display = get_ai_phrase(self.ai_personality, "miss")

        self.turn_count += 1
        self.player_turn = True
        self.text_status = f"Tour de {self.player.name} !"

    # ------------------------ ÉVÉNEMENTS ------------------------
    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or self.winner:
            return
        x, y = event.pos

        # cartes
        card_x, card_y = 50, 520
        for card in self.player.cards:
            rect = pygame.Rect(card_x, card_y, 120, 40)
            if rect.collidepoint(x, y):
                if CARDS_ENABLED:
                    self.selected_card = card
                    self.awaiting_target = True
                break
            card_x += 130

        if self.selected_card and self.awaiting_target:
            col = (x - GRID_OFFSET_X_ENEMY) // CELL_SIZE
            row = (y - GRID_OFFSET_Y) // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                self.play_card(self.player, self.selected_card, row, col)
                if self.selected_card in self.player.cards:
                    self.player.cards.remove(self.selected_card)
                self.selected_card = None
                self.awaiting_target = False
            return

        # tir normal (vérifie que c’est bien le tour du joueur)
        if self.player_turn:
            col = (x - GRID_OFFSET_X_ENEMY) // CELL_SIZE
            row = (y - GRID_OFFSET_Y) // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                self.shoot(self.player, row, col)
                if self.extra_shot > 0:
                    self.extra_shot -= 1
                else:
                    self.player_turn = False
                    self.text_status = "Tour de l'IA..."
                    # délai avant IA
                    self.ia_delay = 250
                    self.ia_pending = True

    # ------------------------ UPDATE ------------------------
    def update(self):
        # texte dynamique déjà mis à jour dans ai_play et handle_event
        # gestion animation projectile
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

        # gestion timer IA
        if self.ia_pending and not self.projectile:
            if self.ia_delay > 0:
                self.ia_delay -= 16
            else:
                self.ai_play()
                self.ia_pending = False

    # ------------------------ DESSIN ------------------------
    def draw_grid(self, player, offset_x, show_ships=True):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(offset_x + col*CELL_SIZE, GRID_OFFSET_Y + row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                val = player.grid[row][col]
                if val == 0:
                    color = (0,105,148)
                elif val == 1:
                    color = (105,105,105) if show_ships else (0,105,148)
                elif val == -1:
                    color = (255,0,0)
                elif val == -2:
                    color = (0,105,148)  # pas de changement couleur
                else:
                    color = (0,105,148)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)

                # croix noire sur eau touchée
                if val == -2:
                    start = (rect.left + 5, rect.top + 5)
                    end = (rect.right - 5, rect.bottom - 5)
                    pygame.draw.line(self.screen, (0,0,0), start, end, 2)
                    start2 = (rect.left + 5, rect.bottom - 5)
                    end2 = (rect.right - 5, rect.top + 5)
                    pygame.draw.line(self.screen, (0,0,0), start2, end2, 2)

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
        self.screen.fill((0,105,148))
        self.draw_grid(self.player, GRID_OFFSET_X_PLAYER, show_ships=True)
        self.draw_grid(self.enemy, GRID_OFFSET_X_ENEMY, show_ships=False)
        self.draw_cards(self.player)

        # noms
        name_player = self.title_font.render(self.player.name, True, (255,255,255))
        name_enemy = self.title_font.render(self.enemy.name, True, (255,255,255))
        self.screen.blit(name_player, (GRID_OFFSET_X_PLAYER, GRID_OFFSET_Y - 40))
        self.screen.blit(name_enemy, (GRID_OFFSET_X_ENEMY, GRID_OFFSET_Y - 40))

        # phrase IA
        if self.ai_phrase_to_display:
            phrase_surf = self.font.render(self.ai_phrase_to_display, True, (255,255,255))
            self.screen.blit(phrase_surf, (GRID_OFFSET_X_ENEMY + name_enemy.get_width() + 10, GRID_OFFSET_Y - 40))

        # texte dynamique tour (décalé légèrement à droite)
        status_surf = self.font.render(getattr(self, "text_status", ""), True, (0,255,0) if self.player_turn else (255,0,0))
        self.screen.blit(status_surf, (80, 20))

        # animation projectile
        if self.projectile:
            pygame.draw.circle(self.screen, self.projectile["color"], (int(self.projectile["pos"][0]), int(self.projectile["pos"][1])), 8)

        # victoire
        if self.winner:
            msg = self.title_font.render(f"{self.winner.name} a gagné !", True, (255,255,0))
            self.screen.blit(msg, (200, 100))




