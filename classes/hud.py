# classes/hud.py
# Mostra corações das vidas e mensagens de GAME OVER / reiniciar.

import pygame as pg

class HUD:
    def __init__(self, janela, jogo):
        # Recebe a janela e o objeto jogo para ler número de vidas etc.
        self.janela = janela
        self.jogo = jogo

        try:
            self.coracao_cheio = pg.image.load("imagens_pygame/cora.png").convert_alpha()
            self.coracao_vazio = pg.image.load("imagens_pygame/vazio.png").convert_alpha()
            TAMANHO = (45, 45)
            self.coracao_cheio = pg.transform.scale(self.coracao_cheio, TAMANHO)
            self.coracao_vazio = pg.transform.scale(self.coracao_vazio, TAMANHO)
        except Exception as e:
            print("❌ Erro ao carregar ícones de coração:", e)
            self.coracao_cheio = None
            self.coracao_vazio = None

        self.fonte_gameover = pg.font.Font(None, 84)
        self.fonte_instrucao = pg.font.Font(None, 36)
        self.cor_gameover = (255, 50, 50)
        self.cor_instrucao = (255, 255, 255)
        self.sombra = (0, 0, 0)

    def desenhar_vidas(self):
        # desenha 3 corações (cheios/vazios) no topo esquerdo
        if not self.coracao_cheio or not self.coracao_vazio:
            return
        x_inicial = 25
        y = 20
        for i in range(3):
            x = x_inicial + i * 55
            if i < self.jogo.vidas:
                self.janela.blit(self.coracao_cheio, (x, y))
            else:
                self.janela.blit(self.coracao_vazio, (x, y))

    def desenhar_gameover(self):
        texto = "GAME OVER"
        surf = self.fonte_gameover.render(texto, True, self.cor_gameover)
        rect = surf.get_rect(center=(self.janela.get_width() // 2, self.janela.get_height() // 2 - 40))
        sombra_surf = self.fonte_gameover.render(texto, True, self.sombra)
        sombra_rect = sombra_surf.get_rect(center=(rect.centerx + 3, rect.centery + 3))
        self.janela.blit(sombra_surf, sombra_rect)
        self.janela.blit(surf, rect)

    def desenhar_reiniciar_instrucao(self):
        texto = "Pressione R para reiniciar"
        surf = self.fonte_instrucao.render(texto, True, self.cor_instrucao)
        rect = surf.get_rect(center=(self.janela.get_width() // 2, self.janela.get_height() // 2 + 40))
        sombra_surf = self.fonte_instrucao.render(texto, True, self.sombra)
        sombra_rect = sombra_surf.get_rect(center=(rect.centerx + 2, rect.centery + 2))
        self.janela.blit(sombra_surf, sombra_rect)
        self.janela.blit(surf, rect)
