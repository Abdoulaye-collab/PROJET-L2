# PROJET-L2

# Wizard Battleship : Une bataille navale pas comme les autres

> Une réinterprétation immersive du jeu de stratégie classique, développée en Python avec Pygame.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?style=flat&logo=pygame)
![Status](https://img.shields.io/badge/Status-Terminé-success)

## L'Expérience de Jeu
Ce projet ne se contente pas de reproduire la bataille navale : il vous plonge dans la peau d'un sorcier des mers. Le jeu est conçu comme une progression en trois phases distinctes, chacune avec sa propre identité visuelle :

### 1. La Cabine du Capitaine (Identification)
L'aventure débute dans le calme avant la tempête. Vous êtes **installé à votre bureau**, face à une vue imprenable sur l'océan. C'est dans ce cadre, prêt à ouvrir le livre des secrets, que vous signez votre entrée dans le conflit.

### 2. Le Grimoire Tactique (Phase de Placement)
Le jeu bascule **à l'intérieur du grimoire**. Les pages s'ouvrent pour révéler la carte de bataille. C'est le moment de la réflexion : vous tracez vos plans et dessinez la position de votre flotte magique sur le parchemin.

### 3. Le Duel des Arcanes (Phase de Combat)
Le grimoire se referme, la magie opère. Le plateau de jeu s'anime d'énergies néons et cyan. Chaque tir est un sortilège, chaque impact une explosion de particules. Vous affrontez une IA tactique dans un déluge d'effets visuels.

## Galerie
| L'Accueil | Le Grimoire (Placement) | Le Duel (Combat) |

| *Immersion à la 1ère personne* | *Stratégie sur parchemin* | *Magie et Particules* |

## Commandes et Contrôles
Le jeu se joue entièrement à la souris pour une fluidité maximale.
| Action | Commande | Contexte |
| :--- | :--- | :--- |
| **Placer un navire** | Clic Gauche | Phase de Placement |
| **Pivoter un navire** | Touche `R` | Phase de Placement |
| **Tirer un projectile** | Clic Gauche | Phase de Combat (Grille Ennemie) |
| **Activer une Carte** | Clic Gauche sur le haut de la carte | Phase de Combat (sous la Grille du Joueur) |
| **Utilisation de la carte** | Clic Gauche | Phase de Combat (Grille Enemie)
| **Annuler la carte** | Clic Gauche sur le haut de la carte | Phase de Combat |
| **Quitter** | Croix de la fenêtre | Tout le temps |

## Fonctionnalités Clés
* **Interface Complète :** Navigation fluide entre plusieurs écrans :
    * *Inscription du Sorcier:* Saisissez votre nom et nommez votre rival depuis votre bureau de commandement (Vue sur mer).
    * *Options :* Paramétrez le son et l'affichage avant le combat.
* **Système de Cartes & Mana :** Utilisez des sorts (Radar, Bombe, Salve...) pour renverser le cours de la bataille.
* **Moteur de Particules :** Explosions dynamiques, effets magique et impacts visuels faits "main".
* **Intelligence Artificielle :** Une IA capable de "chasser" (Target mode) lorsqu'elle touche un navire.
* **Design Sonore :** Musique d'ambiance, bruitages d'impacts, de sort pour renforcer l'immersion.

* ## Structure du Projet
Voici comment est organisé le code source :
```text
PROJET-L2/
├── assets/              # Images (fonds), Sons (.wav/.mp3), Polices (.ttf)
├── screenshots/         # Images pour ce README et Overleaf
├── main.py              # Point d'entrée : Lance le jeu
├── input_name.py        # Phase 1 : Menu d'accueil et saisie des noms 
├── placement.py         # Phase 2 : Grille tactique dans le grimoire (Placement des navires)
├── game.py              # Phase 3 : Cœur du jeu (Boucle de combat, tirs, affichage)
├── player.py            # Classes Player et Ship (Gestion de la flotte)
├── cards.py             # Logique des cartes magiques (Sorts)
├── ai_llm.py            # Cerveau de l'IA (Algorithme de chasse)
├── game_over.py         # Gestion de l'écran de victoire/défaite
└── settings.py          # Fichier de configuration (Constantes, Couleurs, Tailles)
````
## Installation 
1. Cloner le projet:
git clone [https://github.com/Abdoulaye/PROJET-L2.git](https://github.com/Abdoulaye/PROJET-L2.git)
cd PROJET-L2

2. Installer les dépendances:

3. Lancer le jeu: python main.py

## Pistes d'Amélioration 
Si le temps le permettait, voici les fonctionnalités qu'on aimerait ajouter : 
*
*
*

## Crédits
Sons du jeu : https://freesound.org/
## L'Équipe de Développement

Ce projet a été réalisé en collaboration par :

* **[Shelly-Linda] [Rakotoarivelo]** 
* **[Abdoulaye] [LY]** 
* **Cadre :** Projet de Licence 2 Informatique - [Université Paris Nanterre]
* **Ressource:**
    * Moteur: Pygame Community
    * Images/Sons: 
