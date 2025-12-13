import pygame
from settings import (
    COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, COLOR_SHIP, COLOR_UI_BACKGROUND,
    COLOR_PREVIEW_VALID,COLOR_PREVIEW_INVALID, 
    GRID_OFFSET_X_PLAYER,GRID_OFFSET_Y,GRID_WIDTH_TOTAL,
    FONT_NAME,
)
CELL_SIZE = 40
GRID_SIZE = 10

# ====================================================================
#       CLASSE PLACEMENT : GESTION DE LA PHASE DE DÉPLOIEMENT
# ===================================================================

class Placement:
    # ----------------------------------------------------------------------
    # A. INITIALISATION
    # ----------------------------------------------------------------------
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        # --- État du placement ---
        self.current_ship_index = 0
        self.orientation = "H"
        self.done = False

    #----------------------------------------------------------------------
    # B. GESTION DES ÉVÉNEMENTS
    # ----------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Raccourci pour changer l'orientation
            if event.key == pygame.K_r:
                self.orientation = "V" if self.orientation == "H" else "H"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            #Calcul des coordonnées de la cellule cliquée
            col = (x - GRID_OFFSET_X_PLAYER) // CELL_SIZE
            row = (y - GRID_OFFSET_Y) // CELL_SIZE

            self.place_ship(row, col)

    # ----------------------------------------------------------------------
    # C. LOGIQUE DE PLACEMENT ET VALIDATION
    # ----------------------------------------------------------------------
    def place_ship(self, row, col):
        #Vérification de la validité du placement
        if self.current_ship_index >= len(self.player.ships):
            self.done = True
            return
        
        name, size = self.player.ships[self.current_ship_index]
        
        # 1. Valisation du placement
        is_valid,positions = self.check_placement_validity(row, col, size)
        if not is_valid:
            return
        
        # 2. Mise à jour de la grille du joueur
        for r,c in positions:
            self.player.board[r][c] = 1

        #3. Création de l'objet Ship et mise à jour des positions
        self.player.ship_positions[name] = positions

        self.current_ship_index += 1

        if self.current_ship_index >= len(self.player.ships):
            self.done = True

    def check_placement_validity(self, start_row, start_col, size):
        """Vérifie si le bateau peut être placé et retourne les cellules et l'état de validité."""
        
        cells = []
        is_valid = True
        
        for i in range(size):
            # Calcul des coordonnées de chaque segment du bateau
            r = start_row + i if self.orientation == "V" else start_row
            c = start_col + i if self.orientation == "H" else start_col
            
            # 1. Vérification des limites de la grille (hors zone)
            if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                is_valid = False
            # 2. Vérification de chevauchement avec un bateau existant (valeur 1 dans la grille)
            elif self.player.board[r][c] != 0:
                is_valid = False
                
            cells.append((r, c))

        # Si le placement est invalide pour une raison (limite ou chevauchement), retourner False
        return is_valid, cells

    # ----------------------------------------------------------------------
    # D. AFFICHAGE DE LA GRILLE (Fixe)
    # ----------------------------------------------------------------------
    def draw_grid(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                #Calcul de la position de la cellule
                x= GRID_OFFSET_X_PLAYER + col * CELL_SIZE
                y= GRID_OFFSET_Y + row * CELL_SIZE
                rect = pygame.Rect(x,y, CELL_SIZE, CELL_SIZE)
                
                # Couleur selon la présence d'un bateau
                color = (COLOR_SHIP) if self.player.board[row][col] == 1 else (COLOR_OCEAN_DARK)
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)

    # ----------------------------------------------------------------------
    # E. AFFICHAGE DE L'ÉCRAN DE PLACEMENT
    # ----------------------------------------------------------------------
    def draw(self):
        self.screen.fill(COLOR_UI_BACKGROUND)
        
        # Polices
        font_thematic_large = pygame.font.Font(FONT_NAME, 30)
        font_readable = pygame.font.SysFont("Verdana", 20)

        # ----------------Titre de la Grille--------------------------------
        GRID_TITLE = f"Grille du Sorcier : {self.player.name}"
        grid_title_surf = font_thematic_large.render(GRID_TITLE, True, COLOR_TEXT_MAGIC)
        center_x_grid = GRID_OFFSET_X_PLAYER + (GRID_WIDTH_TOTAL // 2)
        grid_title_rect = grid_title_surf.get_rect(centerx=center_x_grid, y=50) # Y=50 pour être bien au-dessus
        self.screen.blit(grid_title_surf, grid_title_rect)

        # ------------------ Calcul des Coordoonnées Droite  -----------------------
        GRID_END_X=GRID_OFFSET_X_PLAYER + GRID_WIDTH_TOTAL
        GAP_SIZE_RIGHT=10
        RIGHT_COL_X=GRID_END_X + GAP_SIZE_RIGHT 
    
        # -----------------------Instructions de placement------------------------
        if self.current_ship_index < len(self.player.ships):
            name, size = self.player.ships[self.current_ship_index]

            instr_line1 = f"Déployez votre {name} : PLacez la proue."
            instr_line2 = f"[R] pour modifier l'Orientation ."

            text_surf1 = font_readable.render(instr_line1, True, COLOR_TEXT_MAGIC)
            self.screen.blit(text_surf1,(RIGHT_COL_X, 110))
            text_surf2 = font_readable.render(instr_line2, True, COLOR_TEXT_MAGIC)
            self.screen.blit(text_surf2,(RIGHT_COL_X, 140))
        
        # ------------------ Liste des Bateaux à Placer ------------------
        fleet_text = font_readable.render("Flotte à Placer :", True, COLOR_TEXT_MAGIC)
        self.screen.blit(fleet_text,(RIGHT_COL_X, 180))
        next_ship_y = 215
        
        # Parcourir la liste des bateaux
        for index, (name, size) in enumerate(self.player.ships):
            is_placed = index < self.current_ship_index
            
            text_color = (150, 150, 150) if is_placed else COLOR_TEXT_MAGIC
            status = " [EN PLACE]" if is_placed else f" ({size} cases)"
            
            ship_surf = font_readable.render(f"- {name}{status}", True, text_color)
            self.screen.blit(ship_surf, (RIGHT_COL_X, next_ship_y))
            next_ship_y += 35

        self.draw_grid()
        
        #-----------------------------------------------------------------------
        # F. PREVISUALISATION DU PLACEMENT
        #-----------------------------------------------------------------------
        if self.current_ship_index < len(self.player.ships):
            name, size = self.player.ships[self.current_ship_index]
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Calculer la cellule sous le curseur
            col = (mouse_x - GRID_OFFSET_X_PLAYER) // CELL_SIZE
            row = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE

            # 1. Obtenir la validité et les cellules (Utiliser la nouvelle fonction)
            is_valid, cells_to_preview = self.check_placement_validity(row, col, size)
            
            # 2. Définir la couleur de lueur et l'opacité
            if is_valid:
                preview_color = COLOR_PREVIEW_VALID    # Violet Magique
                opacity = 128                          # 50% de transparence
            else:
                preview_color = COLOR_PREVIEW_INVALID  # Rouge Erreur
                opacity = 180                          # Moins de transparence (pour plus de visibilité)
            
            # 3. Dessiner chaque cellule de prévisualisation
            for r, c in cells_to_preview:
                
                # Vérification des limites (juste au cas où)
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    
                    x = GRID_OFFSET_X_PLAYER + c * CELL_SIZE
                    y = GRID_OFFSET_Y + r * CELL_SIZE
                    
                    # Dessin du fond de lueur avec transparence (pygame.SRCALPHA)
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    s.fill(preview_color + (opacity,)) 
                    self.screen.blit(s, (x, y))
                    
                    # Dessiner la bordure blanche pour l'effet de lueur (plus thématique que le noir)
                    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
    