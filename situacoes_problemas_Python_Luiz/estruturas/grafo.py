"""Grafo com LISTA DE ADJACÊNCIA (direcionado ou não, com ou sem pesos).

Representação:
  * cada vértice tem um nome (texto) e recebe um índice inteiro 0, 1, 2...;
  * a tradução nome -> índice fica numa TabelaHash própria (O(1) em média);
  * _adjacencia[i] é a lista de vizinhos do vértice i, como pares (j, peso).

Por que lista de adjacência e não matriz?
    Redes reais são ESPARSAS: cada pessoa tem poucos amigos perto do total de
    usuários. A lista ocupa O(V + E); a matriz ocuparia O(V²) mesmo com
    pouquíssimas arestas.

Custos (V = vértices, E = arestas, grau(v) = quantidade de vizinhos de v):
    adicionar_vertice ............ O(1) em média
    adicionar_aresta ............. O(grau) (confere se a aresta já existe)
    vizinhos / grau .............. O(grau)
    busca em largura (BFS) ....... O(V + E)
    caminho_mais_curto (BFS) ..... O(V + E)   -> menor número de arestas
    componentes .................. O(V + E)
"""

from __future__ import annotations

from estruturas.fila import Fila
from estruturas.tabela_hash import TabelaHash


class Grafo:
    """Grafo por lista de adjacência; vértices identificados por nome."""

    def __init__(self, direcionado: bool = False):
        self.direcionado = direcionado
        self._indice_por_nome = TabelaHash()  # nome -> índice
        self._nomes = []                      # índice -> nome
        self._adjacencia = []                 # índice -> [(vizinho, peso), ...]
        self._num_arestas = 0

    # ------------------------------------------------------------------ vértices
    def adicionar_vertice(self, nome: str) -> bool:
        """Cria o vértice. Devolve False se ele já existia. O(1) em média."""
        if nome in self._indice_por_nome:
            return False
        self._indice_por_nome[nome] = len(self._nomes)
        self._nomes.append(nome)
        self._adjacencia.append([])
        return True

    def contem_vertice(self, nome: str) -> bool:
        return nome in self._indice_por_nome

    def _indice(self, nome: str) -> int:
        indice = self._indice_por_nome.buscar(nome)
        if indice is None:
            raise KeyError(f"vértice inexistente: {nome}")
        return indice

    def vertices(self) -> list:
        """Nomes dos vértices na ordem em que foram criados."""
        return list(self._nomes)

    def num_vertices(self) -> int:
        return len(self._nomes)

    def num_arestas(self) -> int:
        return self._num_arestas

    # ------------------------------------------------------------------ arestas
    def adicionar_aresta(self, origem: str, destino: str, peso=1) -> bool:
        """Liga origem e destino (cria os vértices se preciso). O(grau).

        Devolve False se a aresta já existia. Laços (origem == destino) não
        são permitidos.
        """
        if origem == destino:
            raise ValueError("um vértice não pode ser ligado a ele mesmo")
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        if self.tem_aresta(origem, destino):
            return False
        i, j = self._indice(origem), self._indice(destino)
        self._adjacencia[i].append((j, peso))
        if not self.direcionado:                 # não direcionado: liga nos dois sentidos
            self._adjacencia[j].append((i, peso))
        self._num_arestas += 1
        return True

    def remover_aresta(self, origem: str, destino: str) -> bool:
        """Desfaz a ligação. Devolve True se ela existia. O(grau)."""
        if not (self.contem_vertice(origem) and self.contem_vertice(destino)):
            return False
        i, j = self._indice(origem), self._indice(destino)
        if not self._remover_da_lista(i, j):
            return False
        if not self.direcionado:
            self._remover_da_lista(j, i)
        self._num_arestas -= 1
        return True

    def _remover_da_lista(self, i: int, j: int) -> bool:
        lista = self._adjacencia[i]
        for posicao in range(len(lista)):
            if lista[posicao][0] == j:
                lista.pop(posicao)
                return True
        return False

    def tem_aresta(self, origem: str, destino: str) -> bool:
        """Existe ligação origem -> destino? O(grau(origem))."""
        if not (self.contem_vertice(origem) and self.contem_vertice(destino)):
            return False
        j = self._indice(destino)
        for vizinho, _ in self._adjacencia[self._indice(origem)]:
            if vizinho == j:
                return True
        return False

    def vizinhos(self, nome: str) -> list:
        """Nomes dos vizinhos, na ordem em que as ligações foram criadas. O(grau)."""
        return [self._nomes[j] for j, _ in self._adjacencia[self._indice(nome)]]

    def vizinhos_com_peso(self, nome: str) -> list:
        """Pares (vizinho, peso) — base para algoritmos como o de Dijkstra. O(grau)."""
        return [(self._nomes[j], peso) for j, peso in self._adjacencia[self._indice(nome)]]

    def grau(self, nome: str) -> int:
        return len(self._adjacencia[self._indice(nome)])

    # ------------------------------------------------------------------ busca em largura
    def _bfs(self, inicio: int, alvo: int = -1):
        """BFS a partir do índice `inicio`. O(V + E).

        Devolve (distancia, pai, ordem):
          * distancia[v] = número de arestas no menor caminho (-1 = inalcançável);
          * pai[v] = vértice anterior a v nesse menor caminho;
          * ordem = vértices na ordem em que foram descobertos (camada por camada).
        Se `alvo` for informado, a busca para assim que ele é descoberto.
        """
        distancia = [-1] * len(self._nomes)
        pai = [-1] * len(self._nomes)
        distancia[inicio] = 0
        ordem = [inicio]
        fila = Fila()
        fila.enqueue(inicio)
        while not fila.is_empty():
            atual = fila.dequeue()
            for vizinho, _ in self._adjacencia[atual]:
                if distancia[vizinho] == -1:            # ainda não visitado
                    distancia[vizinho] = distancia[atual] + 1
                    pai[vizinho] = atual
                    ordem.append(vizinho)
                    if vizinho == alvo:
                        return distancia, pai, ordem
                    fila.enqueue(vizinho)
        return distancia, pai, ordem

    def busca_em_largura(self, origem: str) -> list:
        """Vértices alcançáveis a partir da origem, na ordem da BFS. O(V + E).

        Devolve pares (nome, distância); as distâncias aparecem em ordem
        crescente, camada por camada (1ª camada = vizinhos diretos).
        """
        distancia, _, ordem = self._bfs(self._indice(origem))
        return [(self._nomes[v], distancia[v]) for v in ordem]

    def caminho_mais_curto(self, origem: str, destino: str):
        """Menor caminho em número de arestas (BFS). Lista de nomes ou None. O(V + E)."""
        inicio, fim = self._indice(origem), self._indice(destino)
        if inicio == fim:
            return [origem]
        _, pai, _ = self._bfs(inicio, alvo=fim)
        if pai[fim] == -1:
            return None                                  # não há caminho
        caminho = []
        atual = fim
        while atual != -1:                               # volta de pai em pai até a origem
            caminho.append(self._nomes[atual])
            atual = pai[atual]
        caminho.reverse()
        return caminho

    def componentes(self) -> list:
        """Grupos de vértices ligados entre si (grafo não direcionado). O(V + E).

        Faz uma BFS a partir de cada vértice ainda não visitado; tudo o que
        essa BFS alcança forma um grupo (componente conexo).
        """
        visitado = [False] * len(self._nomes)
        grupos = []
        for inicio in range(len(self._nomes)):
            if visitado[inicio]:
                continue
            grupo = []
            visitado[inicio] = True
            fila = Fila()
            fila.enqueue(inicio)
            while not fila.is_empty():
                atual = fila.dequeue()
                grupo.append(self._nomes[atual])
                for vizinho, _ in self._adjacencia[atual]:
                    if not visitado[vizinho]:
                        visitado[vizinho] = True
                        fila.enqueue(vizinho)
            grupos.append(grupo)
        return grupos
