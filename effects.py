import pygame
import random

class ParticleSystem:
    """
    Système de gestion de particules pour les effets visuels.
    Gère les explosions (tirs) et les effets d'ambiance (magie/fumée).
    """
    def __init__(self):
        # Liste qui stocke toutes les particules actives
        # Chaque particule est un dictionnaire {x, y, dx, dy, timer, size, color}
        self.particles = []

    # ====================================================================
    #  CRÉATION DE PARTICULES
    # ====================================================================
    def trigger_hit_particles(self, x, y, main_color):
        """
        Crée une explosion de particules (Ex: quand un bateau est touché).
        Génère 20 particules qui partent dans toutes les directions.
        """
        r, g, b = main_color

        for _ in range(20): 
            # Variation légère de la couleur pour plus de réalisme
            var = random.randint(-30, 30)
            color = (max(0, min(255, r + var)), max(0, min(255, g + var)), max(0, min(255, b + var)))
            
            self.particles.append({
                'x': x,
                'y': y,
                'dx': random.uniform(-3, 3), # Vitesse horizontale aléatoire
                'dy': random.uniform(-3, 3), # Vitesse verticale aléatoire
                'timer': random.randint(20, 40), # Durée de vie (en frames)
                'size': random.randint(4, 8), # Taille de départ
                'color': color
            })
    
    def add_particle(self, x, y, color):
        """
        Ajoute une seule particule qui monte doucement (pour l'ambiance, fumée, magie).
        """
        self.particles.append({
            'x': x, 'y': y,
            'dx': random.uniform(-0.5, 0.5), # Bouge peu horizontalement
            'dy': random.uniform(-2, -0.5),  # Monte vers le haut (négatif)
            'timer': random.randint(20, 40),
            'size': random.randint(2, 4),
            'color': color
        })

    # ====================================================================
    #  MISE À JOUR ET DESSIN
    # ====================================================================
    def update_and_draw(self, screen):
        """
        Met à jour la position de chaque particule et les dessine.
        Gère la transparence (Alpha Blending) pour un effet de fondu.
        """

        # On parcourt la liste à l'envers pour pouvoir supprimer des éléments sans bug
        for i in range(len(self.particles) - 1, -1, -1):
            p = self.particles[i]
           
           # 1. Mise à jour physique
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['timer'] -= 1    # La vie diminue
            p['size'] -= 0.1   # La taille diminue
            
            # 2. Nettoyage : Si la particule est morte ou trop petite, on l'efface
            if p['timer'] <= 0 or p['size'] <= 0:
                self.particles.pop(i)
                continue
            
            # 3. Calcul de la transparence (Alpha)
            # Plus le timer est bas, plus alpha est bas (transparent)
            alpha = int((p['timer'] / 40) * 255)
            if alpha < 0: alpha = 0
            
            # 4. Dessin
            # On crée une petite surface temporaire pour gérer la transparence
            surface_size = int(p['size'] * 2)
            s = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
           
            # On dessine le cercle sur cette surface
            pygame.draw.circle(
                s, p['color'] + (alpha,), 
                (int(p['size']), int(p['size'])), 
                int(p['size'])
            )
            # On colle la surface sur l'écran principal
            screen.blit(s, (p['x'] - p['size'], p['y'] - p['size']))

    