import pygame
import os
import noise
import numpy as np
import random

from mundoInterface import carregarMapa, desenharJogoPrincipal

# Configurações
width, height = 800, 608
scale = 50
octaves = 6
persistence = 0.5
lacunarity = 2.0
cellSize = 16

# Raio máximo da ilha
maxIslandRadius = 200

# Fator de irregularidade da ilha
irregularityFactor = 0.1

# Níveis de zoom
zoom_levels = [1, 2]
current_zoom = 0

# Inicialização do Pygame
pygame.init()

# Criar a janela
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gerador de Mapa com Ilha Irregular no Oceano")

seed = random.randint(0, 1000)


def loadMap(filename="saved_map.npy"):
    if os.path.exists(filename):
        return np.load(filename)
    else:
        print(f"Arquivo {filename} não encontrado. Criando novo mapa.")


def generateDetailedMap(startX, startY):
    detailedMap = np.zeros((width, height), dtype=object)
    for i in range(width):
        for j in range(height):
            value = noise.pnoise2(
                (i + startX) / scale, (j + startY) / scale,
                octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)

            distanceToCenter = np.sqrt(
                (i + cellSize/2 - width/2)**2 + (j + cellSize/2 - height/2)**2)

            islandRadius = int(maxIslandRadius * (value + 1) / 2)

            if distanceToCenter < islandRadius:
                detailedMap[i][j] = "terra"
            else:
                detailedMap[i][j] = "agua"

    return detailedMap


def drawMap(zoom, offset):
    mapSurface = pygame.Surface((width, height))
    for i in range(0, width, cellSize):
        for j in range(0, height, cellSize):
            terrain_type = detailedMap[i][j]

            if terrain_type == "terra":
                color = (34, 139, 34)  # Cor verde para a terra
            elif terrain_type == "agua":
                color = (0, 0, 255)

            # Calcular a nova posição centralizada para o zoom
            new_center_x = (
                i * zoom - offset[0]) + width/2 * (1-zoom)
            new_center_y = (
                j * zoom - offset[1]) + height/2 * (1-zoom)

            pygame.draw.rect(mapSurface, color, (new_center_x,
                             new_center_y, cellSize * zoom, cellSize * zoom))

    return mapSurface


def drawGrid():
    for i in range(0, width, cellSize):
        for j in range(0, height, cellSize):
            rect = pygame.Rect(i * zoom - offset[0] + width/2 * (
                1-zoom), j * zoom - offset[1] + height/2 * (1-zoom), cellSize * zoom, cellSize * zoom)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)


# Gerar mapa de ruído
noiseMap = loadMap()

# Posição de visualização do mapa
offset = [0, 0]

detailedMap = generateDetailedMap(0, 0)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                current_zoom = (current_zoom + 1) % len(zoom_levels)
                fator = 2 if current_zoom == 1 else 0.5
                offset = [offset[0] * fator, offset[1] * fator]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                cellX = mouse_x // cellSize
                cellY = mouse_y // cellSize
                desenharJogoPrincipal()

    # Verificar teclas de seta para mover o mapa
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        offset[0] -= 8
    if keys[pygame.K_RIGHT]:
        offset[0] += 8
    if keys[pygame.K_UP]:
        offset[1] -= 8
    if keys[pygame.K_DOWN]:
        offset[1] += 8

    # Desenhar a superfície do mapa e a grade com o zoom atual e a posição de visualização
    zoom = zoom_levels[current_zoom]
    mapSurface = drawMap(zoom, offset)
    screen.blit(mapSurface, (0, 0))
    drawGrid()

    # Atualizar a tela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()
