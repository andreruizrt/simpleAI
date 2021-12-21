from numpy import double
import math

import pygame
from model.jogo import Jogo

import model.redeNeural as rn
import model.camada as camada
import model.carro as carro

import constants.main as constants
from log.simpleLog import logging


class Animation2:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.largura: int = 0
        self.altura: int = 0
        self.angulo: double = 0.0

        self.ativada: bool = False
        self.frameAtual: int = 0
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



game = Jogo()

paredes: list = [0.0]*constants.LARGURA_CENARIO*constants.ALTURA_CENARIO
paredesVirtual: list = [0.0]*constants.LARGURA_CENARIO*constants.ALTURA_CENARIO
quantidadeParede: int = 0

cenario: list = [['.']*constants.LARGURA_CENARIO]*constants.ALTURA_CENARIO
distancias: list = [[0]*constants.LARGURA_CENARIO]*constants.ALTURA_CENARIO
matrizBoost: list = [[0.0]*constants.LARGURA_CENARIO]*constants.ALTURA_CENARIO

spritePista: int = 0
spriteCarros: list = [0]*10
spriteCarroQueimado: int = 0
spritesExplosao: list = [0]*50
listaExplosoes: list = [Animation2()]*constants.MAX_EXPLOSOES
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

obstaculos: list = [Obstaculo()]*constants.QTD_OBSTACULO
zonas: list = [Zona()]*constants.QTD_ZONA

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


def buscarMelhorFitness(self):
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
        dist = 30
        x1 = carro.x
        y1 = carro.y
        angulo = (double)(carro.angulo - 90.0 + (i*180.0) /
                          (constants.CAR_BRAIN_QTD_INPUT-2.0))

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


def calcularCor(intensidade: double, corBase: tuple):
    """
    Calcular cor que será renderizada no pygame pelo RGB
    :param cor: cor de base
    :param intensidade: intensidade
    """
    r = (int)(corBase[0] >> 16)
    g = (int)(corBase[1] >> 8)
    b = (int)(corBase[2])

    cor = []
    cor.append((int)(r * intensidade))
    cor.append((int)(g * intensidade))
    cor.append((int)(b * intensidade))

    print("Cor x Intensidade: RGB(", cor[0], ",", cor[1],
          ",", cor[2], ")")

    return cor


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
    spriteNeuronDesativado = pygame.image.load(
        "/home/andreruxx/Desktop/simpleAI/images/neuronio7.png")
    # spriteNeuronDesativado = pygame.color.Color(spriteNeuronDesativado, (0, 0, 0))
    # definirColoracao(spriteNeuronDesativado, PRETO)

    # Alterar para a cor branca
    spriteNeuronAtivado = pygame.image.load(
        "/home/andreruxx/Desktop/simpleAI/images/neuronio7.png")
    # spriteNeuronAtivado = pygame.color.Color(spriteNeuronAtivado, (255, 255, 255))
    # definirColoracao(spriteNeuronAtivado, BRANCO)

    spriteContornoNeuronio = pygame.image.load(
        "/home/andreruxx/Desktop/simpleAI/images/branco.png")

    spriteLuzAmarelo = pygame.image.load(
        "/home/andreruxx/Desktop/simpleAI/images/luz.png")

    spriteLuzAzul = pygame.image.load(
        "/home/andreruxx/Desktop/simpleAI/images/luzAzul.png")

    spriteSeta = pygame.image.load(
        "/home/andreruxx/Desktop/simpleAI/images/seta2.png")
    # definirColoracao(spriteSeta, PRETO)


