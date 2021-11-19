from numpy import double


class Neuronio:
  def __init__(self, quantidadeLigacoes: int = 0):
    self.quantidadeLigacoes = quantidadeLigacoes
    self.peso: list = []
    self.erro: double = 0.0
    self.saida: double = 0.0