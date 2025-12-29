import requests
import re
import random
from settings import GRID_SIZE

# ====================================================================
#  1. CONFIGURATION API (Hugging Face)
# ====================================================================
HF_API_KEY = "hf_xxxxxxxxxxxxx"  # Mets ici ton token HuggingFace
MODEL = "gpt2"

def query_huggingface(payload):
    """
    Envoie une requête POST à l'API Hugging Face avec un timeout de sécurité.
    """
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    try:
        # Timeout de 2 secondes pour ne pas figer le jeu si l'IA est lente
        response = requests.post(MODEL, headers=headers, json=payload, timeout=2)
        return response.json()
    except:
        # En cas d'erreur réseau (coupure, latence), on retourne None
        # Cela déclenchera automatiquement le mode Fallback
        # print(f"Erreur API : {e}") # Décommente pour débugger
        return None

# ====================================================================
#  2. FONCTIONS DE TRAITEMENT (Parsing & Prompt)
# ====================================================================
def get_llm_coordinates():
    """
    Mode INTUITION : Demande au LLM de générer des coordonnées.
    Retourne un tuple (row, col) ou None si échec.
    """
    prompt = "Battleship move strategy. Best coordinates: 5,5 - 2,3 - 9,0 - "
    
    data = query_huggingface({
        "inputs": prompt,
        "parameters": {"max_new_tokens": 5, "temperature": 0.7}
    })
    # Analyse de la réponse (Parsing)
    if data and isinstance(data, list) and 'generated_text' in data[0]:
        text = data[0]['generated_text']
        new_text = text.replace(prompt, "")
        # On utilise une Regex pour trouver le premier pattern "chiffre, chiffre"
        match = re.search(r"(\d)\s*,\s*(\d)", new_text)
        
        if match:
            return int(match.group(1)), int(match.group(2))

    return None

# ====================================================================
#  3. CERVEAU PRINCIPAL DE L'IA
# ====================================================================
def calculate_ai_move(player_board, targets_buffer):
    """
    Décide où tirer en utilisant dans l'ordre :
    1. La mémoire (Target Mode) si on a touché un bateau.
    2. Le LLM (HuggingFace) pour l'intuition.
    3. Le hasard intelligent (Damier) si le reste échoue.
    """
    row, col = None, None

# -----------------------------------------------------------
# NIVEAU 1 : MODE TARGET (Finition)
# -----------------------------------------------------------
    # On travaille sur une copie pour éviter les erreurs de modification de liste
    # On fait une copie de la liste pour ne pas bugger
    buffer_copy = targets_buffer[:] 
    
    for candidate in buffer_copy:
        r, c = candidate

        # Vérification basique des limites
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            # On vérifie si la case est valide et non jouée (0=Eau, 1=Bateau)
            if player_board[r][c] in [0, 1]: 
                row, col = r, c
                targets_buffer.remove(candidate) # On l'enlève de la liste
                print(f"IA (TARGET) : Je vise {row},{col}")
                return row, col
        else:
            # Si invalide, on le retire aussi
            if candidate in targets_buffer: targets_buffer.remove(candidate)

# -----------------------------------------------------------
# NIVEAU 2 : MODE CHASSE (Appel au LLM)
# -----------------------------------------------------------
    # Si on n'a aucune cible prioritaire, on tente l'intuition artificielle
    if row is None:
        llm_move = get_llm_coordinates()
        if llm_move:
            r, c = llm_move
            # On vérifie que le LLM ne propose pas une bêtise (case déjà jouée)
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and player_board[r][c] in [0, 1]:
                row, col = r, c
                print(f"IA (LLM) : L'Oracle suggère {row},{col}")

# -----------------------------------------------------------
# NIVEAU 3 : MODE FALLBACK (Algorithme du Damier)
# -----------------------------------------------------------
    # Si l'API échoue ou donne une case invalide, on utilise les maths.
    if row is None:
        available = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if player_board[r][c] in [0, 1]:
                    available.append((r, c))
        
        if available:
            # STRATÉGIE DU DAMIER (Checkerboard Strategy)
            # On ne vise que les cases dont la somme (r+c) est paire.
            # Mathématiquement, tout bateau >= 2 cases touche forcément une case paire.
            # Cela réduit l'espace de recherche de 50%.
            checkerboard = [p for p in available if (p[0] + p[1]) % 2 == 0]
            
            # Au début du jeu (>40 cases libres), on utilise le Damier pour optimiser.
            # À la fin, on tire sur tout ce qui bouge.
            if checkerboard and len(available) > 40: # Au début, on vise large
                row, col = random.choice(checkerboard)
            else:
                row, col = random.choice(available)
            print(f"IA (RANDOM) : Tir en {row},{col}")

    return row, col