def desenharRedeNeural(self, x: int, y: int, largura: int, altura: int):
    """
    Desenha a rede neural na tela
    :param x: Posição X
    :param largura: Largura
    :param altura: Altura
    """
    global game

    neuronEntradaX: list = [0.0]*constants.CAR_BRAIN_QTD_INPUT
    neuronEntradaY: list = [0.0]*constants.CAR_BRAIN_QTD_INPUT
    neuronEscondidoX: list = [
        [0.0]*constants.CAR_BRAIN_QTD_LAYERS]*constants.CAR_BRAIN_QTD_HIDE
    neuronEscondidoY: list = [
        [0.0]*constants.CAR_BRAIN_QTD_LAYERS]*constants.CAR_BRAIN_QTD_HIDE
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

    escalaAltura: double = ((double)(alturaPintura)) / \
        ((double)(qtdNeuroEscondidas - 1))
    escalaLargura: double = ((double)(larguraPintura-475)) / \
        ((double)(qtdEscondidas + 1))

    temp: double = yOrigem - (escalaAltura * (qtdNeuroEscondidas - 2)) / \
        2.0 + (escalaAltura*(qtdNeuroSaida - 1))/2.0

    self.textoAcelerar = game.desenharTexto("Acelerar", tamanho=20,
                                            x=(x + largura - 130),
                                            y=(temp - 0*escalaAltura - 5 - constants.DESLOCAMENTO_NEURONIOS))

    self.textoRe = game.desenharTexto("RÉ", tamanho=20,
                                      x=(x + largura - 130),
                                      y=(temp - 1*escalaAltura - 5 - constants.DESLOCAMENTO_NEURONIOS))

    self.textoVirarEsquerda = game.desenharTexto("Virar Esquerda", tamanho=20,
                                                 x=(x + largura - 130),
                                                 y=(temp - 2*escalaAltura - 5 - constants.DESLOCAMENTO_NEURONIOS))

    self.textoVirarDireita = game.desenharTexto("Virar Direita", tamanho=20,
                                                x=(x + largura - 130),
                                                y=(temp - 3*escalaAltura - 5 - constants.DESLOCAMENTO_NEURONIOS))

    game.tela.blits(self.textoAcelerar, self.textoRe,
                    self.textoVirarEsquerda, self.textoVirarDireita)

    for i in range(qtdNeuroEntrada):
        neuronEntradaX[i] = xOrigem
        neuronEntradaY[i] = yOrigem - (escalaAltura * i)

    for i in range(qtdEscondidas):
        qtdCamadaAnterior: int = 0
        CamadaAnterior: camada.Camada() = None
        xAnterior: list = 0.0
        yAnterior: list = 0.0

        if i == 0:
            qtdCamadaAnterior = qtdNeuroEntrada
            CamadaAnterior = melhorCarro.cerebro.camadaEntrada
            xAnterior = neuronEntradaX
            yAnterior = neuronEntradaY
        else:
            qtdCamadaAnterior = qtdNeuroEscondidas
            CamadaAnterior = melhorCarro.cerebro.camadaEscondida[i-1]
            xAnterior = neuronEscondidoX[i-1]
            yAnterior = neuronEscondidoY[i-1]

        for j in range(qtdNeuroEscondidas):
            neuronEscondidoX[i][j] = xOrigem + (i+1)*escalaLargura
            neuronEscondidoY[i][j] = yOrigem - j * \
                escalaAltura - constants.DESLOCAMENTO_NEURONIOS

            # sprite = spriteNeuronDesativado
            # saidaNeuronio = melhorCarro.cerebro.camadaEscondida[i].neuronios[j].saida
            # if(saidaNeuronio > 0.0):
            #     sprite = spriteNeuronAtivado

            for k in range(qtdCamadaAnterior):
                peso = melhorCarro.cerebro.camadaEscondida[i].neuronios[j].pesos[k]
                saida = CamadaAnterior.neuronios[k].saida
                if (peso*saida > 0.0):
                    # desenhar linha simples
                    self.linha1 = pygame.draw.line(game.tela, (255, 0, 255), (
                        xAnterior[k], yAnterior[k]), (neuronEscondidoX[i][j], neuronEscondidoY[i][j]), 2)
                else:
                    self.linha1 = pygame.draw.line(game.tela, (128, 128, 128), (
                        xAnterior[k], yAnterior[k]), (neuronEscondidoX[i][j], neuronEscondidoY[i][j]), 2)

    for i in range(qtdNeuroSaida):
        ultimaCamada: int = melhorCarro.cerebro.quantidadeEscondidas-1
        temp = yOrigem - (escalaAltura*(qtdNeuroEscondidas-2)) / \
            2.0 + (escalaAltura*(qtdNeuroSaida-1))/2.0

        neuronSaidaX[i] = xOrigem + (qtdEscondidas+1)*escalaLargura
        neuronSaidaY[i] = temp - i*escalaAltura - \
            constants.DESLOCAMENTO_NEURONIOS

        # sprite = spriteNeuronDesativado
        # saidaNeuronio = melhorCarro.cerebro.camadaSaida.neuronios[i].saida
        # if(saidaNeuronio > 0.5):
        #     sprite = spriteNeuronAtivado

        for j in range(qtdNeuroEscondidas-1):
            peso = melhorCarro.cerebro.camadaSaida.neuronios[i].pesos[j]
            saida = melhorCarro.cerebro.camadaEscondida[ultimaCamada].neuronios[j].saida
            if (peso*saida > 0.0):
                # desenhar linha simples
                self.linha2 = pygame.draw.line(game.tela, (255, 0, 255), (
                    neuronEscondidoX[ultimaCamada][j], neuronEscondidoY[ultimaCamada][j]), (neuronSaidaX[i], neuronSaidaY[i]), 2)
            else:
                self.linha2 = pygame.draw.line(game.tela, (128, 128, 128), (
                    neuronEscondidoX[ultimaCamada][j], neuronEscondidoY[ultimaCamada][j]), (neuronSaidaX[i], neuronSaidaY[i]), 2)

    # desenhar neuronios

    for i in range(qtdNeuroEntrada):
        # neuronEntradaX = xOrigem
        # neuronEntradaY = yOrigem - (escalaAltura * i)

        cor = (255, 0, 255)
        opacidade: double = 0.5

        if (i == constants.CAR_BRAIN_QTD_INPUT-1):
            if(entrada[i] > 15.0):
                opacidade = 1.0
            else:
                opacidade = entrada[i]/15.0
            cor = calcularCor(opacidade, (255, 255, 255))
        else:
            if(entrada[i] > 200.0):
                opacidade = 0
            else:
                opacidade = (200.0 - entrada[i])/200.0
            cor = calcularCor(opacidade, (255, 255, 255))

        # definirColoracao(spriteNeuronAtivado, cor)
        # definirOpacidade(spriteLuzAmarelo, opacidade*255)

        # desenharSprite(SpriteLuzAmarelo,
        #                NeuronEntradaX[i],
        #                NeuronEntradaY[i],
        #                3.5*TamanhoNeuronio,
        #                3.5*TamanhoNeuronio, 0, 0)

        # desenharSprite(spriteContornoNeuronio,
        #                neuronEntradaX[i],
        #                neuronEntradaY[i],
        #                tamanhoNeuronio*1.1,
        #                tamanhoNeuronio*1.1, 0, 0)

        # desenharSprite(spriteNeuronAtivado,
        #                neuronEntradaX[i],
        #                neuronEntradaY[i],
        #                tamanhoNeuronio,
        #                tamanhoNeuronio, 0, 0)

        # definirOpacidade(spriteLuzAmarelo, 255)
        # definirColoracao(spriteNeuronAtivado, (255, 255, 255))

        # desenharSprite(spriteSeta,
        #                 neuronEntradaX[i] - 56,
        #                 neuronEntradaY[i],
        #                 64/(cameraZoom+1),
        #                 12/(cameraZoom+1), 0)

    for i in range(qtdEscondidas):
        qtdCamadaAnterior = 0
        qtdCamadaAnterior = camada.Camada()
        xAnterior = 0.0
        yAnterior = 0.0

        if(i == 0):
            qtdCamadaAnterior = qtdNeuroEntrada
            CamadaAnterior = melhorCarro.cerebro.camadaEntrada
            xAnterior = neuronEntradaX
            yAnterior = neuronEntradaY
        else:
            qtdCamadaAnterior = qtdNeuroEscondidas
            CamadaAnterior = melhorCarro.cerebro.camadaEscondida[i-1]
            xAnterior = neuronEscondidoX[i-1]
            yAnterior = neuronEscondidoY[i-1]

        for j in range(qtdCamadaAnterior):
            neuronEscondidoX[i][j] = xOrigem + (i+1)*escalaLargura
            neuronEscondidoY[i][j] = yOrigem - j*escalaAltura

            sprite = spriteNeuronDesativado
            saidaNeuronio = melhorCarro.cerebro.camadaEscondida[i].neuronios[j].saida
            if(saidaNeuronio > 0):
                sprite = spriteNeuronAtivado
                # desenharSprite(spriteLuzAmarelo,
                #                 neuronEscondidoX[i][j],
                #                 neuronEscondidoY[i][j],
                #                 3.5*tamanhoNeuronio,
                #                 3.5*tamanhoNeuronio, 0, 0)

            # for k in range(qtdCamadaAnterior-1):
            #     peso = melhorCarro.cerebro.camadaEscondida[i].neuronios[j].pesos[k]
            #     saida = CamadaAnterior.neuronios[k].saida
            #     if(peso*saida > 0.0):
            #         # desenhar linha simples
            #         self.linha = pygame.draw.line(game.tela, (255, 0, 0), (
            #             xAnterior[k], yAnterior[k]), (neuronEscondidoX[i][j], neuronEscondidoY[i][j]), 2)
            #     else:
            #         self.linha = pygame.draw.line(game.tela, (0, 0, 0), (
            #             xAnterior[k], yAnterior[k]), (neuronEscondidoX[i][j], neuronEscondidoY[i][j]), 2)

            # desenharSprite(spriteContornoNeuronio,
            #                 neuronEscondidoX[i][j],
            #                 neuronEscondidoY[i][j],
            #                 tamanhoNeuronio*1.1,
            #                 tamanhoNeuronio*1.1, 0, 0)

            # desenharSprite(sprite,
            #                 neuronEscondidoX[i][j],
            #                 neuronEscondidoY[i][j],
            #                 tamanhoNeuronio,
            #                 tamanhoNeuronio, 0, 0)

    for i in range(qtdNeuroSaida):
        ultimaCamada = melhorCarro.cerebro.quantidadeEscondidas-1
        temp = yOrigem - (escalaAltura*(qtdNeuroEscondidas-2) /
                          2.0) + (escalaAltura*(qtdNeuroSaida-1)/2.0)

        neuronSaidaX[i] = xOrigem + (qtdEscondidas+1)*escalaLargura
        neuronSaidaY = temp - i*escalaAltura

        sprite = spriteNeuronDesativado
        saidaNeuronio = melhorCarro.cerebro.camadaSaida.neuronios[i].saida
        if(saidaNeuronio > 0.5):
            sprite = spriteNeuronAtivado
            # desenharSprite(spriteLuzAmarelo,
            #                 neuronSaidaX[i],
            #                 neuronSaidaY,
            #                 3.5*tamanhoNeuronio,
            #                 3.5*tamanhoNeuronio, 0, 0)

        for k in range(qtdNeuroEscondidas-1):
            peso = melhorCarro.cerebro.camadaSaida.neuronios[i].pesos[k]
            saida = melhorCarro.cerebro.camadaEscondida[ultimaCamada].neuronios[k].saida
            if(peso*saida > 0.0):
                # desenhar linha simples
                self.linha = pygame.draw.line(game.tela, (255, 0, 0), (
                    neuronEscondidoX[ultimaCamada][k], neuronEscondidoY[ultimaCamada][k]), (neuronSaidaX[i], neuronSaidaY), 2)
            else:
                self.linha = pygame.draw.line(game.tela, (0, 0, 0), (
                    neuronEscondidoX[ultimaCamada][k], neuronEscondidoY[ultimaCamada][k]), (neuronSaidaX[i], neuronSaidaY), 2)

        # desenharSprite(spriteContornoNeuronio,
        #                 neuronSaidaX[i],
        #                 neuronSaidaY[i],
        #                 tamanhoNeuronio*1.1,
        #                 tamanhoNeuronio*1.1, 0, 0)

        # desenharSprite(sprite,
        #                 neuronSaidaX[i],
        #                 neuronSaidaY[i],
        #                 tamanhoNeuronio,
        #                 tamanhoNeuronio, 0, 0)

