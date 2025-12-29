import pygame
from settings import *

# ====================================================================
#  1. DESSIN DES BATEAUX (FORMES CONTINUES)
# ====================================================================
def draw_continuous_ships(screen, player, start_x, start_y, cell_size, theme_color, border_color):
    """
    Dessine les bateaux sous forme de rectangles arrondis continus au lieu de simples cases.
    """
    for ship_name, positions in player.ship_positions.items():
        if not positions: continue
        
        # On trie les positions pour trouver le début et la fin du bateau
        sorted_pos = sorted(positions)
        start_row, start_col = sorted_pos[0]
        
        # Calcul de l'orientation et de la longueur
        if len(positions) > 1:
            end_row, end_col = sorted_pos[-1]
            if start_row == end_row: orientation, length = "H", (end_col - start_col) + 1
            else: orientation, length = "V", (end_row - start_row) + 1
        else:
            orientation, length = "H", 1

        # Conversion en pixels
        px = start_x + start_col * cell_size
        py = start_y + start_row * cell_size
        padding = 4 
        
        # Calcul du rectangle selon l'orientation
        if orientation == "H":
            rect_w = length * cell_size - (padding * 2)
            rect_h = cell_size - (padding * 2)
        else:
            rect_w = cell_size - (padding * 2)
            rect_h = length * cell_size - (padding * 2)
        
        # Dessin du corps du bateau + bordure
        ship_rect = pygame.Rect(px + padding, py + padding, rect_w, rect_h)
        pygame.draw.rect(screen, theme_color, ship_rect, border_radius=15)
        pygame.draw.rect(screen, border_color, ship_rect, 2, border_radius=15)

# ====================================================================
#  2. DESSIN DES GRILLES ET MARQUEURS (TIRS)
# ====================================================================
def draw_grid_lines_and_markers(screen, player, start_x, start_y, cell_size, font, is_player):
    """
    Dessine la grille, les tirs et les textes.
    is_player : True si c'est le joueur (Cyan), False si c'est l'IA (Violet).
    """
    
    # A. Effet visuel du Bouclier (si actif)
    if "Bouclier_Actif" in player.reinforced_ships:
        total = GRID_SIZE * cell_size
        pygame.draw.rect(screen, (0, 191, 255), (start_x-5, start_y-5, total+10, total+10), 4, border_radius=5)
    
    # B. Configuration des couleurs selon le camp
    if is_player:
        # --- THEME PLAYER (CYAN) ---
        current_grid_color = COLOR_GRID_NEON 
        current_text_color = COLOR_GRID_NEON
        font_coords = pygame.font.Font(FONT_NAME_GRIMOIRE, 30)
        text_margin = 20
        hull_color = (0, 100, 120) # Couleur impact joueur
        border_hull = (0, 150, 180)
    else:
        # --- THÈME IA (VIOLET) ---
        current_grid_color = COLOR_GRID_IA_PURPLE
        current_text_color = COLOR_GRID_IA_PURPLE
        font_coords = pygame.font.Font(FONT_NAME_GRIMOIRE, 50)
        text_margin = 30
        hull_color = (80, 20, 120) # Couleur impact ia
        border_hull = (120, 40, 180)

    # C. Boucle de dessin de la grille
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(start_x + col*cell_size, start_y + row*cell_size, cell_size, cell_size)
            val = player.board[row][col]
            
            # 1. Contour de la case
            pygame.draw.rect(screen, current_grid_color, rect, 1)

            # 2. Gestion des Tirs
            if val == -1: # TOUCHÉ
                hull_rect = rect.inflate(-4, -4)
                pygame.draw.rect(screen, hull_color, hull_rect, border_radius=5)
                pygame.draw.rect(screen, border_hull, hull_rect, 2, border_radius=5)
                
                center_pos = rect.center
                radius = cell_size // 4

                # Effet visuel rouge
                s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 0, 0, 150), (cell_size//2, cell_size//2), radius + 4)
                screen.blit(s, rect)
                
                pygame.draw.circle(screen, (220, 0, 0), center_pos, radius)
                pygame.draw.circle(screen, (255, 100, 100), (center_pos[0]-2, center_pos[1]-2), radius//3)

            elif val == -2: # MANQUÉ (croix)
                pygame.draw.line(screen, (200, 200, 255), (rect.left+10, rect.top+10), (rect.right-10, rect.bottom-10), 2)
                pygame.draw.line(screen, (200, 200, 255), (rect.left+10, rect.bottom-5), (rect.right-10, rect.top+5), 2)

    # D. Coordonnées (Lettres A-J et Chiffres 1-10)
    for i in range(GRID_SIZE):
        # Lettres en haut
        x_pos = start_x + i * cell_size + cell_size // 2
        letter = chr(ord('A') + i)
        
        t = font_coords.render(letter, True, current_text_color)
        screen.blit(t, t.get_rect(center=(x_pos, start_y - text_margin)))
        
        # Chiffres à gauche
        y_pos = start_y + i * cell_size + cell_size // 2
        t2 = font_coords.render(str(i + 1), True, current_text_color)
        screen.blit(t2, t2.get_rect(center=(start_x - text_margin, y_pos)))


# ====================================================================
#  3. DESSIN DE L'INTERFACE DES CARTES
# ====================================================================
def draw_cards(screen, player, selected_card, font):
    """Affiche la main de cartes du joueur en bas de l'écran."""
    if not CARDS_ENABLED: return
    x = START_X_PLAYER 
    y = START_Y_PLAYER + (GRID_SIZE*CELL_SIZE_PLAYER) + 30 
    
    for card in player.cards:
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT) 

        # Effet visuel si sélectionné
        if card == selected_card:
            rect.y -= 10 
            bg_color = (255, 255, 255)
        else:
            bg_color = (200, 240, 255)
        
        pygame.draw.rect(screen, bg_color, rect, border_radius=8)
        pygame.draw.rect(screen, (0,0,0), rect, 3, border_radius=8)
        
        # Nom de la carte
        text_surf = font.render(card, True, (0,0,0))
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))
        x += CARD_WIDTH + CARD_SPACING 

