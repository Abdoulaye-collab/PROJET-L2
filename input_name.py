import pygame
import sys
import random
import math
from settings import * 
from utils import transition_fade, fade_in_action, draw_outlined_text, draw_dotted_line
# J'ai ajouté draw_outlined_text dans les imports utils, 
# sinon copie la fonction draw_outlined_text tout en haut de ce fichier.

# Si tu as une fonction draw_dotted_line quelque part, assure-toi qu'elle est accessible.
# Sinon, ajoute-la ou importe-la ici.

def input_names(screen):
    pygame.font.init()
    
    # --- CONSTANTES D'INTERFACE (TES COULEURS) ---
    HEIGHT_BOX = 50
    WIDTH_BOX = 300
    GAP_VERTICAL = 80
    GAP_LABEL_TO_BOX = 10
    LINE_THICKNESS = 3
    DASH_LENGTH = 8 
    TEXT_COLOR = (255,255,255)
    
    # Chargement images
    background_menu = pygame.image.load('images/fond_bateau.png').convert()
    background_menu = pygame.transform.smoothscale(background_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

    parchemin_img = pygame.image.load('images/parchemin2.png').convert_alpha()
    PARCHMENT_WIDTH = 500 
    PARCHMENT_HEIGHT = 300
    parchemin_img = pygame.transform.smoothscale(parchemin_img, (PARCHMENT_WIDTH, PARCHMENT_HEIGHT))
    parchemin_rect = parchemin_img.get_rect(midbottom=(screen.get_width()//2, screen.get_height()-20))
    parchemin_loaded = True

    # --- INITIALISATION DES POLICES ET HORLOGE ---
    welcome_font = pygame.font.Font(FONT_NAME, 50) 
    font = pygame.font.Font(FONT_NAME, 35) 
    font_saisie = pygame.font.Font(FONT_NAME_GRIMOIRE, 40)
    clock = pygame.time.Clock()

    # --- CONSTANTE ET POSITIONNEMENT ---
    center_x = screen.get_width() // 2 
    BOX_CENTERED_X = center_x - (WIDTH_BOX // 2)

    # Position Y de référence
    Y_PLAYER_REF = parchemin_rect.top + 100
    
    input_box_player = pygame.Rect(BOX_CENTERED_X, Y_PLAYER_REF, WIDTH_BOX, HEIGHT_BOX)
    input_box_ai = pygame.Rect(BOX_CENTERED_X, Y_PLAYER_REF + GAP_VERTICAL, WIDTH_BOX, HEIGHT_BOX)

    # Couleurs d'interaction
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_player = color_inactive
    color_ai = color_inactive

    # États
    active_player = False
    active_ai = False
    text_player = ''
    text_ai = ''
    done = False

    # --- CURSEUR CLIGNOTANT ET PARTICULES ---
    cursor_visible = True
    cursor_timer = pygame.time.get_ticks()
    particles = []
    CURSOR_BLINK_RATE = 500 

    # ====================================================================
    #  LA FONCTION DE DESSIN (C'est ici qu'on a mis tout ton code de rendu)
    # ====================================================================
    def draw_whole_scene():
        # 1. Fond & Parchemin
        screen.blit(background_menu,(0,0))
        if parchemin_loaded:
            screen.blit(parchemin_img, parchemin_rect)

        # 2. Titre
        Y_TITRE = 100
        welcome_text = "Déclinez votre Identité !"
        welcome_surf = welcome_font.render(welcome_text, True, COLOR_MAGIC_PLAYER) 
        welcome_rect = welcome_surf.get_rect(center=(center_x, 90))

        # Ombre magique (Ton code original)
        SHADOW_COLOR = (150, 0, 200) 
        shadow_rect = welcome_surf.get_rect(center=(center_x + 5, 93))
        screen.blit(welcome_font.render(welcome_text, True, SHADOW_COLOR), shadow_rect)
        
        # Contour Titre (Ton code original)
        draw_outlined_text(
            screen=screen,
            text=welcome_text,
            font=welcome_font,
            color=COLOR_MAGIC_PLAYER,
            target_rect=welcome_rect
        )

        DISTANCE_SOUS_LE_TITRE = 80
        START_Y_BOITES = Y_TITRE + DISTANCE_SOUS_LE_TITRE

        # 3. Étiquettes de Rôles
        
        # a. Joueur
        label_player_str = "Amiral des Arcanes"
        label_player_surf = font.render(label_player_str, True, (150, 0, 200))
        label_player_rect = label_player_surf.get_rect(
            centerx=input_box_player.centerx,
            y=START_Y_BOITES
        )
        draw_outlined_text(screen, label_player_str, font, (150, 0, 200), label_player_rect)
        
        # Mise à jour position boîte Joueur
        input_box_player.y = label_player_rect.bottom + GAP_LABEL_TO_BOX

        # b. IA
        ESPACE_ENTRE_LES_DEUX = 130
        label_ai_str = "Menace des Profondeurs"
        label_ai_surf = font.render(label_ai_str, True, (150, 0, 200))
        label_ai_rect = label_ai_surf.get_rect(
            centerx=input_box_ai.centerx,
            y=input_box_player.y + ESPACE_ENTRE_LES_DEUX
        )
        draw_outlined_text(screen, label_ai_str, font, (150, 0, 200), label_ai_rect)
        
        # Mise à jour position boîte IA
        input_box_ai.y = label_ai_rect.bottom + GAP_LABEL_TO_BOX

        # 4. Lignes Pointillées (Ton code original)
        # (J'assume que la fonction draw_dotted_line existe dans ton projet)
        try:
            draw_dotted_line(screen, color_player, (input_box_player.left, input_box_player.bottom), (input_box_player.right, input_box_player.bottom), LINE_THICKNESS, DASH_LENGTH)
            draw_dotted_line(screen, color_ai, (input_box_ai.left, input_box_ai.bottom), (input_box_ai.right, input_box_ai.bottom), LINE_THICKNESS, DASH_LENGTH)
        except NameError:
            # Sécurité si la fonction n'est pas importée, on fait une ligne simple
            pygame.draw.line(screen, color_player, (input_box_player.left, input_box_player.bottom), (input_box_player.right, input_box_player.bottom), LINE_THICKNESS)
            pygame.draw.line(screen, color_ai, (input_box_ai.left, input_box_ai.bottom), (input_box_ai.right, input_box_ai.bottom), LINE_THICKNESS)

        # 5. Texte Saisi
        player_text_surf = font_saisie.render(text_player, True, TEXT_COLOR)
        player_text_rect = player_text_surf.get_rect(center=input_box_player.center)
        screen.blit(player_text_surf, player_text_rect)

        ai_text_surf = font_saisie.render(text_ai, True, TEXT_COLOR)
        ai_text_rect = ai_text_surf.get_rect(center=input_box_ai.center)
        screen.blit(ai_text_surf, ai_text_rect)

        # 6. Curseur Magique & Particules (Ton code exact)
        target_box = None
        current_text = ""
        ORB_COLOR = (255, 255, 255) # Valeur par défaut
        
        if active_ai:
            target_box = input_box_ai
            current_text = text_ai
            ORB_COLOR = (160, 32, 240)
        elif active_player:
            target_box = input_box_player
            current_text = text_player
            ORB_COLOR = (0, 255, 255)
            
        if target_box:
            text_surf = font.render(current_text, True, TEXT_COLOR)
            text_width = text_surf.get_width()
            cursor_x = target_box.centerx + (text_width // 2) + 2
            cursor_y = target_box.centery

            # Spawn particules
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
            
            # Orbe central
            current_time_orb = pygame.time.get_ticks()
            alpha = int(abs(math.sin(current_time_orb / 300)) * 200) + 55
            radius = 8
            orb_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(orb_surface, ORB_COLOR + (alpha,), (radius, radius), radius)
            pygame.draw.circle(orb_surface, (255, 255, 255), (radius, radius), radius - 3)
            screen.blit(orb_surface, (cursor_x - radius, cursor_y - radius))

        # Gestion Particules
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
    #  LANCEMENT DE LA TRANSITION FLUIDE
    # ====================================================================
    # On appelle la transition EN LUI DONNANT LA FONCTION DE DESSIN
    fade_in_action(screen, draw_whole_scene)

    # ====================================================================
    #  BOUCLE PRINCIPALE
    # ====================================================================
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_player = input_box_player.collidepoint(event.pos)
                active_ai = input_box_ai.collidepoint(event.pos)
                
                color_player = color_active if active_player else color_inactive
                color_ai = color_active if active_ai else color_inactive
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if active_player:
                        if text_player.strip() != '':
                            active_player = False; active_ai = True
                            color_player = color_inactive; color_ai = color_active
                            cursor_visible = True
                            cursor_timer = pygame.time.get_ticks()
                    elif active_ai: 
                        if text_ai.strip() != '' and text_player.strip() != '':
                            done = True
                            continue # On sort pour valider

                if active_ai:
                    if event.key == pygame.K_BACKSPACE:
                        text_ai = text_ai[:-1]
                    elif len(text_ai) < 15:
                        text_ai += event.unicode
                
                elif active_player:
                    if event.key == pygame.K_BACKSPACE:
                        text_player = text_player[:-1]
                    elif len(text_player) < 15:
                        text_player += event.unicode

        # --- DESSIN : ON APPELLE NOTRE FONCTION MAGIQUE ---
        draw_whole_scene()
        
        pygame.display.flip()
        clock.tick(30)

    # Fin de la boucle
    transition_fade(screen)
    return text_player.strip(), text_ai.strip() or "Le Léviathan"