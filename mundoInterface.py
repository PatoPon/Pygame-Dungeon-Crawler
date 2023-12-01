import pygame

from pygame.locals import QUIT, MOUSEBUTTONUP, KEYDOWN
from atributosInterface import desenharStatus

mapaDoJogo = ""
terrainMap = "grass"

def carregarMapa(mapa):
    global mapaDoJogo
    mapaDoJogo = mapa

def desenharJogoPrincipal():

    pygame.init()

    tileset_grama = pygame.image.load("Sprites\\Tilesets\\GRASS+.png")
    tileset_anao = pygame.image.load("Sprites\\Racas\\Anao.png")

    sub_surface_rect = pygame.Rect(0, 0, 16, 16)
    tile_grama = tileset_grama.subsurface(sub_surface_rect)
    tile_grama = pygame.transform.scale(tile_grama, (32, 32))

    tileset_anao = pygame.transform.scale(tileset_anao, (64, 64))

    largura, altura = 800, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Jogo Principal')

    posicao_jogador = (16, 16)
    destino = (posicao_jogador[0], posicao_jogador[1])

    def visualizeDetailedMap(terrainMap):
        sub_surface_rect_amarela = pygame.Rect(16, 16, 16, 16)
        tile_grama_amarela = tileset_grama.subsurface(sub_surface_rect_amarela)
        tile_grama_amarela = pygame.transform.scale(tile_grama_amarela, (32, 32))

        for i in range(len(mapaDoJogo)):
            for j in range(len(mapaDoJogo[0])):
                x = i * tamanho_celula
                y = j * tamanho_celula

                if terrainMap[i, j] == "sand":
                    tela.blit(tile_grama_amarela, (x, y))
                else:
                    tela.blit(tile_grama, (x, y))


    def irAteLocal(posicao, destino):
        pos_vector = pygame.math.Vector2(posicao)
        dest_vector = pygame.math.Vector2(destino)

        move_vector = dest_vector - pos_vector

        move_vector.x = 0 if abs(move_vector.y) > abs(
        move_vector.x) else move_vector.x
        move_vector.y = 0 if not move_vector.x == 0 else move_vector.y

        if move_vector.length() > tamanho_celula:
            move_vector = move_vector.normalize() * tamanho_celula

        pos_vector += move_vector

        return pos_vector
        
    def movimentacaoPlayer(posicao, key):
        x, y = posicao

        if key == pygame.K_LEFT and x - tamanho_celula >= 0:
            x -= tamanho_celula
        elif key == pygame.K_RIGHT and x + tamanho_celula < largura:
            x += tamanho_celula
        elif key == pygame.K_UP and y - tamanho_celula >= 0:
            y -= tamanho_celula
        elif key == pygame.K_DOWN and y + tamanho_celula < altura - 120:
            y += tamanho_celula

        posicao = x, y
        return posicao

    def desenhar_grid(cell_x, cell_y):
        pygame.draw.rect(tela, (255, 0, 0), (cell_x, cell_y,
                         tamanho_celula, tamanho_celula), 1)

    tamanho_celula = 32

    dados_surface = pygame.Surface((largura, 120))
    dados_surface.fill((255, 255, 255))

    pygame.key.set_repeat(300, 75)

    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                return False
            elif evento.type == KEYDOWN:
                destino = movimentacaoPlayer(
                    posicao_jogador, evento.key)

        posicao_jogador = irAteLocal(
            posicao_jogador, destino)

        tela.fill((0, 0, 0))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cell_x = mouse_x // tamanho_celula * tamanho_celula
        cell_y = mouse_y // tamanho_celula * tamanho_celula

        desenharStatus(dados_surface)
        desenhar_grid(cell_x, cell_y)
        visualizeDetailedMap(terrainMap)
        tela.blit(
            tileset_anao, (posicao_jogador[0] - tamanho_celula, posicao_jogador[1] - tamanho_celula))
        tela.blit(dados_surface, (0, altura - 120))

        pygame.display.flip()
        pygame.time.Clock().tick(30)