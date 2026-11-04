"""SP12 – Rede de Amizades em uma Rede Social Simples.

Estruturas usadas:
  * Grafo não direcionado (lista de adjacência) -> grafo.py
  * Fila (dentro da BFS) -> fila.py
  * Tabela hash (amigos em comum e sugestões) -> tabela_hash.py
  * Merge Sort (listagens em ordem alfabética) -> merge_sort.py

O que o enunciado pede e onde está:
  * grafo não direcionado de usuários ...................... RedeSocial.grafo
  * adicionar amizade, listar amigos, amigos em comum,
    BFS para graus de separação ............................ métodos de RedeSocial
  * rede com pelo menos 15 usuários e consultas ............ executar_demonstracao() (20 usuários)
  * extra (aparece no contexto): sugerir conexões .......... sugerir_conexoes()

Por que grafo: amizade é uma RELAÇÃO entre pares de pessoas, sem hierarquia.
Usuários são vértices e amizades são arestas. Como a amizade vale nos dois
sentidos, o grafo é não direcionado. A BFS visita as pessoas em camadas
(amigos, amigos de amigos...), então a camada em que alguém aparece é
exatamente o grau de separação, isto é, o menor número de amizades no caminho.
"""

from __future__ import annotations


from grafo import Grafo
from tabela_hash import TabelaHash
from merge_sort import merge_sort
from utilidades import cabecalho, configurar_terminal, normalizar_texto, secao


def _em_ordem_alfabetica(nomes: list) -> list:
    nomes = list(nomes)
    merge_sort(nomes, chave=normalizar_texto)   # "Olívia" fica entre "Nicolas" e "Paulo"
    return nomes


class RedeSocial:
    """Rede de amizades sobre um grafo não direcionado."""

    def __init__(self):
        self.grafo = Grafo(direcionado=False)

    def adicionar_usuario(self, nome: str) -> bool:
        return self.grafo.adicionar_vertice(nome)

    def adicionar_amizade(self, pessoa_a: str, pessoa_b: str) -> bool:
        """Cria a amizade (aresta nos dois sentidos). False se já existia. O(grau)."""
        return self.grafo.adicionar_aresta(pessoa_a, pessoa_b)

    def desfazer_amizade(self, pessoa_a: str, pessoa_b: str) -> bool:
        return self.grafo.remover_aresta(pessoa_a, pessoa_b)

    def amigos(self, nome: str) -> list:
        """Amigos diretos em ordem alfabética. O(grau + grau·log grau)."""
        return _em_ordem_alfabetica(self.grafo.vizinhos(nome))

    def amigos_em_comum(self, pessoa_a: str, pessoa_b: str) -> list:
        """Interseção das duas listas de amigos. O(grau(a) + grau(b)) em média.

        Os amigos de A entram numa tabela hash; depois cada amigo de B é
        consultado nela em O(1) médio.
        """
        amigos_de_a = TabelaHash()
        for amigo in self.grafo.vizinhos(pessoa_a):
            amigos_de_a.inserir(amigo)
        comuns = [amigo for amigo in self.grafo.vizinhos(pessoa_b) if amigo in amigos_de_a]
        return _em_ordem_alfabetica(comuns)

    def grau_de_separacao(self, pessoa_a: str, pessoa_b: str):
        """(grau, caminho) pelo menor número de amizades; (None, None) se não houver ligação.

        Usa BFS: O(V + E).
        """
        caminho = self.grafo.caminho_mais_curto(pessoa_a, pessoa_b)
        if caminho is None:
            return None, None
        return len(caminho) - 1, caminho

    def camadas(self, nome: str) -> list:
        """Pessoas alcançáveis agrupadas por grau: [[grau 1], [grau 2], ...]. O(V + E)."""
        grupos = []
        for pessoa, distancia in self.grafo.busca_em_largura(nome):
            if distancia == 0:
                continue
            while len(grupos) < distancia:
                grupos.append([])
            grupos[distancia - 1].append(pessoa)
        return [_em_ordem_alfabetica(grupo) for grupo in grupos]

    def sugerir_conexoes(self, nome: str, limite: int = 5) -> list:
        """Amigos de amigos que ainda não são amigos, por nº de amigos em comum.

        Devolve pares (pessoa, amigos_em_comum), do mais recomendado para o
        menos (empate em ordem alfabética). O(soma dos graus dos amigos + c log c).
        """
        ja_amigos = TabelaHash()
        for amigo in self.grafo.vizinhos(nome):
            ja_amigos.inserir(amigo)
        contagem = TabelaHash()                          # candidato -> amigos em comum
        for amigo in self.grafo.vizinhos(nome):
            for candidato in self.grafo.vizinhos(amigo):
                if candidato != nome and candidato not in ja_amigos:
                    contagem[candidato] = contagem.buscar(candidato, 0) + 1
        sugestoes = list(contagem.itens())
        merge_sort(sugestoes, chave=lambda par: (-par[1], normalizar_texto(par[0])))
        return sugestoes[:limite]

    def estatisticas(self):
        """(usuários, amizades, maior grau, quem tem o maior grau, componentes)."""
        nomes = self.grafo.vertices()
        maior_grau = max(self.grafo.grau(nome) for nome in nomes)
        mais_conectados = _em_ordem_alfabetica([n for n in nomes if self.grafo.grau(n) == maior_grau])
        return (len(nomes), self.grafo.num_arestas(), maior_grau, mais_conectados, self.grafo.componentes())


