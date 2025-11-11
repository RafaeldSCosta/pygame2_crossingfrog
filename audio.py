# audio.py
# Gerenciador de sons. Por enquanto é minimalista: carrega e toca efeitos.
# Use caminhos em 'imagens_pygame' ou crie pasta 'sons/' e ajuste os nomes.

import pygame
from assets import get_asset_path

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sons = {}

    def carregar(self, nome, caminho_relativo):
        """Carrega um som e guarda com a chave 'nome'."""
        try:
            caminho = get_asset_path(caminho_relativo)
            self.sons[nome] = pygame.mixer.Sound(caminho)
        except Exception as e:
            print(f"⚠️ Erro ao carregar som {caminho_relativo}: {e}")

    def tocar(self, nome):
        if nome in self.sons:
            self.sons[nome].play()
