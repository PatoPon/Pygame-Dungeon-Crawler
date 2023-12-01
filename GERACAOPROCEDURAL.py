import noise
import numpy as np
import random

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

seed = random.randint(0, 1000)

def saveMap(noiseMap, filename="saved_map.npy"):
    np.save(filename, noiseMap)

def generateNoiseMap(width, height, scale, octaves, persistence, lacunarity, irregularityFactor):
    noiseMap = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            x = i / scale
            y = j / scale
            value = noise.pnoise2(
                x, y, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)

            irregularity = noise.pnoise2(
                i * irregularityFactor, j * irregularityFactor, octaves=3, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=seed)
            value += irregularity

            noiseMap[i][j] = value
    return noiseMap

mapa = generateNoiseMap(width, height, scale, octaves, persistence, lacunarity, irregularityFactor)
saveMap(mapa)