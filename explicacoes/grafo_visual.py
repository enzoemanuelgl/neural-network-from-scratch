"""Figuras do caderno de explicação do motor autodiff.

Este arquivo só desenha. Ele lê o que os objetos Value já guardam
(data, grad, _prev, _op, _backward) e chama os métodos do próprio motor.
As derivadas exatas que aparecem nas figuras vêm do motor. As
aproximações pela definição (com h pequeno) são calculadas aqui de
propósito, para comparar com ele.
"""

import html
import inspect
import math
import random
import uuid

FONTES = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=STIX+Two+Text:ital,wght@0,400;0,600;1,400;1,600'
    '&family=Instrument+Sans:wght@400;500;600&display=swap">'
)

CSS = """
<style>
.ad {
  --papel: #F8FAFB;
  --grade: #E1E9EF;
  --grafite: #2D3237;
  --tinta: #1E3FA0;
  --correcao: #BF1E33;
  --marca: #FFE15A;
  --apagado: #66707A;
  --fio: #C5D2DC;
  --serifa: "STIX Two Text", Cambria, "Cambria Math", "Times New Roman", serif;
  --sem: "Instrument Sans", "Segoe UI", system-ui, sans-serif;
  color: var(--grafite);
  background-color: var(--papel);
  background-image:
    linear-gradient(var(--grade) 1px, transparent 1px),
    linear-gradient(90deg, var(--grade) 1px, transparent 1px);
  background-size: 18px 18px;
  background-position: -1px -1px;
  border: 1px solid var(--fio);
  border-radius: 6px;
  padding: 18px 22px 20px;
  margin: 4px 0;
  font-family: var(--sem);
  font-size: 14px;
  line-height: 1.5;
  text-align: left;
  max-width: 100%;
  box-sizing: border-box;
}
.ad * { box-sizing: border-box; }
/* o Jupyter estiliza tabelas e código das saídas; aqui a folha manda */
.ad table, .ad tr, .ad td, .ad th { background: transparent !important; color: inherit; border: 0;
  margin: 0; table-layout: auto; font-size: inherit; line-height: 1.4; max-width: none; }
.ad code { font-family: Consolas, "Cascadia Mono", monospace; font-size: 0.9em; padding: 1px 5px;
  border-radius: 3px; background: #E8EEF2 !important; color: var(--grafite) !important; }
.ad b { font-weight: 600; }
.ad i { font-style: italic; }

.ad-eq { font-family: var(--serifa); font-size: 24px; line-height: 1.25; margin: 0 0 6px; }
.ad-eq .ad-eq-sub { font-family: var(--sem); font-size: 14px; color: var(--apagado); margin-left: 10px; }
.ad-legenda { display: flex; flex-wrap: wrap; gap: 4px 18px; color: var(--apagado); font-size: 12.5px;
  margin-bottom: 10px; }
.ad-legenda > span { display: inline-flex; align-items: center; gap: 6px; }
.ad-legenda > span > span { display: inline; }
.ad-sw { width: 10px; height: 10px; border-radius: 2px; display: inline-block; }
.ad-ln { width: 24px; height: 0; border-top: 2px solid; display: inline-block; }
.ad-ln.t { border-color: #1E3FA0; }
.ad-ln.tt { border-color: #1E3FA0; border-top-style: dashed; }
.ad-ln.c { border-color: #BF1E33; }
.ad-ln.ct { border-color: #BF1E33; border-top-style: dashed; }
.ad-ln.g { border-color: #2D3237; }
.ad-ln.n { border-color: #8FA3B8; }
.ad-rolagem { overflow-x: auto; }
.ad svg { display: block; }
.ad svg text { font-family: var(--sem); }

/* grafo */
.ad .s-nome { font-family: var(--serifa); font-style: italic; font-size: 19px; fill: var(--grafite); }
.ad .s-expr { font-size: 12.5px; fill: var(--grafite); }
.ad .s-rot { font-size: 11px; fill: var(--apagado); }
.ad .s-dado { font-family: var(--serifa); font-size: 16px; fill: var(--tinta); font-variant-numeric: tabular-nums; }
.ad .s-grad { font-family: var(--serifa); font-size: 16px; fill: var(--correcao); font-variant-numeric: tabular-nums; }
.ad .s-op { font-family: var(--serifa); font-size: 18px; fill: var(--grafite); }
.ad .s-local { font-family: var(--serifa); font-style: italic; font-size: 13.5px; fill: var(--correcao);
  paint-order: stroke; stroke: var(--papel); stroke-width: 4px; stroke-linejoin: round; }
.ad .s-ordem { font-size: 10.5px; font-weight: 600; fill: #fff; }
.ad .s-marca { fill: var(--marca); animation: ad-sumir 2.4s ease-out forwards; }
@keyframes ad-sumir { 0% { opacity: 1; } 60% { opacity: 0.9; } 100% { opacity: 0.4; } }
@media (prefers-reduced-motion: reduce) { .ad .s-marca { animation: none; opacity: 0.55; } }

/* gráficos no plano */
.ad .p-eixo { stroke: var(--grafite); stroke-width: 1.2; }
.ad .p-zero { stroke: #A9B7C3; stroke-width: 1; }
.ad .p-rot { font-size: 12px; fill: var(--apagado); font-variant-numeric: tabular-nums; }
.ad .p-nome { font-family: var(--serifa); font-style: italic; font-size: 17px; fill: var(--grafite); }
.ad .p-nome-t { font-family: var(--serifa); font-style: italic; font-size: 18px; fill: var(--tinta);
  paint-order: stroke; stroke: var(--papel); stroke-width: 4px; }
.ad .p-curva { fill: none; stroke: var(--grafite); stroke-width: 2.2; stroke-linejoin: round; }
.ad .p-modelo { stroke: var(--grafite); stroke-width: 2.6; }
.ad .p-secante { stroke: var(--tinta); stroke-width: 1.9; }
.ad .p-tangente { stroke: var(--correcao); stroke-width: 2; stroke-dasharray: 8 5; }
.ad .p-perna { stroke: var(--tinta); stroke-width: 1.3; stroke-dasharray: 3 3; }
.ad .p-residuo { stroke: var(--apagado); stroke-width: 1.4; stroke-dasharray: 3 3; }
.ad .p-trilha { stroke: var(--tinta); stroke-width: 1.5; opacity: 0.7; }
.ad .p-ponto { fill: var(--tinta); stroke: #fff; stroke-width: 1.5; }
.ad .p-vazado { fill: #fff; stroke: var(--tinta); stroke-width: 2; }
.ad .p-min { fill: var(--grafite); }
.ad .p-nivel { fill: none; stroke: #8FA3B8; stroke-width: 1.1; }
.ad .p-nivel-atual { fill: none; stroke: var(--grafite); stroke-width: 2.2; }
.ad .p-vale { stroke: var(--grafite); stroke-width: 1.6; stroke-dasharray: 6 4; }
.ad .p-seta-c { stroke: var(--correcao); stroke-width: 2.6; }
.ad .p-seta-c2 { stroke: var(--correcao); stroke-width: 2; stroke-dasharray: 5 4; }
.ad .p-seta-t { stroke: var(--tinta); stroke-width: 2.6; }
.ad .p-texto { font-size: 13px; fill: var(--grafite); paint-order: stroke; stroke: var(--papel);
  stroke-width: 4px; stroke-linejoin: round; }
.ad .p-texto-t { font-size: 13px; fill: var(--tinta); paint-order: stroke; stroke: var(--papel); stroke-width: 4px; }
.ad .p-texto-c { font-size: 13.5px; font-weight: 600; fill: var(--correcao); paint-order: stroke;
  stroke: var(--papel); stroke-width: 4px; }

/* superfície em 3D */
.ad .s3-chao { fill: none; stroke: #8D99A6; stroke-width: 1.1; }
.ad .s3-nivel { fill: none; stroke: #9DB0C4; stroke-width: 1.3; }
.ad .s3-malha { fill: none; stroke: #2D3237; stroke-opacity: 0.26; stroke-width: 1; }
.ad .s3-plano { fill: #1E3FA0; fill-opacity: 0.06; stroke: #1E3FA0; stroke-opacity: 0.35; stroke-width: 1; }
.ad .s3-traco { fill: none; stroke: var(--tinta); stroke-width: 3; stroke-linejoin: round; }
.ad .s3-traco2 { fill: none; stroke: var(--tinta); stroke-width: 3; stroke-dasharray: 8 5; }
.ad .s3-tang { stroke: var(--correcao); stroke-width: 2.6; }
.ad .s3-tang2 { stroke: var(--correcao); stroke-width: 2.6; stroke-dasharray: 7 4; }
.ad .s3-eixo { stroke: var(--grafite); stroke-width: 1.2; }

.ad-fig { display: flex; flex-wrap: wrap; gap: 16px 30px; align-items: flex-start; }
.ad-fig > .ad-grafico { flex: 0 1 600px; min-width: 280px; }
.ad-painel { flex: 1 1 230px; min-width: 220px; padding-top: 4px; }
.ad-rotulo { font-size: 12.5px; color: var(--apagado); margin: 12px 0 1px; }
.ad-rotulo:first-child { margin-top: 0; }
.ad-grande { font-family: var(--serifa); font-size: 34px; line-height: 1.1; font-variant-numeric: tabular-nums; }
.ad-grande.t { color: var(--tinta); }
.ad-grande.c { color: var(--correcao); }
.ad-medio { font-family: var(--serifa); font-size: 21px; line-height: 1.2; font-variant-numeric: tabular-nums; }
.ad-medio.t { color: var(--tinta); }
.ad-medio.c { color: var(--correcao); }
.ad-frase { font-size: 14px; margin-top: 12px; max-width: 52ch; }
.ad-frase .ad-conta { font-family: var(--serifa); font-size: 15.5px; font-variant-numeric: tabular-nums; }
.ad-cinza { color: var(--apagado); font-size: 12.5px; }

.ad .ad-h { border-collapse: collapse; margin-top: 14px; font-variant-numeric: tabular-nums; }
.ad .ad-h th { font-weight: 500; font-size: 12px; color: var(--apagado); text-align: right;
  padding: 0 0 4px 16px; border-bottom: 1px solid var(--fio); }
.ad .ad-h td { font-family: var(--serifa); font-size: 15px; text-align: right; padding: 3px 0 3px 16px;
  border-bottom: 1px solid var(--grade); }
.ad .ad-h th:first-child, .ad .ad-h td:first-child { padding-left: 4px; }
.ad .ad-h tr.ad-atual td { background: rgba(255, 225, 90, 0.8) !important; }

/* passo a passo */
.ad-passo { margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--fio); max-width: 860px; }
.ad-passo-n { font-size: 12.5px; color: var(--apagado); margin-bottom: 2px; }
.ad-passo-t { font-family: var(--serifa); font-size: 20px; line-height: 1.3; margin-bottom: 6px; }
.ad-passo-x { font-size: 15px; line-height: 1.55; }
.ad-passo-l { margin: 8px 0 0; padding: 0; list-style: none; }
.ad-passo-l li { font-size: 15px; padding: 3px 0; }
.ad-passo-l .ad-conta { font-family: var(--serifa); font-size: 16.5px; font-variant-numeric: tabular-nums; }
.ad-passo-l .c { color: var(--correcao); font-weight: 600; }
.ad-passo-l .ad-obs { color: var(--apagado); font-size: 13.5px; }
.ad-no { display: inline-block; padding: 0 7px; border: 1px solid var(--grafite); border-radius: 4px;
  background: #fff; font-size: 13.5px; line-height: 1.5; white-space: nowrap; }
.ad-no.nome { font-family: var(--serifa); font-style: italic; font-size: 16px; }

/* laboratório */
.ad-leitura { display: grid; grid-template-columns: minmax(150px, 0.8fr) minmax(280px, 2fr) minmax(200px, 1fr);
  gap: 18px 26px; margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--fio); }
@media (max-width: 760px) { .ad-leitura { grid-template-columns: 1fr; } }
.ad-titulo { font-size: 12.5px; color: var(--apagado); margin: 0 0 4px; }
.ad-erro { font-family: var(--serifa); font-size: 40px; line-height: 1; color: var(--tinta);
  font-variant-numeric: tabular-nums; }
.ad-sub { color: var(--apagado); font-size: 12.5px; margin-top: 6px; }
.ad-sub b { font-family: var(--serifa); font-weight: 400; color: var(--grafite); font-size: 15px; }
.ad .ad-tab { width: 100%; border-collapse: collapse; }
.ad .ad-tab td { padding: 4px 0; vertical-align: baseline; text-align: left; border-bottom: 1px solid var(--grade); }
.ad .ad-tab td.v { font-family: var(--serifa); font-style: italic; font-size: 18px; width: 28px; }
.ad .ad-tab td.g { font-family: var(--serifa); font-size: 17px; color: var(--correcao); width: 84px;
  font-variant-numeric: tabular-nums; text-align: right; padding-right: 14px; }
.ad .ad-tab td.t { color: var(--apagado); font-size: 12.5px; }
.ad .ad-tab td.t b { color: var(--grafite); font-weight: 500; font-variant-numeric: tabular-nums; }
.ad .ad-tab tr.sep td { padding-top: 10px; font-size: 11.5px; color: var(--apagado); border-bottom: 0; }
.ad .ad-curva text { font-size: 11px; fill: var(--apagado); }

/* tabelas de conferência */
.ad .ad-conf { border-collapse: collapse; font-variant-numeric: tabular-nums; margin-top: 6px; }
.ad .ad-conf th { text-align: right; font-weight: 500; font-size: 12.5px; color: var(--apagado);
  padding: 4px 0 6px 24px; border-bottom: 1px solid var(--fio); }
.ad .ad-conf td { font-family: var(--serifa); font-size: 16px; text-align: right; padding: 5px 0 5px 24px;
  border-bottom: 1px solid var(--grade); }
.ad .ad-conf th:first-child, .ad .ad-conf td:first-child { text-align: left; padding-left: 0; }
.ad .ad-conf td.v { font-style: italic; }
.ad .ad-conf td.cx { color: var(--apagado); font-family: var(--sem); font-size: 12.5px; }
.ad .ad-conf tr.caso td { font-family: var(--sem); font-size: 12.5px; color: var(--apagado); text-align: left;
  padding: 14px 0 2px; border-bottom: 0; }
.ad-ok { color: var(--tinta); font-weight: 600; }
.ad-ruim { color: var(--correcao); font-weight: 600; }
</style>
"""


