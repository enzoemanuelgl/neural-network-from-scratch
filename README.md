# Neural Network from Scratch

Motor de diferenciação automática em modo reverso (*reverse-mode autodiff*), implementado do zero em Python puro.

Projeto da disciplina de **Cálculo 2 — UFPB**.

## Objetivo

Implementar uma classe `Value` que guarda um número, registra as operações feitas com ele e, ao final, calcula as derivadas parciais de uma expressão em relação a cada uma das suas entradas (backpropagation).

## Teste que valida o motor

Com `x = 2`, `y = 6`, `w = 0` e `b = 0`:

```
E = (w*x + b - y)**2
```

| Grandeza  | Esperado |
|-----------|----------|
| `E.data`  | `36.0`   |
| `w.grad`  | `-24.0`  |
| `b.grad`  | `-12.0`  |

Conferência à mão: `E = (wx + b - y)²`, então `∂E/∂w = 2(wx + b - y)·x = 2(-6)(2) = -24` e `∂E/∂b = 2(wx + b - y) = -12`.

## Estrutura

```
rede_neural/     o motor e, depois, as peças da rede neural
  value.py       a classe Value: +, -, *, ** e backward()
explicacoes/     material para apresentar o projeto
  Explicação Motor Autodiff.ipynb
  grafo_visual.py   desenhos e figuras interativas usados pelo notebook
```

## Progresso

- [x] Motor: soma, subtração, multiplicação, potência e `backward()`
- [ ] Ativação (`tanh` ou `relu`), divisão e exponencial
- [ ] Neurônio, camada e rede completa

## Como rodar

O motor não tem nenhuma dependência externa:

```bash
python rede_neural/value.py
```

O notebook de explicação precisa do Jupyter e do `ipywidgets` (os dois já vêm no Anaconda). Abra `explicacoes/Explicação Motor Autodiff.ipynb` e use **Run All**.
