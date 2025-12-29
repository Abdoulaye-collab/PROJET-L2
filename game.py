import pygame
import random

from player import Player
from settings import *
from ai_llm import calculate_ai_move
from ai_personalities import get_ai_phrase
from GameOver import GameOver
from effects import ParticleSystem
from sound_manager import SoundManager

import draw_utils as du
from input_handler import handle_game_events

class Game:
    # ==============================================================================
    #  1. INITIALISATION ET CONFIGURATION
    # ==============================================================================
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets

        # --- JOUEURS ET THÈMES ---
        self.player = Player("Joueur")
        self.THEME_PLAYER = (COLOR_MAGIC_PLAYER)
        self.enemy = Player("IA")
        self.THEME_ENEMY = (COLOR_MAGIC_ENEMY)
        
        # --- ETAT GLOBAL DU JEU ---
        self.turn_count = 1
        self.winner = None
        self.game_over= False
        self.game_over_screen = None
        self.player_turn = True
        self.text_status = f"Tour de {self.player.name} !"
        self.start_time = pygame.time.get_ticks()
       
        # --- IA  ---
        self.ai_personality = "Gentille"
        self.ai_phrase_to_display = ""
        self.ai_targets_buffer = []
        self.ia_delay = 0
        self.ia_pending = False

        # --- BONUS ET CARTES ---
        self.extra_shot = 0
        self.selected_card = None
        self.awaiting_target = False
        self.cards_played_total = 0

        # --- MOTEURS (Son, Particules, Pojectiles) ---
        self.particles = ParticleSystem()
        self.sounds = SoundManager()
        self.projectile = None  
        
        # --- CHARGEMENT DES POLICES (Pour draw_utils) ---
        self.font = pygame.font.Font(FONT_NAME_GRIMOIRE, 50)
        self.title_font = pygame.font.Font(FONT_NAME_GRIMOIRE, 55)
        self.fonts = {
            'std': pygame.font.Font(FONT_NAME_GRIMOIRE, 50),
            'title': pygame.font.Font(FONT_NAME_GRIMOIRE, 55),
            'timer': pygame.font.Font(FONT_NAME, 22),
            'card': pygame.font.Font(FONT_NAME_GRIMOIRE, 30)
        }
        

        # --- CHARGEMENT DU FOND D'ECRAN ---
        try:
            self.background_image = pygame.image.load("assets/images/fond_marin.png").convert()
            self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except :
            self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_image.fill((10, 10, 30))

    # ==============================================================================
    #  2. LOGIQUE DE VICTOIRE ET RÈGLES
    # ==============================================================================
    def is_ship_sunk(self, player, ship_name):
        """ Vérifie si un bateau est entièrement détruit (-1 sur toutes ses cases) """
        return all(player.board[r][c] == -1 for r, c in player.ship_positions[ship_name])
        
    # def ship_positions_hit(self, player, row, col):
    #     for ship, positions in player.ship_positions.items():
    #         if (row, col) in positions:
    #             positions.remove((row, col))
    #             break
    
    def check_win(self):
        """ Vérifie si quelqu'un a perdu tous ses bateaux """
        if self.game_over: return
        
        # Fonction interne pour vérifier la défaite d'un joueur
        def check_player_lost(p):
            return all(self.is_ship_sunk(p, name) for name in p.ship_positions)
        winner = None

        if check_player_lost(self.enemy): winner = self.player   # Joueur gagne
        elif check_player_lost(self.player): winner = self.enemy # IA gagne
        
        # Si personne n'a gagné, on s'arrête là
        if winner is None:
            return
        
        # Sinon, on déclenche la fin de partie
        self.winner = winner
        self.game_over = True

        # Calcul des stats pour l'écran de fin
        duration = (pygame.time.get_ticks() - self.start_time) // 1000
        loser = self.enemy if winner == self.player else self.player

        self.game_over_screen = GameOver(
            self.screen, winner,
            self.enemy if winner == self.player else self.player, duration, 
            self.cards_played_total, winner == self.player
        )

    # ==============================================================================
    #  3. MÉCANIQUE DE TIR (SHOOT)
    # ==============================================================================
    def shoot(self, shooter, row, col):
        """ Gère le tir d'un joueur vers l'autre """
        target = self.enemy if shooter == self.player else self.player
        
        # --- GESTION BOUCLIER ---
        if shooter == self.enemy and "Bouclier_Actif" in target.reinforced_ships:
            target.reinforced_ships.remove("Bouclier_Actif")
            self.text_status = "BOUCLIER : Tir ennemi bloqué !"
            return "Bloqué"

        # --- VÉRIFICATION LIMITES ---
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE): return "Invalid"
        val = target.board[row][col]

        # --- ANIMATION DU PROJECTILE ---
        # Position de départ (Approx. selon le côté de l'écran)
        sx, sy = (225, 425) if shooter == self.player else (1075, 425)
        self.projectile = {
            "target": (row, col), 
            "pos": [sx, sy], 
            "color": self.THEME_PLAYER if shooter == self.player else self.THEME_ENEMY, 
            "owner": shooter
            }
        
        # --- RÉSULTAT DU TIR ---
        if val == 1: #Touché
            target.board[row][col] = -1
            shooter.hits += 1
            self.sounds.play_hit()

            # Position exacte pour l'explosion de particules
            px = (800 if target == self.enemy else 50) + col * (55 if target == self.enemy else 35) + 20
            py = (150 if target == self.enemy else 250) + row * (55 if target == self.enemy else 35) + 20
            self.particles.trigger_hit_particles(px, py, self.projectile["color"])
            
            self.check_win()
            return "Touché"
        
        elif val == 0: # Manqué
            target.board[row][col] = -2
            self.sounds.play_miss()
            return "Manqué"
            
        return "Déjà tiré"
    
    # ==============================================================================
    #  4. INTELLIGENCE ARTIFICIELLE
    # ==============================================================================
    def ai_play(self):
        if self.winner: return
        
        # 1. Le Cerveau (ai_llm) décide où tirer
        row, col = calculate_ai_move(self.player.board, self.ai_targets_buffer)
        if row is not None: 
            # 2. L'IA Tire
            result = self.shoot(self.enemy, row, col)
            
            # 3. Si Touché, on mémorise les cases voisines pour le prochain tour
            if result == "Touché":
                voisins = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
                random.shuffle(voisins) # On mélange pour varier l'attaque
                self.ai_targets_buffer.extend(voisins)

            # 4. L'IA parle (Chat)
            self.ai_phrase_to_display = get_ai_phrase(self.ai_personality, "hit" if result == "Touché" else "miss")
            self.turn_count += 1
            self.player_turn = True
            self.text_status = f"Tour de {self.player.name} !"

    # ==============================================================================
    #  5. BOUCLE DE JEU (EVENTS, UPDATE, DRAW)
    # ==============================================================================
    def handle_event(self, event):
        """ Délègue la gestion des clics à input_handler.py """
        handle_game_events(self, event)

    def update(self):
        """ Met à jour les animations et le timer de l'IA """

        # A. Animation du Projectile
        if self.projectile:
            target_row, target_col = self.projectile["target"]
            # Calcul position cible en pixels
            target_x = (800 if self.projectile["owner"] == self.player else 50) + target_col * (55 if self.projectile["owner"] == self.player else 35) + 20
            target_y = (150 if self.projectile["owner"] == self.player else 250) + target_row * (55 if self.projectile["owner"] == self.player else 35) + 20
            dx = target_x - self.projectile["pos"][0]
            dy = target_y - self.projectile["pos"][1]
            dist = (dx**2 + dy**2)**0.5
            
            if dist < PROJECTILE_SPEED:
                self.projectile = None
            else:
                self.projectile["pos"][0] += PROJECTILE_SPEED * dx / dist
                self.projectile["pos"][1] += PROJECTILE_SPEED * dy / dist

        # B. Gestion du délai de réflexion de l'IA
        if self.ia_pending and not self.projectile:
            if self.ia_delay > 0:
                self.ia_delay -= 16
            else:
                self.ai_play()
                self.ia_pending = False

    def draw(self):
        """ Affiche tout le jeu (Délègue à draw_utils pour l'UI) """

        # 1. Fond d'écran
        self.screen.blit(self.background_image, (0, 0))
        
        # 2. Fonds colorés sous les grilles
        pygame.draw.rect(self.screen, COLOR_CELL_TINT, (50, 250, 350, 350))
        pygame.draw.rect(self.screen, COLOR_OCEAN_DARK, (800, 150, 550, 550))

        # 3. Dessin des Bateaux
        # Joueur
        du.draw_continuous_ships(self.screen, self.player, 50, 250, 35, self.THEME_PLAYER, (200,255,255))
        
        # Ennemis Coulés (On crée un faux joueur contenant juste les bateaux coulés)
        enemy_sunk = Player("X")
        enemy_sunk.ship_positions = {n: p for n, p in self.enemy.ship_positions.items() if self.is_ship_sunk(self.enemy, n)}
        du.draw_continuous_ships(self.screen, enemy_sunk, 800, 150, 55, self.THEME_ENEMY, (220,150,255))

        # 4. Dessin des Grilles et Marqueurs
        du.draw_grid_lines_and_markers(self.screen, self.player, 50, 250, 35, self.fonts['std'], True)
        du.draw_grid_lines_and_markers(self.screen, self.enemy, 800, 150, 55, self.fonts['std'], False)

        # 5. Interface Utilisateur (UI)
        du.draw_enemy_status(self.screen, self.enemy, self.title_font, self.fonts['std'], self.is_ship_sunk)
        du.draw_cards(self.screen, self.player, self.selected_card, self.fonts['card'])
        
        # On prépare les infos pour l'interface textuelle
        game_state = {
            'player_turn': self.player_turn,
            'text_status': self.text_status,
            'start_time': self.start_time,
            'ai_phrase': self.ai_phrase_to_display
        }
        du.draw_game_interface(self.screen, self.player, self.enemy, self.fonts, game_state)

        # 6. Effets Visuels (FX)
        if self.projectile: 
            pygame.draw.circle(self.screen, self.projectile["color"], (int(self.projectile["pos"][0]), int(self.projectile["pos"][1])), 8)
        self.particles.update_and_draw(self.screen)
        
        # 7. Écran de Fin (Sécurité, normalement géré par main.py)
        if self.game_over and self.game_over_screen: 
            self.game_over_screen.draw()
