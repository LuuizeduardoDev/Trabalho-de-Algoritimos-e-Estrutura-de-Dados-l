"""Pilha (LIFO) usando a lista nativa do Python como vetor base.

O enunciado permite (e recomenda) usar o array nativo da linguagem como base
da pilha. Empilhar e desempilhar sempre no FINAL do vetor custa O(1)
(amortizado), porque nenhum outro elemento precisa ser deslocado.

Operações:
    push     -> empilha no topo ............ O(1) amortizado
    pop      -> desempilha do topo ......... O(1)
    peek     -> consulta o topo ............ O(1)
    is_empty -> a pilha está vazia? ........ O(1)
    size     -> quantidade de elementos .... O(1)
"""

from __future__ import annotations


class Pilha:
    """Pilha LIFO: o último elemento que entra é o primeiro que sai."""

    def __init__(self):
        self._itens = []  # o topo da pilha é o ÚLTIMO elemento do vetor

    def push(self, valor) -> None:
        """Coloca um elemento no topo. O(1) amortizado."""
        self._itens.append(valor)

    def pop(self):
        """Remove e devolve o elemento do topo. O(1).

        Lança IndexError se a pilha estiver vazia.
        """
        if not self._itens:
            raise IndexError("pop em pilha vazia")
        return self._itens.pop()

    def peek(self):
        """Devolve o elemento do topo sem removê-lo. O(1)."""
        if not self._itens:
            raise IndexError("peek em pilha vazia")
        return self._itens[-1]

    def is_empty(self) -> bool:
        """True se a pilha não tiver elementos. O(1)."""
        return len(self._itens) == 0

    def size(self) -> int:
        """Quantidade de elementos. O(1)."""
        return len(self._itens)

    def limpar(self) -> None:
        """Esvazia a pilha (útil, por exemplo, para descartar um histórico de refazer)."""
        self._itens = []

    def __len__(self) -> int:
        return len(self._itens)

    def __iter__(self):
        """Percorre do TOPO para a BASE (mesma ordem em que pop devolveria). O(n)."""
        for indice in range(len(self._itens) - 1, -1, -1):
            yield self._itens[indice]

    def __repr__(self) -> str:
        return "Pilha(topo -> [" + ", ".join(repr(valor) for valor in self) + "])"
