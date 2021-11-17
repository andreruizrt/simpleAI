from model.camada import Camada
import constants.redeNeural as constants
from model.neuronio import Neuronio


class RedeNeural:
    def __init__(
        self,
        camadaEntrada=Camada(),
        camadaEscondida=Camada(),
        camadaSaida=Camada(),
        QuantidadeEscondidas=0
    ):
        self.camadaEntrada = camadaEntrada
        self.camadaEscondida = camadaEscondida
        self.camadaSaida = camadaSaida
        self.QuantidadeEscondidas = QuantidadeEscondidas

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

        for i in range(rede.camadaEscondida.QuantidadeNeuronios):
            for k in range(rede.camadaEscondida.QuantidadeNeuronios):
                for l in range(rede.camadaSaida.QuantidadeNeuronios):
                    rede.camadaEscondida.neuronios[i].pesos[j] = vetor[l]
                    j += 1

        ########################################################################
        for i in range(rede.camadaSaida.QuantidadeNeuronios):
            for k in range(rede.camadaSaida.QuantidadeNeuronios):
                rede.camadaSaida.neuronios[i].pesos[k] = vetor[k]
                j += 1

    def RNA_CopiarCamadasParaVetor(self, rede, vetor):
        j = 0

        for i in range(rede.camadaEscondida.QuantidadeNeuronios):
            for k in range(rede.camadaEscondida.QuantidadeNeuronios):
                for l in range(rede.camadaSaida.QuantidadeNeuronios):
                    vetor[j] = rede.camadaEscondida.neuronios[i].pesos[j]
                    j += 1

        ########################################################################
        for i in range(rede.camadaSaida.QuantidadeNeuronios):
            for k in range(rede.camadaSaida.QuantidadeNeuronios):
                vetor[j] = rede.camadaSaida.neuronios[i].pesos[k]
                j += 1

    # TODO: Retornar rede
    def RNA_CopiarParaEntrada(self, rede, vetorEntrada):
        for i in range(rede.camadaEntrada.QuantidadeNeuronios - constants.BIAS):
            rede.camadaEntrada.neuronios[i].saida = vetorEntrada[i]

    def RNA_QuatidadePesos(self, rede):
        soma = 0

        for i in range(rede.camadaEscondida.QuantidadeNeuronios):
            for k in range(rede.camadaEscondida.QuantidadeNeuronios):
                soma += rede.camadaEscondida.neuronios[i].QuantidadeLigacoes

            for l in range(rede.camadaSaida.QuantidadeNeuronios):
                soma += rede.camadaSaida.neuronios[l].QuantidadeLigacoes

            return soma

    def RNA_CopiarDaSaida(self, rede, vetorSaida):
        for i in range(rede.camadaSaida.QuantidadeNeuronios):
            vetorSaida[i] = rede.camadaSaida.neuronios[i].saida

    def RNA_CalcularSaida(self, rede):
        for i in range(rede.camadaEscondida.QuantidadeNeuronios):
            soma = 0.0
            for k in range(rede.camadaEntrada.QuantidadeNeuronios - constants.BIAS):
                soma += rede.camadaEntrada.neuronios[k].saida * \
                    rede.camadaEscondida.neuronios[i].pesos[k]
            rede.camadaEscondida.neuronios[i].saida = self.relu(soma)

    """ FUTURE
    def RNA_BackPropagation(self, rede, entrada, saidaEsperada):
        for i in range(rede.camadaSaida.QuantidadeNeuronios):
            rede.camadaSaida.neuronios[i].erro = saidaEsperada[i] - rede.camadaSaida.neuronios[i].saida
            rede.camadaSaida.neuronios[i].erro = rede.camadaSaida.neuronios[i].erro * self.reluDx(rede.camadaSaida.neuronios[i].saida)

        for i in range(rede.camadaEscondida.QuantidadeNeuronios):
            soma = 0.0
            for k in range(rede.camadaSaida.QuantidadeNeuronios):
                soma += rede.camadaSaida.neuronios[k].erro * rede.camadaEscondida.neuronios[i].pesos[k]
            rede.camadaEscondida.neuronios[i].erro = soma * self.reluDx(rede.camadaEscondida.neuronios[i].saida)
    """

    def RNA_CriarNeuronio(neuron=Neuronio(), quantidadeLigacoes=0):
        """
        Funcao que cria um neuronio
        :param neuron: Neuronio
        :param quantidadeLigacoes: Quantidade de ligações que o neuronio terá
        """
        neuron.QuantidadeLigacoes = quantidadeLigacoes
        neuron.peso = [0.0] * quantidadeLigacoes
        
        
