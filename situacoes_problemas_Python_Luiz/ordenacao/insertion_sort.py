"""Insertion Sort (e inserção individual em lista ordenada).

Ideia: a parte esquerda do vetor já está ordenada; cada novo elemento é
"encaixado" nela, deslocando para a direita os que devem ficar depois dele
(como quem organiza cartas na mão).

Complexidade:
    melhor caso (já ordenado) ....... O(n): n-1 comparações e nenhum deslocamento
    quase ordenado .................. O(n + k), k = pares fora de ordem (inversões)
    caso médio e pior caso .......... O(n²)
    espaço extra .................... O(1)
    estável ......................... sim

É por isso que o Insertion Sort é a escolha natural para dados que chegam aos
poucos ou que mudam pouco de um dia para o outro (ranking de vendedores).
"""

from __future__ import annotations

from time import perf_counter

from ordenacao.metricas import Metricas, criar_comparador


def insertion_sort(lista: list, chave=None, decrescente: bool = False) -> Metricas:
    """Ordena `lista` no próprio lugar e devolve as métricas da execução.

    Em `trocas` são contados os DESLOCAMENTOS (cada elemento empurrado uma
    posição para a direita).
    """
    metricas = Metricas("Insertion Sort", len(lista))
    deve_vir_depois = criar_comparador(chave, decrescente, metricas)
    inicio = perf_counter()

    for i in range(1, len(lista)):
        metricas.passadas += 1
        atual = lista[i]
        j = i - 1
        # desloca para a direita os elementos que devem ficar depois de `atual`
        while j >= 0 and deve_vir_depois(lista[j], atual):
            lista[j + 1] = lista[j]
            metricas.trocas += 1
            j -= 1
        lista[j + 1] = atual   # encaixa `atual` no espaço aberto

    metricas.tempo_ms = (perf_counter() - inicio) * 1000
    return metricas


def inserir_em_ordem(lista: list, item, chave=None, decrescente: bool = False) -> int:
    """Insere UM item numa lista já ordenada, mantendo-a ordenada. O(n).

    É o passo interno do Insertion Sort aplicado a um único elemento novo
    (por exemplo, uma carta recebida). Devolve a posição em que o item ficou.
    """
    metricas = Metricas("Inserção individual", len(lista) + 1)
    deve_vir_depois = criar_comparador(chave, decrescente, metricas)
    lista.append(item)
    j = len(lista) - 2
    while j >= 0 and deve_vir_depois(lista[j], item):
        lista[j + 1] = lista[j]
        j -= 1
    lista[j + 1] = item
    return j + 1
