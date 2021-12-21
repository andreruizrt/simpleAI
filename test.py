from model.jogo import Jogo
from log.simpleLog import logging

class Test:
    game = None


    def testar_criacao_jogo(self):
        logging.info("[ TEST ] criando jogo")
        self.game = Jogo()
        self.game.inicializar()

    def testar_desenharTexto(self):
        logging.info("[ TEST ] desenharTexto")
        pass

    def testar_desenharSprite(self):
        logging.info("[ TEST ] desenhar_sprite")
        pass


        
