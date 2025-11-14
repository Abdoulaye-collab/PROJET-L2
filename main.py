# main.py
import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from menu import MainMenuView

def main():
    # Crée la fenêtre principale
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # Affiche le menu principal
    menu_view = MainMenuView()
    window.show_view(menu_view)

    # Lance la boucle principale
    arcade.run()

if __name__ == "__main__":
    main()







