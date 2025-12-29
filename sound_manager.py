import pygame

class SoundManager:
    """
    Gestionnaire centralisé de l'audio (Musique et Effets Sonores).
    Permet de charger les sons en toute sécurité sans faire planter le jeu
    si un fichier est manquant.
    """
    def __init__(self):
        self.enabled = False

        # Initialisation du module de son de Pygame
        # (frequency, size, channels, buffer)
        try:
            pygame.mixer.init(44100, -16, 2, 2048)
            self.enabled = True
        except Exception as e:
            print(f" Erreur critique Audio : {e}")
            self.enabled = False
            return
        
        # --- 1. CHARGEMENT DE LA MUSIQUE ---
        try:
            # On charge la musique de fond
            pygame.mixer.music.load("assets/sounds/theme.mp3")
            pygame.mixer.music.set_volume(0.2) # Volume bas pour l'ambiance (20%)
            pygame.mixer.music.play(-1)        # -1 = Boucle infinie
            
        except Exception as e:
            print(f" Audio désactivé : {e}")

        # --- 2. CHARGEMENT DES EFFETS SONORES ---
        # On initialise à None pour éviter les crashs si le fichier manque
        self.sound_hit = None 
        self.sound_miss = None 
        self.sound_card = None 
            
    # Fonction helper pour charger un son en sécurité
        def load_sound(path, volume=0.5):
            try:
                snd = pygame.mixer.Sound(path)
                snd.set_volume(volume)
                return snd
            except:
                print(f" Fichier son manquant : {path}")
                return None
        
    # Chargement effectif
        self.sound_hit = load_sound("assets/sounds/hit.wav", 0.6)
        self.sound_miss = load_sound("assets/sounds/miss.wav", 0.4)
        self.sound_card = load_sound("assets/sounds/card.wav", 0.7)

    # ====================================================================
    #  MÉTHODES DE LECTURE (SÉCURISÉES)
    # ====================================================================

    def play_hit(self):
        """Joue le son d'explosion (Touché)."""
        if self.enabled: self.sound_hit.play()

    def play_miss(self):
        """Joue le son d'eau (Raté)."""
        if self.enabled: self.sound_miss.play()

    def play_card(self):
        """Joue le son magique d'activation de carte."""
        if self.enabled: self.sound_card.play()
    
    def stop_music(self):
        """Coupe la musique."""
        if self.enabled:
            pygame.mixer.music.stop()