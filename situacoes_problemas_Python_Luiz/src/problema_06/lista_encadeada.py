"""Lista simplesmente encadeada com ponteiros para o início e o fim.

Cada nó guarda um valor e a referência para o próximo nó. Diferente de um
vetor, inserir ou remover um elemento não exige deslocar os demais: basta
religar ponteiros. O custo fica em ENCONTRAR a posição, que exige percorrer
a lista a partir do início.

Operações e custos (n = número de elementos):
    inserir_inicio / inserir_fim ............ O(1)
    inserir_em(posicao) ..................... O(n)
    remover_inicio .......................... O(1)
    remover_em(posicao) / remover_se(cond) .. O(n)
    buscar / filtrar / obter / indice ....... O(n)

As buscas recebem uma função-condição (por exemplo,
`lambda produto: produto.codigo == "CIM-50"`), assim a mesma lista serve
para produtos, músicas, contatos etc.
"""

from __future__ import annotations


class _No:
    """Nó da lista: guarda um valor e aponta para o próximo nó."""

    __slots__ = ("valor", "proximo")

    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class ListaEncadeada:
    """Lista simplesmente encadeada genérica."""

    def __init__(self, itens=None):
        self._inicio = None
        self._fim = None
        self._tamanho = 0
        if itens is not None:
            for item in itens:
                self.inserir_fim(item)

    # ------------------------------------------------------------------ inserções
    def inserir_inicio(self, valor) -> None:
        """Insere antes do primeiro elemento. O(1)."""
        novo = _No(valor, self._inicio)
        self._inicio = novo
        if self._fim is None:          # lista estava vazia
            self._fim = novo
        self._tamanho += 1

    def inserir_fim(self, valor) -> None:
        """Insere depois do último elemento. O(1) graças ao ponteiro de fim."""
        novo = _No(valor)
        if self._fim is None:
            self._inicio = novo
        else:
            self._fim.proximo = novo
        self._fim = novo
        self._tamanho += 1

    def inserir_em(self, posicao: int, valor) -> None:
        """Insere de forma que o valor fique na `posicao` (0 = início). O(n).

        Posições válidas: 0 até len(lista). Fora disso lança IndexError.
        """
        if posicao < 0 or posicao > self._tamanho:
            raise IndexError(f"posição {posicao} inválida para lista com {self._tamanho} elementos")
        if posicao == 0:
            self.inserir_inicio(valor)
            return
        if posicao == self._tamanho:
            self.inserir_fim(valor)
            return
        anterior = self._no_na_posicao(posicao - 1)
        anterior.proximo = _No(valor, anterior.proximo)
        self._tamanho += 1

    # ------------------------------------------------------------------ remoções
    def remover_inicio(self):
        """Remove e devolve o primeiro elemento. O(1)."""
        if self._inicio is None:
            raise IndexError("remoção em lista vazia")
        no = self._inicio
        self._inicio = no.proximo
        if self._inicio is None:
            self._fim = None
        self._tamanho -= 1
        return no.valor

    def remover_em(self, posicao: int):
        """Remove e devolve o elemento da `posicao`. O(n)."""
        if posicao < 0 or posicao >= self._tamanho:
            raise IndexError(f"posição {posicao} inválida para lista com {self._tamanho} elementos")
        if posicao == 0:
            return self.remover_inicio()
        anterior = self._no_na_posicao(posicao - 1)
        return self._remover_depois_de(anterior)

    def remover_se(self, condicao):
        """Remove o PRIMEIRO elemento que satisfaz `condicao`. O(n).

        Devolve o valor removido, ou None se nenhum elemento satisfizer.
        """
        anterior = None
        atual = self._inicio
        while atual is not None:
            if condicao(atual.valor):
                if anterior is None:
                    return self.remover_inicio()
                return self._remover_depois_de(anterior)
            anterior = atual
            atual = atual.proximo
        return None

    def _remover_depois_de(self, anterior: _No):
        """Desliga o nó seguinte a `anterior` religando os ponteiros. O(1)."""
        removido = anterior.proximo
        anterior.proximo = removido.proximo
        if removido is self._fim:       # removemos o último: o fim recua
            self._fim = anterior
        self._tamanho -= 1
        return removido.valor

    # ------------------------------------------------------------------ consultas
    def buscar(self, condicao):
        """Devolve o primeiro valor que satisfaz `condicao`, ou None. O(n)."""
        for valor in self:
            if condicao(valor):
                return valor
        return None

    def filtrar(self, condicao) -> list:
        """Devolve (em uma lista do Python) todos os valores que satisfazem `condicao`. O(n)."""
        return [valor for valor in self if condicao(valor)]

    def indice(self, condicao) -> int:
        """Posição do primeiro valor que satisfaz `condicao`, ou -1. O(n)."""
        for posicao, valor in enumerate(self):
            if condicao(valor):
                return posicao
        return -1

    def obter(self, posicao: int):
        """Devolve o valor da `posicao`. O(n)."""
        if posicao < 0 or posicao >= self._tamanho:
            raise IndexError(f"posição {posicao} inválida para lista com {self._tamanho} elementos")
        return self._no_na_posicao(posicao).valor

    def _no_na_posicao(self, posicao: int) -> _No:
        atual = self._inicio
        for _ in range(posicao):
            atual = atual.proximo
        return atual

    # ------------------------------------------------------------------ utilidades
    def esta_vazia(self) -> bool:
        return self._tamanho == 0

    def para_lista(self) -> list:
        """Copia os valores para uma lista do Python (só para exibição)."""
        return list(self)

    def __len__(self) -> int:
        return self._tamanho

    def __iter__(self):
        atual = self._inicio
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def __repr__(self) -> str:
        return "ListaEncadeada([" + " -> ".join(repr(valor) for valor in self) + "])"
