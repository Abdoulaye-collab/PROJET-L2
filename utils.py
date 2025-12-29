import pygame

# ====================================================================
#  FONCTIONS DE TRANSITION (FADE IN / FADE OUT)
# ====================================================================
def transition_fade(screen: pygame.Surface, speed: int = 25):
    """
    Fait un fondu au noir (FERMETURE) pour une transition fluide.
    Bloque le jeu le temps de l'animation.
    """

    # Création d'une surface noire transparente
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    
    for alpha in range(0, 256, speed): 
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(15) # Pause en millisecondes
        
        # Dit à l'ordinateur que le jeu est vivant
        pygame.event.pump() 
    
    # Sécurité : Écran noir total + petite pause
    screen.fill((0,0,0))
    pygame.display.flip()
    pygame.time.delay(50)
    
    # CRUCIAL : On supprime tous les clics faits pendant le noir
    pygame.event.clear() 

def fade_in_action(screen: pygame.Surface, draw_function,speed: int = 25):
    """
    Fait apparaître l'écran doucement (OUVERTURE).
    draw_function : La fonction qui dessine ce qu'il y a derrière le noir.
    """
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    
    # On va de 255 (Noir) à 0 (Transparent)
    for alpha in range(255, -1, -speed):
        
        # 1. On dessine la scène cachée derrière
        # Le try/except empêche le crash si le dessin rate
        try:
            draw_function() 
        except Exception as e:
            # Si ça plante, on continue quand même pour ne pas fermer le jeu
            pass 
        
        # 2. On dessine le voile noir par dessus
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        
        pygame.display.flip()
        pygame.time.delay(15)
        pygame.event.pump()
    
    # CRUCIAL : On supprime les clics parasites avant de rendre la main au joueur
    pygame.event.clear()


# ====================================================================
#  FONCTIONS DE DESSIN UTILITAIRES
# ====================================================================
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


def draw_outlined_text(screen, text, font, color, target_rect):
        """
        Dessine un texte avec un contour blanc automatique.
        """

        COLOR_CONTOUR = (255, 255, 255) # Blanc
        EPAISSEUR = 1 # Épaisseur du contour (2 est bon pour les petits textes)
        
        # Création des surfaces
        surf_main = font.render(text, True, color)
        surf_outline = font.render(text, True, COLOR_CONTOUR)
        
        # On centre le texte sur la zone cible
        rect = surf_main.get_rect(center=target_rect.center)
        
        # Dessiner le contour (8 directions)
        offsets = [
            (-EPAISSEUR, -EPAISSEUR), (0, -EPAISSEUR), (EPAISSEUR, -EPAISSEUR),
            (-EPAISSEUR, 0),                           (EPAISSEUR, 0),
            (-EPAISSEUR, EPAISSEUR),  (0, EPAISSEUR),  (EPAISSEUR, EPAISSEUR)
        ]
        
        # 1. Dessiner le contour (en dessous)
        for dx, dy in offsets:
            # rect_decale = rect.move(dx,dy)
            screen.blit(surf_outline, rect.move(dx, dy))
            
        # 2. Dessiner le texte principal (au dessus)
        screen.blit(surf_main,rect)
            