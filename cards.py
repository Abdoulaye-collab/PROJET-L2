import random

def apply_card_effect(game, card_name, target_row, target_col):
    """
    Applique l'effet d'une carte sur le jeu.
    Args:
        game: L'instance principale du jeu (accès à player, enemy, sounds, etc.)
        card_name (str): Le nom de la carte jouée.
        target_row, target_col: La case visée (utile pour Radar/Salve).
    """
    
    player = game.player
    enemy = game.enemy

    # 1. Normalisation du nom
    name_upper = str(card_name).upper().strip()

    print(f"--- [CARDS] ACTIVATION : '{name_upper}' visée ({target_row}, {target_col}) ---")
    
    # ===========================================================
    #  CARTE 1 : DOUBLE TIR (Bonus d'action)
    # ===========================================================
    if "2" in name_upper or "DOUBLE" in name_upper:
        print("   -> Effet : DOUBLE TIR activé")
        game.extra_shot += 1
        game.text_status = "DOUBLE TIR : +1 munition !"
        game.sounds.play_card()

    # ===========================================================
    #  CARTE 2 : RADAR (Information)
    # ===========================================================
    elif "RADAR" in name_upper or "SCAN" in name_upper:
        print("   -> Effet : RADAR activé")
        valeur_case = enemy.board[target_row][target_col]
        
        if valeur_case == 1: 
            game.text_status = "RADAR : CIBLE DÉTECTÉE (Navire) !"
            print("      Résultat : Bateau")
        elif valeur_case == 0:
            game.text_status = "RADAR : Zone vide (Eau)."
            print("      Résultat : Eau")
        elif valeur_case == -1:
            game.text_status = "RADAR : Épave détectée."
        
        game.sounds.play_card()

    # ===========================================================
    #  CARTE 3 : BOMBE (Frappe Aléatoire)
    # ===========================================================
    elif "BOMB" in name_upper or "BOUM" in name_upper:
        print("   -> Effet : BOMBE activée")
        # On choisit une case au hasard sur toute la grille
        r, c = random.randint(0, 9), random.randint(0, 9)
        
        game.text_status = f"BOUM ! Bombe larguée en {chr(65+c)}{r+1} !"
        # On utilise la fonction de tir du jeu pour gérer les dégâts/partic
        game.shoot(player, r, c)

    # ===========================================================
    #  CARTE 4 : BOUCLIER (Défense)
    # ===========================================================
    elif "BOUCLIER" in name_upper or "SHIELD" in name_upper:
        print("   -> Effet : BOUCLIER activé")
        if "Bouclier_Actif" not in player.reinforced_ships:
            player.reinforced_ships.append("Bouclier_Actif")
            game.text_status = "BOUCLIER ACTIF : Flotte protégée !"
            game.sounds.play_card()
        else:
            game.text_status = "Bouclier déjà actif !"

    # ===========================================================
    #  CARTE 5 : SABOTAGE (Contrôle)
    # ===========================================================
    elif "SABO" in name_upper or "HACK" in name_upper:
        print("   -> Effet : SABOTAGE activé")
        game.ia_pending = False # Annule le timer de réflexion de l'IA
        game.player_turn = True # Force le tour à revenir au joueur
        game.text_status = "SABOTAGE : L'IA passe son tour !"
        game.sounds.play_card()

    # ===========================================================
    #  CARTE 6 : SALVE (Attaque de Zone - Ligne entière)
    # ===========================================================
    elif "SALVE" in name_upper or "RAFALE" in name_upper:
        print("   -> Effet : SALVE activée")
        game.text_status = f"SALVE : Tir de barrage ligne {target_row + 1} !"
        # On tire sur les 10 colonnes de la ligne visée
        for c in range(10):
            game.shoot(player, target_row, c)

    # ===========================================================
    #  ERREUR (Nom inconnu)
    # ===========================================================       
    else:
        print(f" ERREUR : Le nom '{card_name}' n'est pas reconnu dans cards.py !")