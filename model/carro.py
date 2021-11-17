import constants.main as constants

class Carro:
  def __init__(self):
    self.X, self.Y = 0.0, 0.0
    self.VX, self.VY = 0.0, 0.0
    self.Angulo = 0.0
    self.Velocidade = 0.0
    self.Colidiu = False
    self.Queimado = False
    
    self.Sprite = 0
    self.DistanciaSensores = list()
    self.DistanciaSensores[constants.CAR_BRAIN_QTD_INPUT-1] = 0.0

    self.TamanhoDNA = 0
    self.DNA = 0.0
    self.Fitness = 0.0





