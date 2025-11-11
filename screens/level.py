# screens/level.py
# Tela de level: apenas mostra o fundo e instrução.
# Pressione [E] para encerrar/voltar ao menu de start.

import pygame
from .base import BaseScreen
from settings import SCREENHEIGHT

class LevelScreen(BaseScreen):
    def __init__(self, display, gsm):
        super().__init__(display, gsm, "imagens_pygame/level_1.png")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.gsm.set_state('end')

    def run(self):
        self.display.blit(self.bg, (0, 0))
        self.draw_centered("LEVEL - Pressione [E] para encerrar", self.font_text, SCREENHEIGHT - 100)
