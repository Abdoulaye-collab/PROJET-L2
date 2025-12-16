import pygame
import sys
import math
import random
from settings import FONT_NAME,COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, COLOR_UI_BACKGROUND,SCREEN_WIDTH,SCREEN_HEIGHT


# --- FONCTION UTILITAIRE DE DESSIN (DOIT ÊTRE EN DEHORS DE input_names) ---
def draw_dotted_line(surface, color, start_point, end_point, thickness, dash_length):
    """Dessine une ligne pointillée (seulement horizontale pour la simplicité ici)."""
    if start_point[1] != end_point[1]:
        return 
    x1, y = start_point
    x2, _ = end_point
    current_x = x1
    while current_x < x2:
        start = (current_x, y)
        end = (current_x + dash_length, y)
        pygame.draw.line(surface, color, start, end, thickness)
        current_x += dash_length * 2

# --- FONCTION UTILITAIRE CONTOUR TEXTE ---
def draw_outlined_text(screen, text, font, color, target_rect):
        """
        Dessine un texte avec un contour blanc automatique.
        """
        COLOR_CONTOUR = (255, 255, 255) # Blanc
        EPAISSEUR = 1 # Épaisseur du contour (2 est bon pour les petits textes)
        
        surf_main = font.render(text, True, color)
        surf_outline = font.render(text, True, COLOR_CONTOUR)
        rect = surf_main.get_rect(center=target_rect.center)
        
        # Dessiner le contour (8 directions)
        offsets = [
            (-EPAISSEUR, -EPAISSEUR), (0, -EPAISSEUR), (EPAISSEUR, -EPAISSEUR),
            (-EPAISSEUR, 0),                           (EPAISSEUR, 0),
            (-EPAISSEUR, EPAISSEUR),  (0, EPAISSEUR),  (EPAISSEUR, EPAISSEUR)
        ]
        
        for dx, dy in offsets:
            # rect_decale = rect.move(dx,dy)
            screen.blit(surf_outline, rect.move(dx, dy))
        
        screen.blit(surf_main,rect)
            
