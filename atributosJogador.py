class Player:
    
    def __init__(self, strength=5, intellect=5, perception=5, luck=5, race="Humano", specialization="Guerreiro"):
        self.strength = strength
        self.intellect = intellect
        self.perception = perception
        self.luck = luck
        self.race = race
        self.specialization = specialization

    def display_stats(self):
        print("Atributos do Jogador:")
        print(f"Força: {self.strength}")
        print(f"Inteligência: {self.intellect}")
        print(f"Percepção: {self.perception}")
        print(f"Sorte: {self.luck}")
        print(f"Raça: {self.race}")
        print(f"Especialização: {self.specialization}")