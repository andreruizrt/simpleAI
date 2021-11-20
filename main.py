from numpy import double
import pygame
import model.redeNeural as rn
import model.carro as carro
import constants.main as constants
import types
import math

class Animation2:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.largura: int = 0
        self.altura: int = 0
        self.angulo: double = 0.0

        self.ativada: bool = False
        self.frame_atual: int = 0
        self.quatidadeFrames: int = 0

class Obstaculo:
    def __init__(self):
        self.x: double = 0
        self.y: double = 0
        self.vx: double = 0
        self.vy: double = 0
        self.angulo: double = 0
        self.velocidadeRotacao: double = 0
        self.tamanhoX: double = 0
        self.tamanhoY: double = 0
        self.rangeMaxMovimento: double = 0
        self.rangeAtualMovimento: double = 0
        self.emMovimento: bool = False

class Zona:
    def __init__(self):
        self.valor: double = 0.0
        self.angulo: double = 0.0
        self.x: double = 0.0
        self.y: double = 0.0
        self.larguraX: double = 0.0
        self.alturaY: double = 0.0


paredes: list = [0.0]*constants.LARGURA_CENARIO*constants.ALTURA_CENARIO
paredesVirtual: list = [0.0]*constants.LARGURA_CENARIO*constants.ALTURA_CENARIO
quantidadeParede: int = 0

cenario: list = [['c']*constants.LARGURA_CENARIO]*constants.ALTURA_CENARIO
distancias: list = [[0]*constants.LARGURA_CENARIO]*constants.ALTURA_CENARIO
matrizBoost: list = [[0.0]*constants.LARGURA_CENARIO]*constants.ALTURA_CENARIO

spritePista: int = 0
spriteCarros: list = [10]
spriteCarroQueimado: int = 0
spritesExplosao: list = [50]
listaExplosoes: list = []
timerGeral: int = 0
carrosColididos: list = []
carros = [carro.Carro()]*constants.QTD_CARROS
distanciaRecorde: int = 0
geracao: int = 0
valorDesfazerPista: int = 0
maiorDistancia: int = 0
velocidadeLazer: double = 0.0
fonte: int = 0
periodo: double = 0.01
spriteEstrelasLigadas: int = 0
spriteEstrelasDesligadas: int = 0
estrelasOpacidade: int = 255
spriteEspinho: int = 0
spriteLama: int = 0
spriteTurbo: int = 0

cores: list = ["AMARELO", "CIANO", "VERMELHO", "AZUL", "VERDE", "ROXO"]

obstaculos: list = [Obstaculo()*constants.QTD_OBSTACULO]
zonas: list = [Zona()*constants.QTD_ZONA]

spriteNeuronDesativado: int = 0
spriteNeuronAtivado: int = 0
spriteLuzAmarelo: int = 0
spriteLuzAzul: int = 0
spriteSeta: int = 0
spriteContornoNeuronio: int = 0

def buscarMelhorCarroVivo(self):
    """
    Busca o carro que está com a melhor distância ainda vivo
    """
    menor = 999999
    indice = 0
    for i in range(constants.QTD_CARROS):
        if(carros[i].colidiu == False):
            dist = distancias[carros[i].x][carros[i].y]
            if(dist < menor):
                menor = dist
                indice = i

    return indice        

def buscarMelhorCarro(self):
    """
    Busca o carro que está com a melhor distância
    """
    menor = 999999
    indice = 0
    for i in range(constants.QTD_CARROS):
        dist = distancias[carros[i].x][carros[i].y]
        if(dist < menor):
            menor = dist
            indice = i

    return indice

def BuscarMelhorFitness(self):
    """
    Busca o carro que está com a melhor distância fitness
    """
    maior = carros[0].fitness
    indice = 0
    for i in range(constants.QTD_CARROS):
        if(i != 0):
            fit = carros[i].fitness
            if(fit > maior):
                maior = fit
                indice = i
    
    return indice

def aplicarSensores(self, carro: carro.Carro(), entrada: double):
    """
    Aplica os sensores do carro
    :param carro: Carro
    :param entrada: Entrada
    """
    for i in range(constants.CAR_BRAIN_QTD_INPUT-1):
        x1 = carro.x
        y1 = carro.y
        angulo = (double)(carro.angulo - 90.0 + (i*180.0)/(constants.CAR_BRAIN_QTD_INPUT-2.0))

        # Calcular o cosseno do angulo multiplicado por PI dividido por 180
        adjacente = (double)((math.cos(math.radians(angulo))*math.pi)/180.0)
        oposto = (double)((math.sin(math.radians(angulo))*math.pi)/180.0)

        while(True):
            x1 = x1 + adjacente
            y1 = y1 + oposto

            if(cenario[(int)(x1)][(int)(y1)] == 0):
                x1 = x1 - adjacente
                y1 = y1 - oposto

                # dist = distanciaEntrePontos(carro.x, carro.y, x1, y1)
                if(entrada != None):
                    entrada[i] = dist
                
                carro.distanciaSensores[i] = dist
                break

        if(entrada != None):
            entrada[i] = carro.velocidade

