from numpy import double
import constants.main as constants
import model.redeNeural as rn
import pygame as pg

class Carro(pg.sprite.Sprite):
    def __init__(self,
                 x: double = 0.0, y: double = 0.0,
                 vx: double = 0.0, vy: double = 0.0,
                 angulo: double = 0.0,
                 velocidade: double = 0.0,
                 colidiu: bool = False,
                 queimado: bool = False,
                 sprite: bool = False,
                 tamanhoDNA: int = 0,
                 DNA: double = 0.0,
                 fitness: double = 0.0
                 ):
        pg.sprite.Sprite.__init__(self)
        self.x: double = x
        self.y: double = y
        self.vx: double = vx
        self.vy: double = vy
        self.angulo: double = angulo
        self.velocidade: double = velocidade
        self.colidiu: bool = colidiu
        self.queimado: bool = queimado

        self.sprite: int = sprite
        self.distanciaSensores: list = [[0.0]*(constants.CAR_BRAIN_QTD_INPUT-1)]

        self.tamanhoDNA: int = tamanhoDNA
        self.DNA: double = DNA
        self.fitness: double = fitness

        self.cerebro: rn.RedeNeural = rn.RedeNeural()
