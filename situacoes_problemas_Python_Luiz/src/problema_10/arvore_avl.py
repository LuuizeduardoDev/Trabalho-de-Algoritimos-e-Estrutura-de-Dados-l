"""Árvore AVL: árvore binária de busca que se mantém balanceada.

Em cada nó, a diferença de altura entre as subárvores esquerda e direita
(o FATOR DE BALANCEAMENTO) fica sempre em -1, 0 ou +1. Quando uma inserção
ou remoção quebra essa regra, a árvore se corrige com ROTAÇÕES:

    caso LL (pesada à esquerda-esquerda) .... 1 rotação à direita
    caso RR (pesada à direita-direita) ...... 1 rotação à esquerda
    caso LR (esquerda, depois direita) ...... rotação dupla (esquerda + direita)
    caso RL (direita, depois esquerda) ...... rotação dupla (direita + esquerda)

Com isso a altura fica sempre O(log n) (no máximo ~1,44 * log2(n + 2)),
e busca, inserção e remoção custam O(log n) mesmo no PIOR caso.

Cada nó também guarda o TAMANHO da sua subárvore. Esse campo extra permite
descobrir a posição de uma chave na ordem (posicao) e a k-ésima chave
(k_esimo) em O(log n), o que é útil para rankings.

Convenção: árvore vazia tem altura 0 e um nó sozinho tem altura 1.
"""

from __future__ import annotations

from dataclasses import dataclass


class NoAVL:
    """Nó da AVL: chave, valor, filhos, altura e tamanho da subárvore."""

    __slots__ = ("chave", "valor", "esquerda", "direita", "altura", "tamanho")

    def __init__(self, chave, valor=None):
        self.chave = chave
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1    # um nó novo é sempre folha
        self.tamanho = 1   # quantidade de nós na subárvore que começa aqui


def _altura(no) -> int:
    return no.altura if no is not None else 0


def _tamanho(no) -> int:
    return no.tamanho if no is not None else 0


@dataclass
class ContadorRotacoes:
    """Quantas rotações de cada tipo a árvore já precisou fazer."""

    ll: int = 0  # rotação simples à direita
    rr: int = 0  # rotação simples à esquerda
    lr: int = 0  # rotação dupla esquerda-direita
    rl: int = 0  # rotação dupla direita-esquerda

    @property
    def total(self) -> int:
        return self.ll + self.rr + self.lr + self.rl

    def __str__(self) -> str:
        return f"LL={self.ll}, RR={self.rr}, LR={self.lr}, RL={self.rl} (total {self.total})"


