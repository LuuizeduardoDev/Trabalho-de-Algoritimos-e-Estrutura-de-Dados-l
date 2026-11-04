"""Selection Sort.

Ideia: na passada i, procura o elemento que deve ocupar a posição i (o menor,
ou o maior na ordem decrescente) entre os que ainda não foram posicionados e
faz UMA troca para colocá-lo lá.

Complexidade:
    comparações ........ sempre n(n-1)/2 -> O(n²), em qualquer caso
    trocas ............. no máximo n-1 -> O(n) (vantagem quando trocar é caro)
    espaço extra ....... O(1)
    estável ............ NÃO: a troca pode pular um elemento por cima de outro
                         com a mesma chave. Quando a ordem entre empates
                         importa, use uma chave com critério de desempate.
"""

from __future__ import annotations

from time import perf_counter

from ordenacao.metricas import Metricas, criar_comparador


def selection_sort(lista: list, chave=None, decrescente: bool = False) -> Metricas:
    """Ordena `lista` no próprio lugar e devolve as métricas da execução."""
    metricas = Metricas("Selection Sort", len(lista))
    deve_vir_depois = criar_comparador(chave, decrescente, metricas)
    inicio = perf_counter()

    n = len(lista)
    for i in range(n - 1):
        metricas.passadas += 1
        escolhido = i
        # procura, entre i..n-1, o elemento que deve vir primeiro
        for j in range(i + 1, n):
            if deve_vir_depois(lista[escolhido], lista[j]):
                escolhido = j
        if escolhido != i:      # no máximo uma troca por passada
            lista[i], lista[escolhido] = lista[escolhido], lista[i]
            metricas.trocas += 1

    metricas.tempo_ms = (perf_counter() - inicio) * 1000
    return metricas
