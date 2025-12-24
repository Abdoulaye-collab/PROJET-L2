import pygame
import random
from player import Player, ALL_CARDS
from settings import CARDS_ENABLED, FONT_NAME_2,COLOR_TEXT_MAGIC,FONT_NAME_GRIMOIRE,COLOR_MAGIC_PLAYER,COLOR_MAGIC_ENEMY, FONT_NAME, COLOR_UI_BACKGROUND,SCREEN_WIDTH,SCREEN_HEIGHT
from ai_llm import query_huggingface
from ai_personalities import AI_PERSONALITIES, get_ai_phrase
from cards import apply_card_effect, CARD_HEIGHT, CARD_SPACING, CARD_WIDTH
from GameOver import GameOver
from ai_llm import get_llm_coordinates
from settings import (
    COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, COLOR_WATER_LIT, 
    COLOR_HIT, COLOR_SHIP, 
    CELL_SIZE, GRID_SIZE,
    GRID_OFFSET_X_PLAYER, GRID_OFFSET_X_ENEMY
)
# 1. POUR LES GRILLES
COLOR_GRID_NEON = (0, 255, 255)      # Cyan électrique éclatant (Lignes de la grille)
# Si tu utilises le remplissage transparent "eau" dans les cases, utilise celle-ci :
COLOR_CELL_TINT = (0, 50, 100)       # Un bleu profond pour teinter l'eau (avec set_alpha bas)
COLOR_GRID_IA_PURPLE = (160, 32, 240)
# 2. POUR LES FENÊTRES ET PANNEAUX (ex: Flotte Ennemie)
COLOR_PANEL_BG_DARK = (5, 5, 30)     # Bleu nuit quasi noir pour le fond des panneaux
PANEL_ALPHA_VALUE = 190              # Transparence des panneaux (plus élevé = plus sombre/lisible)
COLOR_PANEL_BORDER = COLOR_GRID_NEON # La bordure des panneaux de la même couleur que la grille

# 3. POUR LE TEXTE
COLOR_TEXT_TITLE = (255, 255, 255)   # Blanc pur éclatant pour les titres importants
COLOR_TEXT_NORMAL = (200, 240, 255)  # Blanc bleuté pour le texte standard (plus doux)

# 1. JOUEUR (Petite grille à gauche)
CELL_SIZE_PLAYER = 35
START_X_PLAYER = 50
START_Y_PLAYER = 250 

# 2. IA RIVALE (Grande grille à droite)
CELL_SIZE_IA = 55
START_X_IA = 800  
START_Y_IA = 150  

GRID_SIZE = 10
GRID_OFFSET_Y = 200
PROJECTILE_SPEED = 80

def load_assets(cell_size):
    """Charge les ressources nécessaires"""
    assets = {}
    FACTOR_SIZE = 1.5
    

