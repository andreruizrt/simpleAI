from numpy import random

import pickle

from log.simpleLog import logging
from model.camada import Camada
from model.neuronio import Neuronio

TAXA_APRENDIZADO = 0.1
TAXA_PESO_INICIAL = 1.0
BIAS = 1

class RedeNeural:
    def __init__(
        self,
        camadaEntrada: Camada = Camada(),
        camadaEscondida: list = list(),
        camadaSaida: Camada = Camada(),
        quantidadeEscondidas: int = 0
    ):
        """
        Cria rede neural
        :param camadaEntrada (Camada, optional): [description]. Defaults to Camada().
        :param camadaEscondida (list, optional): [description]. Defaults to list().
        :param camadaSaida (Camada, optional): [description]. Defaults to Camada().
        :param quantidadeEscondidas (int, optional): [description]. Defaults to 0.
        """
        self.camadaEntrada = camadaEntrada
        self.camadaEscondida = camadaEscondida
        self.camadaSaida = camadaSaida
        self.quantidadeEscondidas = quantidadeEscondidas

    def func(self, X):
        if (X == 0.0):
            return 0.0
        if (X > 0.0):
            return 1.0
        if (X < 0.0):
            return -1.0

    def relu(self, X):
        if (X < 0.0):
            return 0.0
        else:
            if (X < 100000.0):
                return X
            else:
                return 100000.0

    def reluDx(self, X):
        if (X < 0.0):
            return 0.0
        else:
            return 1.0

    def RNA_CopiarVetorParaCamadas(self, rede, vetor):
        logging.info("Copiando vetor para camada escondida")
        j = 0

        for i in range(rede.camadaEscondida.quantidadeNeuronios):
            for k in range(rede.camadaEscondida.quantidadeNeuronios):
                for l in range(rede.camadaSaida.quantidadeNeuronios):
                    rede.camadaEscondida.neuronios[i].pesos[j] = vetor[l]
                    j += 1

        ########################################################################
        logging.info("Copiando vetor para camada saida")
        for i in range(rede.camadaSaida.quantidadeNeuronios):
            for k in range(rede.camadaSaida.quantidadeNeuronios):
                rede.camadaSaida.neuronios[i].pesos[k] = vetor[k]
                j += 1

    def RNA_CopiarCamadasParaVetor(self, rede, vetor):
        logging.info("Copiando camada escondida para vetor")
        j = 0

        for i in range(rede.camadaEscondida.quantidadeNeuronios):
            for k in range(rede.camadaEscondida.quantidadeNeuronios):
                for l in range(rede.camadaSaida.quantidadeNeuronios):
                    vetor[j] = rede.camadaEscondida.neuronios[i].pesos[j]
                    j += 1

        ########################################################################
        logging.info("Copiando camada saida para vetor")
        for i in range(rede.camadaSaida.quantidadeNeuronios):
            for k in range(rede.camadaSaida.quantidadeNeuronios):
                vetor[j] = rede.camadaSaida.neuronios[i].pesos[k]
                j += 1

    # TODO: Retornar rede
    def RNA_CopiarParaEntrada(self, rede, vetorEntrada):
        logging.info("Copiando vetor para camada entrada")
        for i in range(rede.camadaEntrada.quantidadeNeuronios - BIAS):
            rede.camadaEntrada.neuronios[i].saida = vetorEntrada[i]

    def RNA_CopiarDaSaida(self, rede, vetorSaida):
        logging.info("Copiando da camada saida para vetor")
        for i in range(rede.camadaSaida.quantidadeNeuronios):
            vetorSaida[i] = rede.camadaSaida.neuronios[i].saida

    def RNA_QuatidadePesos(self, rede):
        """
        Retorna a quantidade de pesos da rede
        :param rede: rede neural
        """
        logging.info("Lendo a quantidade de pesos da camada de entrada e saida")
        soma = 0

        for i in range(rede.quantidadeEscondidas):
            for k in range(rede.camadaEscondida[i].quantidadeNeuronios):
                soma += rede.camadaEscondida[i].neuronios[k].quantidadeLigacoes

            for l in range(rede.camadaSaida.quantidadeNeuronios):
                soma += rede.camadaSaida.neuronios[l].quantidadeLigacoes

        return soma

    def RNA_CalcularSaida(self, rede):
        """
        Calcula a saida da rede
        :param rede: rede neural
        """
        logging.info("Calculando saida da camada escondida")
        for i in range(rede.camadaEscondida.quantidadeNeuronios):
            soma = 0.0
            for k in range(rede.camadaEntrada.quantidadeNeuronios - BIAS):
                soma += rede.camadaEntrada.neuronios[k].saida * \
                    rede.camadaEscondida.neuronios[i].pesos[k]
            rede.camadaEscondida.neuronios[i].saida = self.relu(soma)

    """ FUTURE
    def RNA_BackPropagation(self, rede, entrada, saidaEsperada):
        for i in range(rede.camadaSaida.quantidadeNeuronios):
            rede.camadaSaida.neuronios[i].erro = saidaEsperada[i] - rede.camadaSaida.neuronios[i].saida
            rede.camadaSaida.neuronios[i].erro = rede.camadaSaida.neuronios[i].erro * self.reluDx(rede.camadaSaida.neuronios[i].saida)

        for i in range(rede.camadaEscondida.quantidadeNeuronios):
            soma = 0.0
            for k in range(rede.camadaSaida.quantidadeNeuronios):
                soma += rede.camadaSaida.neuronios[k].erro * rede.camadaEscondida.neuronios[i].pesos[k]
            rede.camadaEscondida.neuronios[i].erro = soma * self.reluDx(rede.camadaEscondida.neuronios[i].saida)
    """

    def RNA_CriarNeuronio(self, quantidadeLigacoes: int = 0):
        """
        Funcao que cria um neuronio
        :param quantidadeLigacoes: quantidade de ligações que o neuronio terá
        return: neuronio
        """
        logging.info("Criando neuronio")

        neuron = Neuronio(quantidadeLigacoes)
        neuron.peso = [0.0] * quantidadeLigacoes
        
        for i in range(quantidadeLigacoes):
            if (random.uniform(0, 1) < 0.5):
                neuron.peso[i] = random.uniform(-1, 1)/TAXA_PESO_INICIAL
            else:
                neuron.peso[i] = -random.uniform(-1, 1)/TAXA_PESO_INICIAL
                
        neuron.erro = 0.1
        neuron.saida = 1.0
        
        return neuron
    
    def RNA_CriarRedeNeural(self, quantidadeEscondidas, qtdNeuroniosEntrada,
                            qtdNeuroniosEscondidos, qtdNeuroniosSaida):
        """
        Funcao que cria uma rede neural
        :param quantidadeEscondidas: quantidade de camadas escondidas
        :param qtdNeuroniosEntrada: quantidade de neuronios na camada de entrada
        :param qtdNeuroniosEscondidos: quantidade de neuronios na camada escondida
        :param qtdNeuroniosSaida: quantidade de neuronios na camada de saida
        """
        logging.info("Iniciando criacao da rede neural")
        
        qtdNeuroniosEntrada += BIAS
        qtdNeuroniosEscondidos += BIAS
        
        rede = RedeNeural()
        rede.camadaEntrada = Camada(qtdNeuroniosEntrada)
        rede.camadaEntrada.neuronios = [Neuronio(qtdNeuroniosEntrada)] * qtdNeuroniosEntrada
        
        for i in range(qtdNeuroniosEntrada):
            rede.camadaEntrada.neuronios[i].saida = 1.0
            
        rede.quantidadeEscondidas = quantidadeEscondidas
        rede.camadaEscondida = [Camada()] * quantidadeEscondidas
        
        for i in range(quantidadeEscondidas):
            rede.camadaEscondida[i].quantidadeNeuronios = qtdNeuroniosEscondidos
            rede.camadaEscondida[i].neuronios = [Neuronio()] * qtdNeuroniosEscondidos
            
            for j in range(qtdNeuroniosEscondidos):
                if (i == 0):
                    rede.camadaEscondida[i].neuronios[j] = self.RNA_CriarNeuronio(qtdNeuroniosEntrada)
                else:
                    rede.camadaEscondida[i].neuronios[j] = self.RNA_CriarNeuronio(qtdNeuroniosEscondidos)
        
        rede.camadaSaida = Camada(qtdNeuroniosSaida)
        rede.camadaSaida.neuronios = [Neuronio()] * qtdNeuroniosSaida
    
        for i in range(qtdNeuroniosSaida):
            rede.camadaSaida.neuronios[i] = self.RNA_CriarNeuronio(qtdNeuroniosEscondidos)
                      
        print("Criada uma rede neural com:\n\n1 Camada de entrada com", 
              qtdNeuroniosEntrada - 1,"neuronio(s) + 1 BIAS.")
        print(quantidadeEscondidas,"Camada(s) escondida(s), cada uma com",
              qtdNeuroniosEscondidos - 1, "neuronio(s) + 1 BIAS.")
        print("1 Camada de saida com", qtdNeuroniosSaida,"neuronio(s).\n\n")
        print("#"*30)
        
        print(rede.camadaEntrada)
        for i in rede.camadaEntrada.neuronios:
            print("\t", i)
        print("#"*30)
        
        for i in range(quantidadeEscondidas):
            print(rede.camadaEscondida[i])
            for j in rede.camadaEscondida[i].neuronios:
                print("\t", j)
        print("#"*30)
        
        print(rede.camadaSaida)
        for i in rede.camadaSaida.neuronios:
            print("\t", i)
        print("#"*30)

        logging.info("Rede neural criada com sucesso")        
        return rede
    
    def RNA_DestruirRedeNeural(self, rede):
        """
        Funcao que destroi rede neural
        :param rede: rede neural que será destruida
        """
        logging.info("Destruindo rede neural")
        rede = None
        
        # for i in range(rede.camadaEntrada.quantidadeNeuronios):
        #     rede.camadaEntrada.neuronios[i] = None
            
        # for i in range(rede.quantidadeEscondidas):
        #     for j in range(rede.camadaEscondida[i].quantidadeNeuronios):
        #         rede.camadaEscondida[i].neuronios[j].peso = None
        #         rede.camadaEscondida[i].neuronios[j].erro = None
        #         rede.camadaEscondida[i].neuronios[j].saida = 0.0
                
        # for i in range(rede.camadaSaida.quantidadeNeuronios):
        #     rede.camadaSaida.neuronios[i].peso = []
        #     rede.camadaSaida.neuronios[i].erro = 0.0
        #     rede.camadaSaida.neuronios[i].saida = 0.0
        
        logging.info("Rede neural destruida")
        return rede
    
    def RNA_CarregarRede(self, stringRede):
        """
        Funcao que carrega uma rede neural
        :param stringRede: caminho para arquivo da rede neural
        :return: rede neural carregada
        """
        logging.info("Iniciando carregamento da rede neural")

        arq = open(stringRede, "rb")
        if(arq == None):
            logging.error("Erro ao abrir arquivo de rede neural")
            return None
        else:
            rede = pickle.load(arq)
            arq.close()
            logging.info("Rede carregada com sucesso.")
            return rede
     
    def RNA_SalvarRede(self, stringRede, rede):
        """
        Funcao que salva uma rede neural
        :param stringRede: caminho para arquivo da rede neural
        :param rede: rede neural que será salva
        """
        logging.info("Iniciando salvamento da rede neural")

        arq = open(stringRede, "wb")
        if(arq):
            pickle.dump(rede, arq)
            logging.info("Rede salva com sucesso.")
        else:
            logging.error("Erro ao salvar rede.")
        
        arq.close()

        # arq = open(stringRede, "w")
        # if (arq):
        #     arq.write("QTD_CAMADAS_ESCONDIDAS="+ str(rede.quantidadeEscondidas) + "\n")
        #     arq.write("QTD_NEURONIOS_ENTRADA="+ str(rede.camadaEntrada.quantidadeNeuronios) + "\n")
        #     arq.write("QTD_NEURONIOS_ESCONDIDA=" + str(rede.camadaEscondida[0].quantidadeNeuronios) + "\n")
        #     arq.write("QTD_NEURONIOS_SAIDA=" + str(rede.camadaSaida.quantidadeNeuronios) + "\n")
            
        #     for i in range(rede.quantidadeEscondidas):
        #         for j in range(rede.camadaEscondida[i].quantidadeNeuronios):
        #             for k in range(rede.camadaEscondida[i].neuronios[j].quantidadeLigacoes):
        #                 arq.write("PESO_" + str(k) + "_NEURONIO_" + str(j) + "_ESCONDIDA_" + str(i) + "="+ str(rede.camadaEscondida[i].neuronios[j].peso[k]) + "\n")
        
        #     for i in range(rede.camadaSaida.quantidadeNeuronios):
        #         for j in range(rede.camadaSaida.neuronios[i].quantidadeLigacoes):
        #             arq.write("PESO" + str(j) + "_NEURONIO_" + str(i) + "_SAIDA="+ str(rede.camadaSaida.neuronios[i].peso[j]) + "\n")
                    
        #     arq.close()
        
        # tentando salvar em arquivo de bytes, entretanto, não há conversão
        # de float para bytes diretamente
        # arq = open(stringRede, "wb")
        # if (arq):
        #     arq.write(rede.quantidadeEscondidas.to_bytes(4, byteorder='big'))
        #     arq.write(rede.camadaEntrada.quantidadeNeuronios.to_bytes(4, byteorder='big'))
        #     arq.write(rede.camadaEscondida[0].quantidadeNeuronios.to_bytes(4, byteorder='big'))
        #     arq.write(rede.camadaSaida.quantidadeNeuronios.to_bytes(4, byteorder='big'))
            
        #     for i in range(rede.quantidadeEscondidas):
        #         for j in range(rede.camadaEscondida[i].quantidadeNeuronios):
        #             for k in range(rede.camadaEscondida[i].neuronios[j].quantidadeLigacoes):
        #                 arq.write(str(rede.camadaEscondida[i].neuronios[j].peso[k]).to_bytes(4, byteorder='big'))
        
        #     for i in range(rede.camadaSaida.quantidadeNeuronios):
        #         for j in range(rede.camadaSaida.neuronios[i].quantidadeLigacoes):
        #             arq.write(rede.camadaSaida.neuronios[i].peso[j].to_bytes(4, byteorder='big'))
                    
        #     arq.close()
    
    def RNA_ImprimirPesos(self, rede):
        """
        Funcao que imprime os pesos da rede neural
        :param rede: rede neural que será impressa
        """
        logging.info("Iniciando impressao dos pesos da rede neural")
        pass
    
    def InicializarGeradorAleatorio(self, seed):
        """
        Inicializa gerador randomico
        :param seed: valor de seed
        return: gerador randomico
        """
        logging.info("Gerador randomico")
        return random.seed(seed)
    
    def main(self):
        gerador = self.InicializarGeradorAleatorio(1)
        
        Andre = self.RNA_CriarRedeNeural(5, 2, 10, 1)
        # Andre = self.RNA_CarregarRede("/home/andreruxx/Desktop/simpleAI/rede/rede")

        # for i in range(1000):
        #     print("\n")
        #     self.RNA_BackPropagation(Andre, [0,0], [0])
        #     self.RNA_BackPropagation(Andre, [1,1], [1])
        #     self.RNA_BackPropagation(Andre, [0,1], [1])
        #     self.RNA_BackPropagation(Andre, [1,0], [0])
                
        self.RNA_SalvarRede("/home/andreruxx/Desktop/simpleAI/rede/rede", Andre)
        Andre = self.RNA_DestruirRedeNeural(Andre)
        
        return 0
        
