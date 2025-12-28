# PROJET-L2

![Bannière du Jeu](assets/images/banner.png)
# Wizard Battleship : Une bataille navale pas comme les autres...

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
| La Cabine | Le Grimoire | Le Duel |
| :---: | :---: | :---: |
| <img width="200" alt="nomsV2" src="https://github.com/user-attachments/assets/a298e519-1685-44d5-b6d3-1962816c099f" /> | <img width="200" alt="grimoire" src="https://github.com/user-attachments/assets/3df465fa-2bef-4931-8a3f-d09b730386dd" /> | <img width="200" alt="combatV2" src="https://github.com/user-attachments/assets/ee445c9f-8ede-41f2-9418-1a91ef3f8e59" /> |

## Commandes et Contrôles
Le jeu se joue entièrement à la souris pour une fluidité maximale.
| Action | Commande | Contexte |
| :--- | :--- | :--- |
| **Placer un navire** | Clic Gauche | Phase de Placement |
| **Pivoter un navire** | Touche `R` | Phase de Placement |
| **Tirer un projectile** | Clic Gauche | Phase de Combat (Grille Ennemie) |
| **Activer une Carte** | Clic Gauche sur la carte | Phase de Combat (sous la Grille du Joueur) |
| **Utilisation de la carte** | Clic Gauche | Phase de Combat (Grille Enemie)
| **Annuler la carte** | Clic Gauche sur la carte | Phase de Combat |
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
│
├── main.py                 #  Point d'entrée principal du programme
├── settings.py             #  Configuration globale (Dimensions, Couleurs, Assets)
│
├──  Moteur de Jeu
│   ├── game.py             # Cœur du jeu : Boucle principale, tours, tirs
│   ├── player.py           # Classe Joueur : Gestion de la grille, flotte et inventaire
│   ├── placement.py        # Phase de placement des navires (Drag & Drop)
│   └── cards.py            # Logique des sortilèges (Double Tir, Radar, etc.)
│
├──  Interface & Graphismes
│   ├── menu.py             # Menu Principal animé
│   ├── input_name.py       # Écran de saisie des noms
│   ├── GameOver.py         # Écran de fin de partie (Victoire/Défaite)
│   ├── draw_utils.py       # Fonctions de dessin spécifiques (Grilles, HUD, Bateaux)
│   ├── effects.py          # Système de particules (Explosions, Magie)
│   └── utils.py            # Utilitaires génériques (Transitions, Texte contouré)
│
├──  Contrôles & Audio
│   ├── input_handler.py    # Gestionnaire d'événements (Clics souris, Clavier)
│   └── sound_manager.py    # Gestionnaire audio centralisé (Musique, SFX)
│
├──  Intelligence Artificielle
│   ├── ai_llm.py           # Algorithme de décision de tir (Stratégie)
│   └── ai_personalities.py # Système de dialogue et réactions de l'IA
│
└──  assets/              # Dossier contenant Images, Sons et Polices
````
## Installation 
1. Cloner le projet:
git clone [https://github.com/Abdoulaye-collab/PROJET-L2](https://github.com/Abdoulaye/PROJET-L2.git)
cd PROJET-L2

2. Installer les dépendances:

## 📋 Prérequis au bon fonctionnement

Pour lancer le jeu correctement, votre environnement doit impérativement contenir :

* **PYTHON version 3.11** : Version recommandée pour la compatibilité des bibliothèques.
* **PYGAME** : Le moteur graphique pour l'interface et les sons.
* **Bibliothèque Hugging Face** : Pour permettre la communication avec l'IA.
* **Clé API Hugging Face** : Un token d'accès pour activer les capacités de réflexion de l'IA.

---

### Installation de Pygame

Pygame est indispensable pour gérer l'affichage graphique, les sons et les interactions avec la souris. Voici comment l'installer selon votre système :

#### 1. Commande d'installation classique
Dans la plupart des cas, cette commande dans votre terminal suffit :
bash
pip install pygame

## Instructions d'Installation

### Installation des bibliothèques (Dépendances)
Ouvrez votre terminal et exécutez la commande suivante pour installer tout le nécessaire :


pip install pygame huggingface_hub

4. Lancer le jeu: python main.py

## Pistes d'Amélioration 
Si le temps le permettait, voici les fonctionnalités qu'on aimerait ajouter : 
* Un mode jouer contre jouer
* Un mode mort subite ou les deux joeurs n'ont qu' un seul bateau
* Un mode avec des cartes 50/50 qui permettrait d'avoir une chance sur deux d'etre benefique ou negatif pour les joueurs 

## Crédits
Sons du jeu : https://freesound.org/
## L'Équipe de Développement

Ce projet a été réalisé en collaboration par :

* **[Shelly-Linda] [Rakotoarivelo]** 
* **[Abdoulaye] [LY]** 
* **Cadre :** Projet en Algorithmique et Programmation de Licence 2 MIASHS parcours MIAGE - [Université Paris Nanterre]
* **Ressource:**
    * Moteur: Pygame Community
    * Images: générées par GEMINI et modifiées avec CANVA
    * Sons: 
