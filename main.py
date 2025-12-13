import pygame
from menu import Menu
#from game import Game
from input_name import input_names
from player import Player
from placement import Placement
from settings import COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC,SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wizards Battleship")
clock = pygame.time.Clock()
FPS = 30

# Saisie des noms
player_name, ai_name = input_names(screen)
if not player_name:
    pygame.quit()
    exit()

menu = Menu(screen)
in_menu = True
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
            if menu.selected == "Jouer":
                from game import Game
                # Création du joueur et placement manuel
                player = Player(player_name)
                placement_screen = Placement(screen, player)
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
                # Création du jeu avec joueur et IA
                game = Game(screen)
                game.player = player
                game.enemy.name = ai_name
                game.enemy.place_random_ships()
                in_menu = False
            elif menu.selected == "Quitter":
                running = False
        else:
            game.handle_event(event)

    if in_menu:
        menu.draw()
    else:
        screen.fill(COLOR_OCEAN_DARK)
        game.update()
        game.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
