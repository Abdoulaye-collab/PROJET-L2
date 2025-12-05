import pygame
from menu import Menu
from game import Game
from input_name import input_names
from player import Player
from placement import Placement

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WIZARDS BATTLESHIP")
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_menu:
            menu.handle_event(event)
            if menu.selected == "Jouer":
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
        screen.fill((0,105,148))
        game.update()
        game.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
