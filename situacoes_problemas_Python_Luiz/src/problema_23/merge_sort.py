"""Merge Sort (dividir para conquistar) e a etapa de intercalação (merge).

Ideia:
  1. DIVIDIR: parte o vetor ao meio, recursivamente, até sobrarem pedaços de
     tamanho 1 (que já estão ordenados);
  2. CONQUISTAR: INTERCALA (merge) pares de pedaços ordenados, sempre tirando
     o menor elemento da frente de um dos dois, até remontar o vetor inteiro.

Complexidade:
    tempo ........... O(n log n) em TODOS os casos (log n níveis, O(n) por nível)
    espaço extra .... O(n) para as listas auxiliares da intercalação
    estável ......... sim: no empate, o elemento da metade ESQUERDA sai primeiro
"""

from __future__ import annotations

from time import perf_counter

from metricas import Metricas, criar_comparador


def merge_sort(lista: list, chave=None, decrescente: bool = False) -> Metricas:
    """Ordena `lista` e devolve as métricas.

    A ordenação monta uma lista nova e copia o resultado de volta, então quem
    chamou vê a própria lista ordenada (como nos outros algoritmos).
    Em `trocas` são contadas as cópias feitas durante as intercalações.
    """
    metricas = Metricas("Merge Sort", len(lista))
    deve_vir_depois = criar_comparador(chave, decrescente, metricas)
    inicio = perf_counter()

    lista[:] = _merge_sort(lista, deve_vir_depois, metricas)

    metricas.tempo_ms = (perf_counter() - inicio) * 1000
    return metricas


def _merge_sort(vetor: list, deve_vir_depois, metricas: Metricas) -> list:
    if len(vetor) <= 1:
        return vetor[:]                                  # caso base: já ordenado
    meio = len(vetor) // 2
    esquerda = _merge_sort(vetor[:meio], deve_vir_depois, metricas)   # dividir
    direita = _merge_sort(vetor[meio:], deve_vir_depois, metricas)
    return _intercalar(esquerda, direita, deve_vir_depois, metricas)  # conquistar


def _intercalar(esquerda: list, direita: list, deve_vir_depois, metricas: Metricas) -> list:
    """Junta duas listas ORDENADAS em uma lista ordenada. O(len(esq) + len(dir))."""
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        # Só tira da direita se o da esquerda tiver que vir DEPOIS dele.
        # No empate sai o da esquerda (que veio antes no vetor): estabilidade.
        if deve_vir_depois(esquerda[i], direita[j]):
            resultado.append(direita[j])
            j += 1
        else:
            resultado.append(esquerda[i])
            i += 1
    # uma das listas acabou: o resto da outra já está em ordem
    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1
    while j < len(direita):
        resultado.append(direita[j])
        j += 1
    metricas.trocas += len(resultado)
    return resultado


def intercalar(esquerda: list, direita: list, chave=None, decrescente: bool = False):
    """Etapa de merge pública: intercala duas listas já ordenadas.

    Devolve (lista_intercalada, metricas). Não altera as listas recebidas.
    """
    metricas = Metricas("Intercalação (merge)", len(esquerda) + len(direita))
    deve_vir_depois = criar_comparador(chave, decrescente, metricas)
    inicio = perf_counter()
    resultado = _intercalar(esquerda, direita, deve_vir_depois, metricas)
    metricas.tempo_ms = (perf_counter() - inicio) * 1000
    return resultado, metricas
