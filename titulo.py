import pygame
import sys

from criacaoDePersonagem import *

TITULO = "Abyssal Descent"

# Inicializa o Pygame
pygame.init()

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Definindo as dimensões da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Menu')

# Carrega a fonte padrão do Pygame
fonte = pygame.font.Font(None, 36)

OPCOES = ["Jogar", "Sair"]
opcaoAtual = 0

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                opcaoAtual = (opcaoAtual - 1) % len(OPCOES)
            elif evento.key == pygame.K_DOWN:
                opcaoAtual = (opcaoAtual + 1) % len(OPCOES)
            elif evento.key == pygame.K_RETURN:
                opcaoSelecionada = OPCOES[opcaoAtual]

                if opcaoSelecionada == "Jogar":
                    # Chame aqui a função para criar o personagem usando o Pygame
                    jogador = Player()
                    escolherNome(jogador)
                    escolherRaca(jogador)
                    escolherClasse(jogador)
                    escolherAtributos(jogador)
                    salvarJogador(jogador, 'Dados\\dadosJogador.json')

                    main_menu()

                elif opcaoSelecionada == "Sair":
                    pygame.quit()
                    sys.exit()

    tela.fill(PRETO)

    # Desenha o título
    for i, linha in enumerate(TITULO):
        texto = fonte.render(linha, True, BRANCO)
        tela.blit(texto, ((LARGURA - texto.get_width()) // 2, (ALTURA // 2) + 7 - 10 + i * 30))

    # Desenha as opções
    for i, opcao in enumerate(OPCOES):
        cor = BRANCO if i == opcaoAtual else PRETO
        texto = fonte.render(opcao, True, cor)
        tela.blit(texto, ((LARGURA - texto.get_width()) // 2, (ALTURA // 2) + (i + 1) * 30))

    pygame.display.flip()