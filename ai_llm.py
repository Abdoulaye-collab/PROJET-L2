import requests
import re
import random

HF_API_KEY = "hf_xxxxxxxxxxxxx"  # Mets ici ton token HuggingFace
MODEL = "gpt2"

def query_huggingface(payload):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    try:
        # Timeout court (2s) pour ne pas bloquer le jeu si internet est lent
        response = requests.post(MODEL, headers=headers, json=payload, timeout=2)
        return response.json()
    except:
        return None

def get_llm_coordinates():
    """
    Mode HUNT : Demande au LLM de choisir une case.
    """
    prompt = "Battleship move strategy. Best coordinates: 5,5 - 2,3 - 9,0 - "
    
    data = query_huggingface({
        "inputs": prompt,
        "parameters": {"max_new_tokens": 5, "temperature": 0.7}
    })

    if data and isinstance(data, list) and 'generated_text' in data[0]:
        text = data[0]['generated_text']
        # On nettoie pour trouver "chiffre,chiffre"
        new_text = text.replace(prompt, "")
        match = re.search(r"(\d)\s*,\s*(\d)", new_text)
        if match:
            return int(match.group(1)), int(match.group(2))

    return None
