import curses
from curses import wrapper

import threading

from mundoInterface import desenharMundo
from atributosInterface import desenharStatus

TITULO = [
    "___ _  _ ____    ____ ___  _   _ ____ ____ ____ _       ____ _  _ ___  ____ ___  _ ___ _ ____ _  _",
    " |  |__| |___    |__| |__]  \_/  [__  [__  |__| |       |___  \/  |__] |___ |  \ |  |  | |  | |\ |",
    " |  |  | |___    |  | |__]   |   ___] ___] |  | |___    |___ _/\_ |    |___ |__/ |  |  | |__| | \|",
]

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    
    OPCOES = ["Jogar", "Sair"]
    
    opcaoAtual = 0
    
    while True:
        stdscr.clear()

        HEIGHT, WIDTH = stdscr.getmaxyx()
        
        X = (WIDTH - max(len(opcao) for opcao in OPCOES)) // 2
        Y = (HEIGHT // 2) + 7

        for i, linha in enumerate(TITULO):
            stdscr.addstr(Y - 10 + i, (WIDTH - len(linha)) // 2, linha)

        caixa_x = X - 1
        caixa_y = Y - 1
        caixa_height = len(OPCOES) + 4
        caixa_width = max(len(opcao) for opcao in OPCOES) + 4
        
        stdscr.box()
        stdscr.hline(caixa_y, caixa_x + 1, curses.ACS_HLINE, caixa_width - 2)
        stdscr.hline(caixa_y + caixa_height - 1, caixa_x + 1, curses.ACS_HLINE, caixa_width - 2)
        stdscr.vline(caixa_y + 1, caixa_x, curses.ACS_VLINE, caixa_height - 2)
        stdscr.vline(caixa_y + 1, caixa_x + caixa_width - 1, curses.ACS_VLINE, caixa_height - 2)
        
        for i, opcao in enumerate(OPCOES):
            if i == opcaoAtual:
                stdscr.addstr(Y + (i + 1), X, f"> {opcao}", curses.A_STANDOUT)
            else:
                stdscr.addstr(Y + (i + 1), X, f"  {opcao}")
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            opcaoAtual = (opcaoAtual - 1) % len(OPCOES)
        elif key == curses.KEY_DOWN:
            opcaoAtual = (opcaoAtual + 1) % len(OPCOES)
        elif key == 10:
            opcaoSelecionada = OPCOES[opcaoAtual]
            
            if opcaoSelecionada == "Jogar":

                stdscr.clear()

                mundoWidth = WIDTH * 3 // 4

                janela = curses.newwin(HEIGHT,mundoWidth, 0, 0)

                mundo_thread = threading.Thread(target=desenharMundo, args=(janela,))

                statusWidth = WIDTH - mundoWidth
                xStart = 0 + mundoWidth

                janela2 = curses.newwin(HEIGHT, statusWidth, 0, xStart)

                atributos_thread = threading.Thread(target=desenharStatus, args=(janela2,))

                atributos_thread.start()
                mundo_thread.start()

                atributos_thread.join()
                mundo_thread.join()

                break

            elif opcaoSelecionada == "Sair":
                break

wrapper(main)