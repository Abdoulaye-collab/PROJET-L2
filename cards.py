import random

def apply_card_effect(game, card_name, target_row, target_col):
    player = game.player
    enemy = game.enemy

    if card_name == "Double Tir":
        game.extra_shot += 1
        game.text_status = "✨ DOUBLE TIR : +1 munition !"
        # Effet visuel : petit flash sur le texte
        
    elif card_name == "Radar":
        # Couleur spéciale pour le radar (Cyan)
        if enemy.board[target_row][target_col] == 1:
            game.text_status = "📡 RADAR : NAVIRE REPRÉRÉ !"
            enemy.board[target_row][target_col] = 1 # On peut forcer un affichage temporaire ici si on veut
        else:
            game.text_status = "📡 RADAR : Zone vide..."

    elif card_name == "Bombe":
        r, c = random.randint(0, 9), random.randint(0, 9)
        # On force la couleur du projectile en Orange pour la bombe
        game.text_status = "💥 BOUM ! Bombe larguée !"
        game.shoot(player, r, c)

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