# ---------------------------------------------------------------------- dados
USUARIOS = [
    "Ana", "Bruno", "Carla", "Daniel", "Eduarda", "Felipe", "Gabriela", "Hugo", "Isabela", "João",
    "Karina", "Lucas", "Mariana", "Nicolas", "Olívia", "Paulo", "Rafaela", "Sofia", "Tiago", "Vitória",
]

AMIZADES = [
    # turma da faculdade
    ("Ana", "Bruno"), ("Ana", "Carla"), ("Ana", "Daniel"), ("Bruno", "Carla"),
    ("Bruno", "Eduarda"), ("Carla", "Daniel"), ("Daniel", "Eduarda"),
    # colegas de trabalho da Carla
    ("Carla", "Felipe"), ("Felipe", "Gabriela"), ("Felipe", "Hugo"), ("Gabriela", "Hugo"),
    ("Gabriela", "Isabela"), ("Hugo", "Isabela"),
    # time de futebol do Hugo
    ("Hugo", "João"), ("João", "Karina"), ("João", "Lucas"), ("Karina", "Lucas"), ("Lucas", "Mariana"),
    # vizinhos da Mariana
    ("Mariana", "Nicolas"), ("Mariana", "Olívia"), ("Nicolas", "Olívia"), ("Olívia", "Paulo"),
    # grupo que não se conecta com o resto
    ("Rafaela", "Sofia"), ("Sofia", "Vitória"),
    # Tiago acabou de criar a conta e ainda não tem amigos
]


def montar_rede() -> RedeSocial:
    rede = RedeSocial()
    for nome in USUARIOS:
        rede.adicionar_usuario(nome)
    for pessoa_a, pessoa_b in AMIZADES:
        rede.adicionar_amizade(pessoa_a, pessoa_b)
    return rede


def _mostrar_separacao(rede: RedeSocial, pessoa_a: str, pessoa_b: str) -> None:
    grau, caminho = rede.grau_de_separacao(pessoa_a, pessoa_b)
    if grau is None:
        print(f"  {pessoa_a} -> {pessoa_b}: não estão conectados (nenhum caminho de amizades)")
    else:
        rotulo = "grau" if grau == 1 else "graus"
        print(f"  {pessoa_a} -> {pessoa_b}: {grau} {rotulo} | {' -> '.join(caminho)}")


def executar_demonstracao() -> None:
    cabecalho("SP12 - Rede de amizades (Grafo não direcionado + BFS)")
    rede = montar_rede()
    usuarios, amizades, maior_grau, mais_conectados, grupos = rede.estatisticas()
    print(f"{usuarios} usuários e {amizades} amizades (lista de adjacência).")

    secao("Listar amigos")
    for nome in ["Ana", "Hugo", "Tiago"]:
        amigos = rede.amigos(nome)
        print(f"  {nome} ({len(amigos)}): {', '.join(amigos) if amigos else 'nenhum amigo ainda'}")

    secao("Amigos em comum")
    for pessoa_a, pessoa_b in [("Ana", "Eduarda"), ("Felipe", "Isabela"), ("Ana", "Hugo")]:
        comuns = rede.amigos_em_comum(pessoa_a, pessoa_b)
        print(f"  {pessoa_a} e {pessoa_b}: {', '.join(comuns) if comuns else 'nenhum'}")

    secao("Graus de separação (BFS)")
    for pessoa_a, pessoa_b in [("Ana", "Bruno"), ("Ana", "Felipe"), ("Ana", "Paulo"),
                               ("Ana", "Sofia"), ("Tiago", "Ana")]:
        _mostrar_separacao(rede, pessoa_a, pessoa_b)

    secao("Camadas da BFS a partir de Ana")
    for grau, pessoas in enumerate(rede.camadas("Ana"), start=1):
        print(f"  {grau}º grau: {', '.join(pessoas)}")

    secao("Sugestões de conexão (amigos de amigos)")
    for nome in ["Ana", "Hugo", "Tiago"]:
        sugestoes = rede.sugerir_conexoes(nome)
        texto = ", ".join(f"{pessoa} ({comuns} em comum)" for pessoa, comuns in sugestoes)
        print(f"  Para {nome}: {texto if texto else 'nenhuma (ainda não tem amigos)'}")

    secao("Nova amizade encurta caminhos")
    rede.adicionar_amizade("Daniel", "Paulo")
    print("  Daniel e Paulo se conheceram num evento e viraram amigos.")
    _mostrar_separacao(rede, "Ana", "Paulo")
    print(f"  Tentar repetir a amizade Paulo-Daniel: "
          f"{'criada' if rede.adicionar_amizade('Paulo', 'Daniel') else 'já existia, nada muda'}")

    secao("Visão geral da rede")
    usuarios, amizades, maior_grau, mais_conectados, grupos = rede.estatisticas()
    print(f"  Usuários: {usuarios} | amizades: {amizades}")
    print(f"  Mais conectados ({maior_grau} amigos): {', '.join(mais_conectados)}")
    print(f"  Grupos sem ligação entre si (componentes): {len(grupos)}")
    for grupo in grupos:
        rotulo = "pessoa" if len(grupo) == 1 else "pessoas"
        print(f"    - {len(grupo)} {rotulo}: {', '.join(_em_ordem_alfabetica(grupo))}")


if __name__ == "__main__":
    configurar_terminal()
    executar_demonstracao()
