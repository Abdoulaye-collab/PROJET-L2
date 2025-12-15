import pygame
import random
from player import Player, ALL_CARDS
from settings import CARDS_ENABLED, COLOR_TEXT_MAGIC, FONT_NAME, COLOR_UI_BACKGROUND
from ai_llm import get_ai_move
from ai_personalities import AI_PERSONALITIES, get_ai_phrase
from cards import apply_card_effect, CARD_HEIGHT,CARD_SPACING,CARD_WIDTH  # Import de la logique externe
from settings import (
    COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, COLOR_WATER_LIT, 
    COLOR_HIT, COLOR_SHIP, 
    CELL_SIZE, GRID_SIZE,
    GRID_OFFSET_X_PLAYER, GRID_OFFSET_X_ENEMY
)
# 1. JOUEUR (Petite grille à gauche)
CELL_SIZE_PLAYER = 35
START_X_PLAYER = 50
# On centre verticalement sur une hauteur de 800px environ
START_Y_PLAYER = 250 

# 2. IA RIVALE (Grande grille à droite - La cible principale !)
CELL_SIZE_IA = 55
# On la place à droite (ex: à 1400 - largeur grille - marge)
START_X_IA = 800  # Ajuste cette valeur selon la largeur de ton écran
START_Y_IA = 150  # Un peu plus haut

# On garde GRID_SIZE qui ne change pas (10 cases)
GRID_SIZE = 10

def load_assets(cell_size):
    """Charge les ressources nécessaires (images, sons, etc.)"""
    assets = {}

    FACTOR_SIZE = 1.5
    icon_width = int(CELL_SIZE * FACTOR_SIZE)
    icon_height = int(CELL_SIZE * FACTOR_SIZE)
    icon_size_tuple= (icon_width, icon_height)
    chapeau_icon = pygame.image.load('images/chapeau.png').convert_alpha()
    assets['chapeau'] = pygame.transform.scale(chapeau_icon, icon_size_tuple)
    
    
    return assets

# CHANGEMENT : GRID_OFFSET_Y réduit pour remonter les grilles
GRID_OFFSET_Y = 200
PROJECTILE_SPEED = 20  

