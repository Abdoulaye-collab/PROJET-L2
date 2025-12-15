import pygame
import time
import sys
from menu import Menu
from game import Game, load_assets
from input_name import input_names
from player import Player
from placement import Placement
from settings import COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC,SCREEN_WIDTH, SCREEN_HEIGHT,CELL_SIZE
from GameOver import GameOver

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wizards Battleship")
clock = pygame.time.Clock()
FPS = 30

GAME_ASSETS = load_assets(CELL_SIZE)

# Saisie des noms
player_name, ai_name = input_names(screen)
if not player_name:
    pygame.quit()
    exit()

player = Player(player_name)
enemy = Player(ai_name)
menu = Menu(screen)
in_menu = True
in_game = False
game_over_screen = None
game = None

running = True
while running:
    if in_menu and menu.selected is None:
        menu = Menu(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_menu:
            menu.handle_event(event)
        elif game_over_screen:
            game_over_screen.handle_event(event)
        elif game:
            game.handle_event(event)

    if in_menu and menu.selected == "Jouer":
    
        # Création du joueur et placement manuel
        enemy.place_random_ships()
        placement_screen = Placement(screen, player,GAME_ASSETS)
        placing = True

        while placing:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                placement_screen.handle_event(ev)

            placement_screen.draw()
            pygame.display.flip()
            clock.tick(FPS)
            placing = not placement_screen.done

        player = placement_screen.player

        game = Game(screen,GAME_ASSETS)
        game.player = player
        game.enemy = enemy
        game.start_time = pygame.time.get_ticks()
                
        in_menu = False
        menu.selected = None

    elif in_menu and menu.selected == "Quitter":
        running = False
        
    if game and game.game_over:
        end_time = pygame.time.get_ticks()
        total_time_seconds = (end_time - game.start_time) // 1000

        winner = game.winner
        loser = game.enemy.name if winner == game.player.name else game.player.name

        game_over_screen = GameOver(screen, winner, loser, total_time_seconds)
        game = None
        
    if game_over_screen and game_over_screen.done:
        in_menu = True
        game_over_screen = None


    if in_menu:
        menu.draw()
    elif game_over_screen:
        game_over_screen.draw()
    elif game:
        screen.fill(COLOR_OCEAN_DARK)
        game.update()
        game.draw() 

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
