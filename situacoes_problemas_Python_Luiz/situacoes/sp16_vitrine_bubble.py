"""SP16 – Ordenação de Produtos por Preço em uma Vitrine Pequena.

Algoritmo usado: Bubble Sort com parada antecipada -> ordenacao/bubble_sort.py

O que o enunciado pede e onde está:
  * ordenar produtos (nome + preço) com Bubble Sort ... ordenar_vitrine()
  * opção de ordem crescente ou decrescente .......... parâmetro `crescente`
  * demonstração com 10 a 20 produtos ................ VITRINE (15 produtos)

Por que Bubble Sort aqui: a vitrine tem poucos itens (15), então O(n²) significa
no máximo 105 comparações, instantâneo. O algoritmo é ESTÁVEL (produtos com o
mesmo preço mantêm a ordem em que foram cadastrados) e, com a parada
antecipada, uma vitrine que já está em ordem é conferida em uma única passada.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):  # permite rodar este arquivo diretamente
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ordenacao.bubble_sort import bubble_sort
from situacoes.utilidades import cabecalho, imprimir_tabela, moeda, secao


@dataclass
class ProdutoVitrine:
    nome: str
    preco: float


def ordenar_vitrine(produtos: list, crescente: bool = True):
    """Devolve (nova lista ordenada por preço, métricas). A lista original não muda."""
    copia = list(produtos)
    metricas = bubble_sort(copia, chave=lambda produto: produto.preco, decrescente=not crescente)
    return copia, metricas


VITRINE = [
    ProdutoVitrine("Fone de ouvido bluetooth", 129.90),
    ProdutoVitrine("Garrafa térmica 1 L", 89.90),
    ProdutoVitrine("Caneca personalizada", 39.90),
    ProdutoVitrine("Mochila escolar", 149.00),
    ProdutoVitrine("Luminária LED de mesa", 74.50),
    ProdutoVitrine("Mouse sem fio", 59.90),
    ProdutoVitrine("Caderno inteligente", 99.00),
    ProdutoVitrine("Chaveiro de couro", 39.90),
    ProdutoVitrine("Kit canetas coloridas", 24.90),
    ProdutoVitrine("Smartwatch esportivo", 349.00),
    ProdutoVitrine("Pen drive 64 GB", 45.00),
    ProdutoVitrine("Suporte para celular", 29.90),
    ProdutoVitrine("Teclado compacto", 119.00),
    ProdutoVitrine("Carregador portátil 10.000 mAh", 139.90),
    ProdutoVitrine("Agenda 2027", 34.90),
]


def _mostrar(produtos: list) -> None:
    imprimir_tabela(["#", "Produto", "Preço"],
                    [[i, p.nome, moeda(p.preco)] for i, p in enumerate(produtos, start=1)], "><>")


def executar_demonstracao() -> None:
    cabecalho("SP16 - Vitrine ordenada por preço (Bubble Sort com parada antecipada)")

    secao(f"Vitrine na ordem de cadastro ({len(VITRINE)} produtos)")
    _mostrar(VITRINE)

    secao("Menor preço primeiro (crescente)")
    crescente, metricas = ordenar_vitrine(VITRINE, crescente=True)
    _mostrar(crescente)
    print(metricas.resumo())

    secao("Maior preço primeiro (decrescente)")
    decrescente, metricas = ordenar_vitrine(VITRINE, crescente=False)
    _mostrar(decrescente)
    print(metricas.resumo())

    secao("Estabilidade: empate de preço")
    empatados = [p.nome for p in crescente if p.preco == 39.90]
    print(f"  'Caneca personalizada' e 'Chaveiro de couro' custam {moeda(39.90)}.")
    print(f"  Cadastro: Caneca antes do Chaveiro | depois de ordenar: {' antes de '.join(empatados)}")
    print("  O Bubble Sort só troca vizinhos ESTRITAMENTE fora de ordem, então empates nunca se invertem.")

    secao("Parada antecipada: quanto custa cada situação (n = 15)")
    _, ja_ordenada = ordenar_vitrine(crescente, crescente=True)
    _, invertida = ordenar_vitrine(decrescente, crescente=True)
    _, original = ordenar_vitrine(VITRINE, crescente=True)
    imprimir_tabela(
        ["Entrada", "Passadas", "Comparações", "Trocas"],
        [["já em ordem crescente (melhor caso)", ja_ordenada.passadas, ja_ordenada.comparacoes, ja_ordenada.trocas],
         ["ordem de cadastro", original.passadas, original.comparacoes, original.trocas],
         ["em ordem decrescente (pior caso)", invertida.passadas, invertida.comparacoes, invertida.trocas]],
        "<>>>")
    print("Sem a parada antecipada, as três entradas fariam 14 passadas e 105 comparações.")


if __name__ == "__main__":
    executar_demonstracao()
