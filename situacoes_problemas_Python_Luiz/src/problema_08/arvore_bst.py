"""Árvore Binária de Busca (BST) genérica.

Regra da BST: para todo nó, as chaves da subárvore ESQUERDA são menores que a
chave do nó e as da subárvore DIREITA são maiores. Isso permite descartar
metade da árvore a cada comparação, quando ela está razoavelmente equilibrada.

Custos (h = altura da árvore):
    inserir / buscar / remover ...... O(h)  -> O(log n) em média, O(n) no pior caso
    em_ordem (listagem ordenada) .... O(n)
    espaço .......................... O(n) nós

O pior caso O(n) acontece quando as chaves chegam já ordenadas: a árvore vira
uma "lista" inclinada para um lado. É exatamente esse problema que a árvore
AVL (SP10, pasta problema_10) resolve.

Convenção de altura usada no trabalho: árvore vazia = 0, um único nó = 1
(a altura é o número de NÍVEIS).
"""

from __future__ import annotations


class NoBST:
    """Nó da árvore: chave de ordenação, valor associado e dois filhos."""

    __slots__ = ("chave", "valor", "esquerda", "direita")

    def __init__(self, chave, valor=None):
        self.chave = chave
        self.valor = valor
        self.esquerda = None
        self.direita = None


class ArvoreBST:
    """Árvore Binária de Busca sem balanceamento."""

    def __init__(self):
        self.raiz = None
        self._tamanho = 0

    # ------------------------------------------------------------------ inserção
    def inserir(self, chave, valor=None) -> bool:
        """Insere (chave, valor). O(h).

        Se a chave já existir, apenas atualiza o valor e devolve False.
        Devolve True quando um nó novo foi criado.
        """
        if self.raiz is None:
            self.raiz = NoBST(chave, valor)
            self._tamanho = 1
            return True
        atual = self.raiz
        while True:
            if chave < atual.chave:              # menor: desce para a esquerda
                if atual.esquerda is None:
                    atual.esquerda = NoBST(chave, valor)
                    break
                atual = atual.esquerda
            elif chave > atual.chave:            # maior: desce para a direita
                if atual.direita is None:
                    atual.direita = NoBST(chave, valor)
                    break
                atual = atual.direita
            else:                                # chave repetida: só atualiza
                atual.valor = valor
                return False
        self._tamanho += 1
        return True

    # ------------------------------------------------------------------ busca
    def buscar(self, chave, padrao=None):
        """Devolve o valor associado à chave, ou `padrao` se não existir. O(h)."""
        no = self._buscar_no(chave)
        return padrao if no is None else no.valor

    def _buscar_no(self, chave):
        atual = self.raiz
        while atual is not None:
            if chave < atual.chave:
                atual = atual.esquerda
            elif chave > atual.chave:
                atual = atual.direita
            else:
                return atual
        return None

    def __contains__(self, chave) -> bool:
        return self._buscar_no(chave) is not None

    # ------------------------------------------------------------------ remoção
    def remover(self, chave) -> bool:
        """Remove a chave. Devolve True se ela existia. O(h).

        Três casos clássicos:
          1. nó folha ............ simplesmente sai da árvore;
          2. nó com um filho ..... o filho ocupa o lugar dele;
          3. nó com dois filhos .. copia o SUCESSOR (menor chave da subárvore
             direita) para o nó e remove o sucessor, que tem no máximo um filho.
        """
        self._removeu = False
        self.raiz = self._remover(self.raiz, chave)
        if self._removeu:
            self._tamanho -= 1
        return self._removeu

    def _remover(self, no, chave):
        if no is None:
            return None                       # chave não encontrada
        if chave < no.chave:
            no.esquerda = self._remover(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._remover(no.direita, chave)
        else:
            self._removeu = True
            if no.esquerda is None:           # casos 1 e 2
                return no.direita
            if no.direita is None:
                return no.esquerda
            sucessor = no.direita             # caso 3
            while sucessor.esquerda is not None:
                sucessor = sucessor.esquerda
            no.chave, no.valor = sucessor.chave, sucessor.valor
            no.direita = self._remover(no.direita, sucessor.chave)
        return no

    # ------------------------------------------------------------------ percursos e medidas
    def em_ordem(self):
        """Gera os pares (chave, valor) em ordem CRESCENTE de chave. O(n)."""
        yield from self._em_ordem(self.raiz)

    def _em_ordem(self, no):
        if no is not None:
            yield from self._em_ordem(no.esquerda)
            yield (no.chave, no.valor)
            yield from self._em_ordem(no.direita)

    def altura(self) -> int:
        """Número de níveis da árvore (vazia = 0). O(n)."""
        return self._altura(self.raiz)

    def _altura(self, no) -> int:
        if no is None:
            return 0
        return 1 + max(self._altura(no.esquerda), self._altura(no.direita))

    def minimo(self):
        """Menor chave da árvore. O(h)."""
        if self.raiz is None:
            raise ValueError("árvore vazia")
        atual = self.raiz
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual.chave

    def maximo(self):
        """Maior chave da árvore. O(h)."""
        if self.raiz is None:
            raise ValueError("árvore vazia")
        atual = self.raiz
        while atual.direita is not None:
            atual = atual.direita
        return atual.chave

    def __len__(self) -> int:
        return self._tamanho
