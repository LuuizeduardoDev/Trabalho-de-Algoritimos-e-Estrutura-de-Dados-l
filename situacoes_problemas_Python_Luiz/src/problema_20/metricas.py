"""Métricas comuns a todos os algoritmos de ordenação.

Todos os algoritmos de ordenação deste trabalho seguem o mesmo formato:

    metricas = algoritmo(lista, chave=None, decrescente=False)

  * ordenam a lista NO PRÓPRIO LUGAR (quem precisar da original faz uma cópia antes);
  * `chave` é uma função que extrai o critério (ex.: lambda p: p.preco);
  * `decrescente=True` inverte a ordem SEM perder a estabilidade dos algoritmos estáveis;
  * devolvem um objeto Metricas, com os contadores no mesmo formato, para que
    os algoritmos possam ser comparados entre si.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Metricas:
    """Contadores de uma execução de um algoritmo de ordenação."""

    algoritmo: str = ""
    n: int = 0
    comparacoes: int = 0   # comparações entre chaves de elementos
    # trocas: trocas de posição (Bubble, Selection, Quick) ou movimentações
    # (Insertion: deslocamentos; Merge: cópias feitas nas intercalações)
    trocas: int = 0
    passadas: int = 0      # passadas completas pelo vetor (Bubble e Selection)
    tempo_ms: float = 0.0  # tempo de execução em milissegundos

    def resumo(self) -> str:
        texto = f"{self.algoritmo}: n={self.n}, comparações={self.comparacoes}, trocas={self.trocas}"
        if self.passadas:
            texto += f", passadas={self.passadas}"
        return texto + ", tempo=" + f"{self.tempo_ms:.2f}".replace(".", ",") + " ms"


def criar_comparador(chave, decrescente: bool, metricas: Metricas):
    """Cria a função `deve_vir_depois(a, b)` usada por todos os algoritmos.

    Ela responde: "na ordem desejada, `a` precisa ficar DEPOIS de `b`?"
    Só devolve True em caso de desigualdade ESTRITA, por isso elementos com
    a mesma chave nunca são trocados entre si sem necessidade — é isso que
    mantém Bubble, Insertion e Merge estáveis também na ordem decrescente.
    Cada chamada conta uma comparação.
    """
    if chave is None:
        chave = _identidade

    if decrescente:
        def deve_vir_depois(a, b) -> bool:
            metricas.comparacoes += 1
            return chave(a) < chave(b)
    else:
        def deve_vir_depois(a, b) -> bool:
            metricas.comparacoes += 1
            return chave(a) > chave(b)

    return deve_vir_depois


def _identidade(valor):
    return valor
