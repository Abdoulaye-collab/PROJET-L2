import requests
import re

HF_API_KEY = "hf_xxxxxxxxxxxxx"  # Mets ici ton token HuggingFace
MODEL = "gpt2"

def get_ai_move(player_grid, personality_style=""):
    """
    Envoie la grille + personnalité au modèle HF et reçoit une proposition de tir (row, col)
    Retourne (-1, -1) si problème (tir aléatoire sera utilisé dans game.py)
    """

    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    grid_str = "\n".join(" ".join(str(c) for c in row) for row in player_grid)

    prompt = (
        f"{personality_style}\n"
        "Tu joues à la bataille navale.\n"
        "Voici la grille du joueur :\n"
        "(0=vide, 1=bateau, -1=touché, -2=manqué)\n\n"
        f"{grid_str}\n\n"
        "Donne uniquement des coordonnées (row,col)."
    )

    try:
        response = requests.post(url,
                                 headers=headers,
                                 json={"inputs": prompt, "parameters": {"max_new_tokens": 10}})
        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            text = data[0]["generated_text"]
        else:
            return (-1, -1)

        match = re.search(r"(\d+)\s*,\s*(\d+)", text)
        if match:
            return int(match.group(1)), int(match.group(2))

    except Exception:
        return (-1, -1)

    return (-1, -1)
