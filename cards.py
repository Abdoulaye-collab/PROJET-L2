import random
# --- PARAMÈTRES DES CARTES ---
CARD_WIDTH = 110   # Assez large pour le texte
CARD_HEIGHT = 150  # Format "Portrait" (hauteur > largeur)
CARD_SPACING = 20  # Espace entre deux cartes

def apply_card_effect(game, card_name, target_row, target_col):
    """
    Applique l'effet d'une carte. 
    Les modifications sont répercutées directement sur l'objet 'game'.
    """
    player = game.player
    enemy = game.enemy

    # --- CARTE 1 : TIR DOUBLE ---
    if card_name == "Double Tir":
        # Ajoute simplement un tir bonus au compteur
        game.extra_shot += 1
        game.text_status = "✨ DOUBLE TIR : +1 munition !"
         # Effet visuel : petit flash sur le texte

    # --- CARTE 2 : RADAR (Dévoile une zone) ---
    elif card_name == "Radar":
        # Révèle si un bateau est présent sur la case sans tirer
        if enemy.board[target_row][target_col] == 1:
            game.text_status = "📡 RADAR : NAVIRE REPRÉRÉ !"
            enemy.board[target_row][target_col] = 1 # On peut forcer un affichage temporaire ici si on veut
        else:
            game.text_status = "Radar : Zone vide."

    # --- CARTE 3 : BOMBE (Tir aléatoire sur l'IA) ---
    elif card_name == "Bombe":
        # Choisit une case au hasard chez l'ennemi et tire
        r, c = random.randint(0, 9), random.randint(0, 9)
        res = game.shoot(player, r, c)
        game.text_status = "💥 BOUM ! Bombe larguée !"

    elif card_name == "Bouclier":
        if "Bouclier_Actif" not in player.reinforced_ships:
            player.reinforced_ships.append("Bouclier_Actif")
            game.text_status = "🛡️ BOUCLIER : Flotte protégée !"    
    
    elif card_name == "Sabotage":
        game.ia_pending = False
        game.player_turn = True
        game.text_status = "⚡ SABOTAGE : Système IA hors-service !"

    elif card_name == "Salve":
        game.text_status = f"🚀 SALVE : Barrage sur la ligne {target_row + 1} !"
        for c in range(10):
            # Les projectiles de salve seront tirés en rafale par l'update
            game.shoot(player, target_row, c)