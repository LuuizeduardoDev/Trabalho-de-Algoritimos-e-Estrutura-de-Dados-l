"""SP23 – Ordenação de Catálogo de Produtos de E-commerce.

Algoritmo usado: Quick Sort (mediana-de-três + partição de Hoare) -> ordenacao/quick_sort.py
Comparado com: Merge Sort -> ordenacao/merge_sort.py

O que o enunciado pede e onde está:
  * Quick Sort com pivô mediana-de-três ........... ordenacao/quick_sort.py
  * ordenar produtos por diferentes critérios ...... CRITERIOS (preço, nome, popularidade, avaliação)
  * teste com pelo menos 100 produtos (gerados
    ou lidos de arquivo) ........................... dados/catalogo_produtos.csv (1.200 produtos)
  * comparação de tempo com Merge Sort (valorizado)  comparar_com_merge_sort()

Por que Quick Sort: o catálogo fica todo na memória e é reordenado a cada
clique do usuário ("menor preço", "mais vendidos"...). O Quick Sort é, em
geral, o mais rápido na prática para vetores em memória e ordena no próprio
vetor, usando só O(log n) de memória extra (o Merge Sort precisa de O(n)).

Dois cuidados:
  * PIVÔ: catálogos costumam já estar ordenados por algum critério; com pivô
    fixo isso é o pior caso O(n²). A mediana-de-três resolve (ver a seção
    "escolha do pivô" da demonstração).
  * ESTABILIDADE: o Quick Sort não é estável. Cada critério termina com o
    código do produto como desempate, então a ordem é sempre a mesma.
"""

from __future__ import annotations

import csv
import math
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

if __package__ in (None, ""):  # permite rodar este arquivo diretamente
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ordenacao.merge_sort import merge_sort
from ordenacao.quick_sort import quick_sort
from situacoes.utilidades import cabecalho, imprimir_tabela, moeda, normalizar_texto, numero, secao

ARQUIVO_CATALOGO = Path(__file__).resolve().parent.parent / "dados" / "catalogo_produtos.csv"


@dataclass
class Produto:
    codigo: str
    nome: str
    categoria: str
    preco: float
    popularidade: int     # unidades vendidas nos últimos 30 dias
    avaliacao: float      # nota média de 1,0 a 5,0
    nome_ordenacao: str = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        # calculado uma vez só: normalizar texto a cada comparação deixaria a ordenação lenta
        self.nome_ordenacao = normalizar_texto(self.nome)


# Critérios de ordenação: (rótulo, função-chave). Todos terminam no código do
# produto, que é único: assim nunca há empate e o resultado é determinístico.
CRITERIOS = [
    ("Menor preço", lambda p: (p.preco, p.nome_ordenacao, p.codigo)),
    ("Maior preço", lambda p: (-p.preco, p.nome_ordenacao, p.codigo)),
    ("Nome (A-Z)", lambda p: (p.nome_ordenacao, p.codigo)),
    ("Mais vendidos", lambda p: (-p.popularidade, -p.avaliacao, p.codigo)),
    ("Melhor avaliados", lambda p: (-p.avaliacao, -p.popularidade, p.codigo)),
]


def ordenar_catalogo(produtos: list, criterio: str):
    """Devolve (nova lista ordenada pelo critério, métricas do Quick Sort)."""
    for rotulo, chave in CRITERIOS:
        if rotulo == criterio:
            copia = list(produtos)
            return copia, quick_sort(copia, chave=chave)
    raise ValueError(f"critério desconhecido: {criterio}")


