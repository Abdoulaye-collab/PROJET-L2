import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game

class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()

        # Couleur de fond
        self.background_color = arcade.color.DARK_BLUE

        # Textes pré-rendus (rapides)
        self.title_text = arcade.Text(
            "Bataille Navale",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 100,
            arcade.color.WHITE,
            48,
            anchor_x="center"
        )

        self.play_text = arcade.Text(
            "1. Jouer",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.LIGHT_GRAY,
            32,
            anchor_x="center"
        )

        self.quit_text = arcade.Text(
            "2. Quitter",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 60,
            arcade.color.LIGHT_GRAY,
            32,
            anchor_x="center"
        )

    def on_draw(self):
        self.clear(self.background_color)
        self.title_text.draw()
        self.play_text.draw()
        self.quit_text.draw()

    def on_key_press(self, key, modifiers):
        # Touche pour démarrer
        if key in (arcade.key.KEY_1, arcade.key.ENTER):
            game_view = Game()
            self.window.show_view(game_view)

        # Touche pour quitter
        elif key in (arcade.key.KEY_2, arcade.key.ESCAPE):
            arcade.close_window()

    def on_mouse_press(self, x, y, button, modifiers):
        # Clic sur "Jouer"
        if SCREEN_WIDTH/2 - 100 < x < SCREEN_WIDTH/2 + 100 and SCREEN_HEIGHT/2 - 15 < y < SCREEN_HEIGHT/2 + 15:
            game_view = Game()
            self.window.show_view(game_view)

        # Clic sur "Quitter"
        elif SCREEN_WIDTH/2 - 100 < x < SCREEN_WIDTH/2 + 100 and SCREEN_HEIGHT/2 - 75 < y < SCREEN_HEIGHT/2 - 45:
            arcade.close_window()
