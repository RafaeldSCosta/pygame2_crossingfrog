# assets.py
# Função utilitária para resolver caminhos de arquivos relativos à pasta deste projeto.
# Facilita mover o projeto sem quebrar paths.

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(relative_path):
    """Retorna o caminho completo para um ativo (imagem, som, etc.)."""
    return os.path.join(BASE_DIR, relative_path)
