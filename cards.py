import random

# --- PARAMÈTRES DES CARTES ---
CARD_WIDTH = 130   
CARD_HEIGHT = 150  
CARD_SPACING = 20  

def apply_card_effect(game, card_name, target_row, target_col):
    """
    Applique l'effet d'une carte sur le jeu.
    """
    # Debug pour voir le nom exact reçu
    print(f"--- ACTIVATION : Reçu '{card_name}' (Type: {type(card_name)}) ---")
    
    player = game.player
    enemy = game.enemy

    # On met le nom en majuscule pour éviter les soucis (ex: "Bombe" devient "BOMBE")
    name_upper = str(card_name).upper().strip()

    # --- CARTE 1 : TIR DOUBLE (Accepte "2-TIR", "DOUBLE TIR", "2 TIR") ---
    if "2" in name_upper or "DOUBLE" in name_upper:
        print("   -> Effet : DOUBLE TIR activé")
        game.extra_shot += 1
        game.text_status = "DOUBLE TIR : +1 munition !"
        if hasattr(game, 'sound_card'): game.sound_card.play()

    # --- CARTE 2 : RADAR (Accepte "RADAR", "SCAN") ---
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
        
        if hasattr(game, 'sound_card'): game.sound_card.play()

    # --- CARTE 3 : BOMBE (Accepte "BOMBE", "BOUM", "BOMB") ---
    elif "BOMB" in name_upper or "BOUM" in name_upper:
        print("   -> Effet : BOMBE activée")
        r, c = random.randint(0, 9), random.randint(0, 9)
        game.text_status = f"BOUM ! Bombe larguée en {chr(65+c)}{r+1} !"
        game.shoot(player, r, c)

    # --- CARTE 4 : BOUCLIER (Accepte "BOUCLIER", "SHIELD", "PROTECTION") ---
    elif "BOUCLIER" in name_upper or "SHIELD" in name_upper:
        print("   -> Effet : BOUCLIER activé")
        if "Bouclier_Actif" not in player.reinforced_ships:
            player.reinforced_ships.append("Bouclier_Actif")
            game.text_status = "BOUCLIER ACTIF : Flotte protégée !"
            if hasattr(game, 'sound_card'): game.sound_card.play()
        else:
            game.text_status = "Bouclier déjà actif !"

    # --- CARTE 5 : SABOTAGE (Accepte "SABOTAGE", "HACK") ---
    elif "SABO" in name_upper or "HACK" in name_upper:
        print("   -> Effet : SABOTAGE activé")
        game.ia_pending = False
        game.player_turn = True
        game.text_status = "SABOTAGE : L'IA passe son tour !"
        if hasattr(game, 'sound_card'): game.sound_card.play()

    # --- CARTE 6 : SALVE (Accepte "SALVE", "RAFALE") ---
    elif "SALVE" in name_upper or "RAFALE" in name_upper:
        print("   -> Effet : SALVE activée")
        game.text_status = f"SALVE : Tir de barrage ligne {target_row + 1} !"
        for c in range(10):
            game.shoot(player, target_row, c)
            
    else:
        print(f"⚠️ ERREUR : Le nom '{card_name}' n'est pas reconnu dans cards.py !")