# EXPLOSOES

def criarTexturaExplosoes(self):
    self.texturaExplosao = []
    for i in range(44):
        self.texturaExplosao.append(pygame.image.load(
            "/home/andreruxx/Desktop/simpleAI/images/explosion/exp ("+str(i+1)+").png").convert_alpha())

def criarExplosao(self, x: int, y: int, largura: int,
                  altura: int, angulo: double):
    global listaExplosoes
    for i in range(constants.MAX_EXPLOSOES):
        if(listaExplosoes[i].ativada == False):
            listaExplosoes[i].ativada = True
            listaExplosoes[i].x = x
            listaExplosoes[i].y = y
            listaExplosoes[i].largura = largura
            listaExplosoes[i].altura = altura
            listaExplosoes[i].angulo = angulo
            listaExplosoes[i].frameAtual = 0
            listaExplosoes[i].quatidadeFrames = 44
            return

def trocarFrameExplosoes():
    global listaExplosoes
    for i in range(constants.MAX_EXPLOSOES):
        if(listaExplosoes[i].ativada == True):
            listaExplosoes[i].frameAtual += 1

            if(listaExplosoes[i].frameAtual > listaExplosoes[i].quatidadeFrames):
                listaExplosoes[i].ativada = False
                listaExplosoes[i].frameAtual = 0