def _W():
    import ipywidgets
    return ipywidgets


def _mostra(conteudo):
    from IPython.display import HTML, display
    display(HTML(conteudo))


def _exibe(widget):
    from IPython.display import display
    display(widget)


# ------------------------------------------------------------------ números

def fmt(v, casas=4):
    """36.0 -> '36.0', -0.25 -> '−0.25', 1.23456789 -> '1.2346'."""
    v = float(v)
    if math.isnan(v) or math.isinf(v):
        return "∞" if v > 0 else ("−∞" if v < 0 else "?")
    if abs(v) < 0.5 * 10 ** -casas:
        v = 0.0
    s = f"{v:.{casas}f}".rstrip("0")
    if s.endswith("."):
        s += "0"
    if s == "-0.0":
        s = "0.0"
    return s.replace("-", "−")


def _num(v):
    """Inteiros sem casa decimal (2 em vez de 2.0)."""
    v = float(v)
    if v.is_integer() and abs(v) < 1e12:
        return str(int(v)).replace("-", "−")
    return fmt(v)


def _par(v):
    """Número negativo entre parênteses, para aparecer dentro de uma conta."""
    return f"({fmt(v)})" if float(v) < 0 else fmt(v)


def _vetor(a, b, casas=4):
    return f"({fmt(a, casas)}, {fmt(b, casas)})"


