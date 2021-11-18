from numpy.random.mtrand import randint
from numpy import random

from camada import Camada
from neuronio import Neuronio

TAXA_APRENDIZADO = 0.1
TAXA_PESO_INICIAL = 1.0
BIAS = 1
class RedeNeural:

    def __init__(
        self,
        camadaEntrada=Camada(),
        camadaEscondida=Camada(),
        camadaSaida=Camada(),
        quantidadeEscondidas=0
    ):
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
        j = 0

        for i in range(rede.camadaEscondida.quantidadeNeuronios):
            for k in range(rede.camadaEscondida.quantidadeNeuronios):
                for l in range(rede.camadaSaida.quantidadeNeuronios):
                    rede.camadaEscondida.neuronios[i].pesos[j] = vetor[l]
                    j += 1

        ########################################################################
        for i in range(rede.camadaSaida.quantidadeNeuronios):
            for k in range(rede.camadaSaida.quantidadeNeuronios):
                rede.camadaSaida.neuronios[i].pesos[k] = vetor[k]
                j += 1

    def RNA_CopiarCamadasParaVetor(self, rede, vetor):
        j = 0

        for i in range(rede.camadaEscondida.quantidadeNeuronios):
            for k in range(rede.camadaEscondida.quantidadeNeuronios):
                for l in range(rede.camadaSaida.quantidadeNeuronios):
                    vetor[j] = rede.camadaEscondida.neuronios[i].pesos[j]
                    j += 1

        ########################################################################
        for i in range(rede.camadaSaida.quantidadeNeuronios):
            for k in range(rede.camadaSaida.quantidadeNeuronios):
                vetor[j] = rede.camadaSaida.neuronios[i].pesos[k]
                j += 1

    # TODO: Retornar rede
    def RNA_CopiarParaEntrada(self, rede, vetorEntrada):
        for i in range(rede.camadaEntrada.quantidadeNeuronios - BIAS):
            rede.camadaEntrada.neuronios[i].saida = vetorEntrada[i]

    def RNA_QuatidadePesos(self, rede):
        soma = 0

        for i in range(rede.camadaEscondida.quantidadeNeuronios):
            for k in range(rede.camadaEscondida.quantidadeNeuronios):
                soma += rede.camadaEscondida.neuronios[i].quantidadeLigacoes

            for l in range(rede.camadaSaida.quantidadeNeuronios):
                soma += rede.camadaSaida.neuronios[l].quantidadeLigacoes

            return soma

    def RNA_CopiarDaSaida(self, rede, vetorSaida):
        for i in range(rede.camadaSaida.quantidadeNeuronios):
            vetorSaida[i] = rede.camadaSaida.neuronios[i].saida

    def RNA_CalcularSaida(self, rede):
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

    def RNA_CriarNeuronio(self, quantidadeLigacoes=0):
        """
        Funcao que cria um neuronio
        :param neuron: Neuronio
        :param quantidadeLigacoes: quantidade de ligações que o neuronio terá
        """
        neuron = Neuronio()
        neuron.quantidadeLigacoes = quantidadeLigacoes
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
        :param quantidadeEscondidas: quantidade de neuronios na camada escondida
        :param qtdNeuroniosEntrada: quantidade de neuronios na camada de entrada
        :param qtdNeuroniosEscondidos: quantidade de neuronios na camada escondida
        :param qtdNeuroniosSaida: quantidade de neuronios na camada de saida
        """
        
        qtdNeuroniosEntrada += BIAS
        qtdNeuroniosEscondidos += BIAS
        
        rede = RedeNeural()
        rede.camadaEntrada = Camada(qtdNeuroniosEntrada)
        rede.camadaEntrada.neuronios = [Neuronio()] * qtdNeuroniosEntrada
        
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
              qtdNeuroniosEntrada - 1,"neuronio(s) + 1 BIAS.\n",
              quantidadeEscondidas,"Camada(s) escondida(s), cada uma com",
              qtdNeuroniosEscondidos - 1, "neuronio(s) + 1 BIAS.\n1  Camada de saida com",
              qtdNeuroniosSaida,"neuronio(s).\n\n")
                
        return rede
    
    def main(self):
        redePrincipal = RedeNeural()
        redePrincipal = self.RNA_CriarRedeNeural(30, 784, 30, 10)
        
        
        
RedeNeural().main()