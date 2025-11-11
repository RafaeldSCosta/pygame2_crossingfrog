# screens/end.py
# Tela final com instruções para reiniciar ou sair.
# [R] reinicia (volta para start) e [Q] fecha o jogo.

import pygame
import sys
from .base import BaseScreen
from settings import SCREENWIDTH, SCREENHEIGHT

class EndScreen(BaseScreen):
    def __init__(self, display, gsm):
        super().__init__(display, gsm, "imagens_pygame/game_over.png")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.gsm.set_state('start')
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    def run(self):
        self.display.blit(self.bg, (0, 0))
        self.draw_centered("Pressione [R] para reiniciar ou [Q] para sair", self.font_text, SCREENHEIGHT // 2)
