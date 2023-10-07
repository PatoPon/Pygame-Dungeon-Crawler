import curses
from atributosJogador import Player
from curses.textpad import Textbox, rectangle

import random

def desenharStatus(janela):
    # Configuração inicial do curses
    curses.curs_set(0)

    height, width = janela.getmaxyx() 

    # Loop principal do jogo
    while True:

        janela.erase()

        jogador = Player(strength=7, intellect=8, perception=12, luck=5, race="Elfo", specialization="Mago")

        # Desenhar a barra de janela
        janela.addstr(1, 1, "Status:")

        janela.addstr(2, 1, f"Força: {jogador.strength}")
        janela.addstr(3, 1, f"Inteligência: {jogador.intellect}")
        janela.addstr(4, 1, f"Percepção: {jogador.perception}")
        janela.addstr(5, 1, f"Sorte: {jogador.luck}")
        janela.addstr(6, 1, f"Raça: {jogador.race}")
        janela.addstr(7, 1, f"Especialização: {jogador.specialization}")

        janela.border()

        janela.refresh()