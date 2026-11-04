"""Algoritmos de ordenação implementados do zero, todos com a mesma interface.

    metricas = algoritmo(lista, chave=None, decrescente=False)

Ordenam a lista no próprio lugar e devolvem um objeto Metricas (comparações,
trocas/movimentações, passadas e tempo), para que possam ser comparados.
"""

from ordenacao.metricas import Metricas
from ordenacao.bubble_sort import bubble_sort
from ordenacao.selection_sort import selection_sort
from ordenacao.insertion_sort import insertion_sort, inserir_em_ordem
from ordenacao.merge_sort import merge_sort, intercalar
from ordenacao.quick_sort import quick_sort

__all__ = [
    "Metricas",
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "inserir_em_ordem",
    "merge_sort",
    "intercalar",
    "quick_sort",
]