def desenharFrameExplosoes():
    for i in range(constants.MAX_EXPLOSOES):
        if(listaExplosoes[i].ativada == True):
            x = listaExplosoes[i].x
            y = listaExplosoes[i].y

            # x = ((x+cameraPosX)+((x+cameraPosX)-LARG_TELA/2.0))*cameraZoom
            # y = ((y+cameraPosY)+((y+cameraPosY)-ALT_TELA/2.0))*cameraZoom

            # desenharSprite(spritesExplosao[listaExplosoes[i].frameAtual],
            #                x,
            #                y,
            #                listaExplosoes[i].largura,
            #                listaExplosoes[i].altura,
            #                listaExplosoes[i].angulo)


def desenhar():
    pass


# adicionais configurações iniciais

def criar_timer(self):
    pass

def inicializar_gerador_aleatorio(self):
    pass

def preencher_matriz_colisao(self):
    pass

def preencher_matriz_distancias(self):
    pass

def inicializar_obstaculos(self):
    pass

def criar_sprite(self, nome_arquivo: str, retirar_fundo: int = 0):
    logging.info("Criando sprite: ", nome_arquivo)
    pass

def inicializar_sprites(self):
    logging.info("Inicializando sprites")
    pass

def inicializar_zonas(self):
    pass

def criar_ponto_desenho_colisao(self):
    pass

