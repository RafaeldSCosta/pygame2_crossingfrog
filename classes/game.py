import pygame as pg
from sys import exit

class CruzamentoFazenda:
    def __init__(self):
        pg.init()
        self.janela = pg.display.set_mode((800, 835))
        pg.display.set_caption("Cruzamento da Fazenda")
        self.relogio = pg.time.Clock()

        try:
            # --- Fundo e sprites ---
            self.fundo_imagem = pg.image.load("imagens_pygame/fundo_fazenda.png").convert()
            self.fundo_imagem = pg.transform.scale(self.fundo_imagem, (800, 835))

            TAMANHO_RAPOSA = (50, 50)

            img_frente = pg.image.load("imagens_pygame/frente.png").convert_alpha()
            self.sprite_frente = pg.transform.scale(img_frente, TAMANHO_RAPOSA)

            img_costas = pg.image.load("imagens_pygame/costas.png").convert_alpha()
            self.sprite_costas = pg.transform.scale(img_costas, TAMANHO_RAPOSA)

            img_esquerda = pg.image.load("imagens_pygame/LADO_E.png").convert_alpha()
            self.sprite_esquerda = pg.transform.scale(img_esquerda, TAMANHO_RAPOSA)

            img_direita = pg.image.load("imagens_pygame/LADO_D.png").convert_alpha()
            self.sprite_direita = pg.transform.scale(img_direita, TAMANHO_RAPOSA)

            self.sprite_raposa_atual = self.sprite_frente

            # --- Ovelhas / jacarés ---
            TAMANHO_OVELHA = (60, 60)
            self.ovelhas_frames = [
                pg.transform.scale(pg.image.load("imagens_pygame/ov.frame1.png").convert_alpha(), TAMANHO_OVELHA),
                pg.transform.scale(pg.image.load("imagens_pygame/ov.frame2.png").convert_alpha(), TAMANHO_OVELHA),
                pg.transform.scale(pg.image.load("imagens_pygame/ov.frame3.png").convert_alpha(), TAMANHO_OVELHA),
                pg.transform.scale(pg.image.load("imagens_pygame/ov.frame4.png").convert_alpha(), TAMANHO_OVELHA),
            ]

            self.indice_ovelha = 0
            self.tempo_animacao = 0.0
            self.vel_animacao = 0.15

        except Exception as e:
            print(" ERRO ao carregar imagens:", e)
            pg.quit()
            exit()

        # --- Posições e parâmetros ---
        self.pos_raposa = [370, 760]
        self.velocidade = 15

        self.linhas_das_plataformas = [
            [0, 150, 250, 600],
            [60, 180, 420, 660],
            [50, 650],
            [50, 250, 450, 800],
            [120, 360, 720],
            [0, 700],
            [100, 250, 450, 700, 800],
        ]

        self.cor_fundo = (100, 150, 255)
        self.cor_tronco = (139, 69, 19)
        self.cor_tartaruga = (160, 100, 50)
        self.cor_planta = (34, 139, 34)

        self.tamanho_raposa = self.sprite_frente.get_rect().size
        self.tamanho_tronco = (150, 30)
        self.tamanho_tartaruga = (80, 40)
        self.tamanho_planta = (40, 40)

        self.vidas = 3
        self.ajuste_y_raposa = -35
        self.game_over = False

    # -------------------------------------------------------------
    def limpar_janela(self):
        self.janela.blit(self.fundo_imagem, (0, 0))

    # -------------------------------------------------------------
    def desenhar_plataformas(self):
        y_posicoes = [95, 195, 295, 395, 495, 595, 695]

        self.tempo_animacao += self.vel_animacao
        if self.tempo_animacao >= 1:
            self.indice_ovelha = (self.indice_ovelha + 1) % len(self.ovelhas_frames)
            self.tempo_animacao = 0

        for linha, xs in enumerate(self.linhas_das_plataformas):
            y = y_posicoes[linha]
            for x in xs:
                if linha in (0, 3, 6):
                    ovelha = self.ovelhas_frames[self.indice_ovelha]
                    rect = ovelha.get_rect(center=(x + self.tamanho_planta[0] // 2, y))
                    self.janela.blit(ovelha, rect)
                elif linha in (1, 4):
                    rect = pg.Rect(x, y - self.tamanho_tartaruga[1] // 2,
                                   self.tamanho_tartaruga[0], self.tamanho_tartaruga[1])
                    pg.draw.ellipse(self.janela, self.cor_tartaruga, rect)
                elif linha in (2, 5):
                    rect = pg.Rect(x, y - self.tamanho_tronco[1] // 2,
                                   self.tamanho_tronco[0], self.tamanho_tronco[1])
                    pg.draw.rect(self.janela, self.cor_tronco, rect)

    # -------------------------------------------------------------
    def atualizar_plataformas(self):
        for y in range(len(self.linhas_das_plataformas)):
            for i in range(len(self.linhas_das_plataformas[y])):
                if y in (0, 3, 6):
                    self.linhas_das_plataformas[y][i] += 1
                    if self.linhas_das_plataformas[y][i] > 800:
                        self.linhas_das_plataformas[y][i] = -100
                elif y in (1, 4):
                    self.linhas_das_plataformas[y][i] -= 1
                    if self.linhas_das_plataformas[y][i] < -120:
                        self.linhas_das_plataformas[y][i] = 800
                elif y in (2, 5):
                    self.linhas_das_plataformas[y][i] += 2
                    if self.linhas_das_plataformas[y][i] > 800:
                        self.linhas_das_plataformas[y][i] = -300

    # -------------------------------------------------------------
    def raposa_colidiu_com_objeto(self):
        raposa_rect = pg.Rect(
            int(self.pos_raposa[0]),
            int(self.pos_raposa[1] + self.ajuste_y_raposa),
            int(self.tamanho_raposa[0]),
            int(self.tamanho_raposa[1])
        )

        y_posicoes = [95, 195, 295, 395, 495, 595, 695]

        for linha, xs in enumerate(self.linhas_das_plataformas):
            y_plat = y_posicoes[linha]
            for x in xs:
                if linha in (0, 3, 6):
                    largura = self.tamanho_planta[0]
                    plat_rect = pg.Rect(int(x), int(y_plat - largura // 2), int(largura), int(largura))
                elif linha in (1, 4):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.tamanho_tartaruga[1] // 2),
                                        int(self.tamanho_tartaruga[0]), int(self.tamanho_tartaruga[1]))
                else:
                    plat_rect = pg.Rect(int(x), int(y_plat - self.tamanho_tronco[1] // 2),
                                        int(self.tamanho_tronco[0]), int(self.tamanho_tronco[1]))

                if raposa_rect.colliderect(plat_rect):
                    return True
        return False

    # -------------------------------------------------------------
    def resetar_posicao_raposa(self, colisao=False):
        if colisao:
            self.vidas -= 1
            if self.vidas < 0:
                self.vidas = 0
            print(f"Colidiu! Vidas restantes: {self.vidas}")
            if self.vidas == 0:
                self.game_over = True

        self.pos_raposa = [370, 760]
        self.sprite_raposa_atual = self.sprite_frente

    # -------------------------------------------------------------
    def desenhar_raposa(self):
        self.janela.blit(self.sprite_raposa_atual,
                         (self.pos_raposa[0], self.pos_raposa[1] + self.ajuste_y_raposa))

    # -------------------------------------------------------------
    def mover_raposa(self, tecla):
        if self.game_over:
            return
        if tecla == "up":
            self.sprite_raposa_atual = self.sprite_frente
            self.pos_raposa[1] -= self.velocidade
        elif tecla == "down":
            self.sprite_raposa_atual = self.sprite_costas
            self.pos_raposa[1] += self.velocidade
        elif tecla == "left":
            self.sprite_raposa_atual = self.sprite_esquerda
            self.pos_raposa[0] -= self.velocidade
        elif tecla == "right":
            self.sprite_raposa_atual = self.sprite_direita
            self.pos_raposa[0] += self.velocidade
        elif tecla == "r":
            self.__init__()

    # -------------------------------------------------------------
    def checar_colisoes_e_reagir(self):
        if self.game_over:
            return
        if self.raposa_colidiu_com_objeto():
            self.resetar_posicao_raposa(colisao=True)
