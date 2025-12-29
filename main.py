import pygame
import time
import sys
from menu import Menu
from game import Game
from input_name import input_names
from player import Player
from placement import Placement
from settings import COLOR_OCEAN_DARK, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE
from GameOver import GameOver
from utils import transition_fade, fade_in_action


# ====================================================================
#  INITIALISATION
# ====================================================================
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wizards Battleship")
clock = pygame.time.Clock()
FPS = 30

game = Game(screen, {})

# --- ETAT DU JEU ---
menu = Menu(screen)
in_menu = True
in_game = False
game_over_screen = None
game = None

# Intro stylée au lancement
fade_in_action(screen, menu.draw)

running = True
while running:
    
    # Gestion des événements globaux
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if in_menu:
            menu.handle_event(event)
        elif game_over_screen:
            game_over_screen.handle_event(event)
        elif game:
            game.handle_event(event)

    # =================================================================
    # LOGIQUE PRINCIPALE (CHANGEMENTS D'ÉTATS)
    # =================================================================
    
    # 1. MENU -> JOUER
    if in_menu and menu.selected == "Jouer":
        
        transition_fade(screen) 
        
        names = input_names(screen) 
        
        if not names: 
            running = False
            break
            
        player_name, ai_name = names
        
        # Placement
        player = Player(player_name)
        enemy = Player(ai_name)
        enemy.place_random_ships()
        
        placement_screen = Placement(screen, player, {})
        
        # Fade In sur le Placement
        fade_in_action(screen, placement_screen.draw)

        # Boucle de placement
        placing = True
        while placing:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                placement_screen.handle_event(ev)

            placement_screen.draw()
            pygame.display.flip()
            clock.tick(FPS)
            placing = not placement_screen.done

        # Fin Placement -> Lancement Jeu
        transition_fade(screen)

        player = placement_screen.player 
        game = Game(screen, {})
        game.player = player
        game.enemy = enemy
        game.start_time = pygame.time.get_ticks()
        
        # Petite fonction pour dessiner le jeu au démarrage (pour le fade in)
        def draw_game_start():
            screen.fill(COLOR_OCEAN_DARK)
            game.draw()
            
        fade_in_action(screen, draw_game_start)
                
        in_menu = False
        menu.selected = None

    # 2. MENU -> QUITTER
    elif in_menu and menu.selected == "Quitter":
        transition_fade(screen)
        running = False
        
# 3. JEU -> GAME OVER
    # On vérifie "game" d'abord pour éviter les erreurs si game est None
    if game and game.game_over:
        
        # 1. On lance la transition noire TOUT DE SUITE
        transition_fade(screen)
        
        # 2. PENDANT que l'écran est noir, on prépare la suite
        # Calcul des stats
        end_time = pygame.time.get_ticks()
        total_time_seconds = (end_time - game.start_time) // 1000
        
        is_player_win = (game.winner == game.player)
        winner_obj = game.player if is_player_win else game.enemy
        loser_obj = game.enemy if is_player_win else game.player

        # Création de l'écran de fin
        game_over_screen = GameOver(
            screen, 
            winner_obj, loser_obj, 
            total_time_seconds, 
            game.cards_played_total,
            is_player_win
        )
        
        # 3. CRUCIAL : On détruit l'objet game pour arrêter d'entrer dans ce if
        game = None 
        
        # 4. On lance l'ouverture (Fade In) sur l'écran de victoire
        fade_in_action(screen, game_over_screen.draw)
        
        # Petite sécurité : on vide encore les événements
        pygame.event.clear()
        
# 4. GAME OVER -> RETOUR MENU
    if game_over_screen and game_over_screen.done:
        
        # 1. Transition noire
        transition_fade(screen)
        
        # 2. On détruit l'écran de fin et on remet le menu
        game_over_screen = None 
        in_menu = True
        
        # On recrée un menu tout neuf
        menu = Menu(screen) 
        menu.selected = None # On s'assure qu'aucun bouton n'est pré-sélectionné
        
        # 3. Ouverture (Fade In) sur le menu
        fade_in_action(screen, menu.draw)
        
        pygame.event.clear()

    # =================================================================
    # BOUCLE D'AFFICHAGE STANDARD
    # =================================================================
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