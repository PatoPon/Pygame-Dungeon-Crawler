import curses

# Loop principal do jogo
def desenharMundo(janelaJogo):

    curses.curs_set(0)
    height, width = janelaJogo.getmaxyx()
    curses.curs_set(0)

    janelaJogo.keypad(True)
    janelaJogo.nodelay(True)

    y = height // 2
    x = width // 2

    minX, minY = 1, 1
    maxX, maxY = 88, 28

    while True:

        try:
            key = janelaJogo.getch()
        except:
            key = None

        # Verifique se o movimento é válido antes de atualizar a posição
        if key == curses.KEY_LEFT and x > minX:
            x -= 1
        elif key == curses.KEY_RIGHT and x < maxX:
            x += 1
        elif key == curses.KEY_UP and y > minY:
            y -= 1
        elif key == curses.KEY_DOWN and y < maxY:
            y += 1

        janelaJogo.erase()
        janelaJogo.addstr(y, x, "#")
        janelaJogo.border()
        janelaJogo.addstr(5, 10, f'X: {x}')
        janelaJogo.addstr(6, 10, f'Y: {y}')
        janelaJogo.refresh()