# ---------------------------------------------------------------------- geração e leitura do catálogo
CATEGORIAS = [
    # (categoria, (preço mínimo, preço máximo), tipos de produto)
    ("Informática", (29.90, 5_999.00), [
        "Mouse sem fio", "Teclado mecânico", "Monitor 24 pol.", "Notebook", "SSD 1 TB",
        "Pen drive 64 GB", "Webcam Full HD", "Headset gamer", "Hub USB-C", "Roteador Wi-Fi 6"]),
    ("Casa e Cozinha", (39.90, 1_899.00), [
        "Panela de pressão", "Air fryer", "Liquidificador", "Cafeteira", "Jogo de toalhas",
        "Jogo de cama", "Aspirador de pó", "Ventilador de mesa", "Micro-ondas", "Jogo de facas"]),
    ("Esporte", (19.90, 2_499.00), [
        "Tênis de corrida", "Bola de futebol", "Garrafa térmica", "Tapete de yoga", "Halteres 5 kg",
        "Bicicleta aro 29", "Corda de pular", "Mochila de trilha", "Luvas de academia", "Bermuda de ciclismo"]),
    ("Livros", (19.90, 189.00), [
        "Livro de receitas", "Romance policial", "Guia de Python", "HQ de aventura", "Livro de fantasia",
        "Biografia", "Livro infantil ilustrado", "Manual de finanças", "Atlas geográfico", "Dicionário escolar"]),
    ("Beleza", (12.90, 899.00), [
        "Perfume 100 ml", "Protetor solar FPS 50", "Secador de cabelo", "Kit de maquiagem", "Hidratante corporal",
        "Prancha alisadora", "Shampoo 400 ml", "Barbeador elétrico", "Esmalte", "Sérum facial"]),
    ("Brinquedos", (24.90, 799.00), [
        "Blocos de montar", "Quebra-cabeça 1000 peças", "Carrinho de controle remoto", "Boneca articulada",
        "Jogo de tabuleiro", "Pelúcia", "Kit de ciência", "Drone infantil", "Pista de corrida",
        "Massinha de modelar"]),
    ("Celulares", (14.90, 4_999.00), [
        "Smartphone 128 GB", "Smartphone 256 GB", "Capa protetora", "Película de vidro", "Carregador turbo",
        "Fone bluetooth", "Smartwatch", "Power bank", "Cabo USB-C", "Suporte veicular"]),
    ("Ferramentas", (14.90, 1_299.00), [
        "Furadeira de impacto", "Jogo de chaves", "Parafusadeira", "Trena 5 m", "Serra tico-tico",
        "Nível a laser", "Caixa de ferramentas", "Alicate universal", "Lixadeira orbital", "Escada de alumínio"]),
]
MARCAS = ["Aurora", "Vértice", "Nimbus", "Solaris", "Kappa", "Orion", "Lince", "Atlas", "Boreal", "Zênite"]
MODELOS = ["Lite", "Plus", "Pro", "Max", "Mini", "X", "S", "Ultra"]


def gerar_catalogo(quantidade: int, semente: int = 2026) -> list:
    """Gera produtos realistas (preços terminados em ,90, poucos campeões de venda)."""
    sorteio = random.Random(semente)
    produtos = []
    for numero_produto in range(1, quantidade + 1):
        categoria, (minimo, maximo), tipos = sorteio.choice(CATEGORIAS)
        tipo = sorteio.choice(tipos)
        nome = f"{tipo} {sorteio.choice(MARCAS)} {sorteio.choice(MODELOS)} {sorteio.randint(1, 9)}"
        preco = math.exp(sorteio.uniform(math.log(minimo), math.log(maximo)))
        preco = int(preco) + 0.90                                    # ex.: 149,90
        popularidade = min(20_000, int(sorteio.paretovariate(1.3) * 8) - 8)
        avaliacao = round(min(5.0, max(1.0, sorteio.gauss(4.2, 0.55))), 1)
        produtos.append(Produto(f"P{numero_produto:05d}", nome, categoria, preco, popularidade, avaliacao))
    return produtos


def salvar_catalogo(produtos: list, caminho: Path = ARQUIVO_CATALOGO) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["codigo", "nome", "categoria", "preco", "popularidade", "avaliacao"])
        for p in produtos:
            escritor.writerow([p.codigo, p.nome, p.categoria, f"{p.preco:.2f}", p.popularidade, f"{p.avaliacao:.1f}"])


def carregar_catalogo(caminho: Path = ARQUIVO_CATALOGO) -> list:
    """Lê o CSV (separado por ';'). Se o arquivo não existir, gera e salva 1.200 produtos."""
    if not caminho.exists():
        salvar_catalogo(gerar_catalogo(1_200), caminho)
    produtos = []
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        for linha in csv.DictReader(arquivo, delimiter=";"):
            produtos.append(Produto(linha["codigo"], linha["nome"], linha["categoria"], float(linha["preco"]),
                                    int(linha["popularidade"]), float(linha["avaliacao"])))
    return produtos


# ---------------------------------------------------------------------- comparações de desempenho
def _melhor_tempo(algoritmo, dados: list, chave, repeticoes: int = 5):
    """Roda o algoritmo `repeticoes` vezes em cópias e devolve as métricas da execução mais rápida."""
    melhor = None
    for _ in range(repeticoes):
        copia = list(dados)
        metricas = algoritmo(copia, chave=chave)
        if melhor is None or metricas.tempo_ms < melhor.tempo_ms:
            melhor = metricas
    return melhor


