# game.py
import pygame
from player import Player
import random

CELL_SIZE = 40
GRID_SIZE = 10
GRID_SPACING = 20

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.top_y = 100
        self.left_grid_x = 50
        self.right_grid_x = self.left_grid_x + GRID_SIZE*CELL_SIZE + GRID_SPACING

        self.player = Player("Joueur")
        self.enemy = Player("IA")
        self.player.place_random_ships()
        self.enemy.place_random_ships()
        
        self.turn = "player"
        self.game_over = False

        # Cartes spéciales
        self.double_shot_active = False
        self.shield_active = False
        self.revealed_cells = []

    def handle_event(self, event):
        if self.game_over:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Clic sur cartes
            for i, card in enumerate(self.player.cards):
                rect = pygame.Rect(50 + i*150, 500, 140, 40)
                if rect.collidepoint(event.pos):
                    self.use_card(card)
                    return

            # Clic sur grille ennemie
            if self.turn == "player":
                if (self.right_grid_x <= x < self.right_grid_x + GRID_SIZE*CELL_SIZE) and \
                   (self.top_y <= y < self.top_y + GRID_SIZE*CELL_SIZE):
                    col = (x - self.right_grid_x) // CELL_SIZE
                    row = (y - self.top_y) // CELL_SIZE
                    self.attack(self.enemy, row, col)
                    if self.double_shot_active:
                        self.double_shot_active = False
                    else:
                        if not self.game_over:
                            self.turn = "enemy"

    def use_card(self, card_name):
        if card_name == "Double Tir":
            self.double_shot_active = True
            self.player.cards.remove(card_name)
        elif card_name == "Radar":
            self.activate_radar()
            self.player.cards.remove(card_name)
        elif card_name == "Bouclier":
            self.shield_active = True
            self.player.cards.remove(card_name)

    def activate_radar(self):
        row = random.randint(1, GRID_SIZE-2)
        col = random.randint(1, GRID_SIZE-2)
        self.revealed_cells = [(r,c) for r in range(row-1,row+2) for c in range(col-1,col+2)]

    def attack(self, target, row, col):
        if target == self.player and self.shield_active and target.grid[row][col] == 1:
            self.shield_active = False
            return

        if target.grid[row][col] == 1:
            target.grid[row][col] = 2
        elif target.grid[row][col] == 0:
            target.grid[row][col] = -1

        winner = self.check_victory()
        if winner:
            self.game_over = True
            self.show_victory_message(winner)

    def enemy_turn(self):
        if self.game_over or self.turn != "enemy":
            return
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        while self.player.grid[row][col] in [2, -1]:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
        self.attack(self.player, row, col)
        if not self.game_over:
            self.turn = "player"

    def check_victory(self):
        player_ships = sum(cell == 1 for row in self.player.grid for cell in row)
        enemy_ships = sum(cell == 1 for row in self.enemy.grid for cell in row)
        if player_ships == 0:
            return self.enemy.name
        elif enemy_ships == 0:
            return self.player.name
        else:
            return None

    def show_victory_message(self, winner):
        font = pygame.font.SysFont("Arial", 60)
        text_surf = font.render(f"🎉 {winner} a gagné ! 🎉", True, (255,255,0))
        text_rect = text_surf.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(text_surf, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    def draw_grid(self, grid, x_offset, is_enemy=False):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(
                    x_offset + col*CELL_SIZE,
                    self.top_y + row*CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                color = (200,200,200)
                if grid[row][col] == 1 and not is_enemy:
                    color = (0,255,0)
                elif grid[row][col] == 2:
                    color = (255,0,0)
                elif grid[row][col] == -1:
                    color = (0,0,255)
                if is_enemy and grid[row][col] == 1 and (row,col) in self.revealed_cells:
                    color = (0,255,0)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)

    def draw_cards(self):
        font = pygame.font.SysFont("Arial", 25)
        for i, card in enumerate(self.player.cards):
            rect = pygame.Rect(50 + i*150, 500, 140, 40)
            pygame.draw.rect(self.screen, (255,255,0), rect)
            pygame.draw.rect(self.screen, (0,0,0), rect, 2)
            text_surf = font.render(card, True, (0,0,0))
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)

    def draw_names(self):
        font = pygame.font.SysFont("Arial", 30)
        # Titre du jeu
        game_title = font.render("WIZARDS BATTLESHIP", True, (255, 255, 0))
        self.screen.blit(game_title, (self.screen.get_width()//2 - game_title.get_width()//2, 20))
        # Noms joueurs
        player_surf = font.render(self.player.name, True, (255,255,255))
        enemy_surf = font.render(self.enemy.name, True, (255,255,255))
        self.screen.blit(player_surf, (self.left_grid_x, self.top_y-40))
        self.screen.blit(enemy_surf, (self.right_grid_x, self.top_y-40))

    def update(self):
        self.enemy_turn()

    def draw(self):
        self.draw_grid(self.player.grid, self.left_grid_x)
        self.draw_grid(self.enemy.grid, self.right_grid_x, is_enemy=True)
        pygame.draw.line(
            self.screen, (0,0,0),
            (self.left_grid_x + GRID_SIZE*CELL_SIZE + GRID_SPACING//2, self.top_y),
            (self.left_grid_x + GRID_SIZE*CELL_SIZE + GRID_SPACING//2, self.top_y + GRID_SIZE*CELL_SIZE),
            3
        )
        self.draw_cards()
        self.draw_names()
