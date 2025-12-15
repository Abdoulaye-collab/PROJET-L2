import pygame
from settings import (
    CELL_SIZE, COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, COLOR_SHIP, COLOR_UI_BACKGROUND,
    COLOR_PREVIEW_VALID, COLOR_PREVIEW_INVALID,
    GRID_OFFSET_X_PLAYER, GRID_OFFSET_Y, GRID_WIDTH_TOTAL,
    FONT_NAME, SCREEN_HEIGHT, SCREEN_WIDTH
)

# --- CONSTANTES DE PLACEMENT ---
# On redéfinit ici pour être sûr que ça s'adapte à l'écran de placement
GRID_SIZE = 10
PLACEMENT_CELL_SIZE = 40 
PLACEMENT_GRID_WIDTH_TOTAL = GRID_SIZE * PLACEMENT_CELL_SIZE

# Calculs de position
CENTER_HALF_X = SCREEN_WIDTH // 4 
PLACEMENT_GRID_OFFSET_X = CENTER_HALF_X - (PLACEMENT_GRID_WIDTH_TOTAL // 2)
PLACEMENT_GRID_OFFSET_Y = 250 # On force la grille à être en haut

# ====================================================================
#       CLASSE PLACEMENT : GESTION DE LA PHASE DE DÉPLOIEMENT
# ===================================================================

class Placement:
    def __init__(self, screen, player, assets):
        self.screen = screen
        self.player = player
        self.assets = assets

        # --- État du placement ---
        self.current_ship_index = 0
        self.orientation = "H"
        self.done = False

        image_path = "images/background.png"
        background_img = pygame.image.load(image_path)
        self.background_image = pygame.transform.scale(
            background_img, 
            (self.screen.get_width(), self.screen.get_height())
        )

    # ----------------------------------------------------------------------
    # GESTION DES ÉVÉNEMENTS
    # ----------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Raccourci pour changer l'orientation
            if event.key == pygame.K_r:
                self.orientation = "V" if self.orientation == "H" else "H"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Calcul des coordonnées de la cellule cliquée
            col = (x - PLACEMENT_GRID_OFFSET_X) // PLACEMENT_CELL_SIZE
            row = (y - PLACEMENT_GRID_OFFSET_Y) // PLACEMENT_CELL_SIZE

            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                self.place_ship(row, col)

    # ----------------------------------------------------------------------
    # LOGIQUE DE PLACEMENT
    # ----------------------------------------------------------------------
    def place_ship(self, row, col):
        if self.current_ship_index >= len(self.player.ships):
            self.done = True
            return
        
        name, size = self.player.ships[self.current_ship_index]
        
        # 1. Validation du placement
        is_valid, positions = self.check_placement_validity(row, col, size)
        if not is_valid:
            return
        
        # 2. Mise à jour de la grille du joueur
        for r, c in positions:
            self.player.board[r][c] = 1

        # 3. Enregistrement
        self.player.ship_positions[name] = positions

        self.current_ship_index += 1

        if self.current_ship_index >= len(self.player.ships):
            self.done = True

    def check_placement_validity(self, start_row, start_col, size):
        cells = []
        is_valid = True
        
        for i in range(size):
            r = start_row + i if self.orientation == "V" else start_row
            c = start_col + i if self.orientation == "H" else start_col
            
            # Limites et chevauchement
            if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                is_valid = False
            elif self.player.board[r][c] != 0:
                is_valid = False
                
            cells.append((r, c))

        return is_valid, cells

    # ----------------------------------------------------------------------
    # DESSIN : FORME DE BATEAU CONTINUE
    # ----------------------------------------------------------------------
    def draw_ship_shape(self, row, col, length, orientation, color, alpha=255):
        """Dessine un rectangle arrondi."""
        px = PLACEMENT_GRID_OFFSET_X + col * PLACEMENT_CELL_SIZE
        py = PLACEMENT_GRID_OFFSET_Y + row * PLACEMENT_CELL_SIZE
        
        padding = 5 
        
        if orientation == "H":
            width_px = (length * PLACEMENT_CELL_SIZE) - (padding * 2)
            height_px = PLACEMENT_CELL_SIZE - (padding * 2)
        else: # Vertical
            width_px = PLACEMENT_CELL_SIZE - (padding * 2)
            height_px = (length * PLACEMENT_CELL_SIZE) - (padding * 2)
            
        # Gestion transparence
        if alpha < 255:
            s = pygame.Surface((width_px, height_px), pygame.SRCALPHA)
            rect_surf = pygame.Rect(0, 0, width_px, height_px)
            pygame.draw.rect(s, color + (alpha,), rect_surf, border_radius=15)
            pygame.draw.rect(s, (255, 255, 255, alpha), rect_surf, 2, border_radius=15)
            self.screen.blit(s, (px + padding, py + padding))
        else:
            ship_rect = pygame.Rect(px + padding, py + padding, width_px, height_px)
            pygame.draw.rect(self.screen, color, ship_rect, border_radius=15)
            border_col = (min(color[0]+40, 255), min(color[1]+40, 255), min(color[2]+40, 255))
            pygame.draw.rect(self.screen, border_col, ship_rect, 2, border_radius=15)

    # ----------------------------------------------------------------------
    # DESSIN : GRILLE (CORRIGÉE)
    # ----------------------------------------------------------------------
    def draw_grid(self):
        # On utilise FONT_NAME par sécurité
        try:
            font_coords = pygame.font.Font(FONT_NAME, 20)
        except:
            font_coords = pygame.font.Font(None, 20) # Police par défaut si erreur
            
        letters = "ABCDEFGHIJ"

        for row in range(GRID_SIZE):
            # 1. Chiffres à gauche (1-10)
            label_num = font_coords.render(str(row + 1), True, (255, 255, 255))
            num_rect = label_num.get_rect(
                midright=(PLACEMENT_GRID_OFFSET_X - 10, 
                          PLACEMENT_GRID_OFFSET_Y + row * PLACEMENT_CELL_SIZE + (PLACEMENT_CELL_SIZE // 2))
            )
            self.screen.blit(label_num, num_rect)

            for col in range(GRID_SIZE):
                x = PLACEMENT_GRID_OFFSET_X + col * PLACEMENT_CELL_SIZE
                y = PLACEMENT_GRID_OFFSET_Y + row * PLACEMENT_CELL_SIZE
                rect = pygame.Rect(x, y, PLACEMENT_CELL_SIZE, PLACEMENT_CELL_SIZE)

                # Fond et Ligne
                pygame.draw.rect(self.screen, COLOR_OCEAN_DARK, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

                # 2. Lettres en haut (A-J) - Uniquement pour la première ligne
                if row == 0:
                    label_char = font_coords.render(letters[col], True, (255, 255, 255))
                    char_rect = label_char.get_rect(
                        midbottom=(x + (PLACEMENT_CELL_SIZE // 2), PLACEMENT_GRID_OFFSET_Y - 5)
                    )
                    self.screen.blit(label_char, char_rect)

    # ----------------------------------------------------------------------
    # DESSIN : ÉCRAN GLOBAL
    # ----------------------------------------------------------------------
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
            
        # (Optionnel) Ajout d'un voile noir semi-transparent 
        # pour que le texte reste lisible sur l'image
        voile = pygame.Surface(self.screen.get_size())
        voile.set_alpha(120) # 0 = transparent, 255 = noir total
        voile.fill((0, 0, 0))
        self.screen.blit(voile, (0, 0))
        
        # Constantes locales pour l'affichage
        CENTER_HALF_RIGHT_X = self.screen.get_width() * 3 // 4 
        INSTRUCTION_START_Y = 250 
        LIST_START_Y = INSTRUCTION_START_Y + 100
        LIST_LINE_SPACING = 45
        center_x_screen = self.screen.get_width() // 2
        
        font_large = pygame.font.Font(FONT_NAME, 45)
        font_small = pygame.font.Font(FONT_NAME, 24)

        # 1. TITRE
        GRID_TITLE = f"Grille du Sorcier : {self.player.name}"
        title_surf = font_large.render(GRID_TITLE, True, COLOR_TEXT_MAGIC)
        title_rect = title_surf.get_rect(centerx=center_x_screen, y=50)
        self.screen.blit(title_surf, title_rect)

        # 2. INSTRUCTIONS
        if self.current_ship_index < len(self.player.ships):
            name, size = self.player.ships[self.current_ship_index]
            
            # Texte Instruction Droite
            instr1 = font_small.render(f"Déployez votre {name}", True, COLOR_TEXT_MAGIC)
            self.screen.blit(instr1, instr1.get_rect(centerx=CENTER_HALF_RIGHT_X, y=INSTRUCTION_START_Y))
            
            # Texte Rotation (Sous la grille)
            instr2 = font_small.render("[R] pour tourner le navire", True, (200, 200, 200))
            self.screen.blit(instr2, instr2.get_rect(centerx=CENTER_HALF_X, y=PLACEMENT_GRID_OFFSET_Y + PLACEMENT_GRID_WIDTH_TOTAL + 20))

        # 3. LISTE DES BATEAUX (À Droite)
        title_list = font_small.render("Flotte à Placer :", True, COLOR_TEXT_MAGIC)
        self.screen.blit(title_list, title_list.get_rect(centerx=CENTER_HALF_RIGHT_X, y=LIST_START_Y))
        
        next_y = LIST_START_Y + LIST_LINE_SPACING
        for index, (name, size) in enumerate(self.player.ships):
            is_placed = index < self.current_ship_index
            color = (100, 100, 100) if is_placed else COLOR_TEXT_MAGIC
            ship_surf = font_small.render(f"- {name} ({size})", True, color)
            self.screen.blit(ship_surf, ship_surf.get_rect(centerx=CENTER_HALF_RIGHT_X, y=next_y))
            next_y += LIST_LINE_SPACING

        # 4. AFFICHER LA GRILLE
        self.draw_grid()
        
        # 5. AFFICHER LES BATEAUX VALIDÉS
        for ship_name, positions in self.player.ship_positions.items():
            if not positions: continue
            
            # Calcul orientation/longueur
            sorted_pos = sorted(positions)
            start_r, start_c = sorted_pos[0]
            if len(positions) > 1:
                end_r, end_c = sorted_pos[-1]
                if start_r == end_r:
                    orientation, length = "H", (end_c - start_c) + 1
                else:
                    orientation, length = "V", (end_r - start_r) + 1
            else:
                orientation, length = "H", 1
                
            self.draw_ship_shape(start_r, start_c, length, orientation, (80, 80, 80))

        # 6. AFFICHER LE BATEAU FANTÔME (Sous la souris)
        if self.current_ship_index < len(self.player.ships):
            name, size = self.player.ships[self.current_ship_index]
            mx, my = pygame.mouse.get_pos()
            col = (mx - PLACEMENT_GRID_OFFSET_X) // PLACEMENT_CELL_SIZE
            row = (my - PLACEMENT_GRID_OFFSET_Y) // PLACEMENT_CELL_SIZE

            if -1 <= row <= GRID_SIZE and -1 <= col <= GRID_SIZE:
                is_valid, _ = self.check_placement_validity(row, col, size)
                color = COLOR_PREVIEW_VALID if is_valid else COLOR_PREVIEW_INVALID
                opacity = 150 if is_valid else 180
                self.draw_ship_shape(row, col, size, self.orientation, color, opacity)