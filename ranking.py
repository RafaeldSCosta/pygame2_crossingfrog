# ranking.py
# Implementa um ranking simples (arquivo JSON) para salvar pontuação.
# É opcional — o jogo atual não usa pontuação, mas você pode integrar facilmente.

import json
import os
from assets import get_asset_path

RANKING_FILE = get_asset_path("ranking.json")

def carregar_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    try:
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar_ranking(ranking):
    try:
        with open(RANKING_FILE, "w", encoding="utf-8") as f:
            json.dump(ranking, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Erro ao salvar ranking:", e)

def adicionar_score(nome, pontuacao):
    ranking = carregar_ranking()
    ranking.append({"nome": nome, "score": pontuacao})
    # ordenar do maior para o menor
    ranking.sort(key=lambda x: x["score"], reverse=True)
    salvar_ranking(ranking)
