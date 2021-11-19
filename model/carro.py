from numpy import double
import constants.main as constants
class Carro:
    def __init__(self, x, y: double, vx, vy: double,
                 angulo: double, velocidade: double,
                 colidiu: bool, queimado: bool,
                 sprint: bool, tamanhoDNA: int,
                 DNA: double, fitness: double
                 ):
        self.x: double = x
        self.y: double = y
        self.vx: double = vx
        self.vy: double = vy
        self.angulo: double = angulo
        self.velocidade: double = velocidade
        self.colidiu: bool = False
        self.queimado: bool = False

        self.sprite: int = 0
        self.distanciaSensores: list() = list()
        self.distanciaSensores[constants.CAR_BRAIN_QTD_INPUT-1] = 0.0

        self.tamanhoDNA: int = 0
        self.DNA: double = 0.0
        self.fitness: double = 0.0
