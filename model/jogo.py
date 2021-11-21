import pygame
from pygame import font
import constants.main as constants

pygame.init()
pygame.font.init()

class Jogo:
    def __init__(self):
        self.tela = pygame.display.set_mode(
            (constants.LARGURA_CENARIO, constants.ALTURA_CENARIO))
        pygame.display.set_caption("Rede Neural")
        pygame.display.flip()
        self.rodando = True

    # TODO: passar fonte por parametro
    # fonte=pygame.font.get_default_font(),
    def desenharTexto(self,
                      texto,
                      tamanho=45,
                      cor=(0, 0, 0),
                      x=10, y=10,
                      align="nw"):
        """
        Desenha um texto na tela.
        :param texto: Texto a ser desenhado.
        :param cor: Cor do texto.
        :param x: Posição x do texto.
        :param y: Posição y do texto.
        :param align: Alinhamento do texto.
        """
        pygame.font.init()
        fonteRender = pygame.font.SysFont(
            "/home/andreruxx/Desktop/simpleAI/fonts/arial.ttf", tamanho)
        textSurface = fonteRender.render(texto, True, cor)
        textRect = textSurface.get_rect()
        if align == "nw":
            textRect.topleft = (x, y)
        if align == "ne":
            textRect.topright = (x, y)
        if align == "sw":
            textRect.bottomleft = (x, y)
        if align == "se":
            textRect.bottomright = (x, y)
        if align == "n":
            textRect.midtop = (x, y)
        if align == "s":
            textRect.midbottom = (x, y)
        if align == "e":
            textRect.midright = (x, y)
        if align == "w":
            textRect.midleft = (x, y)
        if align == "center":
            textRect.center = (x, y)
        
        return textSurface, textRect

    def inicializar(self):
        while self.rodando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
            pygame.display.flip()
        pygame.quit()
