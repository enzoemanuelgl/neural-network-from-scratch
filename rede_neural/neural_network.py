import random
from value import Value
class Neuronio:
    def __init__(self,numeroEntradas):
        self.pesos = [Value(random.uniform(-1,1)) for _ in range(numeroEntradas)]
        self.bias = Value(0.0)
    def __call__(self, entradas): # para quando chamar neuronio(lista Dos X)
        assert len(entradas) == len(self.pesos)
        soma = self.bias # Já define como o básico na inicialização pra não ter que definir depois
        for i in range(len(entradas)):
            soma = soma + self.pesos[i] * entradas[i] # produto escalar - cada peso com um correspondente em x
        return soma.tanh() # Tanh criado por nós 
    def parametros(self):
        return self.pesos + [self.bias]
        
class Camada:
    def __init__(self, numeroEntradas, numeroNeuronios):
        # Cria todos os neuronios da camada
        self.listaNeuronios = []
        for _ in range(numeroNeuronios):
            self.listaNeuronios.append(Neuronio(numeroEntradas))
    def __call__(self, x):
        # Junta todas as saídas ( que serão as entradas da próxima camada )
        listaDeSaidas = []
        for neuronio in self.listaNeuronios:
            listaDeSaidas.append(neuronio(x))
        return listaDeSaidas
    def parametros(self):
        # junção dos parametros de todos os neuronios da camada
        listaDeParametros = []
        for neuronio in self.listaNeuronios:
            listaDeParametros += neuronio.parametros()
        return listaDeParametros

class MLP:
    def __init__(self, tamanhos):
        # Cria todas as camadas de modo que a entrada da camada atual 
        # é igual à quantidade de saídas da camada anterior 
        # OBS: O primeiro numero é a quantidade de entradas ( input layer não é camada de fato )
        self.camadas = []
        for i in range(len(tamanhos)-1):
            camada = Camada(tamanhos[i], tamanhos[i+1])
            self.camadas.append(camada)

    def __call__(self, x):
        # Vai passando de camada em camada, passando as saídas de uma
        # camada para a camada seguinte para todas as camadas até o final,
        # retorando "x", que é a output layer
        for camada in  self.camadas:
            x = camada(x)
        return x

    def parametros(self):
        # Junta os parametros de cada camada que, por sua vez, 
        # reune os parametros de cada neurônio
        lista = []
        for camada in self.camadas:
            lista += camada.parametros()
        return lista
        
        
# TESTES ( SÓ PEGAM QUANDO RODAR ESSE ARQUIVO EM ESPECÍFICO )
        
if __name__ == "__main__":
    # TESTE DO NEURONIO UNICO / VENDO ERRO DESCENDO
    n = Neuronio(2)
    entradas = [[0.5, 1.0], [1.0, -1.0], [-0.5, 0.5], [-1.0, -1.0]]
    respostas = [0.8, -0.8, 0.5, -0.9]
    for c in range(101):
        for elemento in n.parametros():
            elemento.grad = 0.0
        erro = Value(0.0)
        for entrada, resposta in zip(entradas, respostas):
            previsao = n(entrada)
            erro += (previsao - resposta) ** 2
        erro.backward()
        for p in n.parametros():
            p.data -= 0.05 * p.grad
        if(c % 10 == 0):
            print(erro.data)
            
    # TESTE - POSSÍVEL VER O ERRO MÉDIO DIMINUINDO PARA CADA
    # UM DOS CASOS EM RELAÇÃO AO ESPERADO ( ERROS APROXIMADAMENTE 
    # 3x - 4x MENORES NOS CASOS DESSES DADOS EM ESPECÍFICO 
    # QUANDO COMPARADO A UM ÚNICO NEURÔNIO )
    rede = MLP([2, 3, 1])
    entradas = [[0.5, 1.0], [1.0, -1.0], [-0.5, 0.5], [-1.0, -1.0]]
    respostas = [0.8, -0.8, 0.5, -0.9]
    for c in range(101):
        for elemento in rede.parametros():
            elemento.grad = 0.0
        erro = Value(0.0)
        for entrada, resposta in zip(entradas, respostas):
            previsao = rede(entrada)[0]
            # Erro = erro + pra poder criar o grafo ( o backward vai voltar todas as camadas )
            erro  = erro + (previsao - resposta) ** 2
        erro.backward()
        for p in rede.parametros():
            p.data -= 0.05 * p.grad
        if(c % 10 == 0):
            if(c == 0):
                print("\n\nValores iniciais ( sem mudanca ainda )")
            print(f"{int(c/10)}a Mudanca: ")
            for entrada, resposta in zip(entradas, respostas):  
                print(entrada, "-->", round(rede(entrada)[0].data, 4), " esperado", resposta)
            print(f"Erro Quadratico: {erro.data:.4f}")
            print("\n\n")