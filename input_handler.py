import pygame
from settings import *
from cards import apply_card_effect

# ====================================================================
#  GESTIONNAIRE D'ÉVÉNEMENTS (CONTROLLER)
# ====================================================================
def handle_game_events(game, event):
    """
    Fonction principale qui redirige les événements vers la bonne logique.
    Permet de garder la boucle principale de 'game.py' propre.
    
    Args:
        game: L'instance de la classe Game (pour accéder aux données).
        event: L'événement Pygame capturé (Clic, Touche, etc.).
    """
    
    # 1. GESTION DE L'ÉCRAN DE FIN (VICTOIRE / DÉFAITE)
    # Si la partie est finie, on passe les clics au bouton "Retour Menu"
    if game.game_over and game.game_over_screen:
        game.game_over_screen.handle_event(event)
        if game.game_over_screen.done:
            game.winner = "MENU"
        return

    # 2. GESTION DU JEU (CLICS SOURIS)
    if event.type == pygame.MOUSEBUTTONDOWN and not game.winner:
        mouse_x, mouse_y = event.pos
        
        # --- A. Clic sur les CARTES ---
        handle_card_click(game, mouse_x, mouse_y)
        
        # --- B. Clic sur la GRILLE IA ---
        handle_grid_click(game, mouse_x, mouse_y)

# ====================================================================
#  FONCTIONS INTERNES (PRIVATE HELPERS)
# ====================================================================
def handle_card_click(game, x, y):
    """
    Vérifie si le joueur clique sur une de ses cartes.
    Gère la sélection et la désélection (Toggle).
    Retourne True si une carte a été cliquée.
    """
    if not CARDS_ENABLED: return
    # Position de départ des cartes
    card_x = START_X_PLAYER
    card_y = START_Y_PLAYER + (GRID_SIZE * CELL_SIZE_PLAYER) + 30
    
    for card in game.player.cards:
        rect = pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
        if rect.collidepoint(x, y):
            # Cas 1 : On désélectionne la carte actuelle
            if game.selected_card == card:
                game.selected_card = None
                game.awaiting_target = False
                game.text_status = "Carte désélectionnée."
            # Cas 2 : On sélectionne une nouvelle carte
            else:
                game.selected_card = card
                game.awaiting_target = True
                game.text_status = f"Carte {card} activée ! Ciblez..."
                game.sounds.play_card()
            return 
        # On décale pour tester la carte suivante
        card_x += CARD_WIDTH + CARD_SPACING

def handle_grid_click(game, x, y):
    """
    Gère le clic sur la grille adverse.
    Déclenche soit un Tir classique, soit un Sortilège.
    """
    # Dimensions de la grille IA
    width_ia = GRID_SIZE * CELL_SIZE_IA
    height_ia = GRID_SIZE * CELL_SIZE_IA
    
    # 1. Vérification : Est-ce qu'on clique DANS la grille ?
    if (START_X_IA <= x < START_X_IA + width_ia and 
        START_Y_IA <= y < START_Y_IA + height_ia):
        
        # 2. Conversion Coordonnées Pixels -> Coordonnées Grille (0-9)
        col = (x - START_X_IA) // CELL_SIZE_IA
        row = (y - START_Y_IA) // CELL_SIZE_IA
        
        # --- SCÉNARIO A : UTILISATION D'UNE CARTE ---
        if game.selected_card and game.awaiting_target:
            # Application de l'effet (Bombe, Radar, etc.)
            apply_card_effect(game, game.selected_card, row, col)

            # Mise à jour des stats et de l'inventaire
            game.cards_played_total += 1
            if game.selected_card in game.player.cards:
                game.player.cards.remove(game.selected_card)

            # Reset de la sélection
            game.selected_card = None
            game.awaiting_target = False
            
        # --- SCÉNARIO B : TIR STANDARD ---
        elif game.player_turn:
            res = game.shoot(game.player, row, col)

            if res != "Déjà tiré":
                # Gestion du Bonus "Double Tir"
                if game.extra_shot > 0:
                    game.extra_shot -= 1
                    game.text_status = f"BONUS : Encore {game.extra_shot + 1} tir(s) !"
                else:
                    # Fin du tour : On passe la main à l'IA
                    game.player_turn = False
                    game.text_status = "Tour de l'IA..."
                    game.ia_delay = 800
                    game.ia_pending = True