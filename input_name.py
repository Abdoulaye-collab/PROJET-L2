import pygame
import sys
import random
import math
from settings import * 
from utils import transition_fade, fade_in_action, draw_outlined_text, draw_dotted_line

def input_names(screen):
    """
    Fonction principale de l'écran de saisie.
    Gère l'affichage, les animations (particules) et la saisie clavier.
    """
    pygame.font.init()
    clock = pygame.time.Clock()

    
    # ====================================================================
    # 1. CONSTANTES & CONFIGURATION 
    # ====================================================================
    HEIGHT_BOX = 50
    WIDTH_BOX = 300
    GAP_VERTICAL = 80
    GAP_LABEL_TO_BOX = 10
    LINE_THICKNESS = 3
    DASH_LENGTH = 8 
    TEXT_COLOR = (255,255,255)
    
    # --- Chargement des Images ---
    background_menu = pygame.image.load('assets/images/fond_bateau.png').convert()
    background_menu = pygame.transform.smoothscale(background_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

    parchemin_img = pygame.image.load('assets/images/parchemin2.png').convert_alpha()
    PARCHMENT_WIDTH = 500 
    PARCHMENT_HEIGHT = 300
    parchemin_img = pygame.transform.smoothscale(parchemin_img, (PARCHMENT_WIDTH, PARCHMENT_HEIGHT))
    parchemin_rect = parchemin_img.get_rect(midbottom=(screen.get_width()//2, screen.get_height()-20))
    parchemin_loaded = True

    # --- Initialisation des Polices ---
    welcome_font = pygame.font.Font(FONT_NAME, 50) 
    font = pygame.font.Font(FONT_NAME, 35) 
    font_saisie = pygame.font.Font(FONT_NAME_GRIMOIRE, 40)
    
    # ====================================================================
    # 2. POSITIONNEMENT DES BOÎTES
    # ====================================================================
    center_x = screen.get_width() // 2 
    BOX_CENTERED_X = center_x - (WIDTH_BOX // 2)

    # Position Y de référence 
    Y_PLAYER_REF = parchemin_rect.top + 100
    
    # Création des rectangles (Hitbox)
    input_box_player = pygame.Rect(BOX_CENTERED_X, Y_PLAYER_REF, WIDTH_BOX, HEIGHT_BOX)
    input_box_ai = pygame.Rect(BOX_CENTERED_X, Y_PLAYER_REF + GAP_VERTICAL, WIDTH_BOX, HEIGHT_BOX)

    # Couleurs d'interaction
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')

    # États du jeu
    active_player = False
    active_ai = False
    text_player = ''
    text_ai = ''
    done = False

    # Gestion des particules et curseur
    particles = []

    # ====================================================================
    # 3. FONCTION DE DESSIN INTERNE 
    # ====================================================================
    def draw_whole_scene():
        # A. Fond & Parchemin
        screen.blit(background_menu,(0,0))
        if parchemin_loaded:
            screen.blit(parchemin_img, parchemin_rect)

        # B. Titre Principal
        Y_TITRE = 100
        welcome_text = "Déclinez votre Identité !"
        welcome_surf = welcome_font.render(welcome_text, True, COLOR_MAGIC_PLAYER) 
        welcome_rect = welcome_surf.get_rect(center=(center_x, 90))

        # Ombre du titre
        SHADOW_COLOR = (150, 0, 200) 
        shadow_rect = welcome_surf.get_rect(center=(center_x + 5, 93))
        screen.blit(welcome_font.render(welcome_text, True, SHADOW_COLOR), shadow_rect)
        
        # Contour du titre (Appel fonction utils)
        draw_outlined_text(
            screen=screen,
            text=welcome_text,
            font=welcome_font,
            color=COLOR_MAGIC_PLAYER,
            target_rect=welcome_rect
        )

        # C. Étiquettes de Rôles ("Amiral" et "Menace")
        DISTANCE_SOUS_LE_TITRE = 80
        START_Y_BOITES = Y_TITRE + DISTANCE_SOUS_LE_TITRE
        
        # -- Joueur --
        label_player_str = "Amiral des Arcanes"
        label_player_surf = font.render(label_player_str, True, (150, 0, 200))
        label_player_rect = label_player_surf.get_rect(
            centerx=input_box_player.centerx,
            y=START_Y_BOITES
        )
        draw_outlined_text(screen, label_player_str, font, (150, 0, 200), label_player_rect)
        
        # Ajustement position boite Joueur sous le texte
        input_box_player.y = label_player_rect.bottom + GAP_LABEL_TO_BOX

        # -- IA --
        ESPACE_ENTRE_LES_DEUX = 130
        label_ai_str = "Menace des Profondeurs"
        label_ai_surf = font.render(label_ai_str, True, (150, 0, 200))
        label_ai_rect = label_ai_surf.get_rect(
            centerx=input_box_ai.centerx,
            y=input_box_player.y + ESPACE_ENTRE_LES_DEUX
        )
        draw_outlined_text(screen, label_ai_str, font, (150, 0, 200), label_ai_rect)
        
        # Ajustement position boite IA sous le texte
        input_box_ai.y = label_ai_rect.bottom + GAP_LABEL_TO_BOX

        # D. Lignes Pointillées (Les zones de saisie)
        color_player = color_active if active_player else color_inactive
        color_ai = color_active if active_ai else color_inactive

        draw_dotted_line(screen, color_player, (input_box_player.left, input_box_player.bottom), (input_box_player.right, input_box_player.bottom), LINE_THICKNESS, DASH_LENGTH)
        draw_dotted_line(screen, color_ai, (input_box_ai.left, input_box_ai.bottom), (input_box_ai.right, input_box_ai.bottom), LINE_THICKNESS, DASH_LENGTH)
       
        # E. Texte Saisi (Le vrai texte)
        player_text_surf = font_saisie.render(text_player, True, TEXT_COLOR)
        player_text_rect = player_text_surf.get_rect(center=input_box_player.center)
        screen.blit(player_text_surf, player_text_rect)

        ai_text_surf = font_saisie.render(text_ai, True, TEXT_COLOR)
        ai_text_rect = ai_text_surf.get_rect(center=input_box_ai.center)
        screen.blit(ai_text_surf, ai_text_rect)

        # F. Curseur Magique & Particules
        target_box = None
        current_text = ""
        ORB_COLOR = (255, 255, 255) # Valeur par défaut
        
        # Détection de la boite active pour placer l'effet
        if active_ai:
            target_box = input_box_ai
            current_text = text_ai
            ORB_COLOR = (160, 32, 240)
        elif active_player:
            target_box = input_box_player
            current_text = text_player
            ORB_COLOR = (0, 255, 255)
            
        if target_box:
            # Calcul position curseur (à la fin du texte)
            text_surf = font.render(current_text, True, TEXT_COLOR)
            text_width = text_surf.get_width()
            cursor_x = target_box.centerx + (text_width // 2) + 2
            cursor_y = target_box.centery

            # Génération Particules
            for _ in range(2):
                particles.append({
                    'x': cursor_x + random.uniform(-3, 3),
                    'y': cursor_y + random.uniform(-3, 3),
                    'dx': random.uniform(-1, 1),
                    'dy': random.uniform(-2, -0.5),
                    'size': random.randint(2, 5),
                    'life': random.randint(20, 40),
                    'color': ORB_COLOR
                })
            
            # Dessin de l'Orbe (Curseur)
            current_time_orb = pygame.time.get_ticks()
            alpha = int(abs(math.sin(current_time_orb / 300)) * 200) + 55
            radius = 8

            orb_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(orb_surface, ORB_COLOR + (alpha,), (radius, radius), radius)
            pygame.draw.circle(orb_surface, (255, 255, 255), (radius, radius), radius - 3)
            screen.blit(orb_surface, (cursor_x - radius, cursor_y - radius))

        # Mise à jour et dessin des particules existantes
        for p in particles[:]:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['size'] -= 0.1
            p['life'] -= 1
            
            if p['life'] <= 0 or p['size'] <= 0:
                particles.remove(p)
                continue
            
            alpha_p = int((p['life'] / 40) * 255)
            if alpha_p < 0: alpha_p = 0
            
            s_part = pygame.Surface((int(p['size']*2), int(p['size']*2)), pygame.SRCALPHA)
            pygame.draw.circle(s_part, p['color'] + (alpha_p,), (int(p['size']), int(p['size'])), int(p['size']))
            screen.blit(s_part, (p['x'] - p['size'], p['y'] - p['size']))
    
    # ====================================================================
    # 4. TRANSITION D'ENTRÉE (FADE IN)
    # ====================================================================
    fade_in_action(screen, draw_whole_scene)

    # ====================================================================
    #  BOUCLE PRINCIPALE
    # ====================================================================
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # --- Gestion de la Souris ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_player = input_box_player.collidepoint(event.pos)
                active_ai = input_box_ai.collidepoint(event.pos)
            
            # --- Gestion du Clavier ---
            if event.type == pygame.KEYDOWN:
                # Touche ENTRÉE
                if event.key == pygame.K_RETURN:
                    if active_player:
                        # Si on valide le joueur, on passe auto à l'IA
                        if text_player.strip() != '':
                            active_player = False; active_ai = True
                            active_ai = True

                            pygame.event.clear()
                            continue
                    elif active_ai: 
                        # Si on valide l'IA et que les deux sont remplis, on finit
                        if text_ai.strip() != '' and text_player.strip() != '':
                            done = True
                            continue # On sort pour valider
                
                # Touche EFFACER et ÉCRITURE
                if active_ai:
                    if event.key == pygame.K_BACKSPACE:
                        text_ai = text_ai[:-1]
                    elif len(text_ai) < 15: # Limite caractères
                        text_ai += event.unicode
                
                elif active_player:
                    if event.key == pygame.K_BACKSPACE:
                        text_player = text_player[:-1]
                    elif len(text_player) < 15: # Limite caractères
                        text_player += event.unicode

        # Appel de la fonction de dessin
        draw_whole_scene()
        
        pygame.display.flip()
        clock.tick(30)

    # ====================================================================
    # 6. FIN ET RETOUR
    # ====================================================================
    transition_fade(screen)
    # Si l'IA n'a pas de nom, on met un défaut
    final_ai = text_ai.strip() if text_ai.strip() else "Le Léviathan"
    
    return text_player.strip(), final_ai