"""SP08 – Sistema de Autocomplete de Nomes de Produtos.

Estrutura usada: Árvore Binária de Busca (BST) -> estruturas/arvore_bst.py

O que o enunciado pede e onde está:
  * BST de nomes de produtos ........................ AutocompleteProdutos.arvore
  * dado um prefixo, todos os produtos que começam
    com ele (percurso limitado) ..................... AutocompleteProdutos.sugerir()
  * base com pelo menos 30 produtos e testes ........ PRODUTOS (38) e executar_demonstracao()

Como funciona o "percurso limitado": todos os nomes que começam com um prefixo
P formam um INTERVALO contínuo na ordem alfabética. Assim, em cada nó:
  * se o nome começa com P ......... pode haver resultados dos dois lados;
  * se o nome é menor que P ........ tudo à esquerda é menor ainda: só desce à direita;
  * se o nome é maior (e não começa
    com P) ........................ tudo à direita é maior ainda: só desce à esquerda.
O percurso visita O(h + k) nós (h = altura, k = sugestões), não a árvore inteira,
e as sugestões já saem em ordem alfabética, porque o percurso é em ordem.

As chaves são normalizadas (minúsculas e sem acento), então "cafe", "CAFÉ"
e "Café" encontram os mesmos produtos; o nome original fica guardado como valor.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

if __package__ in (None, ""):  # permite rodar este arquivo diretamente
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from estruturas.arvore_bst import ArvoreBST
from ordenacao.merge_sort import merge_sort
from situacoes.utilidades import cabecalho, normalizar_texto, secao


class AutocompleteProdutos:
    """Sugestões de produtos por prefixo usando uma BST de nomes."""

    def __init__(self, nomes=None):
        self.arvore = ArvoreBST()   # chave: nome normalizado | valor: nome original
        for nome in nomes or []:
            self.adicionar(nome)

    def adicionar(self, nome: str) -> bool:
        """Cadastra um produto. Devolve False se o nome já existia. O(h)."""
        return self.arvore.inserir(normalizar_texto(nome), nome)

    def remover(self, nome: str) -> bool:
        return self.arvore.remover(normalizar_texto(nome))

    def sugerir(self, prefixo: str, limite: int = None):
        """Produtos que começam com `prefixo`, em ordem alfabética.

        Devolve (sugestoes, nos_visitados). Com `limite`, para assim que
        juntar essa quantidade (como a lista suspensa de um site).
        Custo: O(h + k) nós visitados.
        """
        prefixo = normalizar_texto(prefixo)
        sugestoes = []
        visitados = 0

        def coletar(no) -> None:
            nonlocal visitados
            if no is None or (limite is not None and len(sugestoes) >= limite):
                return
            visitados += 1
            if no.chave.startswith(prefixo):
                coletar(no.esquerda)                 # pode haver resultados antes...
                if limite is None or len(sugestoes) < limite:
                    sugestoes.append(no.valor)
                coletar(no.direita)                  # ...e depois deste nó
            elif no.chave < prefixo:
                coletar(no.direita)                  # a esquerda é toda menor: poda
            else:
                coletar(no.esquerda)                 # a direita é toda maior: poda

        coletar(self.arvore.raiz)
        return sugestoes, visitados

    def __len__(self) -> int:
        return len(self.arvore)


# Catálogo da loja, na ordem em que os produtos foram cadastrados (agrupados
# por setor, não em ordem alfabética, para a BST não degenerar).
PRODUTOS = [
    "Notebook 15 polegadas", "Mouse sem fio", "Mousepad gamer", "Monitor 24 polegadas",
    "Teclado mecânico", "Headset com microfone", "Webcam Full HD", "Pen drive 64 GB",
    "Café torrado e moído 500 g", "Cafeteira elétrica", "Café em cápsulas", "Caneca térmica",
    "Garrafa térmica", "Liquidificador", "Panela de pressão", "Panela antiaderente",
    "Fogão 4 bocas", "Caderno universitário", "Caneta esferográfica azul",
    "Calculadora científica", "Cadeira de escritório", "Luminária de mesa", "Lâmpada LED",
    "Cabo USB-C", "Carregador portátil", "Capa para celular", "Celular 128 GB",
    "Câmera de segurança", "Smartwatch", "Smart TV 50 polegadas", "Soundbar",
    "Fone de ouvido bluetooth", "Fone de ouvido com fio", "Suporte para notebook",
    "Mochila para notebook", "Tênis de corrida", "Livro de receitas", "Furadeira de impacto",
]


def executar_demonstracao() -> None:
    cabecalho("SP08 - Autocomplete de nomes de produtos (Árvore Binária de Busca)")
    auto = AutocompleteProdutos(PRODUTOS)
    total = len(auto)
    altura = auto.arvore.altura()
    print(f"{total} produtos na BST | altura {altura} "
          f"(mínimo possível para {total} nós: {math.ceil(math.log2(total + 1))}; "
          f"degenerada seria {total})")

    secao("Usuário digitando 'cafe' letra por letra (até 5 sugestões, como num site)")
    for tamanho in range(1, 5):
        digitado = "cafe"[:tamanho]
        sugestoes, visitados = auto.sugerir(digitado, limite=5)
        print(f"  {repr(digitado):<7} {visitados:>2} de {total} nós visitados -> {', '.join(sugestoes)}")

    secao("Outras buscas (todas as sugestões, sem limite)")
    for prefixo in ["mouse", "fone de", "SMART", "lâm", "lam", "pan", "cad", "x"]:
        sugestoes, visitados = auto.sugerir(prefixo)
        lista = ", ".join(sugestoes) if sugestoes else "(nenhum produto)"
        print(f"  {repr(prefixo):<10} {visitados:>2} nós visitados -> {lista}")

    secao("Cadastro de um produto novo e nova busca")
    auto.adicionar("Cafeteira italiana")
    sugestoes, visitados = auto.sugerir("cafe")
    print(f"  + 'Cafeteira italiana' cadastrada ({len(auto)} produtos, altura {auto.arvore.altura()})")
    print(f"  'cafe'  {visitados} nós visitados -> {', '.join(sugestoes)}")

    secao("Por que a ordem de cadastro importa")
    alfabetica = list(PRODUTOS)
    merge_sort(alfabetica, chave=normalizar_texto)   # nosso Merge Sort, não o sorted() do Python
    em_ordem_alfabetica = AutocompleteProdutos(alfabetica)
    _, visitados_ruim = em_ordem_alfabetica.sugerir("smart")
    _, visitados_bom = AutocompleteProdutos(PRODUTOS).sugerir("smart")
    print(f"  Os mesmos {total} produtos cadastrados em ORDEM ALFABÉTICA formam uma BST de altura "
          f"{em_ordem_alfabetica.arvore.altura()} (uma lista inclinada).")
    print(f"  Buscar 'smart' visita {visitados_ruim} nós nela, contra {visitados_bom} na árvore acima.")
    print("  Esse pior caso O(n) é o motivo de existir a árvore AVL (SP09/SP10).")

    secao("Percurso em ordem completo (os 10 primeiros nomes em ordem alfabética)")
    for posicao, (_, nome) in enumerate(auto.arvore.em_ordem(), start=1):
        print(f"  {posicao:>2}. {nome}")
        if posicao == 10:
            break


def modo_interativo() -> None:
    auto = AutocompleteProdutos(PRODUTOS)
    print(f"\n{len(auto)} produtos carregados. Digite um prefixo (linha vazia para sair).")
    while True:
        try:
            prefixo = input("buscar> ")
        except EOFError:
            break
        if not prefixo:
            break
        sugestoes, visitados = auto.sugerir(prefixo)
        print(f"  {len(sugestoes)} sugestão(ões), {visitados} nós visitados")
        for nome in sugestoes:
            print(f"   - {nome}")


if __name__ == "__main__":
    executar_demonstracao()
