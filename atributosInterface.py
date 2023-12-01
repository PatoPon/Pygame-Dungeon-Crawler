import pygame
import json
from pygame.locals import QUIT


def desenharStatus(surface):

    fonteNome = pygame.font.Font("Essays1743.ttf", 20)
    fonteAtributos = pygame.font.Font("Essays1743.ttf", 16)

    try:
        with open("Dados\\dadosJogador.json", 'r') as arquivo_jogador:
            playerData = json.load(arquivo_jogador)

        width, height = surface.get_size()

        surface.fill((0, 0, 0))
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 2)

        jogador_info = [
            f"{playerData['name']} o {playerData['classe']} {playerData['race']}",
            f"Level {playerData['level']}",
            f"Força: {playerData['atributos']['strength']}",
            f"Inteligência: {playerData['atributos']['intellect']}",
            f"Percepção: {playerData['atributos']['perception']}",
            f"Sorte: {playerData['atributos']['luck']}"
        ]

        jogador_status = [
            f"HP: {playerData['health']['HP']} / {playerData['health']['maxHP']}"
        ]

        nome = fonteNome.render(jogador_info[0], True, (255, 255, 255))
        surface.blit(nome, (10, 0 * 30))

        for i in range(1, len(jogador_info)):
            texto_surface = fonteAtributos.render(
                jogador_info[i], True, (255, 255, 255))
            surface.blit(texto_surface, (10, 8 + i * 16))

        for i, info in enumerate(jogador_status):
            texto_surface = fonteAtributos.render(info, True, (255, 255, 255))
            surface.blit(texto_surface, ((
                width // 2 - texto_surface.get_width() // 2) - 70, 6))

    except FileNotFoundError:
        texto_surface = fonteNome.render(
            "Arquivo 'dadosJogador.json' não encontrado.", True, (255, 255, 255))
        surface.blit(texto_surface, (10, 10))
