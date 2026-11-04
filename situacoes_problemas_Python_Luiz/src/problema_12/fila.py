"""Fila (FIFO) implementada com nós encadeados.

Por que nós encadeados e não a lista do Python?
    Remover do início de uma lista nativa (lista.pop(0)) custa O(n), porque
    todos os outros elementos são deslocados uma posição. Com nós encadeados
    e dois ponteiros (início e fim), enfileirar e desenfileirar custam O(1),
    como o próprio enunciado pede para implementações eficientes.

Operações (com os nomes usados no enunciado):
    enqueue  -> entra no fim da fila .............. O(1)
    dequeue  -> sai do início da fila ............. O(1)
    front    -> consulta o próximo, sem remover ... O(1)
    is_empty -> a fila está vazia? ................ O(1)
    size     -> quantidade de elementos ........... O(1)
"""

from __future__ import annotations


class _No:
    """Nó da fila: guarda um valor e aponta para o nó seguinte."""

    __slots__ = ("valor", "proximo")

    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class Fila:
    """Fila FIFO: o primeiro elemento que entra é o primeiro que sai."""

    def __init__(self, itens=None):
        self._inicio = None  # nó que vai sair primeiro
        self._fim = None     # último nó que entrou
        self._tamanho = 0
        if itens is not None:
            for item in itens:
                self.enqueue(item)

    def enqueue(self, valor) -> None:
        """Insere um elemento no FIM da fila. O(1)."""
        novo = _No(valor)
        if self._fim is None:          # fila vazia: o novo nó é início e fim
            self._inicio = novo
        else:
            self._fim.proximo = novo   # o antigo último passa a apontar para o novo
        self._fim = novo
        self._tamanho += 1

    def dequeue(self):
        """Remove e devolve o elemento do INÍCIO da fila. O(1).

        Lança IndexError se a fila estiver vazia.
        """
        if self._inicio is None:
            raise IndexError("dequeue em fila vazia")
        no = self._inicio
        self._inicio = no.proximo
        if self._inicio is None:       # a fila esvaziou: não existe mais fim
            self._fim = None
        self._tamanho -= 1
        return no.valor

    def front(self):
        """Devolve o próximo elemento a sair, sem removê-lo. O(1)."""
        if self._inicio is None:
            raise IndexError("front em fila vazia")
        return self._inicio.valor

    def is_empty(self) -> bool:
        """True se a fila não tiver elementos. O(1)."""
        return self._tamanho == 0

    def size(self) -> int:
        """Quantidade de elementos. O(1): o contador é atualizado a cada operação."""
        return self._tamanho

    def __len__(self) -> int:
        return self._tamanho

    def __iter__(self):
        """Percorre do início ao fim SEM remover nada (útil para listar). O(n)."""
        atual = self._inicio
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def __repr__(self) -> str:
        return "Fila([" + ", ".join(repr(valor) for valor in self) + "])"