_SOBRESCRITO = str.maketrans("0123456789-.", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻·")


def _sobrescrito(n):
    n = float(n)
    if n.is_integer():
        return str(int(n)).translate(_SOBRESCRITO)
    return "^" + fmt(n)


def _intervalo(a, b, n):
    return [a + (b - a) * i / n for i in range(n + 1)]


# ------------------------------------------------------------------ leitura do grafo

def _operandos(v):
    """Filhos de v na ordem da conta (a − b, e não b − a).

    _prev é um set e perde a ordem. A ordem certa está nas variáveis
    que o _backward de cada operação guardou (self e other).
    """
    fn = v._backward
    celulas = getattr(fn, "__closure__", None)
    nomes = getattr(getattr(fn, "__code__", None), "co_freevars", ())
    if celulas and nomes:
        amb = dict(zip(nomes, (c.cell_contents for c in celulas)))
        ops = [amb[k] for k in ("self", "other") if k in amb and isinstance(amb[k], type(v))]
        if ops:
            return ops
    return list(v._prev)


def _unicos(lista):
    vistos, saida = set(), []
    for item in lista:
        if item not in vistos:
            vistos.add(item)
            saida.append(item)
    return saida


def _topo(raiz):
    """A mesma ordem topológica que Value.backward() monta."""
    ordem, vistos = [], set()

    def constroi(v):
        if v not in vistos:
            vistos.add(v)
            for filho in v._prev:
                constroi(filho)
            ordem.append(v)

    constroi(raiz)
    return ordem


def _derivadas_locais(v):
    """∂v/∂filho para cada filho, rodando o próprio _backward de v com v.grad = 1."""
    filhos = list(v._prev)
    if not filhos:
        return {}
    guardado = {f: f.grad for f in filhos}
    guardado_v = v.grad
    for f in filhos:
        f.grad = 0.0
    v.grad = 1.0
    v._backward()
    locais = {f: f.grad for f in filhos}
    for f, g in guardado.items():
        f.grad = g
    v.grad = guardado_v
    return locais


_PREC = {"+": 1, "-": 1, "*": 2}
_SIMBOLO = {"+": " + ", "-": " − ", "*": "·"}
_GLIFO = {"+": "+", "-": "−", "*": "×"}


def _expressao(v, nomes, memo):
    """Texto da conta que gerou v, por exemplo 'w·x + b − y'."""
    if v in memo:
        return memo[v]
    if v in nomes:
        r = (nomes[v], 9)
    elif not v._prev:
        r = (_num(v.data), 9 if v.data >= 0 else 0)
    else:
        op, ops = v._op, _operandos(v)
        if op in _PREC and len(ops) == 2:
            (a, pa), (b, pb) = (_expressao(o, nomes, memo) for o in ops)
            p = _PREC[op]
            if pa < p:
                a = f"({a})"
            if pb < p or (op == "-" and pb == p):
                b = f"({b})"
            r = (a + _SIMBOLO[op] + b, p)
        elif op.startswith("**") and ops:
            base, pb = _expressao(ops[0], nomes, memo)
            if pb < 9:
                base = f"({base})"
            r = (base + _sobrescrito(op[2:]), 3)
        else:
            r = (f"{op or '?'}(" + ", ".join(_expressao(o, nomes, memo)[0] for o in ops) + ")", 9)
    memo[v] = r
    return r


def _rotulos(raiz, nomes_por_valor):
    memo = {}
    return {v: _expressao(v, nomes_por_valor, memo)[0] for v in _topo(raiz)}


def _letra(c):
    return c.isascii() and (c.isalnum() or c == "_")


def _italico_vars(texto, nomes):
    """Põe em itálico os nomes de variáveis dentro de um texto de conta."""
    saida, i = [], 0
    ordenados = sorted(nomes, key=len, reverse=True)
    while i < len(texto):
        for n in ordenados:
            antes_ok = i == 0 or not _letra(texto[i - 1])
            depois_ok = i + len(n) >= len(texto) or not _letra(texto[i + len(n)])
            if n and texto.startswith(n, i) and antes_ok and depois_ok:
                saida.append(f"<i>{html.escape(n)}</i>")
                i += len(n)
                break
        else:
            saida.append(html.escape(texto[i]))
            i += 1
    return "".join(saida)


# ------------------------------------------------------------------ grafo computacional

COL, LARG, ALT, LINHA, R_OP = 236, 140, 70, 94, 16


def _layout(raiz, ordem):
    rank, pais = {}, {v: [] for v in ordem}
    for v in ordem:
        for f in v._prev:
            pais[f].append(v)
        rank[v] = 0 if not v._prev else 1 + max(rank[f] for f in v._prev)
    for v in ordem:
        if not v._prev and pais[v]:
            rank[v] = min(rank[p] for p in pais[v]) - 1
    menor = min(rank.values())
    rank = {v: r - menor for v, r in rank.items()}

    # folhas em sequência (busca a partir da raiz); contas na média dos operandos
    linha, prox = {}, [0]

    def posiciona(v):
        if v in linha:
            return linha[v]
        ops = _unicos(_operandos(v)) if v._prev else []
        if not ops:
            linha[v] = prox[0]
            prox[0] += 1
        else:
            alturas = [posiciona(o) for o in ops]
            linha[v] = sum(alturas) / len(alturas)
        return linha[v]

    posiciona(raiz)
    for v in ordem:
        if v not in linha:
            linha[v] = prox[0]
            prox[0] += 1
    return rank, linha, prox[0]


def _svg(raiz, nomes, parametros=(), mudou=None, ordem_backward=None, atual=None):
    mudou = mudou or {}
    ordem = _topo(raiz)
    memo = {}
    rotulo = {v: _expressao(v, nomes, memo)[0] for v in ordem}
    rank, linha, n_linhas = _layout(raiz, ordem)

    if ordem_backward is None:
        ordem_backward = {}
        if raiz.grad != 0.0:
            for v in reversed(ordem):
                if v._prev:
                    ordem_backward[v] = len(ordem_backward) + 1

    uid = uuid.uuid4().hex[:8]
    esq, topo = 60, 34
    largura = esq + max(rank.values()) * COL + LARG + 20
    altura = topo + max(0, n_linhas - 1) * LINHA + ALT + 18

    def pos(v):
        return esq + rank[v] * COL, topo + linha[v] * LINHA

    p = [f'<svg width="{largura:.0f}" height="{altura:.0f}" viewBox="0 0 {largura:.0f} {altura:.0f}" '
         f'style="max-width:100%;height:auto" role="img" '
         f'aria-label="Grafo computacional de {html.escape(rotulo[raiz])}">',
         f'<defs><marker id="ad-seta-{uid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
         'markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9" fill="none" '
         'stroke="#2D3237" stroke-width="1.6"/></marker></defs>']

    # arestas primeiro, para ficarem atrás dos nós
    rotulos_arestas = []
    for v in ordem:
        if not v._prev:
            continue
        vx, vy = pos(v)
        ox, oy = vx - 32, vy + ALT / 2
        locais = _derivadas_locais(v) if v in ordem_backward else {}
        for f in v._prev:
            fx, fy = pos(f)
            sx, sy = fx + LARG, fy + ALT / 2
            ex, ey = ox - R_OP - 2, oy
            dx = max(26, (ex - sx) / 2)
            c1, c2 = (sx + dx, sy), (ex - dx, ey)
            if rank[v] - rank[f] >= 2:
                # aresta que pula colunas: faz um arco por cima dos nós do meio
                alto = min(sy, ey) - 0.6 * LINHA
                c1, c2 = (sx + dx, alto), (ex - dx, alto)
            p.append(f'<path d="M{sx:.1f},{sy:.1f} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} '
                     f'{ex:.1f},{ey:.1f}" fill="none" stroke="#8D99A6" stroke-width="1.3" '
                     f'marker-end="url(#ad-seta-{uid})"/>')
            if f in locais:
                mx = 0.125 * sx + 0.375 * c1[0] + 0.375 * c2[0] + 0.125 * ex
                my = 0.125 * sy + 0.375 * c1[1] + 0.375 * c2[1] + 0.125 * ey - 8
                rotulos_arestas.append(
                    f'<text class="s-local" x="{mx:.1f}" y="{my:.1f}" text-anchor="middle">'
                    f'×{fmt(locais[f])}<title>derivada parcial local de {html.escape(rotulo[v])} em relação a '
                    f'{html.escape(rotulo[f])} = {fmt(locais[f])}</title></text>')
        p.append(f'<line x1="{ox + R_OP}" y1="{oy}" x2="{vx}" y2="{oy}" stroke="#8D99A6" stroke-width="1.3"/>')

    for v in ordem:
        x, y = pos(v)
        nome = rotulo[v]
        dado_mudou, grad_mudou = mudou.get(v, (False, False))
        borda = 2.3 if nome in parametros else 1.1
        p.append(f'<g><title>{html.escape(nome)}\ndata = {v.data!r}\ngrad = {v.grad!r}</title>')
        p.append(f'<rect x="{x}" y="{y}" width="{LARG}" height="{ALT}" rx="4" fill="#FFFFFF" '
                 f'stroke="#2D3237" stroke-width="{borda}"/>')
        if v in nomes:
            p.append(f'<text class="s-nome" x="{x + 11}" y="{y + 21}">{html.escape(nome)}</text>')
        else:
            curto = nome if len(nome) <= 20 else nome[:19] + "…"
            p.append(f'<text class="s-expr" x="{x + 11}" y="{y + 19}">{html.escape(curto)}</text>')
        if nome in parametros:
            p.append(f'<text class="s-rot" x="{x + LARG - 10}" y="{y + 19}" text-anchor="end">parâmetro</text>')
        p.append(f'<line x1="{x + 1}" y1="{y + 28}" x2="{x + LARG - 1}" y2="{y + 28}" stroke="#E3E9EE"/>')
        for i, (rot, val, cls, marcar) in enumerate(
                (("data", v.data, "s-dado", dado_mudou), ("grad", v.grad, "s-grad", grad_mudou))):
            ty = y + 46 + i * 18
            if marcar:
                p.append(f'<rect class="s-marca" x="{x + LARG - 78}" y="{ty - 13}" width="70" height="17" rx="2"/>')
            p.append(f'<text class="s-rot" x="{x + 11}" y="{ty}">{rot}</text>')
            p.append(f'<text class="{cls}" x="{x + LARG - 10}" y="{ty}" text-anchor="end">{fmt(val)}</text>')
        p.append('</g>')

    for v in ordem:
        if not v._prev:
            continue
        x, y = pos(v)
        ox, oy = x - 32, y + ALT / 2
        op = v._op
        potencia = op.startswith("**")
        glifo = "(·)" + _sobrescrito(op[2:]) if potencia else _GLIFO.get(op, op)
        tam = ' style="font-size:14px"' if potencia else ""
        if v is atual:
            p.append(f'<circle cx="{ox}" cy="{oy}" r="{R_OP + 5}" fill="none" stroke="#BF1E33" '
                     f'stroke-width="1.5" stroke-dasharray="3 3"/>')
            p.append(f'<circle cx="{ox}" cy="{oy}" r="{R_OP}" fill="#FDECEE" stroke="#BF1E33" stroke-width="2.2"/>')
        else:
            p.append(f'<circle cx="{ox}" cy="{oy}" r="{R_OP}" fill="#FFFFFF" stroke="#2D3237" stroke-width="1.1"/>')
        p.append(f'<text class="s-op" x="{ox}" y="{oy + 6}" text-anchor="middle"{tam}>{html.escape(glifo)}</text>')
        if v in ordem_backward:
            bx, by = ox + 13, oy - 14
            p.append(f'<circle cx="{bx}" cy="{by}" r="8.5" fill="#BF1E33"/>')
            p.append(f'<text class="s-ordem" x="{bx}" y="{by + 3.8}" text-anchor="middle">'
                     f'{ordem_backward[v]}</text>')

    p.extend(rotulos_arestas)
    p.append("</svg>")
    return "".join(p), rotulo


def _cabecalho(raiz, nomes_por_valor):
    nome_raiz = nomes_por_valor.get(raiz)
    corpo = _expressao(raiz, {k: v for k, v in nomes_por_valor.items() if k is not raiz}, {})[0]
    eq = f"{nome_raiz} = {corpo}" if nome_raiz else corpo
    return f'<div class="ad-eq">{_italico_vars(eq, set(nomes_por_valor.values()))}</div>'


def _legenda_grafo(voltou, nome_raiz="E"):
    r = html.escape(nome_raiz)
    itens = ['<span><i class="ad-sw" style="background:#1E3FA0"></i><span>data: o valor, calculado na ida</span></span>',
             f'<span><i class="ad-sw" style="background:#BF1E33"></i><span>grad: a derivada parcial ∂{r}/∂(nó), '
             'calculada na volta</span></span>']
    if voltou:
        itens += ['<span><b style="color:#BF1E33;font-weight:500">×k</b><span>na aresta: derivada parcial local</span></span>',
                  '<span><i class="ad-sw" style="background:#BF1E33;border-radius:50%"></i>'
                  '<span>ordem em que a volta passou</span></span>']
    else:
        itens.append('<span>todo grad ainda é 0: a volta não começou</span>')
    return '<div class="ad-legenda">' + "".join(itens) + "</div>"


def html_grafo(raiz, parametros=(), mudou=None, ordem_backward=None, atual=None, rodape="",
               voltou=None, **nomes):
    """HTML (texto) com o grafo de `raiz`. Os nomes vêm como argumentos: html_grafo(E, E=E, x=x)."""
    nomes_por_valor = {v: k for k, v in nomes.items()}
    svg, _ = _svg(raiz, nomes_por_valor, set(parametros), mudou, ordem_backward, atual)
    if voltou is None:
        voltou = bool(ordem_backward) if ordem_backward is not None else raiz.grad != 0.0
    return (FONTES + CSS + '<div class="ad">' + _cabecalho(raiz, nomes_por_valor)
            + _legenda_grafo(voltou, nomes_por_valor.get(raiz, "E"))
            + f'<div class="ad-rolagem">{svg}</div>' + rodape + "</div>")


def desenha(raiz, parametros=(), **nomes):
    """Mostra o grafo de `raiz` na célula. Exemplo: desenha(E, parametros=("w",), E=E, w=w, x=x)."""
    _mostra(html_grafo(raiz, parametros=parametros, **nomes))


# ------------------------------------------------------------------ o erro do neurônio, E(w, b)

def _erro_de(exemplos):
    """E(w, b) = soma de (w·x + b − y)² nos exemplos. Funciona com float e com Value."""
    def E(w, b):
        return sum((w * x + b - y) ** 2 for x, y in exemplos)
    return E


def _gradiente(Value, exemplos, w, b):
    """E e as duas derivadas parciais, calculadas pelo motor."""
    wv, bv = Value(float(w)), Value(float(b))
    E = _erro_de(exemplos)(wv, bv)
    E.backward()
    return E.data, wv.grad, bv.grad


def _minimos(exemplos):
    """Onde ∇E = 0: ('ponto', w, b) se o mínimo é único, ('reta', x0, y0) se é a reta x0·w + b = y0."""
    n = len(exemplos)
    sx = sum(x for x, _ in exemplos)
    sxx = sum(x * x for x, _ in exemplos)
    sy = sum(y for _, y in exemplos)
    sxy = sum(x * y for x, y in exemplos)
    det = sxx * n - sx * sx
    if abs(det) < 1e-12:
        return ("reta", sx / n, sy / n)
    return ("ponto", (n * sxy - sx * sy) / det, (sxx * sy - sx * sxy) / det)


def _formula_erro(exemplos):
    if len(exemplos) == 1:
        x, y = exemplos[0]
        termo = "<i>w</i>" if x == 1 else f"{_num(x)}<i>w</i>"
        sinal = "−" if y >= 0 else "+"
        return f"({termo} + <i>b</i> {sinal} {_num(abs(y))})²"
    return "Σ (<i>w</i>·<i>x</i> + <i>b</i> − <i>y</i>)²"


def _nome_dados(exemplos):
    return "1 exemplo: x = {}, y = {}".format(*map(_num, exemplos[0])) if len(exemplos) == 1 \
        else f"{len(exemplos)} exemplos"


# ------------------------------------------------------------------ planos cartesianos

def _ticks(a, b, alvo=6):
    bruto = (b - a) / alvo
    mag = 10 ** math.floor(math.log10(bruto))
    passo = next(m * mag for m in (1, 2, 2.5, 5, 10) if bruto <= m * mag)
    t = math.ceil(a / passo - 1e-9) * passo
    saida = []
    while t <= b + 1e-9:
        saida.append(round(t, 10))
        t += passo
    return saida


class _Plano:
    """Um plano cartesiano em SVG, desenhado na mesma folha quadriculada."""

    def __init__(self, xlim, ylim, larg=600, alt=360, margens=(50, 18, 40, 16)):
        (self.x0, self.x1), (self.y0, self.y1) = xlim, ylim
        self.L, self.A = larg, alt
        self.me, self.md, self.mb, self.mc = margens
        self.uid = uuid.uuid4().hex[:8]
        self.cortado, self.livre, self.base = [], [], []

    def sx(self, x):
        return self.me + (x - self.x0) / (self.x1 - self.x0) * (self.L - self.me - self.md)

    def sy(self, y):
        return self.A - self.mb - (y - self.y0) / (self.y1 - self.y0) * (self.A - self.mb - self.mc)

    def eixos(self, nome_x, nome_y, ticks_x=None, ticks_y=None):
        e, d = self.sx(self.x0), self.sx(self.x1)
        baixo, cima = self.sy(self.y0), self.sy(self.y1)
        if self.y0 < 0 < self.y1:
            self.base.append(f'<line class="p-zero" x1="{e}" y1="{self.sy(0):.1f}" x2="{d}" y2="{self.sy(0):.1f}"/>')
        if self.x0 < 0 < self.x1:
            self.base.append(f'<line class="p-zero" x1="{self.sx(0):.1f}" y1="{baixo}" x2="{self.sx(0):.1f}" y2="{cima}"/>')
        self.base.append(f'<line class="p-eixo" x1="{e}" y1="{baixo}" x2="{d}" y2="{baixo}"/>')
        self.base.append(f'<line class="p-eixo" x1="{e}" y1="{baixo}" x2="{e}" y2="{cima}"/>')
        for t in (ticks_x or _ticks(self.x0, self.x1)):
            px = self.sx(t)
            self.base.append(f'<line class="p-eixo" x1="{px:.1f}" y1="{baixo}" x2="{px:.1f}" y2="{baixo + 5}"/>')
            self.base.append(f'<text class="p-rot" x="{px:.1f}" y="{baixo + 19}" text-anchor="middle">{_num(t)}</text>')
        for t in (ticks_y or _ticks(self.y0, self.y1)):
            py = self.sy(t)
            self.base.append(f'<line class="p-eixo" x1="{e - 5}" y1="{py:.1f}" x2="{e}" y2="{py:.1f}"/>')
            self.base.append(f'<text class="p-rot" x="{e - 9}" y="{py + 4:.1f}" text-anchor="end">{_num(t)}</text>')
        self.base.append(f'<text class="p-nome" x="{d}" y="{baixo + 34}" text-anchor="end">{html.escape(nome_x)}</text>')
        self.base.append(f'<text class="p-nome" x="{e - 9}" y="{cima + 6}" text-anchor="end">{html.escape(nome_y)}</text>')

    def curva(self, f, cls="p-curva", n=320):
        pts = []
        for i in range(n + 1):
            x = self.x0 + (self.x1 - self.x0) * i / n
            try:
                y = float(f(x))
            except (OverflowError, ZeroDivisionError, ValueError):
                continue
            y = max(min(y, self.y1 + (self.y1 - self.y0)), self.y0 - (self.y1 - self.y0))
            pts.append(f"{self.sx(x):.1f},{self.sy(y):.1f}")
        self.cortado.append(f'<polyline class="{cls}" points="{" ".join(pts)}"/>')

    def reta(self, xa, ya, m, cls, de=None, ate=None):
        de = self.x0 if de is None else de
        ate = self.x1 if ate is None else ate
        self.seg(de, ya + m * (de - xa), ate, ya + m * (ate - xa), cls)

    def _px(self, x, y):
        limite = 1e5
        return (max(-limite, min(limite, self.sx(x))), max(-limite, min(limite, self.sy(y))))

    def seg(self, xa, ya, xb, yb, cls, livre=False, seta=None):
        if not all(math.isfinite(v) for v in (xa, ya, xb, yb)):
            return
        (pxa, pya), (pxb, pyb) = self._px(xa, ya), self._px(xb, yb)
        extra = f' marker-end="url(#ad-pseta-{seta}-{self.uid})"' if seta else ""
        alvo = self.livre if livre else self.cortado
        alvo.append(f'<line class="{cls}" x1="{pxa:.1f}" y1="{pya:.1f}" x2="{pxb:.1f}" y2="{pyb:.1f}"{extra}/>')

    def segmentos(self, segs, cls):
        if not segs:
            return
        d = " ".join(f"M{self.sx(a[0]):.1f},{self.sy(a[1]):.1f} L{self.sx(b[0]):.1f},{self.sy(b[1]):.1f}"
                     for a, b in segs)
        self.cortado.append(f'<path class="{cls}" d="{d}"/>')

    def ponto(self, x, y, cls="p-ponto", r=5.5):
        if not (math.isfinite(x) and math.isfinite(y)):
            return
        px, py = self._px(x, y)
        self.cortado.append(f'<circle class="{cls}" cx="{px:.1f}" cy="{py:.1f}" r="{r}"/>')

    def texto(self, x, y, s, cls="p-texto", ancora="start", dx=0, dy=0, html_pronto=False):
        conteudo = s if html_pronto else html.escape(s)
        px, py = self._px(x, y)
        self.livre.append(f'<text class="{cls}" x="{px + dx:.1f}" y="{py + dy:.1f}" '
                          f'text-anchor="{ancora}">{conteudo}</text>')

    def dentro(self, x, y):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1

    def svg(self):
        e, d = self.sx(self.x0), self.sx(self.x1)
        baixo, cima = self.sy(self.y0), self.sy(self.y1)
        cores = {"c": "#BF1E33", "t": "#1E3FA0", "g": "#2D3237"}
        marcadores = "".join(
            f'<marker id="ad-pseta-{k}-{self.uid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{cor}"/></marker>'
            for k, cor in cores.items())
        return (f'<svg width="{self.L}" height="{self.A}" viewBox="0 0 {self.L} {self.A}" '
                f'style="max-width:100%;height:auto" role="img">'
                f'<defs><clipPath id="ad-clip-{self.uid}"><rect x="{e}" y="{cima}" width="{d - e}" '
                f'height="{baixo - cima}"/></clipPath>{marcadores}</defs>'
                + "".join(self.base)
                + f'<g clip-path="url(#ad-clip-{self.uid})">' + "".join(self.cortado) + "</g>"
                + "".join(self.livre) + "</svg>")


class _Grade:
    """Valores de f numa grade, para tirar curvas de nível (marching squares)."""

    def __init__(self, f, xlim, ylim, n=64):
        self.n = n
        self.xs = _intervalo(xlim[0], xlim[1], n)
        self.ys = _intervalo(ylim[0], ylim[1], n)
        self.Z = [[float(f(x, y)) for x in self.xs] for y in self.ys]

    def contorno(self, c):
        xs, ys, Z, n = self.xs, self.ys, self.Z, self.n
        segs = []
        for j in range(n):
            for i in range(n):
                cantos = ((xs[i], ys[j], Z[j][i]), (xs[i + 1], ys[j], Z[j][i + 1]),
                          (xs[i + 1], ys[j + 1], Z[j + 1][i + 1]), (xs[i], ys[j + 1], Z[j + 1][i]))
                pts = []
                for k in range(4):
                    x1, y1, z1 = cantos[k]
                    x2, y2, z2 = cantos[(k + 1) % 4]
                    if (z1 > c) != (z2 > c):      # cada vértice fica de um lado só: sem buracos
                        t = (c - z1) / (z2 - z1)
                        pts.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
                if len(pts) == 2:
                    segs.append((pts[0], pts[1]))
                elif len(pts) == 4:
                    segs += [(pts[0], pts[1]), (pts[2], pts[3])]
        return segs


def _marca_minimo(pl, exemplos, lim):
    tipo, a, c = _minimos(exemplos)
    if tipo == "ponto":
        pl.ponto(a, c, "p-min", r=4.5)
        pl.texto(a, c, f"mínimo ({_num(round(a, 3))}, {_num(round(c, 3))})", "p-texto", "start", dx=9, dy=17)
        return
    x0, y0 = a, c          # a reta x0·w + b = y0
    w1, w2 = lim
    pl.seg(w1, y0 - x0 * w1, w2, y0 - x0 * w2, "p-vale")
    visiveis = [w for w in _intervalo(w1, w2, 200) if lim[0] <= y0 - x0 * w <= lim[1]]
    if visiveis:
        wm = visiveis[int(len(visiveis) * 0.18)]
        termo = "w" if x0 == 1 else f"{_num(x0)}w"
        direita = pl.sx(wm) > (pl.sx(pl.x0) + pl.sx(pl.x1)) / 2
        pl.texto(wm, y0 - x0 * wm, f"reta de mínimos: {termo} + b = {_num(y0)}", "p-texto",
                 "end" if direita else "start", dx=-10 if direita else 10, dy=-4)


def _folha(cabecalho, legenda, grafico, painel):
    return (FONTES + CSS + '<div class="ad">' + cabecalho + legenda
            + f'<div class="ad-fig"><div class="ad-grafico">{grafico}</div>'
            + f'<div class="ad-painel">{painel}</div></div></div>')


def _legenda(*itens):
    return '<div class="ad-legenda">' + "".join(f"<span>{a}<span>{b}</span></span>" for a, b in itens) + "</div>"


# ------------------------------------------------------------------ 1. derivada: da secante à tangente

class Derivada:
    """Reta secante encostando na tangente conforme h diminui."""

    def __init__(self, Value, f, x0=3.0, xlim=(0.0, 5.0), nome="x²", hs=(1, 0.5, 0.25, 0.1, 0.01, 0.001)):
        W = _W()
        self.f, self.x0, self.xlim, self.nome = f, float(x0), xlim, nome
        self.hs = [float(h) for h in hs]
        v = Value(self.x0)
        saida = f(v)
        saida.backward()
        self.derivada = v.grad          # a inclinação da tangente vem do motor
        self.y0 = float(f(self.x0))
        amostras = [float(f(xlim[0] + i * (xlim[1] - xlim[0]) / 200)) for i in range(201)]
        lo, hi = min(amostras), max(amostras)
        folga = (hi - lo) * 0.1
        self.ylim = (min(0.0, lo - folga), hi + folga)
        self.h = W.SelectionSlider(options=[(f"{h:g}", h) for h in self.hs], value=self.hs[0],
                                   description="h", continuous_update=True,
                                   style={"description_width": "24px"}, layout=W.Layout(width="380px"))
        self.h.observe(lambda _: self._desenha(), names="value")
        self.quadro = W.HTML()
        self.widget = W.VBox([self.h, self.quadro])
        self._desenha()

    def _desenha(self):
        h, x0, y0, f = self.h.value, self.x0, self.y0, self.f
        x1, y1 = x0 + h, float(f(x0 + h))
        razao = (y1 - y0) / h
        a = _num(x0)

        pl = _Plano(self.xlim, self.ylim)
        pl.eixos("x", "y")
        pl.curva(f)
        pl.reta(x0, y0, self.derivada, "p-tangente")
        pl.reta(x0, y0, razao, "p-secante")
        pl.seg(x0, y0, x1, y0, "p-perna")
        pl.seg(x1, y0, x1, y1, "p-perna")
        if pl.sx(x1) - pl.sx(x0) > 34:
            pl.texto((x0 + x1) / 2, y0, "h", "p-nome", "middle", dy=20)
        if pl.sy(y0) - pl.sy(y1) > 30:
            pl.texto(x1, (y0 + y1) / 2, f"f({a} + h) − f({a})", "p-texto-t", dx=8, dy=4)
        pl.ponto(x0, y0)
        pl.ponto(x1, y1, "p-vazado", r=5)
        pl.texto(x0, y0, f"({a}, {_num(y0)})", "p-texto", "end", dx=-10, dy=-8)

        linhas = []
        for hh in self.hs:
            r = (float(f(x0 + hh)) - y0) / hh
            classe = ' class="ad-atual"' if hh == h else ""
            linhas.append(f"<tr{classe}><td>{hh:g}</td><td>{fmt(f(x0 + hh), 6)}</td><td>{fmt(r, 6)}</td></tr>")
        tabela = ('<table class="ad-h"><tr><th>h</th><th>f(' + a + ' + h)</th><th>razão incremental</th></tr>'
                  + "".join(linhas) + "</table>")

        painel = (f'<div class="ad-rotulo">razão incremental (f({a} + h) − f({a})) / h: inclinação da secante</div>'
                  f'<div class="ad-grande t">{fmt(razao, 6)}</div>'
                  f'<div class="ad-rotulo">derivada f′({a}): o limite quando h → 0</div>'
                  f'<div class="ad-grande c">{fmt(self.derivada)}</div>' + tabela)
        cab = (f'<div class="ad-eq"><i>f</i>(<i>x</i>) = {_italico_vars(self.nome, {"x"})}'
               f'<span class="ad-eq-sub">no ponto <i>x</i> = {a}</span></div>')
        leg = _legenda(('<i class="ad-ln g"></i>', "a curva <i>f</i>(<i>x</i>)"),
                       ('<i class="ad-ln t"></i>', "reta secante, pelos dois pontos"),
                       ('<i class="ad-ln ct"></i>', "reta tangente: o coeficiente angular dela é a derivada"))
        self.quadro.value = _folha(cab, leg, pl.svg(), painel)


def derivada_interativa(Value, f, x0=3.0, xlim=(0.0, 5.0), nome="x²"):
    _exibe(Derivada(Value, f, x0=x0, xlim=xlim, nome=nome).widget)


# ------------------------------------------------------------------ 3. a superfície e os traços

class Superficie:
    """O gráfico de E(w, b) em 3D, com os dois traços que definem as derivadas parciais."""

    def __init__(self, Value, exemplos, wlim=(-1.0, 5.0), blim=(-2.0, 8.0), Emax=60.0,
                 w0=0.0, b0=0.0, giro=-58, niveis_chao=(4.0, 16.0, 36.0)):
        W = _W()
        self.Value = Value
        self.exemplos = [(float(x), float(y)) for x, y in exemplos]
        self.E = _erro_de(self.exemplos)
        self.wlim, self.blim, self.Emax = wlim, blim, float(Emax)
        estilo = {"description_width": "44px"}
        self.sw = W.FloatSlider(value=float(w0), min=wlim[0], max=wlim[1], step=0.1, description="w₀",
                                readout_format=".1f", style=estilo, layout=W.Layout(width="290px"))
        self.sb = W.FloatSlider(value=float(b0), min=blim[0], max=blim[1], step=0.1, description="b₀",
                                readout_format=".1f", style=estilo, layout=W.Layout(width="290px"))
        self.sg = W.IntSlider(value=giro, min=-180, max=180, step=2, description="girar",
                              style=estilo, layout=W.Layout(width="290px"))
        for s in (self.sw, self.sb, self.sg):
            s.observe(lambda _: self._desenha(), names="value")
        grade = _Grade(self.E, wlim, blim, n=48)
        self.chao = [grade.contorno(c) for c in niveis_chao]
        self.quadro = W.HTML()
        self.widget = W.VBox([W.HBox([self.sw, self.sb, self.sg],
                                     layout=W.Layout(gap="10px", flex_flow="row wrap")), self.quadro])
        self._desenha()

    def _projetor(self):
        phi, alfa = math.radians(self.sg.value), math.radians(24)
        (w1, w2), (b1, b2) = self.wlim, self.blim
        wc, bc, hw, hb = (w1 + w2) / 2, (b1 + b2) / 2, (w2 - w1) / 2, (b2 - b1) / 2
        c, s, ca, sa = math.cos(phi), math.sin(phi), math.cos(alfa), math.sin(alfa)
        S, cx, cy = 165, 300, 318

        def P(w, b, E):
            X, Y, Z = (w - wc) / hw, (b - bc) / hb, E / self.Emax
            xr, yr = X * c - Y * s, X * s + Y * c
            return cx + S * xr, cy - S * (1.15 * Z * ca + yr * sa)
        return P

    def _curva3d(self, P, pontos, cls):
        """Polilinha 3D cortada onde E passa do teto Emax."""
        partes, atual, anterior = [], [], None
        for q in pontos:
            dentro = q[2] <= self.Emax
            if anterior is not None and dentro != (anterior[2] <= self.Emax):
                t = (self.Emax - anterior[2]) / (q[2] - anterior[2])
                atual.append(tuple(a + t * (b - a) for a, b in zip(anterior, q)))
                if not dentro:
                    partes.append(atual)
                    atual = []
            if dentro:
                atual.append(q)
            anterior = q
        partes.append(atual)
        saida = []
        for parte in partes:
            if len(parte) >= 2:
                pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (P(*q) for q in parte))
                saida.append(f'<polyline class="{cls}" points="{pts}"/>')
        return "".join(saida)

    def _desenha(self):
        w0, b0 = self.sw.value, self.sb.value
        E0, gw, gb = _gradiente(self.Value, self.exemplos, w0, b0)
        P = self._projetor()
        (w1, w2), (b1, b2), Em, E = self.wlim, self.blim, self.Emax, self.E
        s = []

        def linha(a, c, cls):
            (xa, ya), (xc, yc) = P(*a), P(*c)
            return f'<line class="{cls}" x1="{xa:.1f}" y1="{ya:.1f}" x2="{xc:.1f}" y2="{yc:.1f}"/>'

        def texto(q, conteudo, cls="p-rot", ancora="middle", dx=0, dy=0):
            x, y = P(*q)
            return f'<text class="{cls}" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{ancora}">{conteudo}</text>'

        # chão, curvas de nível no chão e eixos
        cantos = [(w1, b1, 0), (w2, b1, 0), (w2, b2, 0), (w1, b2, 0)]
        s.append('<polygon class="s3-chao" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in (P(*q) for q in cantos)) + '"/>')
        for segs in self.chao:
            d = " ".join("M{:.1f},{:.1f} L{:.1f},{:.1f}".format(*P(a[0], a[1], 0), *P(c[0], c[1], 0)) for a, c in segs)
            if d:
                s.append(f'<path class="s3-nivel" d="{d}"/>')
        s.append(linha((w1, b1, 0), (w1, b1, Em), "s3-eixo"))
        for t in _ticks(0, Em, 4):
            s.append(texto((w1, b1, t), _num(t), ancora="end", dx=-7, dy=4))
        for t in _ticks(w1, w2, 6):
            s.append(texto((t, b1, 0), _num(t), dy=16))
        for t in _ticks(b1, b2, 6):
            s.append(texto((w2, t, 0), _num(t), ancora="start", dx=8, dy=5))
        s.append(texto((w2 + 0.1 * (w2 - w1), b1, 0), "w", "p-nome"))
        s.append(texto((w2, b2 + 0.1 * (b2 - b1), 0), "b", "p-nome"))
        s.append(texto((w1, b1, Em * 1.08), "E", "p-nome"))

        # planos de corte b = b₀ e w = w₀
        for q in ([(w1, b0, 0), (w2, b0, 0), (w2, b0, Em), (w1, b0, Em)],
                  [(w0, b1, 0), (w0, b2, 0), (w0, b2, Em), (w0, b1, Em)]):
            s.append('<polygon class="s3-plano" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in (P(*p) for p in q)) + '"/>')

        # a superfície, como uma malha
        for v in _intervalo(0, 1, 12):
            w = w1 + (w2 - w1) * v
            b = b1 + (b2 - b1) * v
            s.append(self._curva3d(P, [(w, bb, E(w, bb)) for bb in _intervalo(b1, b2, 60)], "s3-malha"))
            s.append(self._curva3d(P, [(ww, b, E(ww, b)) for ww in _intervalo(w1, w2, 60)], "s3-malha"))

        # os dois traços e as tangentes, cujas inclinações são as derivadas parciais
        s.append(self._curva3d(P, [(w, b0, E(w, b0)) for w in _intervalo(w1, w2, 140)], "s3-traco"))
        s.append(self._curva3d(P, [(w0, b, E(w0, b)) for b in _intervalo(b1, b2, 140)], "s3-traco2"))
        for dw, db, g, faixa, cls in ((1, 0, gw, w2 - w1, "s3-tang"), (0, 1, gb, b2 - b1, "s3-tang2")):
            d = 0.2 * faixa
            if abs(g) > 1e-12:
                d = min(d, 0.4 * Em / abs(g))
            s.append(linha((w0 - d * dw, b0 - d * db, E0 - g * d), (w0 + d * dw, b0 + d * db, E0 + g * d), cls))
        px, py = P(w0, b0, E0)
        s.append(f'<circle class="p-ponto" cx="{px:.1f}" cy="{py:.1f}" r="6.5"/>')
        s.append(f'<text class="p-nome-t" x="{px - 12:.1f}" y="{py - 10:.1f}" text-anchor="end">P</text>')
        svg = ('<svg width="600" height="440" viewBox="0 0 600 440" style="max-width:100%;height:auto" role="img" '
               'aria-label="Superfície E(w, b) com os traços">' + "".join(s) + "</svg>")

        painel = (f'<div class="ad-rotulo">ponto P = (w₀, b₀)</div><div class="ad-medio t">{_vetor(w0, b0, 2)}</div>'
                  f'<div class="ad-rotulo">altura da superfície em P: <i>E</i>(P)</div>'
                  f'<div class="ad-medio t">{fmt(E0)}</div>'
                  f'<div class="ad-rotulo">∂<i>E</i>/∂<i>w</i>: inclinação da tangente ao traço no plano b = b₀</div>'
                  f'<div class="ad-grande c">{fmt(gw)}</div>'
                  f'<div class="ad-rotulo">∂<i>E</i>/∂<i>b</i>: inclinação da tangente ao traço no plano w = w₀</div>'
                  f'<div class="ad-grande c">{fmt(gb)}</div>'
                  f'<div class="ad-frase ad-cinza">As duas derivadas parciais foram calculadas pelo motor.</div>')
        cab = (f'<div class="ad-eq"><i>E</i>(<i>w</i>, <i>b</i>) = {_formula_erro(self.exemplos)}'
               f'<span class="ad-eq-sub">{_nome_dados(self.exemplos)}</span></div>')
        leg = _legenda(('<i class="ad-ln g" style="opacity:.4"></i>', "a superfície <i>E</i>(<i>w</i>, <i>b</i>)"),
                       ('<i class="ad-ln t"></i>', "traço no plano b = b₀"),
                       ('<i class="ad-ln tt"></i>', "traço no plano w = w₀"),
                       ('<i class="ad-ln c"></i>', "tangentes aos traços: as inclinações são as derivadas parciais"),
                       ('<i class="ad-ln n"></i>', "curvas de nível, projetadas no chão"))
        self.quadro.value = _folha(cab, leg, svg, painel)


def superficie_interativa(Value, exemplos, wlim=(-1.0, 5.0), blim=(-2.0, 8.0), Emax=60.0, w0=0.0, b0=0.0):
    _exibe(Superficie(Value, exemplos, wlim=wlim, blim=blim, Emax=Emax, w0=w0, b0=b0).widget)


# ------------------------------------------------------------------ 4. descida do gradiente no plano

class DescidaPlano:
    """A descida do gradiente andando sobre o mapa de curvas de nível de E(w, b)."""

    def __init__(self, Value, conjuntos, lim=(-1.0, 5.0), taxas=(0.01, 0.05, 0.1, 0.13, 0.2, 0.25),
                 taxa=0.05, passos=25, niveis=None):
        W = _W()
        if not isinstance(conjuntos, dict):
            conjuntos = {_nome_dados(conjuntos): conjuntos}
        self.Value = Value
        self.conjuntos = {k: [(float(x), float(y)) for x, y in v] for k, v in conjuntos.items()}
        self.lim, self.passos = lim, passos
        self.niveis = list(niveis) if niveis else [k * k for k in range(1, 11)]
        self._mapas = {}
        nomes = list(self.conjuntos)
        controles = []
        self.escolha = None
        if len(nomes) > 1:
            self.escolha = W.ToggleButtons(options=nomes, value=nomes[0], style={"button_width": "110px"})
            self.escolha.observe(lambda _: self._desenha(), names="value")
            controles.append(self.escolha)
        self.taxa = W.SelectionSlider(options=[(f"{t:g}", t) for t in taxas], value=taxa, description="taxa η",
                                      style={"description_width": "50px"}, layout=W.Layout(width="300px"))
        self.passo = W.IntSlider(value=0, min=0, max=passos, description="passos",
                                 style={"description_width": "52px"}, layout=W.Layout(width="300px"))
        self.play = W.Play(value=0, min=0, max=passos, step=1, interval=450)
        W.jslink((self.play, "value"), (self.passo, "value"))
        self.taxa.observe(lambda _: self._desenha(), names="value")
        self.passo.observe(lambda _: self._desenha(), names="value")
        controles += [self.play, self.passo, self.taxa]
        self.quadro = W.HTML()
        self.widget = W.VBox([W.HBox(controles, layout=W.Layout(gap="10px", flex_flow="row wrap",
                                                                 align_items="center")), self.quadro])
        self._desenha()

    def _mapa(self, nome):
        if nome not in self._mapas:
            grade = _Grade(_erro_de(self.conjuntos[nome]), self.lim, self.lim, n=72)
            self._mapas[nome] = (grade, [grade.contorno(c) for c in self.niveis])
        return self._mapas[nome]

    def _desenha(self):
        nome = self.escolha.value if self.escolha else list(self.conjuntos)[0]
        ex = self.conjuntos[nome]
        grade, fundo = self._mapa(nome)
        k, eta = self.passo.value, self.taxa.value
        caminho = [(0.0, 0.0)]
        for _ in range(k):
            w, b = caminho[-1]
            _, gw, gb = _gradiente(self.Value, ex, w, b)
            caminho.append((w - eta * gw, b - eta * gb))
        wk, bk = caminho[-1]
        Ek, gw, gb = _gradiente(self.Value, ex, wk, bk)
        mod = math.hypot(gw, gb)
        prox = (wk - eta * gw, bk - eta * gb)

        pl = _Plano(self.lim, self.lim, larg=440, alt=434, margens=(46, 16, 40, 16))
        pl.eixos("w", "b")
        for segs in fundo:
            pl.segmentos(segs, "p-nivel")
        dentro = pl.dentro(wk, bk) and math.isfinite(Ek)
        if dentro and Ek > 1e-9:
            pl.segmentos(grade.contorno(Ek), "p-nivel-atual")
        _marca_minimo(pl, ex, self.lim)
        for i in range(len(caminho) - 1):
            pl.seg(*caminho[i], *caminho[i + 1], "p-trilha")
        for p in caminho[:-1]:
            pl.ponto(*p, "p-vazado", r=3.8)
        if dentro and mod > 1e-9:
            L = 0.13 * (self.lim[1] - self.lim[0])
            pl.seg(wk, bk, wk - L * gw / mod, bk - L * gb / mod, "p-seta-c", livre=True, seta="c")
            pl.texto(wk - 1.32 * L * gw / mod, bk - 1.32 * L * gb / mod, "−∇E", "p-texto-c", "middle", dy=5)
        if dentro:
            pl.ponto(wk, bk, r=6.5)

        if not dentro:
            frase = "O ponto saiu do mapa: a taxa está grande demais e o erro cresce a cada passo."
        elif mod < 1e-4:
            frase = "∇E ≈ 0: chegou ao fundo do vale. Não há direção que desça, e os passos param."
        else:
            frase = "O próximo passo vai na direção −∇E, perpendicular à curva de nível escura."
        conta = (f'<span class="ad-conta">{_vetor(wk, bk, 3)} − {fmt(eta)} · {_vetor(gw, gb, 3)} '
                 f'= {_vetor(*prox, casas=3)}</span>')
        painel = (f'<div class="ad-rotulo">passo</div><div class="ad-medio">{k} de {self.passos}</div>'
                  f'<div class="ad-rotulo">ponto (<i>w</i>, <i>b</i>)</div><div class="ad-medio t">{_vetor(wk, bk, 3)}</div>'
                  f'<div class="ad-rotulo">erro <i>E</i></div><div class="ad-grande t">{fmt(Ek)}</div>'
                  f'<div class="ad-rotulo">vetor gradiente ∇<i>E</i>, pelo motor</div>'
                  f'<div class="ad-medio c">{_vetor(gw, gb, 3)}</div>'
                  f'<div class="ad-frase">{frase}</div>'
                  f'<div class="ad-frase">Próximo ponto = (<i>w</i>, <i>b</i>) − η ∇<i>E</i><br>{conta}</div>')
        cab = (f'<div class="ad-eq"><i>E</i>(<i>w</i>, <i>b</i>) = {_formula_erro(ex)}'
               f'<span class="ad-eq-sub">{html.escape(nome)}</span></div>')
        leg = _legenda(('<i class="ad-ln n"></i>', "curvas de nível"),
                       ('<i class="ad-ln g"></i>', "curva de nível do ponto atual"),
                       ('<i class="ad-ln t"></i>', "caminho da descida, saindo de (0, 0)"),
                       ('<i class="ad-ln c"></i>', "−∇E: a direção do próximo passo"))
        self.quadro.value = _folha(cab, leg, pl.svg(), painel)


def descida_no_plano(Value, conjuntos, lim=(-1.0, 5.0), taxa=0.05):
    _exibe(DescidaPlano(Value, conjuntos, lim=lim, taxa=taxa).widget)


# ------------------------------------------------------------------ teste da segunda derivada (fora do caderno atual)

def teste_segunda_derivada(Value, modelo, rotulo="", h=1e-4, **ponto):
    """Classifica um ponto crítico de modelo(w, b) pelo sinal de D = E_ww·E_bb − E_wb².

    As derivadas primeiras vêm do motor. As segundas saem derivando o gradiente
    de novo, pela definição (diferença central).
    """
    nomes = list(inspect.signature(modelo).parameters)
    p = {n: float(ponto[n]) for n in nomes}

    def grad(q):
        vs = {n: Value(q[n]) for n in nomes}
        E = modelo(**vs)
        E.backward()
        return [vs[n].grad for n in nomes]

    g0 = grad(p)
    H = [[0.0, 0.0], [0.0, 0.0]]
    for i, ni in enumerate(nomes):
        mais, menos = dict(p), dict(p)
        mais[ni] += h
        menos[ni] -= h
        gm, gn = grad(mais), grad(menos)
        for j in range(2):
            H[i][j] = (gm[j] - gn[j]) / (2 * h)
    a, c = nomes
    fxx, fyy, fxy = H[0][0], H[1][1], (H[0][1] + H[1][0]) / 2
    fxx, fyy, fxy = (round(v, 6) for v in (fxx, fyy, fxy))
    D = fxx * fyy - fxy ** 2
    if abs(D) <= 1e-6 * max(1.0, abs(fxx * fyy)):
        veredito = "D = 0: o teste não decide."
    elif D > 0 and fxx > 0:
        veredito = f"D &gt; 0 e E<sub>{a}{a}</sub> &gt; 0: é um mínimo local."
    elif D > 0:
        veredito = f"D &gt; 0 e E<sub>{a}{a}</sub> &lt; 0: é um máximo local."
    else:
        veredito = "D &lt; 0: é um ponto de sela."
    critico = all(abs(g) < 1e-9 for g in g0)
    sub = lambda s: f"<i>E</i><sub>{s}</sub>"
    linhas = [
        f'<tr><td>vetor gradiente ∇<i>E</i>, pelo motor</td><td>{_vetor(*g0)}</td>'
        f'<td class="cx">{"é um ponto crítico" if critico else "não é ponto crítico"}</td></tr>',
        f'<tr><td>{sub(a + a)}</td><td>{fmt(fxx)}</td><td class="cx">∂²E/∂{a}²</td></tr>',
        f'<tr><td>{sub(c + c)}</td><td>{fmt(fyy)}</td><td class="cx">∂²E/∂{c}²</td></tr>',
        f'<tr><td>{sub(a + c)}</td><td>{fmt(fxy)}</td><td class="cx">∂²E/∂{a}∂{c}</td></tr>',
        f'<tr><td>D = {sub(a + a)} · {sub(c + c)} − ({sub(a + c)})²</td>'
        f'<td>{fmt(fxx)} · {fmt(fyy)} − {_par(fxy)}² = <b>{fmt(D)}</b></td><td></td></tr>',
    ]
    titulo = f"Teste da segunda derivada em ({a}, {c}) = ({_num(p[a])}, {_num(p[c])})"
    sub_titulo = f'<span class="ad-eq-sub">{html.escape(rotulo)}</span>' if rotulo else ""
    _mostra(FONTES + CSS + f'<div class="ad"><div class="ad-eq" style="font-size:21px">{titulo}{sub_titulo}</div>'
            f'<table class="ad-conf">{"".join(linhas)}</table>'
            f'<div class="ad-frase" style="font-size:16px"><b>{veredito}</b></div>'
            f'<div class="ad-frase ad-cinza">As derivadas segundas saíram derivando de novo, pela definição, '
            f'o gradiente que o motor entrega.</div></div>')


# ------------------------------------------------------------------ abertura e seção 10: ajuste de reta

class Ajuste:
    """Treina palpite = w·x + b em vários exemplos com o motor e mostra a reta se ajustando."""

    def __init__(self, Value, exemplos, taxa=0.05, passos=40):
        W = _W()
        self.exemplos = [(float(x), float(y)) for x, y in exemplos]
        self.passos = passos
        w, b = Value(0.0), Value(0.0)
        self.trajetoria = []
        for _ in range(passos + 1):
            E = sum((w * x + b - y) ** 2 for x, y in self.exemplos)
            w.grad, b.grad = 0.0, 0.0
            E.backward()
            self.trajetoria.append((w.data, b.data, E.data))
            w.data -= taxa * w.grad
            b.data -= taxa * b.grad
        xs = [x for x, _ in self.exemplos]
        ys = [y for _, y in self.exemplos]
        self.xlim = (min(xs) - 1, max(xs) + 1)
        folga = (max(ys) - min(ys)) * 0.35 + 1
        self.ylim = (min(min(ys), 0) - folga, max(ys) + folga)
        self.passo = W.IntSlider(value=0, min=0, max=passos, description="passo",
                                 style={"description_width": "46px"}, layout=W.Layout(width="360px"))
        self.play = W.Play(value=0, min=0, max=passos, step=1, interval=220)
        W.jslink((self.play, "value"), (self.passo, "value"))
        self.passo.observe(lambda _: self._desenha(), names="value")
        self.quadro = W.HTML()
        self.widget = W.VBox([W.HBox([self.play, self.passo], layout=W.Layout(gap="10px", align_items="center")),
                              self.quadro])
        self._desenha()

    def _desenha(self):
        k = self.passo.value
        w, b, E = self.trajetoria[k]
        pl = _Plano(self.xlim, self.ylim)
        pl.eixos("entrada", "resposta")
        for x, y in self.exemplos:
            pl.seg(x, y, x, w * x + b, "p-residuo")
        pl.reta(0.0, b, w, "p-modelo")
        for x, y in self.exemplos:
            pl.ponto(x, y, r=6.5)
        xr = self.xlim[1] - 0.15 * (self.xlim[1] - self.xlim[0])
        pl.texto(xr, w * xr + b, "palpite", "p-texto", "end", dy=-12)

        painel = (f'<div class="ad-rotulo">passo do treino</div><div class="ad-medio">{k} de {self.passos}</div>'
                  f'<div class="ad-rotulo">erro total (soma dos quadrados das distâncias tracejadas)</div>'
                  f'<div class="ad-grande t">{fmt(E)}</div>'
                  f'<div class="ad-rotulo">palpite atual</div>'
                  f'<div class="ad-medio">resposta = {fmt(w, 2)} · entrada + {fmt(b, 2)}</div>')
        if k == self.passos:
            painel += ('<div class="ad-frase">A regra escondida era resposta = 2 · entrada + 2. '
                       'Ninguém contou isso para o computador.</div>')
        cab = '<div class="ad-eq">Aprendendo uma regra a partir de exemplos</div>'
        leg = _legenda(('<i class="ad-sw" style="background:#1E3FA0;border-radius:50%"></i>',
                        "exemplos (entrada, resposta certa)"),
                       ('<i class="ad-ln g"></i>', "palpite do computador: w · entrada + b"),
                       ('<i class="ad-ln" style="border-color:#66707A;border-top-style:dashed"></i>',
                        "o quanto cada palpite errou"))
        self.quadro.value = _folha(cab, leg, pl.svg(), painel)


def ajuste_interativo(Value, exemplos, taxa=0.05, passos=40):
    _exibe(Ajuste(Value, exemplos, taxa=taxa, passos=passos).widget)


# ------------------------------------------------------------------ 8. a volta, passo a passo

def _regra(v):
    op = v._op
    if op == "+":
        return "É uma soma: a derivada parcial local é 1 em relação a cada parcela."
    if op == "-":
        return "É uma subtração: a derivada parcial local é 1 em relação ao primeiro termo e −1 em relação ao segundo."
    if op == "*":
        if len(v._prev) == 1:
            return ("É a multiplicação de um nó por ele mesmo: cada fator recebe o valor do outro, "
                    "e as duas partes vão para o mesmo nó.")
        return "É uma multiplicação: a derivada parcial local em relação a cada fator é o valor do outro fator."
    if op.startswith("**"):
        n = float(op[2:])
        base = _operandos(v)[0]
        expo = "" if n - 1 == 1 else _sobrescrito(n - 1)
        return (f"É uma potência. Pela regra da potência (a do tombo), a derivada local de u{_sobrescrito(n)} é "
                f"{_num(n)}·u{expo} = {_num(n)}·{_par(base.data)}{expo} = {fmt(n * base.data ** (n - 1))}.")
    return "Esta conta usa a derivada local que o _backward dela conhece."


class PassoAPasso:
    """Roda a volta um nó por vez, chamando o _backward de cada um na ordem do backward()."""

    def __init__(self, Value, modelo, valores, nome_saida="E", parametros=()):
        W = _W()
        self.Value, self.modelo = Value, modelo
        self.nomes = list(inspect.signature(modelo).parameters)
        self.valores = {n: float(valores[n]) for n in self.nomes}
        self.nome_saida, self.parametros = nome_saida, tuple(parametros)
        self.k = -1
        self.bt_prox = W.Button(description="Próximo passo", button_style="danger")
        self.bt_ant = W.Button(description="Passo anterior")
        self.bt_ini = W.Button(description="Recomeçar")
        self.bt_prox.on_click(lambda _: self._vai(self.k + 1))
        self.bt_ant.on_click(lambda _: self._vai(self.k - 1))
        self.bt_ini.on_click(lambda _: self._vai(-1))
        self.quadro = W.HTML()
        self.widget = W.VBox([W.HBox([self.bt_prox, self.bt_ant, self.bt_ini], layout=W.Layout(gap="8px")),
                              self.quadro])
        self._vai(-1)

    def _monta(self, k):
        vs = {n: self.Value(self.valores[n]) for n in self.nomes}
        E = self.modelo(**vs)
        topo = _topo(E)
        ordem = [v for v in reversed(topo) if v._prev]
        antes = {v: v.grad for v in topo}
        if k >= 0:
            E.grad = 1.0
            for i in range(k):
                antes = {v: v.grad for v in topo}
                ordem[i]._backward()
        return vs, E, topo, ordem, antes

    def _vai(self, k):
        _, _, _, ordem, _ = self._monta(-1)
        self.k = max(-1, min(k, len(ordem)))
        self._desenha()

    def _desenha(self):
        k = self.k
        vs, E, topo, ordem, antes = self._monta(k)
        N = len(ordem)
        nomes = dict(vs)
        nomes[self.nome_saida] = E
        nomes_por_valor = {v: n for n, v in nomes.items()}
        rot = _rotulos(E, nomes_por_valor)
        mudou = {v: (False, abs(v.grad - antes[v]) > 1e-12) for v in topo} if k >= 0 else {}
        executados = {ordem[i]: i + 1 for i in range(min(k, N))}
        atual = ordem[k - 1] if k >= 1 else None

        def caixa(v):
            if v in nomes_por_valor:
                return f'<span class="ad-no nome">{html.escape(rot[v])}</span>'
            return f'<span class="ad-no">{html.escape(rot[v])}</span>'

        s = html.escape(self.nome_saida)
        if k == -1:
            n_txt = "antes da volta"
            titulo = "A ida está pronta."
            texto = (f"Todos os valores (em azul) foram calculados, da esquerda para a direita, até chegar em "
                     f"<i>{s}</i>. Nenhuma derivada ainda: todo grad está em 0. Clique em "
                     f"<b>Próximo passo</b> para começar a volta.")
            itens = []
        elif k == 0:
            n_txt = f"passo 0 de {N}"
            titulo = "A volta começa pelo fim."
            texto = (f"{caixa(E)}.grad = 1, porque ∂{s}/∂{s} = 1: se <i>{s}</i> sobe um pouquinho, "
                     f"<i>{s}</i> sobe exatamente esse pouquinho.")
            itens = []
        else:
            v = ordem[k - 1]
            g = v.grad
            locais = _derivadas_locais(v)
            n_txt = f"passo {k} de {N}"
            titulo = f"O nó {caixa(v)} passa a derivada para trás."
            texto = f"Ele tem grad = <b>{fmt(g)}</b>. {_regra(v)}"
            itens = []
            filhos = _unicos(_operandos(v))
            for c in filhos:
                local = locais[c]
                parte = g * local
                linha = (f'{caixa(c)} recebe <span class="ad-conta">{fmt(g)} × {_par(local)} = '
                         f'<span class="c">{fmt(parte)}</span></span>')
                if v._op == "*" and len(filhos) == 2:
                    outro = filhos[1] if c is filhos[0] else filhos[0]
                    linha += f' <span class="ad-obs">({fmt(local)} é o valor de {html.escape(rot[outro])})</span>'
                if abs(antes[c]) > 1e-12:
                    linha += (f'. <span class="ad-obs">Como já tinha {fmt(antes[c])}, soma: '
                              f'{fmt(antes[c])} + {_par(parte)} = <b>{fmt(c.grad)}</b>.</span>')
                itens.append(f"<li>{linha}</li>")
            if k == N:
                resumo = ""
                if self.parametros:
                    resumo = " " + " ".join(f"∂{s}/∂{n} = <b>{fmt(vs[n].grad)}</b>." for n in self.parametros)
                itens.append(f'<li style="margin-top:8px">Fim da volta: todo nó tem a sua derivada parcial.{resumo} '
                             f'É exatamente o que <code>{s}.backward()</code> faz, numa linha.</li>')

        rodape = (f'<div class="ad-passo"><div class="ad-passo-n">{n_txt}</div>'
                  f'<div class="ad-passo-t">{titulo}</div><div class="ad-passo-x">{texto}</div>'
                  f'<ul class="ad-passo-l">{"".join(itens)}</ul></div>')
        self.quadro.value = html_grafo(E, parametros=self.parametros, mudou=mudou, ordem_backward=executados,
                                       atual=atual, rodape=rodape, voltou=k >= 0, **nomes)
        self.bt_prox.disabled = k >= N
        self.bt_ant.disabled = k <= -1


def passo_a_passo(Value, modelo, nome_saida="E", parametros=(), **valores):
    _exibe(PassoAPasso(Value, modelo, valores, nome_saida=nome_saida, parametros=parametros).widget)


# ------------------------------------------------------------------ conferência pela definição (fora do caderno atual)

def confere(Value, modelo, casos, h=1e-6):
    """Compara o grad do motor com (f(a + h) − f(a − h)) / 2h, que não usa regra da cadeia."""
    nomes = list(inspect.signature(modelo).parameters)
    linhas, pior = [], 0.0
    for caso in casos:
        vals = {n: Value(float(caso[n])) for n in nomes}
        E = modelo(**vals)
        E.backward()
        desc = ", ".join(f"{n} = {fmt(caso[n])}" for n in nomes)
        linhas.append(f'<tr class="caso"><td colspan="4">com {desc}, o resultado é {fmt(E.data)}</td></tr>')
        for n in nomes:
            mais = modelo(**{k: Value(float(caso[k]) + (h if k == n else 0.0)) for k in nomes}).data
            menos = modelo(**{k: Value(float(caso[k]) - (h if k == n else 0.0)) for k in nomes}).data
            pela_definicao = (mais - menos) / (2 * h)
            erro = abs(pela_definicao - vals[n].grad)
            pior = max(pior, erro / max(1.0, abs(pela_definicao)))
            linhas.append(f'<tr><td class="v">∂/∂{n}</td><td>{fmt(vals[n].grad)}</td>'
                          f'<td>{fmt(pela_definicao)}</td><td class="cx">{erro:.1e}</td></tr>')
    if pior < 1e-5:
        veredito = (f'<span class="ad-ok">O motor e a definição concordam em todos os casos.</span> '
                    f'Maior diferença relativa: {pior:.1e}.')
    else:
        veredito = f'<span class="ad-ruim">Não bate.</span> Maior diferença relativa: {pior:.1e}.'
    tabela = ('<table class="ad-conf"><tr><th>derivada parcial</th><th>motor (grad)</th>'
              '<th>pela definição (h = 10⁻⁶)</th><th>diferença</th></tr>' + "".join(linhas) + "</table>")
    _mostra(FONTES + CSS + f'<div class="ad"><div class="ad-titulo">{veredito}</div>{tabela}</div>')


def casos_aleatorios(nomes, n=3, semente=7):
    rng = random.Random(semente)
    return [{k: round(rng.uniform(-4, 4), 2) for k in nomes} for _ in range(n)]


# ------------------------------------------------------------------ 9. laboratório

def _curva_erro(historico, largura=210, altura=78):
    if len(historico) < 2:
        return '<div class="ad-sub">Use “Dar um passo” para ver o erro caindo aqui.</div>'
    finitos = [e for e in historico if math.isfinite(e)]
    m = max(finitos) if finitos else 1.0
    m = m or 1.0
    pts = [(8 + i * (largura - 16) / (len(historico) - 1),
            8 + (1 - min(e, m) / m) * (altura - 26)) for i, e in enumerate(historico)]
    caminho = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    ux, uy = pts[-1]
    return (f'<svg class="ad-curva" width="{largura}" height="{altura}" viewBox="0 0 {largura} {altura}">'
            f'<line x1="8" y1="{altura - 18}" x2="{largura - 8}" y2="{altura - 18}" stroke="#C5D2DC"/>'
            f'<polyline points="{caminho}" fill="none" stroke="#1E3FA0" stroke-width="1.8" '
            f'stroke-linejoin="round"/><circle cx="{ux:.1f}" cy="{uy:.1f}" r="3" fill="#1E3FA0"/>'
            f'<text x="8" y="{altura - 4}">passo 0</text>'
            f'<text x="{largura - 8}" y="{altura - 4}" text-anchor="end">passo {len(historico) - 1}</text></svg>')


class Laboratorio:
    """Sliders para as entradas de `modelo`; refaz a ida e a volta a cada mudança."""

    def __init__(self, Value, modelo, valores, parametros=("w", "b"), passo_dx=0.1):
        W = _W()
        self.Value, self.modelo = Value, modelo
        self.nomes = list(inspect.signature(modelo).parameters)
        self.parametros = tuple(parametros)
        self.dx = passo_dx
        self.inicial = {n: float(valores[n]) for n in self.nomes}
        self.vals = dict(self.inicial)      # a fonte da verdade; os sliders só mostram
        self.historico = []
        self.anterior = {}
        self._interno = False

        self.sliders = {}
        for n in self.nomes:
            s = W.FloatSlider(value=self.vals[n], min=-8.0, max=8.0, step=0.1, description=n,
                              readout_format=".2f", continuous_update=True,
                              style={"description_width": "22px"}, layout=W.Layout(width="300px"))
            s.observe(self._mexeu, names="value")
            self.sliders[n] = s
        self.taxa = W.FloatSlider(value=0.05, min=0.01, max=0.19, step=0.01, description="taxa η",
                                  readout_format=".2f", style={"description_width": "46px"},
                                  layout=W.Layout(width="300px"))
        b1 = W.Button(description="Dar um passo")
        b2 = W.Button(description="Treinar 20 passos")
        b3 = W.Button(description="Recomeçar")
        b1.on_click(lambda _: self._treina(1))
        b2.on_click(lambda _: self._treina(20))
        b3.on_click(self._recomeca)
        for bt in (b1, b2, b3):
            bt.layout = W.Layout(width="auto")
        self.quadro = W.HTML()
        grade = W.GridBox(list(self.sliders.values()),
                          layout=W.Layout(grid_template_columns="repeat(2, 310px)", grid_gap="2px 12px"))
        controles = W.HBox([self.taxa, b1, b2, b3],
                           layout=W.Layout(gap="8px", flex_flow="row wrap", align_items="center"))
        self.widget = W.VBox([grade, controles, self.quadro], layout=W.Layout(gap="8px"))
        self._desenha()

    # monta um grafo novo a cada vez: assim os grad nunca acumulam entre um desenho e outro
    def _calcula(self, vals):
        vs = {n: self.Value(float(vals[n])) for n in self.nomes}
        E = self.modelo(**vs)
        E.backward()
        return E, vs

    def _mexeu(self, mudanca):
        if self._interno:
            return
        n = mudanca["owner"].description
        if abs(mudanca["new"] - self.vals[n]) < 0.051:   # o slider arredonda para o passo dele
            return
        self.vals[n] = float(mudanca["new"])
        self.historico = []
        self._desenha()

    def _treina(self, passos):
        vals = dict(self.vals)
        if not self.historico:
            self.historico.append(self._calcula(vals)[0].data)
        for _ in range(passos):
            _, vs = self._calcula(vals)
            for n in self.parametros:
                vals[n] = vals[n] - self.taxa.value * vs[n].grad
            self.historico.append(self._calcula(vals)[0].data)
        self.vals = vals
        self._interno = True
        for n in self.parametros:
            s = self.sliders[n]
            if math.isfinite(vals[n]):
                s.min, s.max = min(s.min, vals[n] - 1), max(s.max, vals[n] + 1)
                s.value = vals[n]
        self._interno = False
        self._desenha()

    def _recomeca(self, _):
        self.vals = dict(self.inicial)
        self._interno = True
        for n, s in self.sliders.items():
            s.min, s.max = -8.0, 8.0
            s.value = self.inicial[n]
        self._interno = False
        self.historico = []
        self._desenha()

    def _desenha(self):
        E, vs = self._calcula(self.vals)
        nomes = dict(vs)
        nomes["E"] = E
        rot = _rotulos(E, {v: k for k, v in nomes.items()})
        atual = {rot[v]: (v.data, v.grad) for v in _topo(E)}
        mudou = {}
        if self.anterior:
            for v in _topo(E):
                if rot[v] in self.anterior:
                    d0, g0 = self.anterior[rot[v]]
                    mudou[v] = (abs(v.data - d0) > 1e-12, abs(v.grad - g0) > 1e-12)
        self.anterior = atual

        linhas = []
        grupos = (("parâmetros (o treino ajusta)", [n for n in self.nomes if n in self.parametros]),
                  ("dados (o motor também deriva, mas o treino não mexe neles)",
                   [n for n in self.nomes if n not in self.parametros]))
        for titulo, grupo in grupos:
            if not grupo:
                continue
            linhas.append(f'<tr class="sep"><td colspan="3">{titulo}</td></tr>')
            for n in grupo:
                g = vs[n].grad
                novo = dict(self.vals)
                novo[n] += self.dx
                real = self._calcula(novo)[0].data - E.data
                linhas.append(
                    f'<tr><td class="v">{n}</td><td class="g">{fmt(g)}</td>'
                    f'<td class="t">se {n} subir {fmt(self.dx)}, a aproximação linear dá ΔE ≈ '
                    f'{fmt(g)} × {fmt(self.dx)} = <b>{fmt(g * self.dx)}</b>; de verdade, ΔE = {fmt(real)}</td></tr>')

        previsto = ""
        if all(k in vs for k in ("x", "w", "b")):
            previsto = f'palpite <b>w·x + b = {fmt(vs["w"].data * vs["x"].data + vs["b"].data)}</b>'
            if "y" in vs:
                previsto += f'<br>resposta certa <b>y = {fmt(vs["y"].data)}</b>'

        leitura = ('<div class="ad-leitura">'
                   f'<div><div class="ad-titulo">erro E</div><div class="ad-erro">{fmt(E.data)}</div>'
                   f'<div class="ad-sub">{previsto}</div></div>'
                   f'<div><div class="ad-titulo">as derivadas parciais de E (o vetor gradiente)</div>'
                   f'<table class="ad-tab">{"".join(linhas)}</table></div>'
                   f'<div><div class="ad-titulo">erro ao longo do treino</div>{_curva_erro(self.historico)}</div>'
                   '</div>')
        self.quadro.value = html_grafo(E, parametros=self.parametros, mudou=mudou, rodape=leitura, **nomes)


def laboratorio(Value, modelo, parametros=("w", "b"), **valores):
    _exibe(Laboratorio(Value, modelo, valores, parametros=parametros).widget)
