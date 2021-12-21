import pygame
from log.simpleLog import logging
import constants.main as constants

class Jogo:
    def __init__(self):
        logging.info("Jogo::construtor")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.rodando = True


    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color("coral"))
        return fps_text

    
    def criar_janela(self, nome_janela ):
        self.tela = pygame.display.set_mode(
            (constants.LARGURA_CENARIO, constants.ALTURA_CENARIO))
        pygame.display.set_caption(nome_janela)
        pygame.display.flip()



    # TODO: passar fonte por parametro
    # fonte=pygame.font.get_default_font(),
    def desenhar_texto(self,
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
        logging.info("desenhar_texto")
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

   
