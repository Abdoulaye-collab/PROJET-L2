import pygame
from menu import Menu
from game import Game
from input_name import input_names

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
game = None
in_menu = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_menu:
            menu.handle_event(event)
            if menu.selected == "Jouer":
                game = Game(screen)
                game.player.name = player_name
                game.enemy.name = ai_name
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
