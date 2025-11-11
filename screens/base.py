# screens/base.py
# Contém BaseScreen com utilitários compartilhados por todas as telas.

import pygame
from assets import get_asset_path
from settings import SCREENWIDTH, SCREENHEIGHT

class BaseScreen:
    def __init__(self, display, gsm, bg_path):
        self.display = display
        self.gsm = gsm
        full_bg_path = get_asset_path(bg_path)
        self.bg = pygame.image.load(full_bg_path).convert()
        self.bg = pygame.transform.scale(self.bg, (SCREENWIDTH, SCREENHEIGHT))
        self.font_title = pygame.font.SysFont(None, 72)
        self.font_text = pygame.font.SysFont(None, 36)

    def draw_centered(self, text, font, y):
        surface = font.render(text, True, (255, 255, 255))
        rect = surface.get_rect(center=(SCREENWIDTH // 2, y))
        self.display.blit(surface, rect)
        return rect
