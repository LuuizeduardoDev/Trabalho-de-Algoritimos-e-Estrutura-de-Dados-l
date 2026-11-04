"""Bubble Sort com parada antecipada.

Ideia: percorre o vetor comparando VIZINHOS e trocando os que estão fora de
ordem. A cada passada o maior elemento restante "borbulha" até o fim, então a
parte final já ordenada não precisa ser revisitada.

Otimização (pedida na SP15/SP16): se uma passada inteira não fizer nenhuma
troca, o vetor já está ordenado e o algoritmo para.

Complexidade:
    melhor caso (já ordenado) ... O(n): uma passada, n-1 comparações, 0 trocas
    caso médio e pior caso ...... O(n²) comparações e trocas
    espaço extra ................ O(1) (ordena no próprio vetor)
    estável ..................... sim (só troca vizinhos estritamente fora de ordem)
"""

from __future__ import annotations

from time import perf_counter

from metricas import Metricas, criar_comparador


def bubble_sort(lista: list, chave=None, decrescente: bool = False) -> Metricas:
    """Ordena `lista` no próprio lugar e devolve as métricas da execução."""
    metricas = Metricas("Bubble Sort", len(lista))
    deve_vir_depois = criar_comparador(chave, decrescente, metricas)
    inicio = perf_counter()

    n = len(lista)
    for passada in range(n - 1):
        metricas.passadas += 1
        houve_troca = False
        # os últimos `passada` elementos já estão na posição final
        for j in range(n - 1 - passada):
            if deve_vir_depois(lista[j], lista[j + 1]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                metricas.trocas += 1
                houve_troca = True
        if not houve_troca:   # parada antecipada: nenhuma troca = vetor ordenado
            break

    metricas.tempo_ms = (perf_counter() - inicio) * 1000
    return metricas
