import pygame
import random

from settings import *
from effects import ParticleSystem
import draw_utils as du

class Placement:
    # ==============================================================================
    #  1. INITIALISATION
    # ==============================================================================
    def __init__(self, screen, player, assets):
        self.screen = screen
        self.player = player
        self.assets = assets

        # --- ÉTAT DU PLACEMENT ---
        self.current_ship_index = 0
        self.orientation = "H" # "H"orizontal ou "V"ertical
        self.done = False
        
        # --- POLICES D'ÉCRITURE ---
        self.font_grimoire = pygame.font.Font(FONT_NAME_GRIMOIRE, 60)
        self.font_coords = pygame.font.Font(FONT_NAME_GRIMOIRE2, 30)
        self.font_large = pygame.font.Font(FONT_NAME_GRIMOIRE2, 70)

        # --- SYSTÈME DE PARTICULES ---
        self.particles = ParticleSystem()

        # --- CHARGEMENT DU FOND ---
        try:
            image_path = "assets/images/background.png"
            background_img = pygame.image.load(image_path).convert()
            self.background_image = pygame.transform.scale(
                background_img, 
                (self.screen.get_width(), self.screen.get_height())
            )
        except:
            self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_image.fill((10, 10, 30))

    # ==============================================================================
    #  2. GESTION DES ÉVÉNEMENTS (CLAVIER / SOURIS)
    # ==============================================================================
    def handle_event(self, event):
        # Rotation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.orientation = "V" if self.orientation == "H" else "H"

        # Clic gauche pour placer
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = (x - PLACEMENT_GRID_OFFSET_X) // PLACEMENT_CELL_SIZE
            row = (y - PLACEMENT_GRID_OFFSET_Y) // PLACEMENT_CELL_SIZE

            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                self.place_ship(row, col)

    # ==============================================================================
    #  3. LOGIQUE DE PLACEMENT
    # ==============================================================================
    def check_placement_validity(self, start_row, start_col, size):
        """ Vérifie si le bateau rentre dans la grille et ne chevauche pas """
        cells = []
        is_valid = True
        
        for i in range(size):
            r = start_row + i if self.orientation == "V" else start_row
            c = start_col + i if self.orientation == "H" else start_col
            
            # Vérif 1: Hors limites
            if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                is_valid = False
            # Vérif 2: Déjà occupé
            elif self.player.board[r][c] != 0:
                is_valid = False
                
            cells.append((r, c))

        return is_valid, cells
    
    def place_ship(self, row, col):
        """ Valide et enregistre le bateau sur la grille """
        if self.current_ship_index >= len(self.player.ships):
            self.done = True
            return
        
        name, size = self.player.ships[self.current_ship_index]
        is_valid, positions = self.check_placement_validity(row, col, size)
        
        if not is_valid: return
        
        # Enregistrement
        for r, c in positions:
            self.player.board[r][c] = 1

            # FX : Explosion magique lors du placement (Cyan)
            px = PLACEMENT_GRID_OFFSET_X + c * PLACEMENT_CELL_SIZE + PLACEMENT_CELL_SIZE // 2
            py = PLACEMENT_GRID_OFFSET_Y + r * PLACEMENT_CELL_SIZE + PLACEMENT_CELL_SIZE // 2
            self.particles.trigger_hit_particles(px, py, (0, 255, 255))

        self.player.ship_positions[name] = positions
        self.current_ship_index += 1
        
        # Fin du placement ?
        if self.current_ship_index >= len(self.player.ships):
            self.done = True

    # ==============================================================================
    #  4. FONCTIONS DE DESSIN (GRILLE & BATEAUX)
    # ==============================================================================
    def draw_ship_shape(self, row, col, length, orientation, color, alpha=255):
        """ Dessine un rectangle arrondi représentant un bateau """

        px = PLACEMENT_GRID_OFFSET_X + col * PLACEMENT_CELL_SIZE
        py = PLACEMENT_GRID_OFFSET_Y + row * PLACEMENT_CELL_SIZE
        padding = 5 

        # Calcul dimensions selon orientation
        if orientation == "H":
            width_px = (length * PLACEMENT_CELL_SIZE) - (padding * 2)
            height_px = PLACEMENT_CELL_SIZE - (padding * 2)
        else:
            width_px = PLACEMENT_CELL_SIZE - (padding * 2)
            height_px = (length * PLACEMENT_CELL_SIZE) - (padding * 2)
        
        # Cas 1 : Transparence (Preview)
        if alpha < 255:
            s = pygame.Surface((width_px, height_px), pygame.SRCALPHA)
            rect_surf = pygame.Rect(0, 0, width_px, height_px)
            pygame.draw.rect(s, color + (alpha,), rect_surf, border_radius=15)
            pygame.draw.rect(s, (255, 255, 255, alpha), rect_surf, 2, border_radius=15)
            self.screen.blit(s, (px + padding, py + padding))
        # Cas 2 : Solide (Placé)
        else:
            ship_rect = pygame.Rect(px + padding, py + padding, width_px, height_px)
            pygame.draw.rect(self.screen, color, ship_rect, border_radius=15)
            # Bordure un peu plus claire
            border_col = (min(color[0]+40, 255), min(color[1]+40, 255), min(color[2]+40, 255))
            pygame.draw.rect(self.screen, border_col, ship_rect, 2, border_radius=15)

    def draw_grid(self):
        """ Affiche la grille (Lignes, Chiffres, Lettres) """

        letters = "ABCDEFGHIJ"
        font_grid_big = pygame.font.Font(FONT_NAME_GRIMOIRE2, 30)
        for row in range(GRID_SIZE):
            # Chiffre (Gauche)
            label_num = font_grid_big.render(str(row + 1), True, COLOR_GRIMOIRE_INK)
            num_rect = label_num.get_rect(
                midright=(PLACEMENT_GRID_OFFSET_X - 15, 
                          PLACEMENT_GRID_OFFSET_Y + row * PLACEMENT_CELL_SIZE + (PLACEMENT_CELL_SIZE // 2))
            )
            self.screen.blit(label_num, num_rect)

            for col in range(GRID_SIZE):    
                rect = pygame.Rect(
                    PLACEMENT_GRID_OFFSET_X + col * PLACEMENT_CELL_SIZE,
                    PLACEMENT_GRID_OFFSET_Y + row * PLACEMENT_CELL_SIZE,
                    PLACEMENT_CELL_SIZE, PLACEMENT_CELL_SIZE
                )
                # Case vide
                pygame.draw.rect(self.screen, COLOR_GRIMOIRE_INK, rect, 1)
                
                # Lettre (Haut)
                if row == 0:
                    label_char = self.font_coords.render(letters[col], True, COLOR_GRIMOIRE_INK)
                    char_rect = label_char.get_rect(
                        midbottom=(rect.centerx, PLACEMENT_GRID_OFFSET_Y - 10)
                    )
                    self.screen.blit(label_char, char_rect)

    # ==============================================================================
    #  5. DESSIN GLOBAL (INTERFACE UI)
    # ==============================================================================
    def draw(self):
        self.screen.blit(self.background_image,(0,0))
    
        # --- CONSTANTES UI LOCALES ---
        CENTER_HALF_RIGHT_X = self.screen.get_width() * 3 // 4 
        INSTRUCTION_START_Y = 150 
        LIST_START_Y = INSTRUCTION_START_Y + 100
        LIST_LINE_SPACING = 45
        
        # --- A. TITRE ---
        title_surf = self.font_large.render(f"Grille du Sorcier : {self.player.name}", True, (COLOR_GRIMOIRE_INK))
        grid_center_x = PLACEMENT_GRID_OFFSET_X + (GRID_SIZE * PLACEMENT_CELL_SIZE) // 2
        title_rect = title_surf.get_rect(midtop=(grid_center_x, 5))
        self.screen.blit(title_surf, title_rect)

        # --- B. INSTRUCTIONS ---
        if self.current_ship_index < len(self.player.ships):
            name, size = self.player.ships[self.current_ship_index]
            
            instr1 = self.font_grimoire.render(f"Sort: Déploiement du {name}", True, COLOR_GRIMOIRE_INK)
            self.screen.blit(instr1, instr1.get_rect(centerx=CENTER_HALF_RIGHT_X, y=INSTRUCTION_START_Y))
            
            instr2 = self.font_grimoire.render("[R] pour tourner le navire", True, COLOR_GRIMOIRE_INK)
            self.screen.blit(instr2, instr2.get_rect(centerx=CENTER_HALF_X, y=PLACEMENT_GRID_OFFSET_Y + PLACEMENT_GRID_WIDTH_TOTAL + 10))

        # --- C. LISTE DES BATEAUX (DROITE) ---
        title_list = self.font_grimoire.render("Flotte à placer :", True, COLOR_GRIMOIRE_INK)
        self.screen.blit(title_list, title_list.get_rect(centerx=CENTER_HALF_RIGHT_X, y=LIST_START_Y ))
        
        next_y = LIST_START_Y + 80

        for index, (name, size) in enumerate(self.player.ships):
            is_placed = index < self.current_ship_index
            text_display = f" {name}"
            
            # Position du texte
            ship_rect = pygame.Rect(0, 0, 300, 50) # Rect temporaire pour le centrage
            ship_rect.centerx = CENTER_HALF_RIGHT_X
            ship_rect.y = next_y

            if is_placed:
                
                # Effet Néon (Placé)
                shadow_surf = self.font_grimoire.render(text_display, True, COLOR_GRIMOIRE_INK)
                shadow_rect = shadow_surf.get_rect(centerx=CENTER_HALF_RIGHT_X + 2, y=next_y + 2) # Décalage +2
                self.screen.blit(shadow_surf, shadow_rect)
                
                neon_surf = self.font_grimoire.render(text_display, True, COLOR_TEXT_NEON)
                neon_rect = neon_surf.get_rect(centerx=CENTER_HALF_RIGHT_X, y=next_y)
                self.screen.blit(neon_surf, neon_rect)
                
                # Particules sur le texte placé (Magie)
                if random.random() < 0.1:
                    px = random.randint(neon_rect.left, neon_rect.right)
                    py = random.randint(neon_rect.top, neon_rect.bottom)
                    # Appelle la fonction qu'on a ajoutée dans effects.py
                    self.particles.add_particle(px, py, (0, 255, 255))
            else:
                # Effet Encre (Pas encore placé)
                s = self.font_grimoire.render(text_display, True, COLOR_GRIMOIRE_INK)
                self.screen.blit(s, s.get_rect(centerx=CENTER_HALF_RIGHT_X, y=next_y))


            next_y += LIST_LINE_SPACING + 20

        # --- D. GRILLE & BATEAUX PLACÉS ---
        self.draw_grid()
        
        for name, positions in self.player.ship_positions.items():
            if not positions: continue

            # Calcul de la forme
            sorted_pos = sorted(positions)
            start_r, start_c = sorted_pos[0]
            if len(positions) > 1:
                end_r, end_c = sorted_pos[-1]
                orientation, length = ("H", (end_c - start_c) + 1) if start_r == end_r else ("V", (end_r - start_r) + 1)
            else:
                orientation, length = "H", 1
            self.draw_ship_shape(start_r, start_c, length, orientation, COLOR_MAGIC_PLAYER)

            # Effet Fumée Magique sur les bateaux
            for r, c in positions:
                # On calcule px/py AVANT le random pour éviter le crash
                px= PLACEMENT_GRID_OFFSET_X + c * PLACEMENT_CELL_SIZE + PLACEMENT_CELL_SIZE // 2
                py = PLACEMENT_GRID_OFFSET_Y + r * PLACEMENT_CELL_SIZE + PLACEMENT_CELL_SIZE // 2

                if random.random() < 0.2:
                    self.particles.add_particle(
                        px + random.randint(-15, 15), 
                        py + random.randint(-15, 15), 
                        (0, 255, 255)
                    )    

        # --- E. GHOST SHIP (PRÉVISUALISATION) ---
        if self.current_ship_index < len(self.player.ships):
            name, size = self.player.ships[self.current_ship_index]
            mx, my = pygame.mouse.get_pos()

            grid_width = GRID_SIZE * PLACEMENT_CELL_SIZE
            grid_height = GRID_SIZE * PLACEMENT_CELL_SIZE
            grid_end_x = PLACEMENT_GRID_OFFSET_X + grid_width
            grid_end_y = PLACEMENT_GRID_OFFSET_Y + grid_height

            # Si souris dans la grille
            if (PLACEMENT_GRID_OFFSET_X <= mx < grid_end_x) and \
               (PLACEMENT_GRID_OFFSET_Y <= my < grid_end_y):

                col = (mx - PLACEMENT_GRID_OFFSET_X) // PLACEMENT_CELL_SIZE
                row = (my - PLACEMENT_GRID_OFFSET_Y) // PLACEMENT_CELL_SIZE


                if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                    is_valid, _ = self.check_placement_validity(row, col, size)
                    color = COLOR_PREVIEW_VALID if is_valid else COLOR_PREVIEW_INVALID
                    opacity = 150 if is_valid else 180
                    self.draw_ship_shape(row, col, size, self.orientation, color, opacity)
        
        # --- F. MISE À JOUR PARTICULES ---
        self.particles.update_and_draw(self.screen)