# calcular cor que será renderizada no pygame pelo RGB
def calcularCor(self, intensidade: double, corBase: int):
    """
    Calcular cor que será renderizada no pygame pelo RGB
    :param cor: cor de base
    :param intensidade: intensidade
    """
    r = (int)(corBase >> 16)
    g = (int)(corBase >> 8)
    b = (int)(corBase)

    corBase.r = (int)(r * intensidade)
    corBase.g = (int)(g * intensidade)
    corBase.b = (int)(b * intensidade)

    print("Cor x Intensidade: RGB(", corBase.r, ",", corBase.g, 
            ",", corBase.b, ")")

    return corBase
    
def inicializarSpritesNeuronios():
    """
    Inicializa os sprites dos neuronios
    """
    global spriteNeuronDesativado
    global spriteNeuronAtivado
    global spriteContornoNeuronio
    global spriteLuzAmarelo
    global spriteLuzAzul
    global spriteSeta

    # Alterar para a cor preta
    spriteNeuronDesativado = pygame.image.load("/home/andreruxx/Desktop/simpleAI/images/neuronio7.png")
    # spriteNeuronDesativado = pygame.color.Color(spriteNeuronDesativado, (0, 0, 0))
    # definirColoracao(spriteNeuronDesativado, PRETO)

    # Alterar para a cor branca
    spriteNeuronAtivado = pygame.image.load("/home/andreruxx/Desktop/simpleAI/images/neuronio7.png")
    # spriteNeuronAtivado = pygame.color.Color(spriteNeuronAtivado, (255, 255, 255))
    # definirColoracao(spriteNeuronAtivado, BRANCO)

    spriteContornoNeuronio = pygame.image.load("/home/andreruxx/Desktop/simpleAI/images/branco.png")

    spriteLuzAmarelo = pygame.image.load("/home/andreruxx/Desktop/simpleAI/images/luz.png")

    spriteLuzAzul = pygame.image.load("/home/andreruxx/Desktop/simpleAI/images/luzAzul.png")

    spriteSeta = pygame.image.load("/home/andreruxx/Desktop/simpleAI/images/seta2.png")
    # definirColoracao(spriteSeta, PRETO)

def desenharRedeNeural(self, x: int, y: int, largura: int, altura: int):
    """
    Desenha a rede neural na tela
    :param x: Posição X
    :param largura: Largura
    :param altura: Altura
    """
    neuronEntradaX: list = [0.0]*constants.CAR_BRAIN_QTD_INPUT
    neuronEntradaY: list = [0.0]*constants.CAR_BRAIN_QTD_INPUT
    neuronEscondidoX: list = [[0.0]*constants.CAR_BRAIN_QTD_LAYERS]*constants.CAR_BRAIN_QTD_HIDE
    neuronEscondidoY: list = [[0.0]*constants.CAR_BRAIN_QTD_LAYERS]*constants.CAR_BRAIN_QTD_HIDE
    neuronSaidaX: list = [0.0]*constants.CAR_BRAIN_QTD_OUTPUT
    neuronSaidaY: list = [0.0]*constants.CAR_BRAIN_QTD_OUTPUT


    entrada: list = [0.0]*constants.CAR_BRAIN_QTD_INPUT
    xOrigem: double = x + 325
    yOrigem: double = y + altura
    larguraPintura: double = largura
    alturaPintura: double = altura
    tamanhoNeuronio: double = 20
    string = None
    sprint: int = 0

    indice: int = buscarMelhorCarroVivo()
    melhorCarro = carros[indice]

    qtdEscondidas: int = melhorCarro.cerebro.quantidadeEscondidas
    qtdNeuroEntrada: int = melhorCarro.cerebro.camadaEntrada.quantidadeNeuronios
    qtdNeuroEscondidas: int = melhorCarro.cerebro.camadaEscondida[0].quantidadeNeuronios
    qtdNeuroSaida: int = melhorCarro.cerebro.camadaSaida.quantidadeNeuronios

    for i in range(constants.CAR_BRAIN_QTD_INPUT):
        entrada[i] = melhorCarro.cerebro.camadaEntrada.neuronios[i].saida

    escalaAltura: double = ((double)(alturaPintura))/((double)(qtdNeuroEscondidas - 1))
    escalaLargura: double = ((double)(larguraPintura-475))/((double)(qtdEscondidas + 1))
    
    temp: double = yOrigem - (escalaAltura * (qtdNeuroEscondidas - 2))/2.0 + (escalaAltura*(qtdNeuroSaida - 1))/2.0







        

# if __name__ == "__main__":
#     main = main()