# ====================================================================
#  4. PANNEAU DE STATUT ENNEMI (LISTE BATEAUX)
# ====================================================================
def draw_enemy_status(screen, enemy, font_bold, font_small, is_ship_sunk_func):
    """
    Affiche la liste des bateaux ennemis et leur état (Vivant/Coulé).
    Version compacte et centrée.
    """
    # Calculs de positionnement
    font_small = pygame.font.Font(FONT_NAME_2, 40) 
    font_bold = pygame.font.Font(FONT_NAME_GRIMOIRE, 50)
        
    fin_grille_joueur = START_X_PLAYER + (GRID_SIZE * CELL_SIZE_PLAYER)
    debut_grille_ia = START_X_IA
    center_x = (fin_grille_joueur + debut_grille_ia) // 2
        
    hauteur_grille = GRID_SIZE * CELL_SIZE_IA
    centre_vertical_grille = START_Y_IA + (hauteur_grille // 2)

    # Dimensions du panneau
    hauteur_bloc_texte = 400
    decalage_vers_le_haut = 50
    start_y = centre_vertical_grille - (hauteur_bloc_texte // 2) - decalage_vers_le_haut
        
    panel_width = 300
    panel_height = hauteur_bloc_texte + 30
    panel_x = center_x - (panel_width // 2)
    panel_y = start_y - 15

    # Fond semi-transparent
    panel_surface = pygame.Surface((panel_width, panel_height))
    panel_surface.set_alpha(PANEL_ALPHA_VALUE)
    panel_surface.fill(COLOR_PANEL_BG_DARK)
    screen.blit(panel_surface, (panel_x, panel_y))

    # Bordure
    pygame.draw.rect(screen, COLOR_PANEL_BORDER, (panel_x, panel_y, panel_width, panel_height), 1, border_radius=10)

    # Titre
    title = font_bold.render("Flotte Ennemie", True, COLOR_MAGIC_ENEMY)
    screen.blit(title, title.get_rect(midtop=(center_x, start_y - 30)))

    # Liste des navires
    all_ships = enemy.ship_positions.keys()
    i, nb_coules = 0, 0
    line_spacing = 45
    marge_sous_titre = 50
        
    for ship_name in all_ships:
        # Vérification via la fonction callback
        est_coule = is_ship_sunk_func(enemy, ship_name)

        if est_coule:
            color, text_str = (255, 100, 100), f" {ship_name}"
            nb_coules += 1
        else:
            color, text_str = COLOR_TEXT_NORMAL, f" {ship_name}" 

        surf = font_small.render(text_str, True, color)
        rect = surf.get_rect(midtop=(center_x, start_y + marge_sous_titre +(i * line_spacing) ))
        screen.blit(surf, rect)

        # Barre si coulé
        if est_coule:
            pygame.draw.line(screen, color, (rect.left, rect.centery), (rect.right, rect.centery), 2)
        i += 1

    # Score final
    summary = f"Coulés : {nb_coules}/{len(all_ships)}"
    col_summary = (0, 255, 0) if nb_coules == len(all_ships) else (255, 255, 255)
    surf_summary = font_bold.render(summary, True, col_summary)
    rect_summary = surf_summary.get_rect(midtop=(center_x, start_y + marge_sous_titre + (i * line_spacing) + 50))
    
    #cadre autour du score
    pygame.draw.rect(screen, COLOR_MAGIC_ENEMY, rect_summary.inflate(20,5), 1, border_radius=4)
    screen.blit(surf_summary, rect_summary)

# ====================================================================
#  5. INTERFACE GLOBALE (TITRES, CHRONO, CHAT)
# ====================================================================
def draw_game_interface(screen, player, enemy, fonts, game_state):
    """
    Dessine tous les textes d'ambiance et d'information.
    """
    # 1. STATUS (Tour de...)
    color_status = COLOR_MAGIC_PLAYER if game_state['player_turn'] else COLOR_MAGIC_ENEMY
    status_surf = fonts['std'].render(game_state['text_status'], True, color_status)
    screen.blit(status_surf, status_surf.get_rect(midtop=(screen.get_width() // 2, 20)))

    # 2. NOMS DES JOUEURS
    name_player = fonts['title'].render(player.name, True, COLOR_TEXT_NORMAL)
    screen.blit(name_player, name_player.get_rect(
        midbottom=(START_X_PLAYER + (GRID_SIZE*CELL_SIZE_PLAYER)//2, START_Y_PLAYER - 30)
    ))
    
    name_enemy = fonts['title'].render(enemy.name, True, (255, 255, 255))
    screen.blit(name_enemy, name_enemy.get_rect(
        midbottom=(START_X_IA + (GRID_SIZE*CELL_SIZE_IA)//2, START_Y_IA - 35)
    ))

    # 3. CHRONOMÈTRE
    current_time = pygame.time.get_ticks() - game_state['start_time']
    timer_text = f"{current_time // 60000:02}:{(current_time // 1000) % 60:02}"
    
    surf_timer = fonts['timer'].render(f" {timer_text}", True, (255, 255, 255))
    rect_timer = surf_timer.get_rect(topright=(screen.get_width() - 20, 20))
    
    # Fond sombre 
    bg_rect_timer = rect_timer.inflate(20, 10)
    s_timer = pygame.Surface((bg_rect_timer.width, bg_rect_timer.height), pygame.SRCALPHA)
    s_timer.fill((0, 0, 0, 150))
    screen.blit(s_timer, bg_rect_timer)
    screen.blit(surf_timer, rect_timer)

    # 4. PHRASE DE L'IA (CHAT)
    phrase = game_state['ai_phrase']
    if phrase:
        font_phrase = fonts['std']
        center_x_ia = START_X_IA + (GRID_SIZE * CELL_SIZE_IA // 2)
        start_y_phrase = START_Y_IA + (GRID_SIZE * CELL_SIZE_IA) + 20
        
        # Découpage intelligent du texte
        words = phrase.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font_phrase.size(test_line)[0] < (GRID_SIZE * CELL_SIZE_IA + 110):
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))

        for i, line in enumerate(lines):
            phrase_surf = font_phrase.render(line, True, (255, 255, 255))
            phrase_rect = phrase_surf.get_rect(midtop=(center_x_ia, start_y_phrase + (i * 30)))
            
            bg_rect = phrase_rect.inflate(10, 5)
            s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            s.fill((0, 0, 0, 150))
            screen.blit(s, bg_rect)
            screen.blit(phrase_surf, phrase_rect)