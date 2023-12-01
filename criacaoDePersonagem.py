import pygame
import sys
import json
from jogo import main_menu

with open('Dados\\races.json', 'r', encoding='utf-8') as file:
    racasIniciais = json.load(file)

with open('Dados\\classes.json', 'r', encoding='utf-8') as file:
    classesIniciais = json.load(file)

class Player:
    def __init__(self, name="Unknown", level=1, strength=5, intellect=5, perception=5, luck=5, race="Humano", classe="Guerreiro"):
        self.name = name
        self.level = level
        self.strength = strength
        self.intellect = intellect
        self.perception = perception
        self.luck = luck
        self.race = race
        self.classe = classe

pygame.init()

BRANCO = (255, 255, 255)
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Menu')
fonte = pygame.font.Font('Chomsky.otf', 24)

def renderizar_texto(texto, posicao_y):
    texto_surface = fonte.render(str(texto), True, BRANCO)
    rect = texto_surface.get_rect(center=(LARGURA // 2, posicao_y))
    tela.blit(texto_surface, rect.topleft)

def escolherNome(jogador):
    nome_atual = []

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome_atual:
                    jogador.name = ''.join(nome_atual)
                    return True
                elif evento.key == pygame.K_BACKSPACE and nome_atual:
                    nome_atual.pop()
                elif evento.unicode.isalpha():
                    nome_atual.append(evento.unicode)

        tela.fill((0, 0, 0))
        renderizar_texto(f"Digite seu nome: {''.join(nome_atual)}", ALTURA // 2)
        pygame.display.flip()

def escolherRaca(jogador):
    racas = list(racasIniciais.keys())
    raca_atual = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    jogador.race = racas[raca_atual]
                    return True
                elif evento.key == pygame.K_RIGHT:
                    raca_atual = (raca_atual + 1) % len(racas)
                elif evento.key == pygame.K_LEFT:
                    raca_atual = (raca_atual - 1) % len(racas)

        tela.fill((0, 0, 0))
        renderizar_texto(f"Escolha sua raça: {racas[raca_atual]}", ALTURA // 2 - 30)
        descricao = racasIniciais[racas[raca_atual]]['descricao']
        renderizar_texto(descricao, ALTURA // 2)
        pygame.display.flip()

def escolherClasse(jogador):
    classes = list(classesIniciais.keys())
    classe_atual = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    jogador.classe = classes[classe_atual]
                    return True
                elif evento.key == pygame.K_RIGHT:
                    classe_atual = (classe_atual + 1) % len(classes)
                elif evento.key == pygame.K_LEFT:
                    classe_atual = (classe_atual - 1) % len(classes)

        tela.fill((0, 0, 0))
        renderizar_texto(f"Escolha sua classe: {classes[classe_atual]}", ALTURA // 2 - 30)
        descricao = classesIniciais[classes[classe_atual]]
        renderizar_texto(descricao, ALTURA // 2)
        pygame.display.flip()

def escolherAtributos(jogador):
    atributos = ["strength", "intellect", "perception", "luck"]
    atributo_atual = 0
    valor_atual = 5
    pontos = 5

    while atributo_atual < len(atributos):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and valor_atual:
                    setattr(jogador, atributos[atributo_atual], valor_atual)
                    atributo_atual += 1
                    if atributo_atual < len(atributos):
                        valor_atual = getattr(jogador, atributos[atributo_atual])
                    else:
                        valor_atual = 0
                        return True
                elif evento.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                    if len(str(valor_atual)) > 1:
                        valor_atual //= 10
                elif evento.key == pygame.K_RIGHT:
                    if valor_atual < 10 and pontos > 0:
                        pontos -= 1
                        valor_atual = min(valor_atual + 1, 10)
                elif evento.key == pygame.K_LEFT:
                    if valor_atual > 1:
                        pontos += 1
                        valor_atual = max(valor_atual - 1, 1)

        tela.fill((0, 0, 0))
        renderizar_texto(f"Pontos restantes: {pontos}", ALTURA // 2 - 60)
        prompt = f"Pontos {atributos[atributo_atual]}: {valor_atual}"
        renderizar_texto(prompt, ALTURA // 2 - 30)
        renderizar_texto("ENTER para continuar e Q para voltar", ALTURA // 2)
        pygame.display.flip()

def salvarJogador(jogador, arquivo):
    maxHP = calcularMaxHP(jogador.level, jogador.strength)

    jogador_data = {
        "name": jogador.name,
        "level": jogador.level,
        "race": jogador.race,
        "classe": jogador.classe,

        "atributos": {
            "strength": jogador.strength,
            "intellect": jogador.intellect,
            "perception": jogador.perception,
            "luck": jogador.luck
        },

        "health": {
            "maxHP": maxHP,
            "HP": maxHP
        }
    }

    with open(arquivo, 'w') as json_file:
        json.dump(jogador_data, json_file, indent=4)

def calcularMaxHP(level, strength):
    nivel_maximo = 99
    fator_nivel = nivel_maximo / (nivel_maximo - 1)
    fator_forca = (100 - 1) / 5

    maxHP = 1 + (level - 1) * fator_nivel + strength * fator_forca
    return maxHP