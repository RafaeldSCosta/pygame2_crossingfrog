# screens/start.py
# Tela inicial com logo, nuvens animadas e botão START.
# Input: clique no botão ou tecla ESPAÇO inicia o jogo.

import pygame
import random
import math
from .base import BaseScreen
from assets import get_asset_path
from settings import SCREENWIDTH, SCREENHEIGHT

class StartScreen(BaseScreen):
    def __init__(self, display, gsm):
        super().__init__(display, gsm, "imagens_pygame/tela1.png")

        # botão START (imagem)
        button_image_path = get_asset_path("imagens_pygame/botao_start.png")
        self.start_button_image = pygame.image.load(button_image_path).convert_alpha()
        target_width = 200
        original_width, original_height = self.start_button_image.get_size()
        new_height = int(original_height * (target_width / original_width))
        self.start_button_image = pygame.transform.scale(self.start_button_image, (target_width, new_height))
        self.start_button_hover_image = self.start_button_image.copy()
        self.start_button_hover_image.fill((50, 50, 50, 0), special_flags=pygame.BLEND_RGB_SUB)
        self.start_button_rect = None

        # nuvens animadas (apenas efeito visual)
        self.nuvens = []
        for i in range(1, 5):
            img = pygame.image.load(get_asset_path(f"imagens_pygame/nuvem{i}.png")).convert_alpha()
            escala = pygame.transform.scale(img, (int(img.get_width() * 1.0), int(img.get_height() * 1.0)))
            x = i * 250
            base_y = random.randint(40, 180) + (i * 5)
            vel = 1.2 + (i * 0.3)
            phase = random.uniform(0, math.pi * 2)
            self.nuvens.append({"img": escala, "x": x, "base_y": base_y, "vel": vel, "phase": phase})

        # logo do jogo
        logo_path = get_asset_path("imagens_pygame/titulo.png")
        self.logo_img = pygame.image.load(logo_path).convert_alpha()
        self.logo_img = pygame.transform.smoothscale(self.logo_img, (int(SCREENWIDTH * 0.65), int(SCREENHEIGHT * 0.25)))
        self.logo_rect = self.logo_img.get_rect(center=(SCREENWIDTH // 2, 150))

    def handle_event(self, event):
        # clique do mouse no botão inicia (seta o estado 'level' que o run.py usa)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                self.gsm.set_state('level')
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.gsm.set_state('level')

    def mover_nuvens(self):
        t = pygame.time.get_ticks() / 1000.0
        for nuvem in self.nuvens:
            nuvem["x"] += nuvem["vel"]
            if nuvem["x"] > SCREENWIDTH + 200:
                nuvem["x"] = -200
            bob = math.sin(t * 1.5 + nuvem["phase"]) * 6
            y = nuvem["base_y"] + bob
            self.display.blit(nuvem["img"], (nuvem["x"], y))

    def desenhar_logo(self):
        self.display.blit(self.logo_img, self.logo_rect)

    def run(self):
        # desenha fundo, nuvens e botão
        self.display.blit(self.bg, (0, 0))
        self.mover_nuvens()
        self.desenhar_logo()

        button_y_pos = (SCREENHEIGHT // 2) + 285
        mouse_pos = pygame.mouse.get_pos()
        current_button_image = self.start_button_image
        self.start_button_rect = current_button_image.get_rect(center=(SCREENWIDTH // 2, button_y_pos))

        if self.start_button_rect.collidepoint(mouse_pos):
            current_button_image = self.start_button_hover_image

        self.display.blit(current_button_image, self.start_button_rect)
