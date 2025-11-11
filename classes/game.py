# classes/game.py
# Contém a classe CruzamentoFazenda (a maior parte do código original).
# Mantive a lógica original mas com comentários claros e pequenos ajustes.

import pygame as pg
from sys import exit

class CruzamentoFazenda:
    def __init__(self):
        # inicialização do pygame e janela própria
        pg.init()
        self.janela = pg.display.set_mode((950, 880))
        pg.display.set_caption("Cruzamento da Fazenda")
        self.relogio = pg.time.Clock()
        self.v_dif = 0  # dificuldade de velocidade adicional

        try:
            # --- Fundo inicial ---
            self.fundo_imagem = pg.image.load("imagens_pygame/fundo_fazenda.png").convert()
            self.fundo_imagem = pg.transform.scale(self.fundo_imagem, (950, 880))

            # --- Sprites da raposa (4 direções) ---
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

            # --- JACARÉS para fase 1 (animação: jac1..jac9) ---
            TAMANHO_JACARE = (70, 50)
            self.jacare_frames = [
                pg.transform.scale(pg.image.load(f"imagens_pygame/jac{i}.png").convert_alpha(), TAMANHO_JACARE)
                for i in range(1, 10)
            ]
            print("✅ Jacarés carregados com sucesso!")

            # --- RATAZANAS (fase 2) ---
            TAMANHO_RATAZANA = (100, 50)
            self.ratazana_frames = []
            for i in range(1, 5):
                caminho = f"imagens_pygame/rat{i}.png"
                try:
                    img = pg.image.load(caminho).convert_alpha()
                    img = pg.transform.scale(img, TAMANHO_RATAZANA)
                    self.ratazana_frames.append(img)
                    print(f"✅ Carregada {caminho}")
                except Exception as e:
                    print(f"❌ Erro ao carregar {caminho}: {e}")

            # --- FENOS (fase 1) ---
            TAMANHO_FENO = (60, 60)
            self.feno_frames = [
                pg.transform.scale(pg.image.load(f"imagens_pygame/feno{i}.png").convert_alpha(), TAMANHO_FENO)
                for i in range(1, 10)
            ]
            print("✅ Fenos carregados com sucesso!")

            # --- ESCORPIÕES (fase 2) ---
            TAMANHO_ESC = (70, 50)
            self.esc_frames = [
                pg.transform.scale(pg.image.load(f"imagens_pygame/esc{i}.png").convert_alpha(), TAMANHO_ESC)
                for i in range(1, 5)
            ]
            print("✅ Escorpiões carregados com sucesso!")

            # --- COBRAS (ambas fases) ---
            TAMANHO_COBRA = (160, 50)
            self.cobra_frames = []
            for i in range(1, 9):
                if i == 4:
                    continue
                caminho = f"imagens_pygame/cob{i}.png"
                try:
                    img = pg.transform.scale(pg.image.load(caminho).convert_alpha(), TAMANHO_COBRA)
                    self.cobra_frames.append(img)
                except:
                    print(f"⚠️ Não encontrei {caminho}, pulando...")
            print("✅ Cobras carregadas com sucesso!")

            self.indice_animacao = 0
            self.tempo_animacao = 0.0
            self.vel_animacao = 0.20

        except Exception as e:
            print("❌ ERRO ao carregar imagens:", e)
            pg.quit()
            exit()

        # --- parâmetros gerais ---
        self.pos_raposa = [370, 760]
        self.velocidade = 30
        self.fase = 1

        # --- Plataformas iniciais (Fase 1) ---
        self.linhas_das_plataformas = [
            [60, 420, 660],        # fenos (cima)
            [50, 650],             # cobras (cima)
            [50, 250, 450, 800],   # jacarés (meio)
            [120, 360, 720],       # fenos (baixo)
            [0, 700],              # cobras (baixo)
            [100, 250, 700, 800],  # jacarés (fundo)
        ]

        # tamanhos usados para detectar colisões
        self.tamanho_raposa = self.sprite_frente.get_rect().size
        self.tamanho_jacare = (70, 50)
        self.tamanho_ratazana = (100, 50)
        self.tamanho_feno = (60, 60)
        self.tamanho_cobra = (160, 50)
        self.tamanho_esc = (70, 50)
        self.ajuste_y_raposa = -35
        self.vidas = 3
        self.game_over = False

        # áreas especiais do mapa
        self.area_fazenda = pg.Rect(120, 50, 100, 100)
        self.area_ovos = pg.Rect(0, 0, 1, 1)
        # posições Y de acordo com a fase
        self.y_posicoes_fase1 = [195, 295, 395, 495, 595, 695]
        self.y_posicoes_fase2 = [330, 470, 610]

    # limpa a tela desenhando o fundo
    def limpar_janela(self):
        self.janela.blit(self.fundo_imagem, (0, 0))

    # desenha plataformas (jacarés, fenos, cobras, etc.)
    def desenhar_plataformas(self):
        y_posicoes = self.y_posicoes_fase1 if self.fase == 1 else self.y_posicoes_fase2
        self.tempo_animacao += self.vel_animacao
        if self.tempo_animacao >= 1:
            self.indice_animacao = (self.indice_animacao + 1) % max(1, len(self.cobra_frames))
            self.tempo_animacao = 0

        for linha, xs in enumerate(self.linhas_das_plataformas):
            if linha >= len(y_posicoes):
                break
            y = y_posicoes[linha]
            for x in xs:
                # lógica de escolha da imagem dependendo da fase e da linha
                if (self.fase == 1 and linha in (2, 5)):
                    img = self.jacare_frames[self.indice_animacao % len(self.jacare_frames)]
                    rect = img.get_rect(center=(x + self.tamanho_jacare[0] // 2, y))
                    self.janela.blit(img, rect)
                elif (self.fase == 2 and linha == 0):
                    if self.ratazana_frames:
                        img = self.ratazana_frames[self.indice_animacao % len(self.ratazana_frames)]
                        rect = img.get_rect(center=(x + self.tamanho_ratazana[0] // 2, y))
                        self.janela.blit(img, rect)
                elif (self.fase == 1 and linha in (0, 3)):
                    img = self.feno_frames[self.indice_animacao % len(self.feno_frames)]
                    rect = img.get_rect(center=(x + self.tamanho_feno[0] // 2, y))
                    self.janela.blit(img, rect)
                elif (self.fase == 2 and linha == 1):
                    img = self.esc_frames[self.indice_animacao % len(self.esc_frames)]
                    rect = img.get_rect(center=(x + self.tamanho_esc[0] // 2, y))
                    self.janela.blit(img, rect)
                elif (self.fase == 1 and linha in (1, 4)) or (self.fase == 2 and linha == 2):
                    img = self.cobra_frames[self.indice_animacao % len(self.cobra_frames)]
                    rect = img.get_rect(center=(x + self.tamanho_cobra[0] // 2, y))
                    self.janela.blit(img, rect)

    # atualiza posição das plataformas (faz os inimigos/pilhas se moverem)
    def atualizar_plataformas(self):
        for y in range(len(self.linhas_das_plataformas)):
            for i in range(len(self.linhas_das_plataformas[y])):
                if y in (2, 5):  # jacarés / ratazanas
                    self.linhas_das_plataformas[y][i] += 1 + self.v_dif
                    if self.linhas_das_plataformas[y][i] > 880:
                        self.linhas_das_plataformas[y][i] = -100
                elif y in (0, 3):  # fenos / escorpiões
                    self.linhas_das_plataformas[y][i] -= 2 + self.v_dif
                    if self.linhas_das_plataformas[y][i] < -120:
                        self.linhas_das_plataformas[y][i] = 880
                elif y in (1, 4):  # cobras
                    self.linhas_das_plataformas[y][i] += 1.5 + self.v_dif
                    if self.linhas_das_plataformas[y][i] > 950:
                        self.linhas_das_plataformas[y][i] = -300

    # verifica colisão da raposa com qualquer plataforma perigosa
    def raposa_colidiu_com_objeto(self):
        raposa_rect = pg.Rect(int(self.pos_raposa[0]), int(self.pos_raposa[1] + self.ajuste_y_raposa),
                              int(self.tamanho_raposa[0]), int(self.tamanho_raposa[1]))
        y_posicoes = self.y_posicoes_fase1 if self.fase == 1 else self.y_posicoes_fase2
        for linha, xs in enumerate(self.linhas_das_plataformas):
            if linha >= len(y_posicoes): break
            y_plat = y_posicoes[linha]
            for x in xs:
                if (self.fase == 1 and linha in (2, 5)):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.tamanho_jacare[1] // 2),
                                        *self.tamanho_jacare)
                elif (self.fase == 2 and linha == 0):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.tamanho_ratazana[1] // 2),
                                        *self.tamanho_ratazana)
                elif (self.fase == 1 and linha in (0, 3)) or (self.fase == 2 and linha == 1):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.tamanho_feno[1] // 2),
                                        *self.tamanho_feno)
                elif (self.fase == 1 and linha in (1, 4)) or (self.fase == 2 and linha == 2):
                    plat_rect = pg.Rect(int(x), int(y_plat - self.tamanho_cobra[1] // 2),
                                        *self.tamanho_cobra)
                else:
                    continue
                if raposa_rect.colliderect(plat_rect):
                    return True
        return False

    # reseta a raposa no início ou após colisão
    def resetar_posicao_raposa(self, colisao=False):
        if colisao:
            self.vidas -= 1
            if self.vidas < 0:
                self.vidas = 0
            print(f"💥 Colidiu! Vidas restantes: {self.vidas}")
            if self.vidas == 0:
                self.game_over = True
        self.pos_raposa = [370, 760]
        self.sprite_raposa_atual = self.sprite_frente

    # avança para a próxima fase (muda layout e velocidade)
    def proxima_fase(self):
        self.fase += 1
        print(f"🌾 Indo para a fase {self.fase}!")
        if self.fase == 2:
            self.area_ovos = pg.Rect(475, 100, 150, 150)
            self.v_dif = 1.8
            try:
                self.area_fazenda = pg.Rect(0, 0, 1, 1)
                self.fundo_imagem = pg.image.load("imagens_pygame/fundo_fazenda_2.png").convert()
                self.fundo_imagem = pg.transform.scale(self.fundo_imagem, (950, 880))
                print("🐔 Entrou na fazenda — Fase 2 iniciada!")
            except:
                print("⚠️ Fundo da Fase 2 não encontrado!")

            self.linhas_das_plataformas = [
                [50, 250, 450, 800],   # Ratazanas
                [120, 360, 720],       # Escorpiões
                [120, 360, 720],       # Cobras
            ]
            print("⚙️ Fase 2: Ratazanas, Escorpiões e Cobras.")
            self.vel_animacao = 0.15

        elif self.fase == 3:
            print("🚜 Fase 3 iniciada! (ainda sem cenário)")
            self.vel_animacao = 0.3
        else:
            print("🎉 Você zerou o jogo!")
            self.game_over = True
        self.pos_raposa = [370, 760]

    # desenha a raposa na tela
    def desenhar_raposa(self):
        self.janela.blit(self.sprite_raposa_atual,
                         (self.pos_raposa[0], self.pos_raposa[1] + self.ajuste_y_raposa))

    # controla movimento da raposa (muda sprite e posição)
    def mover_raposa(self, tecla):
        if self.game_over:
            return
        if tecla == "up":
            self.sprite_raposa_atual = self.sprite_costas
            self.pos_raposa[1] -= self.velocidade
        elif tecla == "down":
            self.sprite_raposa_atual = self.sprite_frente
            self.pos_raposa[1] += self.velocidade
        elif tecla == "left":
            self.sprite_raposa_atual = self.sprite_esquerda
            self.pos_raposa[0] -= self.velocidade
        elif tecla == "right":
            self.sprite_raposa_atual = self.sprite_direita
            self.pos_raposa[0] += self.velocidade
        elif tecla == "r":
            self.__init__()  # reiniciar o jogo re-inicializando a classe

        raposa_rect = pg.Rect(
            int(self.pos_raposa[0]),
            int(self.pos_raposa[1] + self.ajuste_y_raposa),
            int(self.tamanho_raposa[0]),
            int(self.tamanho_raposa[1])
        )
        # checa se chegou na fazenda (passa de fase)
        if raposa_rect.colliderect(self.area_fazenda):
            print("🐾 A raposa chegou na fazenda!")
            self.proxima_fase()

        if raposa_rect.colliderect(self.area_ovos):
            print("🐾 A raposa chegou nos ovos!")

    # checa colisões e reage (perde vida e reseta)
    def checar_colisoes_e_reagir(self):
        if self.game_over:
            return
        if self.raposa_colidiu_com_objeto():
            self.resetar_posicao_raposa(colisao=True)
