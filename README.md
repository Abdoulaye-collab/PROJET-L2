# PROJET-L2

![Bannière du Jeu](assets/images/banner.png)
# Wizard Battleship : Une bataille navale pas comme les autres...

> Une réinterprétation immersive du jeu de stratégie classique, développée en Python avec Pygame.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?style=flat&logo=pygame)
![Hugging Face](https://img.shields.io/badge/IA-Hugging_Face-yellow)
![Status](https://img.shields.io/badge/Status-Terminé-success)

## L'Expérience de Jeu
Ce projet ne se contente pas de reproduire la bataille navale : il vous plonge dans la peau d'un sorcier des mers. Le jeu est conçu comme une progression en trois phases distinctes, chacune avec sa propre identité visuelle :

### 1. La Cabine du Capitaine (Identification)
L'aventure débute dans le calme avant la tempête. Vous êtes **installé à votre bureau**, face à une vue imprenable sur l'océan. C'est dans ce cadre, prêt à ouvrir le livre des secrets, que vous signez votre entrée dans le conflit.

### 2. Le Grimoire Tactique (Phase de Placement)
Le jeu bascule **à l'intérieur du grimoire**. Les pages s'ouvrent pour révéler la carte de bataille. C'est le moment de la réflexion : vous tracez vos plans et dessinez la position de votre flotte magique sur le parchemin.

### 3. Le Duel des Arcanes (Phase de Combat)
Le grimoire se referme, la magie opère. Le plateau de jeu s'anime d'énergies néons et cyan. Chaque tir est un sortilège, chaque impact une explosion de particules. Vous affrontez une IA tactique dans un déluge d'effets visuels.

---
## Galerie
| La Cabine | Le Grimoire | Le Duel |
| :---: | :---: | :---: |
| <img width="200" alt="nomsV2" src="https://github.com/user-attachments/assets/a298e519-1685-44d5-b6d3-1962816c099f" /> | <img width="200" alt="grimoire" src="https://github.com/user-attachments/assets/3df465fa-2bef-4931-8a3f-d09b730386dd" /> | <img width="200" alt="combatV2" src="https://github.com/user-attachments/assets/ee445c9f-8ede-41f2-9418-1a91ef3f8e59" /> |

## Fonctionnalités Clés
* **Interface Complète :** Navigation fluide entre plusieurs écrans (Menu, Placement, Jeu, Fin).
* **Inscription Immersive :** Saisissez votre nom et nommez votre rival depuis votre bureau de commandement.
* **Système de Cartes :** Utilisez des sorts (Radar, Bombe, Salve...) pour renverser le cours de la bataille.
* **Moteur de Particules :** Explosions dynamiques, effets magique et impacts visuels faits "main".
* **Intelligence Artificielle :** Une IA capable de stratégie (mode "Chasse") et de dialogue via l'API Hugging Face.
* **Design Sonore :** Musique d'ambiance, bruitages d'impacts, de sort pour renforcer l'immersion.
---
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
---
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
└──  assets/               # Dossier contenant Images, Sons et Polices
└── rapport/               # Dossier rapport
    │
    ├── L2_rapport_rakotoarivelo_ly.pdf     #Le fichier final pour la lecture
    ├── L2_rapport_rakotoarivelo_ly.tex     #Le fichier source modifiable
    │
    └── images/                             #Les images insérées dans le rapport
````
---
## Installation et Lancement

### 1. Prérequis Techniques
* **Python 3.11+** doit être installé sur votre machine.
* Une **connexion internet active** est requise pour permettre à l'IA de réfléchir et de discuter (API Hugging Face).

### 2. Récupération du Projet
Ouvrez un terminal et clonez le dépôt (ou extrayez l'archive fournie) :
```bash
git clone [https://github.com/Abdoulaye-collab/PROJET-L2.git](https://github.com/Abdoulaye-collab/PROJET-L2.git)
cd PROJET-L2
````
### 3. Installation des Dépendances
Le jeu nécessite **pygame** pour le moteur graphique et **huggingface_hub** pour l'intelligence artificielle.
Installez-les via pip :
```bash
pip install pygame huggingface_hub
````
### 4. Configuration de l'IA
Note pour la correction : Une clé API Hugging Face valide est déjà intégrée dans le code source (**ai_llm.py**). Vous n'avez aucune configuration à effectuer : le module de chat et la stratégie avancée de l'IA fonctionneront immédiatement.

### 5. Lancer le Jeu
Une fois dans le dossier du projet, lancez simplement la commande :
```bash
python main.py
````
(Note : Sur certains systèmes Mac/Linux, utilisez **python3 main.py**)

### Dépannage rapide
* **Erreur** **ModuleNotFoundError** : Vérifiez que vous avez bien lancé la commande **pip install** de l'étape 3.
* **Pas de son** : Vérifiez que vos haut-parleurs sont activés (le jeu utilise Pygame Mixer).
* **L'IA ne répond pas** : Vérifiez votre connexion internet. Si le réseau de l'université bloque les API externes, essayez en partage de connexion.
---
## Pistes d'Amélioration
Si le temps le permettait, voici les fonctionnalités que nous aimerions ajouter : 

### Interface & Expérience Utilisateur
* **Menu d'Options :** Ajouter une interface pour régler le volume sonore (Musique/Bruitages) et la taille de la fenêtre en temps réel.
* **Personnalisation (Skins) :** Laisser le joueur choisir son allégeance magique au début (Team Cyan ou Team Violet).
* **Système d'Avatars :** Intégrer des portraits visuels ("Mascottes") qui réagissent selon l'état de la partie (Content quand on touche, Triste quand on est touché).
* **Sauvegarde & Navigation :**
    * Ajouter un bouton "Retour" pour naviguer fluidement entre les menus.
    * Implémenter un système de sauvegarde (sérialisation) pour reprendre une partie en cours.
### Nouveaux Modes de Jeu
* **Mode Multijoueur :** Permettre à deux joueurs de s'affronter en réseau local (Sockets) ou sur le même écran..
* **"Mort Subite":** Un mode hardcore où chaque joueur ne possède qu'un seul bateau. La première erreur est fatale !
* **Difficulté IA Modulable :** Ajouter un sélecteur de niveau pour l'IA :
    * *Novice :* Tirs purement aléatoires.
    * *Stratège :* L'IA actuelle (Chasse + LLM).
    * *Omniscient :* Une IA "Impossible" qui triche légèrement (probabilités augmentées).
### Mécaniques de Jeu
* **Cartes "Risque" :** Ajouter des cartes à double tranchant (50% de chance d'aider, 50% de chance de pénaliser).
---
  

## Crédits et Ressources
* Moteur: Pygame Community
* Images: générées par GEMINI et modifiées avec CANVA
* Sons: https://freesound.org/
* Polices : https://fonts.google.com/
  
## L'Équipe de Développement

Ce projet a été réalisé dans le cadre de l'UE *Algorithmique et Programmation* de Licence 2 MIASHS parcours MIAGE à l'**Université Paris Nanterre**.
* **Shelly-Linda Rakotoarivelo** 
* **Abdoulaye LY** 