# ====================================================================
#  FONCTION INPUT_NAMES : GESTION DE LA SAISIE DES NOMS
# ====================================================================
def input_names(screen):
    pygame.font.init()
    # --- CONSTANTES D'INTERFACE ---
    HEIGHT_BOX = 50
    WIDTH_BOX = 300
    GAP_VERTICAL = 80
    GAP_LABEL_TO_BOX = 10
    LINE_THICKNESS = 3
    DASH_LENGTH = 8 
    TEXT_COLOR = (50,30,10)
    background_menu = pygame.image.load('images/fond_bateau.png').convert()
    background_menu = pygame.transform.smoothscale(background_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

   # --- INITIALISATION DES POLICES ET HORLOGE ---
    welcome_font = pygame.font.Font(FONT_NAME, 50) 
    font = pygame.font.Font(FONT_NAME, 35) # La police originale pour les instructions
    
    clock = pygame.time.Clock()

    parchemin_img = pygame.image.load('images/parchemin2.png').convert_alpha()
    PARCHMENT_WIDTH = 500 
    PARCHMENT_HEIGHT = 300
    parchemin_img = pygame.transform.smoothscale(parchemin_img, (PARCHMENT_WIDTH, PARCHMENT_HEIGHT))
    parchemin_rect = parchemin_img.get_rect(midbottom=(screen.get_width()//2, screen.get_height()-20))

    parchemin_loaded = True

    # --- CONSTANTE ET POSITIONNEMENT ---
    center_x = screen.get_width() // 2 
    BOX_CENTERED_X = center_x - (WIDTH_BOX // 2)

    # Position Y de référence pour le joueur
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

    # --- CURSEUR CLIGNOTANT ---
    cursor_visible = True
    cursor_timer = pygame.time.get_ticks()
    particles = []
    CURSOR_BLINK_RATE = 500 # Clignote toutes les 500 millisecondes (0.5s)

    # Ajuster la position X des boîtes pour les centrer
    input_box_player.x = BOX_CENTERED_X
    input_box_ai.x = BOX_CENTERED_X

    #----------------------------------------------------------------------
    # A. BOUCLE PRINCIPALE ET GESTION DES ÉVÉNEMENTS
    # ----------------------------------------------------------------------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # --- Clic de souris ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérification des clics sur les boîtes
                active_player = input_box_player.collidepoint(event.pos)
                active_ai = input_box_ai.collidepoint(event.pos)
               
               # Mise à jour des couleurs
                color_player = color_active if active_player else color_inactive
                color_ai = color_active if active_ai else color_inactive
            
            # --- Saisie au clavier ---
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if active_player:
                            if text_player.strip() != '':
                                active_player = False
                                active_ai = True
                                color_player = color_inactive
                                color_ai = color_active
                                cursor_visible = True
                                cursor_timer = pygame.time.get_ticks()

                        elif active_ai: 
                            if text_ai.strip() != '':
                                if text_player.strip() != '' :
                                    done = True
                        continue

                    if active_ai:
                        if event.key == pygame.K_BACKSPACE:
                            text_ai = text_ai[:-1]
                        elif len(text_ai) < 15:  # Limite de 20 caractères
                            text_ai += event.unicode
                    
                    elif  active_player:
                        if event.key == pygame.K_BACKSPACE:
                            text_player= text_player[:-1]
                        elif len(text_player) < 15:  # Limite de 20 caractères
                            text_player += event.unicode

                # # Validation finale si les deux noms sont saisis
                # if event.key == pygame.K_RETURN and text_player.strip() != ''and text_ai.strip() != '':
                #     done = True
        # ----------------------------------------------------------------------
        # B. MISE A JOUR DU CURSEUR CLIGNOTANT
        # ----------------------------------------------------------------------
        current_time = pygame.time.get_ticks()
        if current_time - cursor_timer > CURSOR_BLINK_RATE:
            cursor_visible = not cursor_visible
            cursor_timer = current_time

        # ----------------------------------------------------------------------
        # c. LOGIQUE D'AFFICHAGE ET DESSIN
        # ----------------------------------------------------------------------
        screen.blit(background_menu,(0,0))

        Y_TITRE = 100

        if parchemin_loaded:
            # On dessine l'image sur l'écran à la position calculée
            screen.blit(parchemin_img, parchemin_rect)

        LINE_THICKNESS = 3
        DASH_LENGTH = 8 
        TEXT_COLOR = (255,255,255)
        # --- 1. Titre de Bienvenue ---
        
        welcome_text = "Bienvenue, Sorcier de la Flotte !"
        welcome_surf = welcome_font.render(welcome_text, True, COLOR_TEXT_MAGIC ) #VIOLET MAGIQUE
        welcome_rect = welcome_surf.get_rect(center=(center_x, 90))


        # Ombre magique
        SHADOW_COLOR = (150, 0, 200) 
        shadow_rect = welcome_surf.get_rect(center=(center_x + 5, 93))
        screen.blit(welcome_font.render(welcome_text, True, SHADOW_COLOR), shadow_rect)
        screen.blit(welcome_surf, welcome_rect)
        
        DISTANCE_SOUS_LE_TITRE = 80
        START_Y_BOITES = Y_TITRE + DISTANCE_SOUS_LE_TITRE



        # --- 2. Etiquettes de Rôles Thématiques ---

        # a. Étiquette du Joueur
        Y_LABEL_PLAYER = 250
        label_player_str = "Nom du Joueur"
        label_player_surf = font.render(label_player_str, True, (150, 0, 200))
        # Positionnement dynamique de l'étiquette
        label_player_rect = label_player_surf.get_rect(
            centerx=input_box_player.centerx,
            y=START_Y_BOITES # position au-dessus de la boîte
        )
        # screen.blit(label_player_surf, label_player_rect)

        draw_outlined_text(
            screen=screen,
            text=label_player_str,
            font=font,
            color=(150, 0, 200),
            target_rect = label_player_rect
        )
        input_box_player.y = label_player_rect.bottom + 5

        # b. Étiquette de l'IA
        ESPACE_ENTRE_LES_DEUX = 130
        Y_LABEL_AI = 450
        label_ai_str = "Nom du Rival (IA)"
        label_ai_surf = font.render(label_ai_str, True, (150, 0, 200))
        # Positionnement dynamique de l'étiquette
        label_ai_rect = label_ai_surf.get_rect(
            centerx=input_box_ai.centerx,
            y=input_box_player.y + ESPACE_ENTRE_LES_DEUX  # position au-dessus de la boît
        )
        # screen.blit(label_ai_surf, label_ai_rect)


        draw_outlined_text(
            screen=screen,
            text=label_ai_str,
            font=font,
            color=(150, 0, 200),
            target_rect=label_ai_rect
        )        
        input_box_ai.y = label_ai_rect.bottom + 5



         # --- 3. Dessin des Pointillés et Saisie ---

        # Mise à jour des positions Y des boîtes (pour qu'elles soient juste sous leur titre)
        input_box_player.y = label_player_rect.bottom + GAP_LABEL_TO_BOX
        input_box_ai.y = label_ai_rect.bottom + GAP_LABEL_TO_BOX
        
        # Ligne Pointillée du Joueur
        draw_dotted_line(
            screen, 
            color_player, 
            (input_box_player.left, input_box_player.bottom),
            (input_box_player.right, input_box_player.bottom), 
            LINE_THICKNESS, 
            DASH_LENGTH
        )
        
        # Ligne Pointillée de l'IA
        draw_dotted_line(
            screen, 
            color_ai, 
            (input_box_ai.left, input_box_ai.bottom), 
            (input_box_ai.right, input_box_ai.bottom), 
            LINE_THICKNESS, 
            DASH_LENGTH
        )
     
        # --- Affichage du Texte Saisi (Centrage) ---
        
        # Texte du Joueur
        player_text_surf = font.render(text_player, True, TEXT_COLOR)
        player_text_rect = player_text_surf.get_rect(center=input_box_player.center)
        screen.blit(player_text_surf, player_text_rect)

        # Texte de l'IA
        ai_text_surf = font.render(text_ai, True, TEXT_COLOR)
        ai_text_rect = ai_text_surf.get_rect(center=input_box_ai.center)
        screen.blit(ai_text_surf, ai_text_rect)

        

        
       # --- 4. Curseur de Saisie (MAGIQUE ET PULSANT) ---
        
        # On détermine quelle boîte est active pour savoir où dessiner et quel texte mesurer
        target_box = None
        current_text = ""
        
        if active_ai:
            target_box = input_box_ai
            current_text = text_ai
            ORB_COLOR = (160, 32, 240)
        elif active_player:
            target_box = input_box_player
            current_text = text_player
            ORB_COLOR = (0, 255, 255)
            
        # Si une boîte est active, on dessine le curseur magique
        if target_box:
            # 1. Calcul de la position X
            # Comme ton texte est centré, le curseur doit être à : centre_boite + (moitié_largeur_texte) + petite_marge
            text_surf = font.render(current_text, True, TEXT_COLOR)
            text_width = text_surf.get_width()
            
            cursor_x = target_box.centerx + (text_width // 2) + 2
            cursor_y = target_box.centery

            # --- A. CRÉATION DES PARTICULES (SPAWN) ---
            # On ajoute 2 particules par image pour faire une belle trainée
            for _ in range(2):
                particles.append({
                    'x': cursor_x + random.uniform(-3, 3),   # Légère variation X
                    'y': cursor_y + random.uniform(-3, 3),   # Légère variation Y
                    'dx': random.uniform(-1, 1),             # Vitesse horizontale
                    'dy': random.uniform(-2, -0.5),          # Vitesse verticale (monte vers le haut)
                    'size': random.randint(2, 5),            # Taille aléatoire
                    'life': random.randint(20, 40),          # Durée de vie
                    'color': ORB_COLOR                       # Couleur de l'orbe actuel
                })
            
            # --- B. DESSIN DE L'ORBE (Pulsation) ---
         
            current_time = pygame.time.get_ticks()
            alpha = int(abs(math.sin(current_time / 300)) * 200) + 55
            radius = 8

            orb_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(orb_surface, ORB_COLOR + (alpha,), (radius, radius), radius)
            pygame.draw.circle(orb_surface, (255, 255, 255), (radius, radius), radius - 3)
            screen.blit(orb_surface, (cursor_x - radius, cursor_y - radius))

        # --- C. GESTION ET AFFICHAGE DES PARTICULES ---
        # On parcourt la liste à l'envers pour pouvoir supprimer des éléments sans bug
        for p in particles[:]:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['size'] -= 0.1  # Rétrécit doucement
            p['life'] -= 1    # Vieillit
            
            # Si la particule est morte ou trop petite, on l'enlève
            if p['life'] <= 0 or p['size'] <= 0:
                particles.remove(p)
                continue
            
            # Calcul de la transparence (fade out)
            # Plus la vie est basse, plus c'est transparent
            alpha_p = int((p['life'] / 40) * 255)
            if alpha_p < 0: alpha_p = 0
            
            # Dessin de la particule
            s_part = pygame.Surface((int(p['size']*2), int(p['size']*2)), pygame.SRCALPHA)
            # On dessine un cercle rempli avec la couleur et l'alpha
            pygame.draw.circle(s_part, p['color'] + (alpha_p,), (int(p['size']), int(p['size'])), int(p['size']))
            screen.blit(s_part, (p['x'] - p['size'], p['y'] - p['size']))
        pygame.display.flip()
        clock.tick(30)
    # ----------------------------------------------------------------------
    # C. FIN DE LA FONCTION
    # ----------------------------------------------------------------------
    
    # Retourne le nom du joueur (strippé) et le nom de l'IA (strippé ou "IA" par défaut)
    return text_player.strip(), text_ai.strip() or "IA"