class Game:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.player = Player("Joueur")
        self.enemy = Player("IA")
        self.turn_count = 1
        self.winner = None
        self.game_over= False
        self.game_over_screen = None
        self.font = pygame.font.Font(FONT_NAME_GRIMOIRE, 50)
        self.title_font = pygame.font.Font(FONT_NAME_GRIMOIRE, 55)
        self.background_image = pygame.image.load("assets/images/fond_marin.png").convert()
        # 2. Redimensionner l'image à la taille exacte de ta fenêtre
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.selected_card = None
        self.awaiting_target = False

        self.ai_personality = "Gentille"
        self.ai_phrase_to_display = ""
        self.ai_targets_buffer = []
        self.extra_shot = 0
        self.projectile = None  
        self.ia_delay = 0
        self.ia_pending = False
        self.player_turn = True
        self.text_status = f"Tour de {self.player.name} !"
        self.cards_played_total = 0
        
        # Audio
        pygame.mixer.init()
        try:
            pygame.mixer.music.load("assets/sounds/theme.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            self.sound_hit = pygame.mixer.Sound("assets/sounds/hit.wav")
            self.sound_miss = pygame.mixer.Sound("assets/sounds/miss.wav")
            self.sound_card = pygame.mixer.Sound("assets/sounds/card.wav")
        except:
            print("⚠️ Erreur Audio : Fichiers sons non trouvés.")

        self.start_time = pygame.time.get_ticks()
        self.winner = None
        self.game_over = False 

        self.THEME_PLAYER = (COLOR_MAGIC_PLAYER)
        self.THEME_ENEMY = (COLOR_MAGIC_ENEMY)
        self.magic_particles = []

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

         # --- GESTION VISUELLE ---
        if shooter == self.player:
            start_x = START_X_PLAYER + (GRID_SIZE*CELL_SIZE_PLAYER)//2
            start_y = START_Y_PLAYER + (GRID_SIZE*CELL_SIZE_PLAYER)//2
            proj_color = self.THEME_PLAYER

            if self.selected_card == "Bombe": proj_color = (255, 165, 0)
            elif self.selected_card == "Salve": proj_color = (255, 50, 50)
            elif self.selected_card == "Radar": proj_color = (0, 255, 255)
        else:
            start_x = START_X_IA + (GRID_SIZE * CELL_SIZE_IA) // 2
            start_y = START_Y_IA + (GRID_SIZE * CELL_SIZE_IA) // 2
            proj_color = self.THEME_ENEMY
        
        self.projectile = {"shooter": shooter, "target": (row, col), "pos": [start_x, start_y], "color": proj_color}

        # --- LOGIQUE DE TOUCHE ---
        if val == 1:
            for ship, pos in target.ship_positions.items():
                if (row, col) in pos and ship in target.reinforced_ships:
                    target.reinforced_ships.remove(ship)
                    return "Renforcé"

            target.board[row][col] = -1
            shooter.hits += 1
            
            # Jouer son (si chargé)
            if hasattr(self, 'sound_hit'): self.sound_hit.play()
            
            if shooter == self.player:
                explosion_color = self.THEME_PLAYER
            else:
                explosion_color = self.THEME_ENEMY

            if target == self.enemy:
                impact_x = START_X_IA + col * CELL_SIZE_IA + (CELL_SIZE_IA // 2)
                impact_y = START_Y_IA + row * CELL_SIZE_IA + (CELL_SIZE_IA // 2)
            else:
                # Si l'IA nous touche (optionnel, si tu veux aussi des particules quand tu es touché)
                impact_x = START_X_PLAYER + col * CELL_SIZE_PLAYER + (CELL_SIZE_PLAYER // 2)
                impact_y = START_Y_PLAYER + row * CELL_SIZE_PLAYER + (CELL_SIZE_PLAYER // 2)
            
            self.trigger_hit_particles(impact_x, impact_y, explosion_color)
            
            self.check_win()
            return "Touché"

        elif val == 0:
            target.board[row][col] = -2
            if hasattr(self, 'sound_miss'): self.sound_miss.play()
            return "Manqué"

        return "Déjà tiré"
    
    def is_ship_sunk(self, player, ship_name):
        """Vérifie si un bateau est entièrement coulé sans supprimer ses coordonnées."""
        positions = player.ship_positions[ship_name]
        if not positions: return True # Sécurité
        
        # On regarde sur le plateau si toutes les cases du bateau valent -1 (Touché)
        for r, c in positions:
            if player.board[r][c] != -1:
                return False # Il reste au moins une case intacte
        return True

    def check_win(self):
        # --- SÉCURITÉ ABSOLUE ---
        # Si la partie est déjà finie, ON ARRÊTE TOUT DE SUITE.
        # Cela empêche le bug du "double affichage" ou du changement de nom.
        if self.game_over: 
            return 
        # ------------------------

        # 1. EST-CE QUE LE JOUEUR A GAGNÉ ? (L'IA n'a plus de bateaux)
        all_sunk_enemy = True
        for ship_name in self.enemy.ship_positions:
            if not self.is_ship_sunk(self.enemy, ship_name):
                all_sunk_enemy = False
                break 
        
        if all_sunk_enemy:
            print("VICTOIRE VALIDÉE : JOUEUR GAGNE") # Debug
            self.winner = self.player
            self.game_over = True # On verrouille la partie
            
            duration = (pygame.time.get_ticks() - self.start_time) // 1000
            
            # ORDRE : (Ecran, GAGNANT, PERDANT, Temps)
            self.game_over_screen = GameOver(
                self.screen, 
                self.player,  # Gagnant = Objet Joueur
                self.enemy,   # Perdant = Objet IA
                duration,
                self.cards_played_total,
                True
            )
            return

        # 2. EST-CE QUE L'IA A GAGNÉ ? (Le Joueur n'a plus de bateaux)
        all_sunk_player = True
        for ship_name in self.player.ship_positions:
            if not self.is_ship_sunk(self.player, ship_name):
                all_sunk_player = False
                break
        
        if all_sunk_player:
            print("VICTOIRE VALIDÉE : IA GAGNE") # Debug
            self.winner = self.enemy
            self.game_over = True # On verrouille la partie
            
            duration = (pygame.time.get_ticks() - self.start_time) // 1000
            
            # ORDRE : (Ecran, GAGNANT, PERDANT, Temps)
            self.game_over_screen = GameOver(
                self.screen, 
                self.enemy,   # Gagnant = Objet IA
                self.player,  # Perdant = Objet Joueur
                duration,
                self.cards_played_total,
                False
            )
            return

    def ai_play(self):
        if self.winner: return
        
        row, col = None, None

        # ---------------------------------------------------------
        # PHASE 1 : MODE TARGET (Logique pure)
        # Si on a des cibles en attente (suite à un touché précédent)
        # ---------------------------------------------------------
        if not hasattr(self, 'ai_targets_buffer'): self.ai_targets_buffer = []

        while self.ai_targets_buffer:
            # On prend la prochaine cible prioritaire
            candidate = self.ai_targets_buffer.pop(0) # On prend le premier (FIFO)
            r, c = candidate
            
            # On vérifie que la case est valide et pas encore jouée
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                valeur = self.player.board[r][c]
                if valeur == 0 or valeur == 1: # Eau ou Bateau caché
                    row, col = r, c
                    print(f"IA (TARGET) : Je finis le bateau en {row},{col}")
                    break 
        
        # ---------------------------------------------------------
        # PHASE 2 : MODE HUNT (Intuition LLM)
        # Si aucune cible prioritaire, on cherche avec le LLM
        # ---------------------------------------------------------
        if row is None or col is None:
            print("IA (HUNT) : Je cherche une nouvelle cible avec le LLM...")
            
            # Appel à ton fichier ai_llm.py
            llm_move = get_llm_coordinates()
            
            if llm_move:
                r_llm, c_llm = llm_move
                # Vérification : Est-ce valide ?
                if (0 <= r_llm < GRID_SIZE and 0 <= c_llm < GRID_SIZE and 
                    self.player.board[r_llm][c_llm] in [0, 1]):
                    row, col = r_llm, c_llm
                    print(f"IA (LLM) : L'Oracle suggère {row},{col}")

            # -----------------------------------------------------
            # PHASE 3 : SECOURS (Aléatoire intelligent)
            # Si le LLM a échoué ou donné une case invalide
            # -----------------------------------------------------
            if row is None:
                print("IA (RANDOM) : LLM indisponible, tir aléatoire.")
                available = []
                for r in range(GRID_SIZE):
                    for c in range(GRID_SIZE):
                        if self.player.board[r][c] in [0, 1]:
                            available.append((r, c))
                
                if available:
                    # Astuce Damier (Checkerboard) pour optimiser la recherche
                    checkerboard = [p for p in available if (p[0] + p[1]) % 2 == 0]
                    if checkerboard and len(available) > 40:
                        row, col = random.choice(checkerboard)
                    else:
                        row, col = random.choice(available)

        # ---------------------------------------------------------
        # ACTION : TIR ET MÉMOIRE
        # ---------------------------------------------------------
        if row is not None and col is not None:
            # On tire
            result = self.shoot(self.enemy, row, col)
            
            # SI TOUCHÉ -> ON AJOUTE LES VOISINS (C'est ta fonction register_result)
            if result == "Touché":
                # Haut, Bas, Gauche, Droite
                voisins = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
                random.shuffle(voisins) # On mélange pour varier l'attaque
                for v in voisins:
                    # On les ajoute à la liste pour les prochains tours
                    self.ai_targets_buffer.append(v)

            # Gestion du texte d'ambiance
            if result in ("Touché", "Renforcé"):
                self.ai_phrase_to_display = get_ai_phrase(self.ai_personality, "hit")
            else:
                self.ai_phrase_to_display = get_ai_phrase(self.ai_personality, "miss")

            self.turn_count += 1
            self.player_turn = True
            self.text_status = f"Tour de {self.player.name} !"

    def handle_event(self, event):
        # 1. GESTION DE L'ÉCRAN DE FIN
        if self.game_over and self.game_over_screen:
            self.game_over_screen.handle_event(event)
            if self.game_over_screen.done:
                self.winner = "MENU" 
            return

        # 2. GESTION CLIC SOURIS (Jeu en cours)
        if event.type == pygame.MOUSEBUTTONDOWN and not self.winner:
            mouse_x, mouse_y = event.pos

            # --- A. CLIC SUR UNE CARTE (Main du joueur) ---
            card_x = START_X_PLAYER
            card_y = START_Y_PLAYER + (GRID_SIZE * CELL_SIZE_PLAYER) + 30
            
            for card in self.player.cards:
                rect = pygame.Rect(card_x, card_y, 120, 40)
                if rect.collidepoint(mouse_x, mouse_y):
                    if CARDS_ENABLED:
                        if self.selected_card == card:
                            # Désélectionner si on reclique dessus
                            self.selected_card = None
                            self.awaiting_target = False
                            self.text_status = "Carte désélectionnée."
                            print("Carte désélectionnée")
                        else:
                            # Sélectionner la carte
                            self.selected_card = card 
                            self.awaiting_target = True
                            self.text_status = f"Carte {card} activée ! Ciblez la grille IA."
                            print(f"Carte sélectionnée : {card}")
                            if hasattr(self, 'sound_card'): self.sound_card.play()
                    return # On arrête ici pour ne pas cliquer ailleurs
                
                card_x += CARD_WIDTH + CARD_SPACING

            # --- B. CLIC SUR LA GRILLE ENNEMIE ---
            width_ia = GRID_SIZE * CELL_SIZE_IA
            height_ia = GRID_SIZE * CELL_SIZE_IA
            
            is_inside_ia_grid = (START_X_IA <= mouse_x < START_X_IA + width_ia and 
                                 START_Y_IA <= mouse_y < START_Y_IA + height_ia)
            
            if is_inside_ia_grid:
                col = (mouse_x - START_X_IA) // CELL_SIZE_IA
                row = (mouse_y - START_Y_IA) // CELL_SIZE_IA
                
                print(f"Clic Grille IA : Case {row},{col}") # DEBUG

                # CAS 1 : UTILISATION DE CARTE
                if self.selected_card and self.awaiting_target:
                    print(f" -> Lancement effet carte : {self.selected_card}") # DEBUG
                    
                    # Appel de cards.py
                    apply_card_effect(self, self.selected_card, row, col)
                    
                    self.cards_played_total += 1
                    
                    # Retirer la carte de la main
                    if self.selected_card in self.player.cards:
                        self.player.cards.remove(self.selected_card)
                    
                    # Reset
                    self.selected_card = None
                    self.awaiting_target = False
                    return # IMPORTANT : On ne tire pas en plus

                # CAS 2 : TIR NORMAL
                if self.player_turn:
                    res = self.shoot(self.player, row, col)
                    
                    if res != "Déjà tiré":
                        # Gestion Bonus Double Tir
                        if self.extra_shot > 0:
                            self.extra_shot -= 1
                            self.text_status = f"BONUS : Encore {self.extra_shot + 1} tir(s) !"
                        else:
                            # Fin du tour
                            self.player_turn = False
                            self.text_status = "Tour de l'IA..."
                            self.ia_delay = 800
                            self.ia_pending = True
    def update(self):
        if self.projectile:
            target_row, target_col = self.projectile["target"]
            if self.projectile["shooter"] == self.player:
                target_x = START_X_IA + target_col * CELL_SIZE_IA + (CELL_SIZE_IA // 2)
                target_y = START_Y_IA + target_row * CELL_SIZE_IA + (CELL_SIZE_IA // 2)
            else:
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

    # ------------------------------------------------------------------
    #  DESSIN DES FORMES CONTINUES (OVALES)
    # ------------------------------------------------------------------
    def draw_continuous_ships(self, player, start_x, start_y, cell_size):
        """Dessine les bateaux comme des formes continues."""
        #COULEUR DES BATEAUX
        if player == self.player:
            ship_color = self.THEME_PLAYER  
            border_color = (200, 255, 255)  
        else:
            ship_color = self.THEME_ENEMY   
            border_color = (220, 150, 255)  
        
        for ship_name, positions in player.ship_positions.items():
            if not positions: continue

            sorted_pos = sorted(positions)
            start_row, start_col = sorted_pos[0]
            
            # Déduction Orientation / Longueur
            if len(positions) > 1:
                end_row, end_col = sorted_pos[-1]
                if start_row == end_row: # Horizontal
                    orientation, length = "H", (end_col - start_col) + 1
                else: # Vertical
                    orientation, length = "V", (end_row - start_row) + 1
            else:
                orientation, length = "H", 1

            px = start_x + start_col * cell_size
            py = start_y + start_row * cell_size
            padding = 4 
            
            if orientation == "H":
                rect_w = length * cell_size - (padding * 2)
                rect_h = cell_size - (padding * 2)
            else:
                rect_w = cell_size - (padding * 2)
                rect_h = length * cell_size - (padding * 2)
            
            ship_rect = pygame.Rect(px + padding, py + padding, rect_w, rect_h)
            pygame.draw.rect(self.screen, ship_color, ship_rect, border_radius=15)
            pygame.draw.rect(self.screen, border_color, ship_rect, 2, border_radius=15)

    # ------------------------------------------------------------------
    #  DESSINE UNIQUEMENT LES LIGNES ET MARQUEURS
    # ------------------------------------------------------------------
    def draw_grid_lines_and_markers(self, player, start_x, start_y, cell_size):
        # 1. Bouclier (optionnel)
        if player == self.player and "Bouclier_Actif" in player.reinforced_ships:
            total = GRID_SIZE * cell_size
            pygame.draw.rect(self.screen, (0, 191, 255), (start_x-5, start_y-5, total+10, total+10), 4, border_radius=5)
        
        # --- STYLE IA (Grande Grille) ---
        if player == self.enemy:
            current_grid_color = COLOR_GRID_IA_PURPLE # Violet pour l'IA
            current_text_color = COLOR_GRID_IA_PURPLE
            font_coords = pygame.font.Font(FONT_NAME_GRIMOIRE,50)
            text_margin = 30
                                    
        # --- STYLE JOUEUR (Petite Grille) --- 
        else:
            current_grid_color = COLOR_GRID_NEON 
            current_text_color =  COLOR_GRID_NEON    # Cyan pour le Joueur
            font_coords = pygame.font.Font(FONT_NAME_GRIMOIRE, 30)
            text_margin = 20

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(start_x + col*cell_size, start_y + row*cell_size, cell_size, cell_size)
                val = player.board[row][col]
                
                pygame.draw.rect(self.screen, current_grid_color, rect, 1)

                # --- MARQUEURS (Touché / Manqué) ---
                if val == -1: # TOUCHÉ
                    hull_rect = rect.inflate(-4, -4)
                    hull_color = (0, 100, 120) if player == self.player else (80, 20, 120)
                    pygame.draw.rect(self.screen, hull_color, hull_rect, border_radius=5)
                    border_color = (0, 150, 180) if player == self.player else (120, 40, 180)
                    pygame.draw.rect(self.screen, border_color, hull_rect, 2, border_radius=5)
                    
                    center_pos = rect.center
                    radius = cell_size // 4

                    s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    pygame.draw.circle(s,(255, 0, 0, 150),(cell_size//2, cell_size//2), radius + 4)
                    self.screen.blit(s, rect)
                    
                    pygame.draw.circle(self.screen, (220, 0, 0), center_pos, radius)
                    pygame.draw.circle(self.screen, (255, 100, 100), (center_pos[0]-2, center_pos[1]-2), radius//3)
                    
            
                elif val == -2: # MANQUÉ
                    pygame.draw.line(self.screen, (200, 200, 255), (rect.left+10, rect.top+10), (rect.right-10, rect.bottom-10), 2)
                    pygame.draw.line(self.screen, (200, 200, 255), (rect.left+10, rect.bottom-5), (rect.right-10, rect.top+5), 2)

        # Coordonnées (Lettres/Chiffres)
        for i in range(GRID_SIZE):
            # Lettres en haut
            x_pos = start_x + i * cell_size + cell_size // 2
            letter = chr(ord('A') + i)
            t = font_coords.render(letter, True, current_text_color)
            self.screen.blit(t, t.get_rect(center=(x_pos, start_y - text_margin)))
            
            # Chiffres à gauche
            y_pos = start_y + i * cell_size + cell_size // 2
            t2 = font_coords.render(str(i + 1), True, current_text_color)
            self.screen.blit(t2, t2.get_rect(center=(start_x - text_margin,y_pos)))

    def draw_cards(self, player):
        if not CARDS_ENABLED: return
        start_x_cards = START_X_PLAYER
        start_y_cards = START_Y_PLAYER + (GRID_SIZE * CELL_SIZE_PLAYER) + 20
        x, y = start_x_cards, start_y_cards

        for card in player.cards:
            rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            if card == self.selected_card:
                rect.y -= 10 
                border_color, bg_color = COLOR_MAGIC_PLAYER, COLOR_TEXT_NORMAL
            else:
                border_color, bg_color = (0, 0, 0), COLOR_TEXT_NORMAL
            
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=8)
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=8)
            
            font_card = pygame.font.Font(FONT_NAME_GRIMOIRE, 30)
            text_surf = font_card.render(card, True, (0,0,0))
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))
            x += CARD_WIDTH + CARD_SPACING

    def draw_enemy_status(self):
        font_small = pygame.font.Font(FONT_NAME_2, 40) 
        font_bold = pygame.font.Font(FONT_NAME_GRIMOIRE, 50)
        
        fin_grille_joueur = START_X_PLAYER + (GRID_SIZE * CELL_SIZE_PLAYER)
        debut_grille_ia = START_X_IA
        center_x = (fin_grille_joueur + debut_grille_ia) // 2
        
        hauteur_grille = GRID_SIZE * CELL_SIZE_IA
        centre_vertical_grille = START_Y_IA + (hauteur_grille // 2)
        hauteur_bloc_texte = 400
        decalage_vers_le_haut = 50
        start_y = centre_vertical_grille - (hauteur_bloc_texte // 2) - decalage_vers_le_haut
        
        panel_width = 300
        panel_height = hauteur_bloc_texte + 30
        panel_x = center_x - (panel_width // 2)
        panel_y = start_y - 15
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(PANEL_ALPHA_VALUE)
        panel_surface.fill(COLOR_PANEL_BG_DARK)
        self.screen.blit(panel_surface, (panel_x, panel_y))

        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, (panel_x, panel_y, panel_width, panel_height), 1, border_radius=10)

        title = font_bold.render("Flotte Ennemie", True, COLOR_MAGIC_ENEMY)
        self.screen.blit(title, title.get_rect(midtop=(center_x, start_y - 30)))

        all_ships = self.enemy.ship_positions.keys()
        i, nb_coules = 0, 0
        line_spacing = 45
        marge_sous_titre = 50
        
        for ship_name in all_ships:
            est_coule = self.is_ship_sunk(self.enemy, ship_name)
            if est_coule:
                color, text_str = (255, 100, 100), f" {ship_name}"
                nb_coules += 1
            else:
                color, text_str = COLOR_TEXT_NORMAL, f" {ship_name}" 

            surf = font_small.render(text_str, True, color)
            rect = surf.get_rect(midtop=(center_x, start_y + marge_sous_titre +(i * line_spacing) ))
            self.screen.blit(surf, rect)
            if est_coule:
                pygame.draw.line(self.screen, color, (rect.left, rect.centery), (rect.right, rect.centery), 2)
            i += 1

        summary = f"Coulés : {nb_coules}/{len(all_ships)}"
        col_summary = (0, 255, 0) if nb_coules == len(all_ships) else (255, 255, 255)
        surf_summary = font_bold.render(summary, True, col_summary)
        rect_summary = surf_summary.get_rect(midtop=(center_x, start_y + marge_sous_titre + (i * line_spacing) + 50))
        #cadre autour du score
        pygame.draw.rect(self.screen, COLOR_MAGIC_ENEMY, rect_summary.inflate(20,5), 1, border_radius=4)
        self.screen.blit(surf_summary, rect_summary)

    # ------------------------------------------------------------------
    #  FONCTION DRAW PRINCIPALE (L'ORDRE EST CRUCIAL)
    # ------------------------------------------------------------------
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        # 1. DESSINER LE FOND DE L'EAU (RECTANGLES BLEUS)
        # Pour le Joueur
        rect_water_p = pygame.Rect(START_X_PLAYER, START_Y_PLAYER, GRID_SIZE*CELL_SIZE_PLAYER, GRID_SIZE*CELL_SIZE_PLAYER)
        pygame.draw.rect(self.screen, COLOR_CELL_TINT, rect_water_p)
        # Pour l'IA
        rect_water_ia = pygame.Rect(START_X_IA, START_Y_IA, GRID_SIZE*CELL_SIZE_IA, GRID_SIZE*CELL_SIZE_IA)
        pygame.draw.rect(self.screen, COLOR_OCEAN_DARK, rect_water_ia)

        # 2. DESSINER LES BATEAUX CONTINUS DU JOUEUR (Par-dessus l'eau, dessous la grille)
        self.draw_continuous_ships(self.player, START_X_PLAYER, START_Y_PLAYER, CELL_SIZE_PLAYER)
        
        enemy_sunk_ships = Player("Temp")
        enemy_sunk_ships.ship_positions = {}

        for name in self.enemy.ship_positions:
            if self.is_ship_sunk(self.enemy, name):
                enemy_sunk_ships.ship_positions[name] = self.enemy.ship_positions[name]

        self.draw_continuous_ships(enemy_sunk_ships, START_X_IA, START_Y_IA, CELL_SIZE_IA)
        # for ship_name, positions in self.enemy.ship_positions.items():
        #     # On ne dessine QUE si le bateau est coulé (liste vide)
        #     if len(positions) == 0: 
        #         pass

        # 3. DESSINER LES LIGNES ET MARQUEURS (Par-dessus tout)
        self.draw_grid_lines_and_markers(self.player, START_X_PLAYER, START_Y_PLAYER, CELL_SIZE_PLAYER)
        self.draw_grid_lines_and_markers(self.enemy, START_X_IA, START_Y_IA, CELL_SIZE_IA)
        
        # Le reste (Textes, UI, etc.)
        self.draw_enemy_status()
        self.draw_cards(self.player)

        # Status
        color_status = (COLOR_MAGIC_PLAYER) if self.player_turn else (COLOR_MAGIC_ENEMY)
        status_surf = self.font.render(self.text_status, True, color_status)
        self.screen.blit(status_surf, status_surf.get_rect(midtop=(self.screen.get_width() // 2, 20)))

        # Noms
        name_player = self.title_font.render(self.player.name, True, COLOR_TEXT_NORMAL)
        self.screen.blit(name_player, name_player.get_rect(midbottom=(START_X_PLAYER + (GRID_SIZE*CELL_SIZE_PLAYER)//2, START_Y_PLAYER - 30)))
        
        name_enemy = self.title_font.render(self.enemy.name, True, (255,255,255))
        self.screen.blit(name_enemy, name_enemy.get_rect(midbottom=(START_X_IA + (GRID_SIZE*CELL_SIZE_IA)//2, START_Y_IA - 35)))

        # Chrono
        current_time = pygame.time.get_ticks() - self.start_time
        timer_text = f"{current_time // 60000:02}:{(current_time // 1000) % 60:02}"
        font_timer = pygame.font.Font(FONT_NAME, 22) 
        surf_timer = font_timer.render(f" {timer_text}", True, (255, 255, 255))
        rect_timer = surf_timer.get_rect(topright=(self.screen.get_width() - 20, 20))
        bg_rect_timer = rect_timer.inflate(20, 10)
        s_timer = pygame.Surface((bg_rect_timer.width, bg_rect_timer.height), pygame.SRCALPHA)
        s_timer.fill((0, 0, 0, 150))
        self.screen.blit(s_timer, bg_rect_timer)
        self.screen.blit(surf_timer, rect_timer)

        # Phrase IA
        if self.ai_phrase_to_display:
            font_phrase = self.font
            center_x_ia = START_X_IA + (GRID_SIZE * CELL_SIZE_IA // 2)
            start_y_phrase = START_Y_IA + (GRID_SIZE * CELL_SIZE_IA) + 20
            
            words = self.ai_phrase_to_display.split(' ')
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
                self.screen.blit(s, bg_rect)
                self.screen.blit(phrase_surf, phrase_rect)

        # Projectile
        if self.projectile:
            pygame.draw.circle(self.screen, self.projectile["color"], (int(self.projectile["pos"][0]), int(self.projectile["pos"][1])), 8)
            pygame.draw.circle(self.screen, (255, 255, 255), 
                               (int(self.projectile["pos"][0]), int(self.projectile["pos"][1])), 9, width=1)
        self.update_and_draw_particles()

        # Victoire
        # --------------------------------------------------------------
        #  BLOC VICTOIRE (CORRIGÉ)
        # --------------------------------------------------------------
        # Cas 1 : L'écran de fin a été créé correctement dans check_win
        if self.game_over and self.game_over_screen:
            self.game_over_screen.draw()
            
        # Cas 2 : Un gagnant est défini, mais l'écran n'est pas prêt (Sécurité)
        elif self.winner: 
            # On affiche juste un texte simple pour éviter le bug
            # NE CRÉE SURTOUT PAS DE 'GameOver(...)' ICI !!!
            nom = self.winner.name if hasattr(self.winner, "name") else str(self.winner)
            msg = self.title_font.render(f"{nom} a gagné !", True, (255, 255, 0))
            
            # Fond noir semi-transparent
            s_win = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            s_win.fill((0, 0, 0, 180))
            self.screen.blit(s_win, (0, 0))
            
            # Message centré
            rect = msg.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
            self.screen.blit(msg, rect)
            
            
            

    # ----------------------------------------------------------------------
    #  GESTION DES PARTICULES D'IMPACT (MAGIE CYAN)
    # ----------------------------------------------------------------------
    def trigger_hit_particles(self, x, y,main_color):
        """Crée une explosion de particules cyan au point (x, y)."""
        import random

        r,g,b = main_color

        for _ in range(20): # 20 particules par impact
            var = random.randint(-30, 30)
            r = max(0, min(255, r + var))
            g = max(0, min(255, g + var))
            b = max(0, min(255, b + var))

            self.magic_particles.append({
                'x': x,
                'y': y,
                # Explosion dans toutes les directions
                'dx': random.uniform(-3, 3),
                'dy': random.uniform(-3, 3),
                'timer': random.randint(20, 40), # Durée de vie
                'size': random.randint(4, 8),
                # Couleur Cyan Magique
                'color': (r,g,b)
            })

    def update_and_draw_particles(self):
        """Met à jour et dessine les particules."""
        for i in range(len(self.magic_particles) - 1, -1, -1):
            p = self.magic_particles[i]
            
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['timer'] -= 1
            p['size'] -= 0.1
            
            if p['timer'] <= 0 or p['size'] <= 0:
                self.magic_particles.pop(i)
                continue
            
            # Dessin avec transparence
            alpha = int((p['timer'] / 40) * 255)
            if alpha < 0: alpha = 0
            
            s = pygame.Surface((int(p['size']*2), int(p['size']*2)), pygame.SRCALPHA)
            pygame.draw.circle(s, p['color'] + (alpha,), (int(p['size']), int(p['size'])), int(p['size']))
            self.screen.blit(s, (p['x'] - p['size'], p['y'] - p['size']))