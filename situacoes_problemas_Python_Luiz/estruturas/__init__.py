"""Estruturas de dados implementadas do zero, sem bibliotecas que já as tragam prontas.

Cada arquivo contém uma estrutura e documenta o custo de cada operação.
A lista nativa do Python é usada apenas como vetor base, como o enunciado permite.
"""

from estruturas.fila import Fila
from estruturas.pilha import Pilha
from estruturas.lista_encadeada import ListaEncadeada
from estruturas.arvore_bst import ArvoreBST
from estruturas.arvore_avl import ArvoreAVL
from estruturas.tabela_hash import TabelaHash
from estruturas.grafo import Grafo

__all__ = [
    "Fila",
    "Pilha",
    "ListaEncadeada",
    "ArvoreBST",
    "ArvoreAVL",
    "TabelaHash",
    "Grafo",
]
