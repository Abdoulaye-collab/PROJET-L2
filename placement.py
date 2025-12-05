import pygame

CELL_SIZE = 40
GRID_SIZE = 10
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 100

class Placement:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.current_ship_index = 0
        self.orientation = "H"
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.orientation = "V" if self.orientation == "H" else "H"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = (x - GRID_OFFSET_X) // CELL_SIZE
            row = (y - GRID_OFFSET_Y) // CELL_SIZE
            self.place_ship(row, col)

    def place_ship(self, row, col):
        if self.current_ship_index >= len(self.player.ships):
            self.done = True
            return
        name, size = self.player.ships[self.current_ship_index]
        positions = []
        for i in range(size):
            r = row + i if self.orientation == "V" else row
            c = col + i if self.orientation == "H" else col
            if r >= GRID_SIZE or c >= GRID_SIZE or self.player.grid[r][c] != 0:
                return
            positions.append((r,c))
        for r,c in positions:
            self.player.grid[r][c] = 1
        self.player.ship_positions[name] = positions
        self.current_ship_index += 1
        if self.current_ship_index >= len(self.player.ships):
            self.done = True

    def draw_grid(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(GRID_OFFSET_X + col*CELL_SIZE, GRID_OFFSET_Y + row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = (0,255,0) if self.player.grid[row][col] == 1 else (200,200,200)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)

    def draw(self):
        self.screen.fill((0,105,148))
        font = pygame.font.SysFont("Arial", 30)
        if self.current_ship_index < len(self.player.ships):
            name, size = self.player.ships[self.current_ship_index]
            instr = f"Placez votre {name} (taille {size}), orientation: {self.orientation}. R pour tourner"
            text_surf = font.render(instr, True, (255,255,255))
            self.screen.blit(text_surf, (50,50))
        self.draw_grid()
