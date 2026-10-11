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

## Progresso

- [ ] Etapa 1: esqueleto da classe (`__init__`, `__repr__`)
- [ ] Etapas 2–8

## Como rodar

Requer Python 3.10+ e nenhuma dependência externa.

```bash
python value.py
```