class Game:
    def __init__(self, screen,assets):
        self.screen = screen
        self.assets = assets
        self.player = Player("Joueur")
        self.enemy = Player("IA")
        self.turn_count = 1
        self.winner = None
        self.font = pygame.font.Font(FONT_NAME, 25)
        self.title_font = pygame.font.Font(FONT_NAME, 30)
        self.selected_card = None
        self.awaiting_target = False

        self.ai_personality = "Gentille"
        self.ai_phrase_to_display = ""
        self.extra_shot = 0
        self.projectile = None  
        self.ia_delay = 0
        self.ia_pending = False
        self.player_turn = True
        self.text_status = f"Tour de {self.player.name} !"
        pygame.mixer.init()

        self.start_time = pygame.time.get_ticks()
        self.winner = None
        self.game_over = False
        

        # Chargement de la musique de fond
        pygame.mixer.music.load("assets/sounds/theme.mp3")
        pygame.mixer.music.set_volume(0.3) # Volume à 30%
        pygame.mixer.music.play(-1) # -1 pour jouer en boucle

        # Chargement des effets sonores
        self.sound_hit = pygame.mixer.Sound("assets/sounds/hit.wav")
        self.sound_miss = pygame.mixer.Sound("assets/sounds/miss.wav")
        self.sound_card = pygame.mixer.Sound("assets/sounds/card.wav")

        self.start_time = pygame.time.get_ticks()
        self.winner = None
        self.game_over = False

    def ship_positions_hit(self, player, row, col):
        for ship, positions in player.ship_positions.items():
            if (row, col) in positions:
                positions.remove((row, col))
                break

    def shoot(self, shooter, row, col):
        target = self.enemy if shooter == self.player else self.player
        
        # --- SÉCURITÉ BOUCLIER ---
        if shooter == self.enemy and "Bouclier_Actif" in target.reinforced_ships:
            target.reinforced_ships.remove("Bouclier_Actif")
            self.text_status = "BOUCLIER : Tir ennemi bloqué !"
            return "Bloqué"

        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return "Invalid"
        
        val = target.board[row][col]

         # --- GESTION VISUELLE DES COULEURS ---
        if shooter == self.player:
            start_x = START_X_PLAYER + (GRID_SIZE*CELL_SIZE_PLAYER)//2
            start_y = START_Y_PLAYER + (GRID_SIZE*CELL_SIZE_PLAYER)//2
            proj_color = (255, 0, 0) # Rouge

            if self.selected_card == "Bombe": proj_color = (255, 165, 0)
            elif self.selected_card == "Salve": proj_color = (255, 50, 50)
            elif self.selected_card == "Radar": proj_color = (0, 255, 255)
        else:
            start_x = START_X_IA + (GRID_SIZE * CELL_SIZE_IA) // 2
            start_y = START_Y_IA + (GRID_SIZE * CELL_SIZE_IA) // 2
            proj_color = (255, 255, 0) # Jaune
        
        # Changement de couleur selon la carte active
        
        self.projectile = {"shooter": shooter, "target": (row, col), "pos": [start_x, start_y], "color": proj_color}

        # --- LOGIQUE DE TOUCHE ---
        if val == 1:
            for ship, pos in target.ship_positions.items():
                if (row, col) in pos and ship in target.reinforced_ships:
                    target.reinforced_ships.remove(ship)
                    return "Renforcé"

            target.board[row][col] = -1
            self.ship_positions_hit(target, row, col)
            shooter.hits += 1
            self.check_win()
            return "Touché"

        elif val == 0:
            target.board[row][col] = -2
            return "Manqué"

        return "Déjà tiré"

    def check_win(self):
        for p in [self.player, self.enemy]:
            if all(len(pos) == 0 for pos in p.ship_positions.values()):
                self.winner = self.enemy if p == self.player else self.player
        if self.enemy.all_ships_sunk():
            self.winner = self.player.name
            self.game_over = True
        return 
    
        if self.player.all_ships_sunk():
            self.winner = self.enemy.name
            self.game_over = True
            return

    def ai_play(self):
        if self.winner:
            return
        personality_style = AI_PERSONALITIES[self.ai_personality]["style"]
        row, col = get_ai_move(self.player.board, personality_style)
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            available = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.player.board[r][c] in [0, 1]]
            if not available:
                return
            row, col = random.choice(available)

        result = self.shoot(self.enemy, row, col)
        if result in ("Touché", "Renforcé"):
            self.ai_phrase_to_display = get_ai_phrase(self.ai_personality, "hit")
        else:
            self.ai_phrase_to_display = get_ai_phrase(self.ai_personality, "miss")

        self.turn_count += 1
        self.player_turn = True
        self.text_status = f"Tour de {self.player.name} !"

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or self.winner:
            return
        mouse_x, mouse_y = event.pos

        # 1. Gestion de la sélection des cartes
        card_x = START_X_PLAYER
        card_y = START_Y_PLAYER + (GRID_SIZE * CELL_SIZE_PLAYER) + 30
    
        for card in self.player.cards:
            rect = pygame.Rect(card_x, card_y, 120, 40)
            if rect.collidepoint(mouse_x, mouse_y):
                if CARDS_ENABLED:
                    if self.selected_card == card:
                        self.selected_card = None
                        self.awaiting_target = False
                    else:
                        self.selected_card = card # Sélectionner
                        self.awaiting_target = True
                        self.sound_card.play()
                return # On arrête ici pour ne pas tirer en sélectionnant
            card_x += CARD_WIDTH + CARD_SPACING
        
        width_ia = GRID_SIZE * CELL_SIZE_IA
        height_ia = GRID_SIZE * CELL_SIZE_IA

        # Est-ce que la souris est à l'intérieur du grand carré de l'IA ?
        is_inside_ia_grid = (
            START_X_IA <= mouse_x < START_X_IA + width_ia and
            START_Y_IA <= mouse_y < START_Y_IA + height_ia
        )
        if is_inside_ia_grid:
        # Conversion Pixels -> Colonne/Ligne
            col = (mouse_x - START_X_IA) // CELL_SIZE_IA
            row = (mouse_y - START_Y_IA) // CELL_SIZE_IA

            # 2. Utilisation de l'effet de la carte sélectionnée
            if self.selected_card and self.awaiting_target:
                apply_card_effect(self, self.selected_card, row, col)
                if self.selected_card in self.player.cards:
                    self.player.cards.remove(self.selected_card)
                self.selected_card = None
                self.awaiting_target = False
                return # INDISPENSABLE : on ne tire pas après avoir utilisé une carte

            # 3. Tir normal (seulement si aucune carte n'est en cours d'usage)
            if self.player_turn:
                res = self.shoot(self.player, row, col)
                if res != "Déjà tiré":
                    if self.extra_shot > 0:
                        self.extra_shot -= 1
                        # On reste en player_turn = True
                    else:
                        self.player_turn = False
                        self.text_status = "Tour de l'IA..."
                        self.ia_delay = 250
                        self.ia_pending = True
        

    def update(self):
        if self.projectile:
            target_row, target_col = self.projectile["target"]
            if self.projectile["shooter"] == self.player:
                # La cible est l'IA (Grande Grille)
                target_x = START_X_IA + target_col * CELL_SIZE_IA + (CELL_SIZE_IA // 2)
                target_y = START_Y_IA + target_row * CELL_SIZE_IA + (CELL_SIZE_IA // 2)
            else:
                # La cible est le Joueur (Petite Grille)
                target_x = START_X_PLAYER + target_col * CELL_SIZE_PLAYER + (CELL_SIZE_PLAYER // 2)
                target_y = START_Y_PLAYER + target_row * CELL_SIZE_PLAYER + (CELL_SIZE_PLAYER // 2)

            dx = target_x - self.projectile["pos"][0]
            dy = target_y - self.projectile["pos"][1]
            dist = (dx**2 + dy**2)**0.5
            if dist < PROJECTILE_SPEED:
                self.projectile = None
            else:
                self.projectile["pos"][0] += PROJECTILE_SPEED * dx / dist
                self.projectile["pos"][1] += PROJECTILE_SPEED * dy / dist

        if self.ia_pending and not self.projectile:
            if self.ia_delay > 0:
                self.ia_delay -= 16
            else:
                self.ai_play()
                self.ia_pending = False
        self.check_win()

    def draw_continuous_ships(self, player, start_x, start_y, cell_size):
        """Dessine les bateaux comme des formes continues au lieu de carrés séparés."""
        
        # Couleur du bateau (Gris foncé / Métal)
        ship_color = (80, 80, 80)
        # Couleur de la bordure (Plus clair pour le relief)
        border_color = (120, 120, 120)
        
        # On parcourt chaque bateau défini dans le dictionnaire du joueur
        # Exemple : ship_name = "Porte-Avions", positions = [(0,0), (0,1), (0,2)...]
        for ship_name, positions in player.ship_positions.items():
            if not positions: continue # Sécurité si le bateau est vide

            # 1. Trouver les coordonnées de départ et de fin
            # On trie les positions pour être sûr d'avoir le début et la fin
            sorted_pos = sorted(positions)
            start_row, start_col = sorted_pos[0]
            end_row, end_col = sorted_pos[-1]

            # 2. Calculer la position pixel du coin haut-gauche
            px = start_x + start_col * cell_size
            py = start_y + start_row * cell_size

            # 3. Calculer la largeur et hauteur totales en pixels
            # On ajoute +1 car si ça va de la col 2 à 4, ça fait 3 cases de large.
            width_cells = (end_col - start_col) + 1
            height_cells = (end_row - start_row) + 1

            # On laisse une petite marge (padding) pour que ça ne colle pas aux lignes
            padding = 4 
            rect_w = width_cells * cell_size - (padding * 2)
            rect_h = height_cells * cell_size - (padding * 2)
            
            # Création du rectangle final
            ship_rect = pygame.Rect(px + padding, py + padding, rect_w, rect_h)

            # 4. DESSIN DE LA FORME ARRONDE
            # border_radius=15 donne l'aspect "ovale/coque" aux extrémités
            pygame.draw.rect(self.screen, ship_color, ship_rect, border_radius=15)
            
            # Ajout d'une bordure pour le style
            pygame.draw.rect(self.screen, border_color, ship_rect, 2, border_radius=15)

    def draw_grid(self, player, start_x, start_y, cell_size, show_ships=True):
         # 1. EFFET VISUEL BOUCLIER (Aura bleue)
        if player == self.player and "Bouclier_Actif" in player.reinforced_ships:
            width_grid = GRID_SIZE * cell_size
            shield_rect = pygame.Rect(start_x - 5, start_y - 5, width_grid + 10, width_grid + 10)
            pygame.draw.rect(self.screen, (0, 191, 255), shield_rect, 4, border_radius=5)
        
        # 2. DESSIN DES CELLULES
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(start_x + col*cell_size, start_y + row*cell_size, cell_size, cell_size)
                val = player.board[row][col]
                
                pygame.draw.rect(self.screen, COLOR_OCEAN_DARK, rect)
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)

                # --- GESTION DES MARQUEURS (Touché / Manqué) ---
                if val == -1: # TOUCHÉ (Hit)
                    # Carré rouge semi-transparent pour voir un peu la coque dessous
                    s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    s.fill((255, 0, 0, 150)) # Rouge transparent
                    self.screen.blit(s, rect)
                    # Croix rouge pour bien marquer
                    pygame.draw.line(self.screen, (150,0,0), (rect.left+5, rect.top+5), (rect.right-5, rect.bottom-5), 3)
                    pygame.draw.line(self.screen, (150,0,0), (rect.left+5, rect.bottom-5), (rect.right-5, rect.top+5), 3)

                elif val == -2: # MANQUÉ (Miss)
                    # Petite croix blanche ou bleue
                    pygame.draw.line(self.screen, (200, 200, 255), (rect.left+10, rect.top+10), (rect.right-10, rect.bottom-10), 2)
                    pygame.draw.line(self.screen, (200, 200, 255), (rect.left+10, rect.bottom-5), (rect.right-10, rect.top+5), 2)
       
        # COORDONNÉES
        for i in range(GRID_SIZE):
            x_pos = start_x + i * cell_size + cell_size // 2
            letter = chr(ord('A') + i)
            text_surf = self.font.render(letter, True, COLOR_TEXT_MAGIC)
            text_rect = text_surf.get_rect(center=(x_pos, start_y - 20))
            self.screen.blit(text_surf, text_rect)
        
        for i in range(GRID_SIZE):
            y_pos = start_y + i * cell_size + cell_size // 2
            text_surf = self.font.render(str(i + 1), True, COLOR_TEXT_MAGIC)
            text_rect = text_surf.get_rect(center=(start_x - 20, y_pos))
            self.screen.blit(text_surf, text_rect)

        
            

    def draw_cards(self, player):
        if not CARDS_ENABLED:
            return
        
        start_x_cards = START_X_PLAYER
        start_y_cards = START_Y_PLAYER + (GRID_SIZE * CELL_SIZE_PLAYER) + 20

        x = start_x_cards
        y = start_y_cards

        for card in player.cards:
            rect = pygame.Rect(x, y, CARD_WIDTH,CARD_HEIGHT)
            if card == self.selected_card:
                rect.y -= 10 
                border_color = (0, 255, 0) # Vert fluo
                bg_color = (255, 250, 240) # Blanc cassé très clair
            else:
                border_color = (0, 0, 0)   # Noir classique
                bg_color = (255, 228, 196) # Couleur "Bisque" (Parchemin)
            
            # 1. Dessiner le fond de la carte
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=8) # Coins arrondis
            # 2. Dessiner la bordure
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=8)
            # 3. Dessiner le texte (Centré)
            # On utilise une police un peu plus petite si le texte est long
            font_card = pygame.font.Font(FONT_NAME, 20)
            text_surf = font_card.render(card, True, (0,0,0))
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
            
            x += CARD_WIDTH + CARD_SPACING

    def draw_enemy_status(self):
        """Affiche la liste des navires ennemis au CENTRE (Version Petite Police)"""
        
        # 1. CRÉATION D'UNE POLICE PLUS PETITE JUSTE POUR ÇA
        # Si FONT_NAME est défini au début, on l'utilise, sinon None (police par défaut)
        # Taille 18 (C'est petit et net)
        font_small = pygame.font.Font(FONT_NAME, 18) 
        font_bold = pygame.font.Font(FONT_NAME, 20) # Pour le titre et le score
        
        # 2. CALCUL DE LA POSITION CENTRALE
        fin_grille_joueur = START_X_PLAYER + (GRID_SIZE * CELL_SIZE_PLAYER)
        debut_grille_ia = START_X_IA
        # Le milieu exact
        center_x = (fin_grille_joueur + debut_grille_ia) // 2
        
        hauteur_grille = GRID_SIZE * CELL_SIZE_IA
        centre_vertical_grille = START_Y_IA + (hauteur_grille // 2)
        hauteur_bloc_texte = 190
        # On remonte un peu le tout pour être sûr que ça rentre
        start_y = centre_vertical_grille - (hauteur_bloc_texte // 2)
        
        # 3. AFFICHAGE DU TITRE
        title = font_bold.render("Flotte Ennemie", True, (255, 215, 0))
        title_rect = title.get_rect(midtop=(center_x, start_y - 30))
        self.screen.blit(title, title_rect)

        # 4. LISTE DES BATEAUX
        all_ships = self.enemy.ship_positions.keys()
        i = 0
        nb_coules = 0
        # Espacement vertical réduit (25 pixels au lieu de 35)
        line_spacing = 25 
        
        for ship_name in all_ships:
            coords_restantes = self.enemy.ship_positions[ship_name]
            est_coule = len(coords_restantes) == 0
            
            if est_coule:
                color = (255, 100, 100) # Rouge clair
                text_str = f" {ship_name}"
                nb_coules += 1
            else:
                color = (200, 200, 200) # Gris
                text_str = f" {ship_name}" 

            surf = font_small.render(text_str, True, color)
            rect = surf.get_rect(midtop=(center_x, start_y + (i * line_spacing)))
            self.screen.blit(surf, rect)
            
            if est_coule:
                start_line = (rect.left, rect.centery)
                end_line = (rect.right, rect.centery)
                pygame.draw.line(self.screen, color, start_line, end_line, 2)
            
            i += 1

        # 5. SCORE / RÉSUMÉ
        total_ships = len(all_ships)
        summary = f"Coulés : {nb_coules}/{total_ships}"
        col_summary = (0, 255, 0) if nb_coules == total_ships else (255, 255, 255)
        
        # On utilise la police un peu plus grasse pour le score
        surf_summary = font_bold.render(summary, True, col_summary)
        
        # On l'affiche en dessous de la liste
        rect_summary = surf_summary.get_rect(midtop=(center_x, start_y + (i * line_spacing) + 15))
        
        # Petit cadre propre
        pygame.draw.rect(self.screen, (255, 255, 255), rect_summary.inflate(15, 8), 1, border_radius=4)
        
        self.screen.blit(surf_summary, rect_summary)

    def draw(self):
        self.screen.fill(COLOR_UI_BACKGROUND)

        self.draw_continuous_ships(self.player, START_X_PLAYER, START_Y_PLAYER, CELL_SIZE_PLAYER)
        # 1. DESSINER LA PETITE GRILLE JOUEUR (Gauche)
        self.draw_grid(self.player, START_X_PLAYER, START_Y_PLAYER, CELL_SIZE_PLAYER, show_ships=True)
        # 2. DESSINER LA GRANDE GRILLE IA (Droite)
        self.draw_grid(self.enemy, START_X_IA, START_Y_IA, CELL_SIZE_IA, show_ships=False)
        #AFFICHER LE STATUS DE LA FLOTTE ENNEMIE
        self.draw_enemy_status()
        # Cartes du joueur
        self.draw_cards(self.player)

        # ---------------------------------------------------------
        # 3. STATUS DU JEU (Centré en haut)
        # ---------------------------------------------------------

        color_status = (0, 255, 0) if self.player_turn else (255, 0, 0)
        status_surf = self.font.render(self.text_status, True, color_status)
        
        center_x = self.screen.get_width() // 2
        status_rect = status_surf.get_rect(midtop=(center_x, 20))
        
        self.screen.blit(status_surf, status_rect)

        # ---------------------------------------------------------
        # 4. NOMS AU DESSUS DES GRILLES (Parfaitement Centrés)
        # ---------------------------------------------------------
        name_player = self.title_font.render(self.player.name, True, (255,255,255))
        name_enemy = self.title_font.render(self.enemy.name, True, (255,255,255))
        
        # --- CENTRAGE JOUEUR ---
        # 1. On calcule la largeur de la grille
        width_grid_player = GRID_SIZE * CELL_SIZE_PLAYER
        # 2. On trouve le centre X : Point de départ + (Largeur / 2)
        center_x_player = START_X_PLAYER + (width_grid_player // 2)
        # 3. On place le bas du texte (midbottom) 20px au-dessus de la grille
        rect_name_player = name_player.get_rect(midbottom=(center_x_player, START_Y_PLAYER - 35))
        self.screen.blit(name_player, rect_name_player)

        # --- CENTRAGE IA ---
        width_grid_ia = GRID_SIZE * CELL_SIZE_IA
        center_x_ia = START_X_IA + (width_grid_ia // 2)
        # Idem pour l'IA
        rect_name_enemy = name_enemy.get_rect(midbottom=(center_x_ia, START_Y_IA - 35))
        self.screen.blit(name_enemy, rect_name_enemy)

        # ---------------------------------------------------------
        # AJOUT : CHRONOMÈTRE (En haut à droite)
        # ---------------------------------------------------------
        
        # 1. Calcul du temps écoulé (en millisecondes)
        current_time = pygame.time.get_ticks() - self.start_time
        
        # 2. Conversion en Minutes:Secondes
        minutes = current_time // 60000
        seconds = (current_time // 1000) % 60
        timer_text = f"{minutes:02}:{seconds:02}"
        
        # 3. Création du texte
        # On utilise une police moyenne (taille 22 par exemple)
        font_timer = pygame.font.Font(FONT_NAME, 22) 
        surf_timer = font_timer.render(f" {timer_text}", True, (255, 255, 255))
        
        # 4. Positionnement (En haut à droite, avec une marge de 20px)
        rect_timer = surf_timer.get_rect(topright=(self.screen.get_width() - 20, 20))
        
        # 5. Petit fond noir semi-transparent (pour la lisibilité)
        bg_rect_timer = rect_timer.inflate(20, 10)
        s_timer = pygame.Surface((bg_rect_timer.width, bg_rect_timer.height), pygame.SRCALPHA)
        s_timer.fill((0, 0, 0, 150)) # Noir transparent
        self.screen.blit(s_timer, bg_rect_timer)
        
        # 6. Affichage du texte
        self.screen.blit(surf_timer, rect_timer)

        # ---------------------------------------------------------
        # 5. PHRASE DE L'IA (Multi-lignes et Centrée)
        # ---------------------------------------------------------
        if self.ai_phrase_to_display:
            # Paramètres
            font_phrase = self.font # Ou une autre police si tu veux
            text_color = (255, 255, 255)
            line_spacing = 30  # Espace entre les lignes
            
            # Limites de la zone de texte
            largeur_grille_ia = GRID_SIZE * CELL_SIZE_IA
            center_x_ia = START_X_IA + (largeur_grille_ia // 2)
            max_width = largeur_grille_ia + 100 # On autorise un peu de débordement
            
            # Position Y de départ (sous la grille)
            start_y_phrase = START_Y_IA + largeur_grille_ia + 20

            # --- ALGORITHME DE DÉCOUPAGE (WORD WRAP) ---
            words = self.ai_phrase_to_display.split(' ')
            lines = []
            current_line = []
            
            for word in words:
                # On teste la taille de la ligne avec le nouveau mot
                test_line = ' '.join(current_line + [word])
                width_test, _ = font_phrase.size(test_line)
                
                if width_test < max_width:
                    current_line.append(word)
                else:
                    # Si c'est trop long, on valide la ligne actuelle et on en commence une nouvelle
                    lines.append(' '.join(current_line))
                    current_line = [word]
            
            # Ne pas oublier d'ajouter la dernière ligne
            lines.append(' '.join(current_line))

            # --- AFFICHAGE DES LIGNES ---
            for i, line in enumerate(lines):
                phrase_surf = font_phrase.render(line, True, text_color)
                
                # Calcul de la position Y pour cette ligne spécifique
                current_y = start_y_phrase + (i * line_spacing)
                
                phrase_rect = phrase_surf.get_rect(midtop=(center_x_ia, current_y))

                # Fond noir pour chaque ligne (pour la lisibilité)
                bg_rect = phrase_rect.inflate(10, 5)
                s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                s.fill((0, 0, 0, 150))
                self.screen.blit(s, bg_rect)

                self.screen.blit(phrase_surf, phrase_rect)

        # ---------------------------------------------------------
        # 6. PROJECTILE
        # ---------------------------------------------------------
        if self.projectile:
            pygame.draw.circle(self.screen, self.projectile["color"], 
                               (int(self.projectile["pos"][0]), int(self.projectile["pos"][1])), 8)

        if self.winner:
            # Sécurité : Si self.winner est un objet Player ou juste un string
            nom_gagnant = self.winner.name if hasattr(self.winner, "name") else str(self.winner)
            
            msg = self.title_font.render(f"{nom_gagnant} a gagné !", True, (255,255,0))
            pygame.mixer.music.stop()
            
            # On centre aussi le message de victoire
            msg_rect = msg.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
            self.screen.blit(msg, msg_rect)