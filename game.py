import arcade
from player import Player
from ai import AI
from constants import GRID_SIZE, CELL_SIZE, OFFSET_X, OFFSET_Y

class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = Player("Joueur")
        self.ai = AI(GRID_SIZE)
        self.turn = "player"
        self.shots = []

    def on_draw(self):
        # Nettoie et prépare le rendu
        self.clear()
        arcade.start_render()

        # Fond (mer)
        arcade.draw_rect_filled(
            self.window.width / 2,
            self.window.height / 2,
            self.window.width,
            self.window.height,
            arcade.color.DARK_BLUE
        )

        # Titre
        arcade.draw_text(
            "Mode Bataille Navale",
            100,
            self.window.height - 80,
            arcade.color.WHITE,
            28,
            bold=True
        )

        # --- Grille ---
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Calcul des coordonnées du centre de chaque case
                center_x = OFFSET_X + col * CELL_SIZE + CELL_SIZE / 2
                center_y = OFFSET_Y + row * CELL_SIZE + CELL_SIZE / 2

                # Case (fond gris clair)
                arcade.draw_solid_rect_filled(
                    center_x, center_y, CELL_SIZE - 2, CELL_SIZE - 2, arcade.color.LIGHT_STEEL_BLUE
                )

                # Contour blanc
                arcade.draw_lrbt_rectangle_outline(
                    center_x - CELL_SIZE / 2,
                    center_x + CELL_SIZE / 2,
                    center_y + CELL_SIZE / 2,
                    center_y - CELL_SIZE / 2,
                    arcade.color.WHITE,
                    border_width=1
                )

        # --- Affichage des tirs ---
        for (x, y, result) in self.shots:
            color = arcade.color.RED if result == "hit" else arcade.color.BLUE
            arcade.draw_circle_filled(
                OFFSET_X + x * CELL_SIZE + CELL_SIZE / 2,
                OFFSET_Y + y * CELL_SIZE + CELL_SIZE / 2,
                6,
                color
            )

        # Texte du tour actuel
        arcade.draw_text(
            f"Tour : {'Joueur' if self.turn == 'player' else 'IA'}",
            100,
            50,
            arcade.color.WHITE,
            16
        )

    def on_mouse_press(self, x, y, _button, _modifiers):
        # Convertir le clic en coordonnées de grille
        col = int((x - OFFSET_X) // CELL_SIZE)
        row = int((y - OFFSET_Y) // CELL_SIZE)

        # Si le joueur clique dans la grille
        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE and self.turn == "player":
            hit = self.ai.receive_shot(col, row)
            self.shots.append((col, row, "hit" if hit else "miss"))
            self.turn = "ai"
            self.ai_turn()

    def ai_turn(self):
        # Tour de l'IA
        x, y = self.ai.play()
        hit = self.player.receive_shot(x, y)
        print(f"L'IA tire sur {x}, {y} : {'touché' if hit else 'raté'}")
        self.turn = "player"

# Fonction principale pour lancer le jeu
def main():
    window = arcade.Window(800, 600, "Bataille Navale")  # Crée une fenêtre de jeu
    game_view = Game()  # Crée l'instance de la vue du jeu
    window.show_view(game_view)  # Affiche la vue du jeu
    arcade.run()  # Lance la boucle principale du jeu

if __name__ == "__main__":
    main()