def comparar_com_merge_sort(tamanhos=(1_000, 5_000, 10_000, 20_000)) -> list:
    """Quick x Merge em catálogos aleatórios e em um catálogo já ordenado (critério: menor preço)."""
    chave = CRITERIOS[0][1]
    linhas = []
    for n in tamanhos:
        dados = gerar_catalogo(n, semente=n)
        linhas.append((f"{numero(n)} aleatórios", _melhor_tempo(quick_sort, dados, chave),
                       _melhor_tempo(merge_sort, dados, chave)))
    ja_ordenados = gerar_catalogo(10_000, semente=7)
    merge_sort(ja_ordenados, chave=chave)
    linhas.append(("10.000 já ordenados", _melhor_tempo(quick_sort, ja_ordenados, chave),
                   _melhor_tempo(merge_sort, ja_ordenados, chave)))
    return linhas


def _quick_sort_pivo_fixo(vetor: list, ini: int, fim: int, chave, contador: list) -> None:
    """Quick Sort INGÊNUO (pivô = último elemento, partição de Lomuto), só para comparação."""
    if ini >= fim:
        return
    pivo = chave(vetor[fim])
    i = ini - 1
    for j in range(ini, fim):
        contador[0] += 1
        if chave(vetor[j]) <= pivo:
            i += 1
            vetor[i], vetor[j] = vetor[j], vetor[i]
    vetor[i + 1], vetor[fim] = vetor[fim], vetor[i + 1]
    _quick_sort_pivo_fixo(vetor, ini, i, chave, contador)
    _quick_sort_pivo_fixo(vetor, i + 2, fim, chave, contador)


# ---------------------------------------------------------------------- demonstração
def executar_demonstracao() -> None:
    cabecalho("SP23 - Catálogo de e-commerce ordenado por vários critérios (Quick Sort)")
    catalogo = carregar_catalogo()
    print(f"{numero(len(catalogo))} produtos lidos de dados/{ARQUIVO_CATALOGO.name} "
          f"({len(CATEGORIAS)} categorias).")

    for rotulo, chave in CRITERIOS:
        ordenado, metricas = ordenar_catalogo(catalogo, rotulo)
        conferencia = list(catalogo)
        merge_sort(conferencia, chave=chave)
        igual = all(a is b for a, b in zip(ordenado, conferencia))
        secao(f"{rotulo} - 5 primeiros")
        imprimir_tabela(["Código", "Produto", "Categoria", "Preço", "Vendas/30d", "Nota"],
                        [[p.codigo, p.nome, p.categoria, moeda(p.preco), numero(p.popularidade),
                          numero(p.avaliacao, 1)] for p in ordenado[:5]], "<<<>>>")
        print(f"{metricas.resumo()} | mesmo resultado do Merge Sort: {'sim' if igual else 'NÃO'}")

    secao("Quick Sort x Merge Sort (melhor de 5 execuções, critério 'Menor preço')")
    linhas = []
    for descricao, quick, merge in comparar_com_merge_sort():
        linhas.append([descricao, f"{numero(quick.tempo_ms, 1)} ms", f"{numero(merge.tempo_ms, 1)} ms",
                       numero(quick.comparacoes), numero(merge.comparacoes),
                       f"{numero(quick.tempo_ms / merge.tempo_ms, 2)}"])
    imprimir_tabela(["Entrada", "Quick", "Merge", "Comp. Quick", "Comp. Merge", "Quick/Merge"], linhas, "<>>>>>")
    print("Os tempos variam de máquina para máquina; o que importa é a proporção entre os dois.")

    secao("Por que a escolha do pivô importa (entrada já ordenada)")
    chave = CRITERIOS[0][1]
    for n in (500, 2_000):
        dados = gerar_catalogo(n, semente=3)
        merge_sort(dados, chave=chave)                      # catálogo que já está em ordem
        mediana = quick_sort(list(dados), chave=chave)
        contador = [0]
        try:
            _quick_sort_pivo_fixo(list(dados), 0, n - 1, chave, contador)
            ingenuo = f"{numero(contador[0])} comparações (= n(n-1)/2, o pior caso)"
        except RecursionError:
            ingenuo = f"RecursionError: a recursão teria {numero(n)} níveis e o Python para em ~1.000"
        print(f"  n = {numero(n)}: pivô fixo -> {ingenuo}")
        print(f"  {'':10}mediana-de-três -> {numero(mediana.comparacoes)} comparações")


if __name__ == "__main__":
    executar_demonstracao()
