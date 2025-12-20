import random

AI_PERSONALITIES = {
    "Gentille": {
        "style": "Tu es une IA gentille, polie et amicale.",
        "hit": [
            "Oh ! J’ai touché quelque chose… désolé ",
            "Pardon… mais j’ai réussi un tir.",
            "Minou ! Je crois que j’ai fait mouche !"
        ],
        "miss": [
            "Oups, rien du tout ici…",
            "Raté ! Tant pis… ",
            "Ah ! J’ai tiré, mais sans succès…"
        ],
    },

    "Mechante": {
        "style": "Tu es une IA arrogante, méchante et moqueuse.",
        "hit": [
            "HAHA ! Prends ça !",
            "Touché ! Tu n’es pas de taille !",
            "Encore un coup magistral de moi !"
        ],
        "miss": [
            "Tch… chanceux !",
            "Hmph, ça ne se reproduira pas.",
            "Raté, mais profite… ça ne durera pas."
        ],
    },

    "Sage": {
        "style": "Tu es une IA calme, philosophique et réfléchie.",
        "hit": [
            "Un tir précis. Le destin a parlé.",
            "La mer m’a guidé vers ta position.",
            "Une frappe juste, mais sans rancune."
        ],
        "miss": [
            "Le vent indique que ce n’était pas le bon endroit.",
            "L’erreur est la voie de la sagesse.",
            "Le silence des eaux m’indique un tir manqué."
        ],
    }
}


def get_ai_phrase(personality, event_type):
    """event_type = 'hit' ou 'miss'"""
    if personality not in AI_PERSONALITIES:
        personality = "Gentille"

    return random.choice(AI_PERSONALITIES[personality][event_type])
