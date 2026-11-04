"""Quick Sort com pivô mediana-de-três e partição de Hoare.

Ideia: escolhe um PIVÔ, rearruma o vetor para que a parte esquerda só tenha
elementos que vêm antes do pivô (ou empatados com ele) e a parte direita só
elementos que vêm depois (ou empatados) e ordena cada parte recursivamente.

Três decisões para fugir do pior caso O(n²):
  1. Pivô MEDIANA-DE-TRÊS: a mediana entre o primeiro, o do meio e o último.
     Em vetores já ordenados ou invertidos (pior caso do pivô fixo) ela é o
     elemento central, então a divisão fica equilibrada.
  2. Partição de HOARE: dois índices andam um em direção ao outro e trocam os
     pares que estão do lado errado. Elementos IGUAIS ao pivô são espalhados
     pelos dois lados, então muitos valores repetidos (mesmo preço, mesma
     categoria) não desequilibram a divisão.
  3. Recursão só na parte MENOR e laço na maior: a profundidade da pilha de
     chamadas fica O(log n), longe do limite de recursão do Python.

Detalhe de eficiência: pedaços com até 3 elementos são ordenados direto (a
própria mediana-de-três já deixa 3 elementos em ordem), sem gastar uma
partição inteira com eles.

Complexidade:
    tempo ........... O(n log n) no melhor caso e em média; O(n²) no pior caso
                      teórico (raríssimo com mediana-de-três)
    espaço extra .... O(log n) (pilha de recursão)
    estável ......... NÃO: use chave com critério de desempate quando a ordem
                      entre empates importar
"""

from __future__ import annotations

from time import perf_counter

from ordenacao.metricas import Metricas, criar_comparador


def quick_sort(lista: list, chave=None, decrescente: bool = False) -> Metricas:
    """Ordena `lista` no próprio lugar e devolve as métricas da execução."""
    metricas = Metricas("Quick Sort", len(lista))
    deve_vir_depois = criar_comparador(chave, decrescente, metricas)
    inicio = perf_counter()

    _quick_sort(lista, 0, len(lista) - 1, deve_vir_depois, metricas)

    metricas.tempo_ms = (perf_counter() - inicio) * 1000
    return metricas


def _trocar(vetor: list, i: int, j: int, metricas: Metricas) -> None:
    vetor[i], vetor[j] = vetor[j], vetor[i]
    metricas.trocas += 1


def _mediana_de_tres(vetor: list, ini: int, fim: int, deve_vir_depois, metricas: Metricas):
    """Ordena vetor[ini], vetor[meio] e vetor[fim] entre si e devolve o do meio.

    Depois disso vetor[ini] <= pivô <= vetor[fim], o que garante que a
    partição sempre divide o intervalo em duas partes não vazias.
    """
    meio = (ini + fim) // 2
    if deve_vir_depois(vetor[ini], vetor[meio]):
        _trocar(vetor, ini, meio, metricas)
    if deve_vir_depois(vetor[ini], vetor[fim]):
        _trocar(vetor, ini, fim, metricas)
    if deve_vir_depois(vetor[meio], vetor[fim]):
        _trocar(vetor, meio, fim, metricas)
    return vetor[meio]


def _particionar(vetor: list, ini: int, fim: int, deve_vir_depois, metricas: Metricas) -> int:
    """Partição de Hoare. Devolve o índice `corte` tal que:

        vetor[ini..corte]   -> vêm antes do pivô ou empatam com ele
        vetor[corte+1..fim] -> vêm depois do pivô ou empatam com ele
    """
    pivo = _mediana_de_tres(vetor, ini, fim, deve_vir_depois, metricas)
    i = ini - 1
    j = fim + 1
    while True:
        i += 1
        while deve_vir_depois(pivo, vetor[i]):   # vetor[i] já está do lado certo (esquerdo)
            i += 1
        j -= 1
        while deve_vir_depois(vetor[j], pivo):   # vetor[j] já está do lado certo (direito)
            j -= 1
        if i >= j:                               # os índices se cruzaram: partição pronta
            return j
        _trocar(vetor, i, j, metricas)           # os dois estavam do lado errado: troca


def _quick_sort(vetor: list, ini: int, fim: int, deve_vir_depois, metricas: Metricas) -> None:
    while fim - ini >= 3:                    # 4 ou mais elementos: particiona
        corte = _particionar(vetor, ini, fim, deve_vir_depois, metricas)
        # recursão na parte menor; a maior continua no laço (pilha O(log n))
        if (corte - ini) < (fim - corte - 1):
            _quick_sort(vetor, ini, corte, deve_vir_depois, metricas)
            ini = corte + 1
        else:
            _quick_sort(vetor, corte + 1, fim, deve_vir_depois, metricas)
            fim = corte
    # Sobraram no máximo 3 elementos: ordena direto, sem partição.
    if fim - ini == 1:
        if deve_vir_depois(vetor[ini], vetor[fim]):
            _trocar(vetor, ini, fim, metricas)
    elif fim - ini == 2:
        _mediana_de_tres(vetor, ini, fim, deve_vir_depois, metricas)   # deixa os três em ordem
