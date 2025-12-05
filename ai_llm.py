import requests
import json

# Mets ton token HuggingFace ici
HF_API_KEY = "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"

# Modèle texte simple et gratuit (peut être changé)
MODEL = "gpt2"


def get_ai_move(player_grid):
    """
    Envoie la grille du joueur au modèle HF et récupère
    une proposition de tir sous la forme (row, col).
    Si la réponse est invalide => un tir aléatoire sera choisi dans game.py.
    """

    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    # On transforme la grille en texte pour l’IA
    grid_str = "\n".join(" ".join(str(c) for c in row) for row in player_grid)

    prompt = (
        "Voici la grille du joueur dans une bataille navale (0=vide, 1=bateau, -1=touché, -2=manqué).\n"
        "Donne uniquement des coordonnées de tir probables sous la forme: row,col\n\n"
        f"{grid_str}\n"
        "Réponse :"
    )

    try:
        response = requests.post(url,
                                 headers=headers,
                                 json={"inputs": prompt, "parameters": {"max_new_tokens": 10}})

        data = response.json()

        # Selon les modèles HF, la réponse peut être sous plusieurs formes
        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            text = data[0]["generated_text"]
        elif "generated_text" in data:
            text = data["generated_text"]
        else:
            return (-1, -1)  # erreur => tir aléatoire

        # Extraction des coordonnées
        import re
        match = re.search(r"(\d+)\s*,\s*(\d+)", text)
        if match:
            r = int(match.group(1))
            c = int(match.group(2))
            return (r, c)

    except Exception:
        return (-1, -1)

    return (-1, -1)
