import pygame
from settings import FONT_NAME,COLOR_OCEAN_DARK, COLOR_TEXT_MAGIC, COLOR_UI_BACKGROUND

# ====================================================================
#  FONCTION INPUT_NAMES : GESTION DE LA SAISIE DES NOMS
# ====================================================================
def input_names(screen):
    pygame.font.init()
    font = pygame.font.Font(FONT_NAME, 35)

   # --- INITIALISATION DES POLICES ET HORLOGE ---
    welcome_font = pygame.font.Font(FONT_NAME, 50) 
    font = pygame.font.Font(FONT_NAME, 30) # La police originale pour les instructions
    
    clock = pygame.time.Clock()
    
    # --- PARAMÈTRES DES BOÎTES DE SAISIE ---
    input_box_player = pygame.Rect(300, 200, 300, 50)
    input_box_ai = pygame.Rect(300, 300, 300, 50)

    # Couleurs d'interaction
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_player = color_inactive
    color_ai = color_inactive

    # États
    active_player = False
    active_ai = False
    text_player = ''
    text_ai = 'IA'
    done = False

    # --- CONSTANTE ET POSITIONNEMENT ---
    center_x = screen.get_width() // 2 
    BOX_CENTERED_X = center_x - (input_box_player.width // 2)

    # Ajuster la position X des boîtes pour les centrer
    input_box_player.x = BOX_CENTERED_X
    input_box_ai.x = BOX_CENTERED_X

    #----------------------------------------------------------------------
    # A. BOUCLE PRINCIPALE ET GESTION DES ÉVÉNEMENTS
    # ----------------------------------------------------------------------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            
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

                # Saisie pour le Joueur
                if active_player:
                    if event.key == pygame.K_RETURN:
                        active_player = False
                        color_player = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text_player = text_player[:-1]
                    else:
                        text_player += event.unicode
                
                # Saisie pour l'IA (si nécessaire)
                elif active_ai:
                    if event.key == pygame.K_RETURN:
                        active_ai = False
                        color_ai = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text_ai = text_ai[:-1]
                    else:
                        text_ai += event.unicode

                # Validation finale si les deux noms sont saisis
                if event.key == pygame.K_RETURN and text_player.strip() != '':
                    done = True

        # ----------------------------------------------------------------------
        # B. LOGIQUE D'AFFICHAGE ET DESSIN
        # ----------------------------------------------------------------------
        screen.fill(COLOR_OCEAN_DARK)

        # --- 1. Panneau de Fond ---
        PANEL_WIDTH = 450
        PANEL_HEIGHT = 280
        PANEL_RECT = pygame.Rect(
            center_x - (PANEL_WIDTH // 2),  # x: Début du panneau
            100,                            # y: Démarre sous le titre de Bienvenue (Y=50)
            PANEL_WIDTH,
            PANEL_HEIGHT
        )
    
        PANEL_COLOR = COLOR_UI_BACKGROUND
        
        # Dessin du panneau (arrière-plan pour les boîtes de saisie)
        pygame.draw.rect(screen, PANEL_COLOR, PANEL_RECT)
        pygame.draw.rect(screen, (0, 0, 0), PANEL_RECT, 3) # Bordure noire
        

        # --- 2. Titre de Bienvenue ---
        welcome_text = "Bienvenue, Sorcier de la Flotte !"
        welcome_surf = welcome_font.render(welcome_text, True, COLOR_TEXT_MAGIC)
        welcome_rect = welcome_surf.get_rect(center=(screen.get_width() // 2, 50))
        
        # Ombre magique
        SHADOW_COLOR = (150, 0, 200) 
        shadow_rect = welcome_surf.get_rect(center=(screen.get_width()//2 + 3, 53))
        screen.blit(welcome_font.render("Bienvenue, Sorcier de la Flotte !", True, SHADOW_COLOR), shadow_rect)
        
        screen.blit(welcome_surf, welcome_rect)
        
        # --- 3. Logo Thématique ---
        LOGO_FILENAME = 'wizard_logo.png' 
        LOGO_SIZE = 120
        
        # Charger et redimensionner l'image
        logo_image = pygame.image.load(LOGO_FILENAME).convert_alpha()
        logo_image = pygame.transform.scale(logo_image, (LOGO_SIZE, LOGO_SIZE))
        logo_rect = logo_image.get_rect(center=(screen.get_width()//2, 475)) 
            
        screen.blit(logo_image, logo_rect)
        
        # --- 4. Etiquettes de Rôles Thématiques ---

        # Étiquette du Joueur
        label_player_text = "Nom du Joueur"
        label_player_surf = font.render(label_player_text, True, COLOR_TEXT_MAGIC)
        label_player_rect = label_player_surf.get_rect(centerx=input_box_player.centerx, y=140)
        screen.blit(label_player_surf, label_player_rect)

        # 3. Étiquette de l'IA
        label_ai_text = "Nom du Rival (IA)"
        label_ai_surf = font.render(label_ai_text, True, COLOR_TEXT_MAGIC)
        label_ai_rect = label_ai_surf.get_rect(centerx=input_box_ai.centerx, y=250)
        screen.blit(label_ai_surf, label_ai_rect)

        # --- 5. Dessin des Boîtes et Saisie ---

        # Bordures des boîtes 
        pygame.draw.rect(screen, color_player, input_box_player, 2)
        pygame.draw.rect(screen, color_ai, input_box_ai, 2)
        
        #Affichage du texte saisi
        PADDING_X = 5
        PADDING_Y = 5
        TEXT_COLOR = (255, 255, 255) # Blanc pour le texte

        # Texte du Joueur
        player_text_surf = font.render(text_player, True, TEXT_COLOR)
        screen.blit(player_text_surf(input_box_player.x + PADDING_X, input_box_player.y + PADDING_Y))

        # Texte de l'IA
        ai_text_surf = font.render(text_ai, True, TEXT_COLOR)
        screen.blit(ai_text_surf, (input_box_ai.x + PADDING_X, input_box_ai.y + PADDING_Y))

        #Mise à jour de l'affichage
        pygame.display.flip()
        clock.tick(30)

    # ----------------------------------------------------------------------
    # C. FIN DE LA FONCTION
    # ----------------------------------------------------------------------
    
    # Retourne le nom du joueur (strippé) et le nom de l'IA (strippé ou "IA" par défaut)
    return text_player.strip(), text_ai.strip() or "IA"
