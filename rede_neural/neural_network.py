import random
from value import Value
class Neuronio:
    def __init__(self,numeroEntradas):
        self.pesos = [Value(random.uniform(-1,1)) for _ in range(numeroEntradas)]
        self.bias = Value(0.0)
    def __call__(self, Xs): # para quando chamar neuronio(lista Dos X)
        assert len(Xs) == len(self.pesos)
        soma = self.bias # Já define como o básico na inicialização pra não ter que definir depois
        for i in range(len(Xs)):
            soma = soma + self.pesos[i] * Xs[i] # produto escalar - cada peso com um correspondente em x
        return soma.tanh() # Tanh criado por nós 
    def parametros(self):
        return self.pesos + [self.bias]
    
    
# TESTE DO NEURONIO UNICO / VENDO ERRO DESCENDO
# n = Neuronio(2)
# entradas = [[0.5, 1.0], [1.0, -1.0], [-0.5, 0.5], [-1.0, -1.0]]
# respostas = [0.8, -0.8, 0.5, -0.9]
# for c in range(101):
#     for elemento in n.parametros():
#         elemento.grad = 0.0
#     erro = Value(0.0)
#     for entrada, resposta in zip(entradas, respostas):
#         previsao = n(entrada)
#         erro = erro + (previsao - resposta) ** 2
#     erro.backward()
#     for p in n.parametros():
#         p.data -= 0.05 * p.grad
#     if(c % 10 == 0):
#         print(erro)
        
        
class Camada:
    def __init__(self, numeroEntradas, numeroNeuronios):
        self.listaNeuronios = []
        for _ in range(numeroNeuronios):
            self.listaNeuronios.append(Neuronio(numeroEntradas))
    def __call__(self, x):
        listaDeSaidas = []
        for neuronio in self.listaNeuronios:
            listaDeSaidas.append(neuronio(x))
            return listaDeSaidas
    def parametros(self):
        listaDeParametros = []
        for neuronio in self.listaNeuronios:
            listaDeParametros += neuronio.parametros()
            return listaDeParametros
c = Camada(2, 3)
saidas = c([Value(0.5), Value(-1.0)])
print(len(saidas))          # 3
print(len(c.parametros()))  # 9