def alocar_carros(self):
    pass

def criar_fonte_normal(self):
    pass

def inicializar_nova_partida(self):
    pass

def atualizar_janela(self):
    pass    
        
def verificar_teclas_usuario(self):
    pass

def tempoDecorrido(self, timer):
    pass

def movimentar_camera(self):
    pass

def controlar_carros(self):
    pass

def movimentar_carros(self):
    pass

def girar_obstaculos(self):
    pass
            
def verificar_interacao_jogador(self):
    pass

def laser_destruidor(self):
    pass

def trocar_frame_explosoes(self):
    pass

def atualizar_opacidade_background(self):
    pass

def verificar_fim_partida(self):
    pass

def reiniciar_timer(timer):
    pass


def configuracoes_iniciais(self):
    # TODO:
    # criar_janela("Rede Neural", 0)
    game.criar_janela(nome_janela="Rede Neural")

    inicializar_sprites()
    timerGeral = criar_timer()

    inicializar_gerador_aleatorio()
    preencher_matriz_colisao()
    logging.info("Matriz de colisão preenchida")
    preencher_matriz_distancias()
    logging.info("Matriz de distancias preenchida")

    inicializar_obstaculos()
    inicializar_zonas()

    criar_ponto_desenho_colisao()

    alocar_carros()

    fonte = criar_fonte_normal()

    distanciaRecorde = 0
    geracao = 0
    
    inicializar_nova_partida()


def main(self):
    configuracoes_iniciais()
        
    while game.rodando:
        atualizar_janela()
        verificar_teclas_usuario()

        if(tempoDecorrido(timerGeral) >= periodo):
            movimentar_camera()

            controlar_carros()
            movimentar_carros()

            girar_obstaculos()

            verificar_interacao_jogador()

            laser_destruidor()

            trocar_frame_explosoes()
            atualizar_opacidade_background()

            verificar_fim_partida()

            desenhar()

            reiniciar_timer(timerGeral)

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self.rodando = False
    #     self.clock.tick(60)
    #     pygame.display.flip()
    # pygame.quit()

    return 0





    
