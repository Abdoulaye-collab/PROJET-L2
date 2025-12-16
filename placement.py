import pygame
import random
import math
from settings import (
    CELL_SIZE, COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, COLOR_SHIP, COLOR_UI_BACKGROUND, COLOR_MAGIC_PLAYER,
    COLOR_PREVIEW_VALID, COLOR_PREVIEW_INVALID,
    GRID_OFFSET_X_PLAYER, GRID_OFFSET_Y, GRID_WIDTH_TOTAL,
    FONT_NAME, FONT_NAME_GRIMOIRE, FONT_NAME_GRIMOIRE2, SCREEN_HEIGHT, SCREEN_WIDTH
)

# --- CONSTANTES DE PLACEMENT ---
GRID_SIZE = 10
PLACEMENT_CELL_SIZE = 55
PLACEMENT_GRID_WIDTH_TOTAL = GRID_SIZE * PLACEMENT_CELL_SIZE

# Calculs de position
CENTER_HALF_X = SCREEN_WIDTH // 4 
PLACEMENT_GRID_OFFSET_X = CENTER_HALF_X - (PLACEMENT_GRID_WIDTH_TOTAL // 2)
PLACEMENT_GRID_OFFSET_Y = 150


# --- NOUVELLES COULEURS THÉMATIQUES ---
COLOR_GRID_NEON = (0, 255, 255)       # Cyan Électrique (Grille)
COLOR_GRIMOIRE_INK = (90, 70, 50)     # Marron foncé (Texte non placé / Ombre)
COLOR_TEXT_NEON = (0, 200, 255)     # Blanc bleuté (Texte placé par-dessus)


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
        
        # On charge les polices ici pour éviter de le faire en boucle
        self.font_grimoire = pygame.font.Font(FONT_NAME_GRIMOIRE, 60)
        self.font_coords = pygame.font.Font(FONT_NAME_GRIMOIRE2, 30)
        self.font_large = pygame.font.Font(FONT_NAME_GRIMOIRE2, 70)

        self.magic_particles = []

        # Chargement fond
        try:
            image_path = "images/background.png"
            background_img = pygame.image.load(image_path).convert()
            self.background_image = pygame.transform.scale(
                background_img, 
                (self.screen.get_width(), self.screen.get_height())
            )
        except:
            # Fallback si l'image n'existe pas
            self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_image.fill((10, 10, 30))

    # ----------------------------------------------------------------------
    # GESTION DES ÉVÉNEMENTS
    # ----------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.orientation = "V" if self.orientation == "H" else "H"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
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
        
        # 1. Validation
        is_valid, positions = self.check_placement_validity(row, col, size)
        if not is_valid:
            return
        
        # 2. Mise à jour grille
        for r, c in positions:
            self.player.board[r][c] = 1

        # 3. Enregistrement
        self.player.ship_positions[name] = positions

        # Effet visuel
        self.trigger_magic_effect(positions)
        
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
    # DESSIN : FORME DE BATEAU
    # ----------------------------------------------------------------------
    def draw_ship_shape(self, row, col, length, orientation, color, alpha=255):
        px = PLACEMENT_GRID_OFFSET_X + col * PLACEMENT_CELL_SIZE
        py = PLACEMENT_GRID_OFFSET_Y + row * PLACEMENT_CELL_SIZE
        padding = 5 
        
        if orientation == "H":
            width_px = (length * PLACEMENT_CELL_SIZE) - (padding * 2)
            height_px = PLACEMENT_CELL_SIZE - (padding * 2)
        else:
            width_px = PLACEMENT_CELL_SIZE - (padding * 2)
            height_px = (length * PLACEMENT_CELL_SIZE) - (padding * 2)
            
        if alpha < 255:
            s = pygame.Surface((width_px, height_px), pygame.SRCALPHA)
            rect_surf = pygame.Rect(0, 0, width_px, height_px)
            pygame.draw.rect(s, color + (alpha,), rect_surf, border_radius=15)
            pygame.draw.rect(s, (255, 255, 255, alpha), rect_surf, 2, border_radius=15)
            self.screen.blit(s, (px + padding, py + padding))
        else:
            ship_rect = pygame.Rect(px + padding, py + padding, width_px, height_px)
            pygame.draw.rect(self.screen, color, ship_rect, border_radius=15)
            # Bordure un peu plus claire
            border_col = (min(color[0]+40, 255), min(color[1]+40, 255), min(color[2]+40, 255))
            pygame.draw.rect(self.screen, border_col, ship_rect, 2, border_radius=15)

    # ----------------------------------------------------------------------
    # DESSIN : GRILLE (STYLE NÉON)
    # ----------------------------------------------------------------------
    def draw_grid(self):
        letters = "ABCDEFGHIJ"
        font_grid_big = pygame.font.Font(FONT_NAME_GRIMOIRE2, 30)
        for row in range(GRID_SIZE):
            # 1. Chiffres à gauche (Cyan/Blanc)
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
                
                # --- MODIFICATION : GRILLE CYAN ---
                pygame.draw.rect(self.screen, COLOR_GRIMOIRE_INK, rect, 1)

                # 2. Lettres en haut (A-J)
                if row == 0:
                    label_char = self.font_coords.render(letters[col], True, COLOR_GRIMOIRE_INK)
                    char_rect = label_char.get_rect(
                        midbottom=(rect.centerx, PLACEMENT_GRID_OFFSET_Y - 10)
                    )
                    self.screen.blit(label_char, char_rect)

    # ----------------------------------------------------------------------
    #  GESTION DES EFFETS MAGIQUES
    # ----------------------------------------------------------------------
    def trigger_magic_effect(self, positions):
        for r, c in positions:
            px = PLACEMENT_GRID_OFFSET_X + c * PLACEMENT_CELL_SIZE + PLACEMENT_CELL_SIZE // 2
            py = PLACEMENT_GRID_OFFSET_Y + r * PLACEMENT_CELL_SIZE + PLACEMENT_CELL_SIZE // 2
            
            for _ in range(20):
                speed = random.uniform(2, 5) # Vitesse variable
                angle = random.uniform(0, 6.28) # Angle aléatoire (0 à 2pi)

                self.magic_particles.append({
                    'x': px,
                    'y': py,
                    'dx': math.cos(angle) * speed,
                    'dy': math.sin(angle) * speed,
                    'timer': random.randint(10, 25),
                    'size': random.randint(3, 6),
                    'color': random.choice([(0, 255, 255), (255, 255, 255)])
                })

    def update_and_draw_particles(self):
        for i in range(len(self.magic_particles) - 1, -1, -1):
            p = self.magic_particles[i]
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['timer'] -= 1
            p['size'] -= 0.1
            
            if p['timer'] <= 0 or p['size'] <= 0:
                self.magic_particles.pop(i)
                continue
            
            alpha = int((p['timer'] / 50) * 255)
            if alpha > 255: alpha = 255
            if alpha < 0: alpha = 0
            radius = int(p['size'])
            if radius < 1: radius = 1

            s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, p['color'] + (alpha,), (radius, radius), radius)
            self.screen.blit(s, (p['x'] - radius, p['y'] - radius))

    # ----------------------------------------------------------------------
    # DESSIN : ÉCRAN GLOBAL
    # ----------------------------------------------------------------------
    def draw(self):
        self.screen.blit(self.background_image,(0,0))
    
        # Constantes locales pour l'affichage
        CENTER_HALF_RIGHT_X = self.screen.get_width() * 3 // 4 
        INSTRUCTION_START_Y = 150 
        LIST_START_Y = INSTRUCTION_START_Y + 100
        LIST_LINE_SPACING = 45
        
        # 1. TITRE
        # On utilise une couleur claire pour le titre principal
        title_surf = self.font_large.render(f"Grille du Sorcier : {self.player.name}", True, (COLOR_GRIMOIRE_INK))
        grid_center_x = PLACEMENT_GRID_OFFSET_X + (GRID_SIZE * PLACEMENT_CELL_SIZE) // 2
        title_rect = title_surf.get_rect(midtop=(grid_center_x, 5))
        self.screen.blit(title_surf, title_rect)

        # 2. INSTRUCTIONS
        if self.current_ship_index < len(self.player.ships):
            name, size = self.player.ships[self.current_ship_index]
            
            instr1 = self.font_grimoire.render(f"Sort: Déploiement du {name}", True, COLOR_GRIMOIRE_INK)
            self.screen.blit(instr1, instr1.get_rect(centerx=CENTER_HALF_RIGHT_X, y=INSTRUCTION_START_Y))
            
            instr2 = self.font_grimoire.render("[R] pour tourner le navire", True, COLOR_GRIMOIRE_INK)
            self.screen.blit(instr2, instr2.get_rect(centerx=CENTER_HALF_X, y=PLACEMENT_GRID_OFFSET_Y + PLACEMENT_GRID_WIDTH_TOTAL + 10))

        # 3. LISTE DES BATEAUX (À Droite)
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
                # --- EFFET MAGIQUE : OMBRE GRIMOIRE + LUMIÈRE NÉON ---
                
                # 1. Couche du dessous (Ombre / Encre)
                shadow_surf = self.font_grimoire.render(text_display, True, COLOR_GRIMOIRE_INK)
                shadow_rect = shadow_surf.get_rect(centerx=CENTER_HALF_RIGHT_X + 2, y=next_y + 2) # Décalage +2
                self.screen.blit(shadow_surf, shadow_rect)
                
                # 2. Couche du dessus (Lumière magique)
                neon_surf = self.font_grimoire.render(text_display, True, COLOR_TEXT_NEON)
                neon_rect = neon_surf.get_rect(centerx=CENTER_HALF_RIGHT_X, y=next_y)
                self.screen.blit(neon_surf, neon_rect)
                
                # Particules sur le texte placé (Magie)
                for _ in range(random.randint(1,2)):
                    px = random.randint(neon_rect.left, neon_rect.right)
                    py = random.randint(neon_rect.top, neon_rect.bottom)
                    self.magic_particles.append({
                        'x': px, 
                        'y': py,
                        'dx': random.uniform(-0.5, 0.5),
                        'dy': random.uniform(-2, -0.5),
                        'timer': random.randint(20, 40),
                        'size': random.randint(2,5),
                        'color': (0, 255, 255)
                    })

            else:
                # --- PAS ENCORE PLACÉ : JUSTE L'ENCRE ---
                ship_surf = self.font_grimoire.render(text_display, True, COLOR_GRIMOIRE_INK)
                self.screen.blit(ship_surf, ship_surf.get_rect(centerx=CENTER_HALF_RIGHT_X, y=next_y))
            
            next_y += LIST_LINE_SPACING + 20

        # 4. AFFICHER LA GRILLE
        self.draw_grid()
        
        # 5. AFFICHER LES BATEAUX VALIDÉS
        for ship_name, positions in self.player.ship_positions.items():
            if not positions: continue
            sorted_pos = sorted(positions)
            start_r, start_c = sorted_pos[0]
            if len(positions) > 1:
                end_r, end_c = sorted_pos[-1]
                orientation, length = ("H", (end_c - start_c) + 1) if start_r == end_r else ("V", (end_r - start_r) + 1)
            else:
                orientation, length = "H", 1
            self.draw_ship_shape(start_r, start_c, length, orientation, COLOR_MAGIC_PLAYER)

            for r, c in positions:
                # On ne génère pas à chaque frame sinon c'est trop chargé (30% de chance par case)
                if random.random() < 0.3: 
                    # Centre de la case
                    px_center = PLACEMENT_GRID_OFFSET_X + c * PLACEMENT_CELL_SIZE + PLACEMENT_CELL_SIZE // 2
                    py_center = PLACEMENT_GRID_OFFSET_Y + r * PLACEMENT_CELL_SIZE + PLACEMENT_CELL_SIZE // 2
                    
                    # On crée une particule
                    self.magic_particles.append({
                        'x': px_center + random.randint(-15, 15), # Un peu partout dans la case
                        'y': py_center + random.randint(-15, 15),
                        'dx': random.uniform(-0.5, 0.5), # Bouge un peu sur les côtés
                        'dy': random.uniform(-2, -0.5),  # Monte doucement vers le haut (Fumée)
                        'timer': random.randint(20, 40), # Durée de vie moyenne
                        'size': random.randint(2, 5),    # Taille variée
                        'color': (0, 255, 255)           # Cyan
                    })

        # 6. AFFICHER LE BATEAU FANTÔME (Prévisualisation)
        if self.current_ship_index < len(self.player.ships):
            name, size = self.player.ships[self.current_ship_index]
            mx, my = pygame.mouse.get_pos()

            grid_width = GRID_SIZE * PLACEMENT_CELL_SIZE
            grid_height = GRID_SIZE * PLACEMENT_CELL_SIZE
            grid_end_x = PLACEMENT_GRID_OFFSET_X + grid_width
            grid_end_y = PLACEMENT_GRID_OFFSET_Y + grid_height

            if (PLACEMENT_GRID_OFFSET_X <= mx < grid_end_x) and \
               (PLACEMENT_GRID_OFFSET_Y <= my < grid_end_y):

                col = (mx - PLACEMENT_GRID_OFFSET_X) // PLACEMENT_CELL_SIZE
                row = (my - PLACEMENT_GRID_OFFSET_Y) // PLACEMENT_CELL_SIZE

                # Correction du bug <= GRID_SIZE (il faut < GRID_SIZE)
                if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                    is_valid, _ = self.check_placement_validity(row, col, size)
                    color = COLOR_PREVIEW_VALID if is_valid else COLOR_PREVIEW_INVALID
                    opacity = 150 if is_valid else 180
                    self.draw_ship_shape(row, col, size, self.orientation, color, opacity)
            
        self.update_and_draw_particles()