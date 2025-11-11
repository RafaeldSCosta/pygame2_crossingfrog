# Running Fox — Estrutura do Projeto (explicação simples)

## Como rodar
1. Tenha Python e pygame instalados.
2. Execute: `python run.py`

## O que cada arquivo faz (explicado para não programadores)
- `run.py`: arquivo principal. É o que você executa para abrir o jogo.
- `settings.py`: valores que você pode mudar facilmente (tamanho da janela, FPS).
- `assets.py`: ajuda a encontrar imagens/sons no computador.
- `audio.py`: onde ficarão os sons (é um gerenciador simples).
- `ranking.py`: salva e carrega placares em um arquivo chamado `ranking.json`.
- `classes/game.py`: contém toda a "lógica" do jogo (inimigos, fases, movimentação).
- `classes/hud.py`: mostra o número de vidas na tela e mensagens.
- `screens/`: pasta com as telas do jogo:
  - `start.py`: tela inicial (botão iniciar).
  - `level.py`: tela de nível / instrução.
  - `end.py`: tela de game over.
  - `gsm.py`: gerenciador de estados (controla qual tela está ativa).
- `imagens_pygame/`: coloque aqui suas imagens (já usadas no código).
- `ranking.json`: arquivo gerado com o ranking (se você usar).

## Dicas para uma pessoa não técnica
- Se faltar uma imagem, o jogo imprime mensagens no terminal identificando o arquivo ausente.
- Para trocar o fundo, substitua a imagem em `imagens_pygame/fundo_fazenda.png`.
- Para ajustar velocidade, abra `classes/game.py` e altere `self.velocidade`.

Se quiser, eu já adapto o código para:
- Carregar sons e tocar quando a raposa perde vida.
- Integrar o ranking automático quando o jogo termina.
- Gerar um instalador simples ou criar um executável.
