# run.py
# Arquivo principal: inicializa o jogo e roda o loop principal.
# Rode este arquivo para iniciar o jogo: python run.py

import pygame
import sys

from settings import SCREENWIDTH, SCREENHEIGHT, FPS
from screens.gsm import GameStateManager
from screens.start import StartScreen
from screens.level import LevelScreen
from screens.end import EndScreen
from classes.game import CruzamentoFazenda
from classes.hud import HUD
from assets import get_asset_path

def mostrar_tela_imagem(screen, imagem_path, duracao_ms=2000):
    """Mostra uma imagem em tela cheia por 'duracao_ms' milissegundos."""
    img = pygame.image.load(get_asset_path(imagem_path)).convert()
    img = pygame.transform.scale(img, (SCREENWIDTH, SCREENHEIGHT))
    screen.blit(img, (0, 0))
    pygame.display.update()
    pygame.time.delay(duracao_ms)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Running Fox Game")
    clock = pygame.time.Clock()

    # Gerenciador de estados e telas
    gsm = GameStateManager('start')
    start_screen = StartScreen(screen, gsm)
    level_screen = LevelScreen(screen, gsm)
    end_screen = EndScreen(screen, gsm)

    # objeto do jogo (lógica)
    jogo = CruzamentoFazenda()
    hud = HUD(jogo.janela, jogo)

    STATE = "menu"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Encaminha eventos para a tela atual (menu, jogo ou end)
            current_state = gsm.get_state()
            if current_state == 'start':
                start_screen.handle_event(event)
                if gsm.get_state() == 'level':
                    # mostra instruções e tela de level 1 antes de entrar no jogo
                    mostrar_tela_imagem(screen, "imagens_pygame/instru.png", duracao_ms=10000)
                    mostrar_tela_imagem(screen, "imagens_pygame/level_1.png", duracao_ms=2000)
                    STATE = "jogo"
            elif current_state == 'level':
                level_screen.handle_event(event)
            elif current_state == 'end':
                end_screen.handle_event(event)
                if gsm.get_state() == 'start':
                    # recria o jogo para reiniciar
                    jogo = CruzamentoFazenda()
                    hud = HUD(jogo.janela, jogo)
                    STATE = "menu"

            # no estado jogo, capturar teclas para movimentar raposa
            if STATE == "jogo" and event.type == pygame.KEYDOWN:
                tecla = pygame.key.name(event.key)
                jogo.mover_raposa(tecla)
                if tecla == "escape":
                    gsm.set_state('end')

        # Atualização e desenho dependendo do estado
        if gsm.get_state() == 'start':
            start_screen.run()
        elif gsm.get_state() == 'level' or STATE == "menu":
            level_screen.run()
        elif gsm.get_state() == 'level' and STATE == "jogo":
            pass  # proteção, mas o fluxo principal usa STATE "jogo"
        elif STATE == "jogo":
            jogo.relogio.tick(FPS)
            jogo.atualizar_plataformas()
            jogo.checar_colisoes_e_reagir()
            jogo.limpar_janela()
            jogo.desenhar_plataformas()
            jogo.desenhar_raposa()
            hud.desenhar_vidas()
            pygame.display.update()

            if jogo.vidas <= 0 or jogo.game_over:
                gsm.set_state('end')

            # Mostra level 2 apenas uma vez
            if jogo.fase == 2 and not hasattr(jogo, "level2_shown"):
                mostrar_tela_imagem(screen, "imagens_pygame/level_2.png", duracao_ms=2000)
                jogo.level2_shown = True

        elif gsm.get_state() == 'end':
            end_screen.run()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