class ArvoreAVL:
    """Árvore AVL genérica (chaves comparáveis com < e >)."""

    def __init__(self):
        self.raiz = None
        self.rotacoes = ContadorRotacoes()

    # ------------------------------------------------------------------ medidas do nó
    @staticmethod
    def fator_balanceamento(no) -> int:
        """altura(esquerda) - altura(direita). Na AVL fica sempre entre -1 e +1."""
        if no is None:
            return 0
        return _altura(no.esquerda) - _altura(no.direita)

    @staticmethod
    def _atualizar(no) -> None:
        """Recalcula altura e tamanho a partir dos filhos. O(1)."""
        no.altura = 1 + max(_altura(no.esquerda), _altura(no.direita))
        no.tamanho = 1 + _tamanho(no.esquerda) + _tamanho(no.direita)

    # ------------------------------------------------------------------ rotações
    def _rotacao_direita(self, y):
        """Rotação simples à direita (corrige excesso à esquerda).

                y                x
               / \\             / \\
              x   C    -->     A   y
             / \\                  / \\
            A   B                B   C
        """
        x = y.esquerda
        y.esquerda = x.direita
        x.direita = y
        self._atualizar(y)   # y desceu: atualiza primeiro
        self._atualizar(x)
        return x             # x é a nova raiz desta subárvore

    def _rotacao_esquerda(self, x):
        """Rotação simples à esquerda (corrige excesso à direita).

              x                    y
             / \\                 / \\
            A   y      -->       x   C
               / \\             / \\
              B   C            A   B
        """
        y = x.direita
        x.direita = y.esquerda
        y.esquerda = x
        self._atualizar(x)
        self._atualizar(y)
        return y

    def _rebalancear(self, no):
        """Atualiza o nó e aplica a rotação necessária, se houver. O(1)."""
        self._atualizar(no)
        fator = self.fator_balanceamento(no)
        if fator > 1:                                         # pesado à esquerda
            if self.fator_balanceamento(no.esquerda) >= 0:    # caso LL
                self.rotacoes.ll += 1
                return self._rotacao_direita(no)
            self.rotacoes.lr += 1                             # caso LR
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)
        if fator < -1:                                        # pesado à direita
            if self.fator_balanceamento(no.direita) <= 0:     # caso RR
                self.rotacoes.rr += 1
                return self._rotacao_esquerda(no)
            self.rotacoes.rl += 1                             # caso RL
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)
        return no                                             # já está balanceado

    # ------------------------------------------------------------------ inserção
    def inserir(self, chave, valor=None) -> bool:
        """Insere (chave, valor) e rebalanceia o caminho até a raiz. O(log n).

        Se a chave já existir, só atualiza o valor e devolve False.
        """
        self._inseriu = False
        self.raiz = self._inserir(self.raiz, chave, valor)
        return self._inseriu

    def _inserir(self, no, chave, valor):
        if no is None:
            self._inseriu = True
            return NoAVL(chave, valor)
        if chave < no.chave:
            no.esquerda = self._inserir(no.esquerda, chave, valor)
        elif chave > no.chave:
            no.direita = self._inserir(no.direita, chave, valor)
        else:
            no.valor = valor
            return no
        return self._rebalancear(no)   # na volta da recursão, corrige cada ancestral

    # ------------------------------------------------------------------ remoção
    def remover(self, chave) -> bool:
        """Remove a chave e rebalanceia o caminho até a raiz. O(log n).

        Devolve True se a chave existia.
        """
        self._removeu = False
        self.raiz = self._remover(self.raiz, chave)
        return self._removeu

    def _remover(self, no, chave):
        if no is None:
            return None
        if chave < no.chave:
            no.esquerda = self._remover(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._remover(no.direita, chave)
        else:
            self._removeu = True
            if no.esquerda is None:            # zero ou um filho: o filho sobe
                return no.direita
            if no.direita is None:
                return no.esquerda
            sucessor = no.direita              # dois filhos: usa o sucessor em ordem
            while sucessor.esquerda is not None:
                sucessor = sucessor.esquerda
            no.chave, no.valor = sucessor.chave, sucessor.valor
            no.direita = self._remover(no.direita, sucessor.chave)
        return self._rebalancear(no)

    # ------------------------------------------------------------------ consultas
    def buscar(self, chave, padrao=None):
        """Devolve o valor associado à chave, ou `padrao`. O(log n)."""
        atual = self.raiz
        while atual is not None:
            if chave < atual.chave:
                atual = atual.esquerda
            elif chave > atual.chave:
                atual = atual.direita
            else:
                return atual.valor
        return padrao

    def __contains__(self, chave) -> bool:
        marcador = object()
        return self.buscar(chave, marcador) is not marcador

    def em_ordem(self):
        """Gera (chave, valor) em ordem crescente de chave. O(n) para tudo.

        Como é um gerador, quem consome pode parar cedo: pegar só os k
        primeiros custa O(log n + k).
        """
        yield from self._em_ordem(self.raiz)

    def _em_ordem(self, no):
        if no is not None:
            yield from self._em_ordem(no.esquerda)
            yield (no.chave, no.valor)
            yield from self._em_ordem(no.direita)

    def primeiros(self, k: int) -> list:
        """Os k primeiros pares (chave, valor) na ordem. O(log n + k)."""
        resultado = []
        if k <= 0:
            return resultado
        for par in self.em_ordem():
            resultado.append(par)
            if len(resultado) == k:
                break
        return resultado

    def posicao(self, chave):
        """Posição (1 = primeira) da chave na ordem crescente, ou None. O(log n).

        Usa o tamanho das subárvores: ao descer para a direita, todos os nós
        da esquerda e o próprio nó ficam antes da chave procurada.
        """
        antes = 0
        atual = self.raiz
        while atual is not None:
            if chave < atual.chave:
                atual = atual.esquerda
            elif chave > atual.chave:
                antes += _tamanho(atual.esquerda) + 1
                atual = atual.direita
            else:
                return antes + _tamanho(atual.esquerda) + 1
        return None

    def k_esimo(self, k: int):
        """Par (chave, valor) que ocupa a posição k (1 = primeira). O(log n)."""
        if k < 1 or k > len(self):
            raise IndexError(f"posição {k} fora do intervalo 1..{len(self)}")
        atual = self.raiz
        while True:
            esquerda = _tamanho(atual.esquerda)
            if k <= esquerda:
                atual = atual.esquerda
            elif k == esquerda + 1:
                return (atual.chave, atual.valor)
            else:
                k -= esquerda + 1
                atual = atual.direita

    def altura(self) -> int:
        """Altura da árvore (número de níveis). O(1): guardada na raiz."""
        return _altura(self.raiz)

    def __len__(self) -> int:
        return _tamanho(self.raiz)

    # ------------------------------------------------------------------ verificação
    def esta_balanceada(self) -> bool:
        """Confere TODAS as regras da AVL (usado nos testes e na demonstração). O(n).

        Verifica a ordem da BST, a altura e o tamanho guardados em cada nó e
        se todo fator de balanceamento está em {-1, 0, +1}.
        """
        def verificar(no, minimo, maximo):
            if no is None:
                return True, 0, 0
            if (minimo is not None and not no.chave > minimo) or (
                maximo is not None and not no.chave < maximo
            ):
                return False, 0, 0
            ok_e, alt_e, tam_e = verificar(no.esquerda, minimo, no.chave)
            ok_d, alt_d, tam_d = verificar(no.direita, no.chave, maximo)
            altura = 1 + max(alt_e, alt_d)
            tamanho = 1 + tam_e + tam_d
            ok = (
                ok_e
                and ok_d
                and abs(alt_e - alt_d) <= 1
                and no.altura == altura
                and no.tamanho == tamanho
            )
            return ok, altura, tamanho

        return verificar(self.raiz, None, None)[0]

    def fatores_de_balanceamento(self) -> list:
        """Lista (chave, altura do nó, fator) em ordem de chave. Útil para exibir."""
        resultado = []

        def visitar(no):
            if no is not None:
                visitar(no.esquerda)
                resultado.append((no.chave, no.altura, self.fator_balanceamento(no)))
                visitar(no.direita)

        visitar(self.raiz)
        return resultado

    def desenho(self, formatar=str) -> list:
        """Desenho da árvore "deitada" (raiz à esquerda, filho direito em cima).

        Devolve uma lista de linhas de texto. Indicado para árvores pequenas.
        """
        linhas = []

        def visitar(no, nivel):
            if no is not None:
                visitar(no.direita, nivel + 1)
                linhas.append("      " * nivel + formatar(no.chave))
                visitar(no.esquerda, nivel + 1)

        visitar(self.raiz, 0)
        return linhas
