import math
class Value:
    #   Inicialização / O que todo valor terá
    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self.grad = 0.0
        self._prev = set(_children)
        self._op = _op
        self._backward = lambda: None



    # O Que aparecerá quando printar
    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"



    #   Soma    
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad * 1.0
            other.grad += out.grad * 1.0

        out._backward = _backward
        return out



    #   Subtração ( Criei um porque se fosse fazer normal eu precisaria inverter o other com o  __mul__ por -1 pra só depois __add__ - criação de 3 nós onde só precisava de 1)
    def __sub__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data - other.data, (self, other), '-')

        def _backward():
            self.grad += out.grad * 1.0
            other.grad += out.grad * (-1.0)

        out._backward = _backward
        return out
    
    
    
    def __rsub__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return other - self
    
    

    #   Multiplicação
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += out.grad * other.data
            other.grad += out.grad * self.data

        out._backward = _backward
        return out



    #   Potenciação
    def __pow__(self, n):
        assert isinstance(n, (int, float)), "expoente deve ser constante"
        out = Value(self.data ** n, (self,), f'**{n}')

        def _backward():
            self.grad += out.grad * (n * self.data ** (n - 1))

        out._backward = _backward
        return out



    #   Transforma em Value independente se o Value estiver na esquerda ou na direita ( permite 2 + v por exemplo )
    __radd__ = __add__
    __rmul__ = __mul__



    #   Inverte o sinal (-x) - Utilizava na subtração antes mas deixarei pra não dar erro quando eu escrever (-x)
    def __neg__(self):
        return self * -1



    #   Tangente hiperbólica - ativação não linear
    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,), 'tanh')

        def _backward():
            self.grad += out.grad * (1 - t**2)

        out._backward = _backward
        return out


#   Colocará 0 se o valor for < 0
    def relu(self):
        out = Value(max(0.0, self.data), (self,), 'relu')

        def _backward():
        #   OBS: em x=0, o gráfico tem um bico, então convencionamos 0 ao em vez de indefinida
            self.grad += out.grad * (1.0 if out.data > 0 else 0.0)

        out._backward = _backward
        return out
    
    
    
    #   Backward
    def backward(self):
        ordem = []
        visitados = set()

        def constroi(v):
            if v not in visitados:
                visitados.add(v)
                for pai in v._prev:
                    constroi(pai)
                ordem.append(v)

        constroi(self)

        self.grad = 1.0
        for no in reversed(ordem):
            no._backward()
