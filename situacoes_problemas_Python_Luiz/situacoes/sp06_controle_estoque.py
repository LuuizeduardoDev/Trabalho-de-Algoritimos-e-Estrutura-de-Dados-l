"""SP06 – Controle de Estoque de uma Pequena Loja (materiais de construção).

Estrutura usada: Lista encadeada -> estruturas/lista_encadeada.py

O que o enunciado pede e onde está:
  * produtos com código, nome, quantidade e preço unitário ... Produto
  * cadastrar, atualizar quantidade, remover, buscar por
    nome/código e listar abaixo do estoque mínimo ............ ControleEstoque
  * simulação de entradas e saídas ao longo de uma semana .... executar_demonstracao()

Decisões de projeto:
  * Cada produto tem o SEU estoque mínimo (cimento gira muito mais que torneira).
  * Duas listas encadeadas: `ativos` e `esgotados`. Quando uma saída zera o
    estoque, o nó sai da lista ativa (como o contexto pede) e vai para a de
    esgotados, para a loja saber o que precisa recomprar. Quando chega
    mercadoria, o produto volta para a lista ativa.

Por que lista encadeada: o catálogo muda o tempo todo (cadastros, remoções,
produtos entrando e saindo da lista ativa) e não tem tamanho máximo conhecido.
Remover no meio só religa ponteiros, sem deslocar os outros elementos.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

if __package__ in (None, ""):  # permite rodar este arquivo diretamente
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from estruturas.lista_encadeada import ListaEncadeada
from situacoes.utilidades import cabecalho, imprimir_tabela, moeda, normalizar_texto, secao


@dataclass
class Produto:
    codigo: str
    nome: str
    quantidade: int
    preco_unitario: float
    estoque_minimo: int = 5

    @property
    def valor_em_estoque(self) -> float:
        return self.quantidade * self.preco_unitario

    @property
    def abaixo_do_minimo(self) -> bool:
        return self.quantidade < self.estoque_minimo


class EstoqueInsuficienteError(ValueError):
    """Saída maior do que a quantidade disponível."""


class ControleEstoque:
    """Estoque com duas listas encadeadas: produtos ativos e esgotados."""

    def __init__(self):
        self.ativos = ListaEncadeada()
        self.esgotados = ListaEncadeada()

    # ------------------------------------------------------------------ cadastro e remoção
    def cadastrar(self, codigo: str, nome: str, quantidade: int, preco: float, estoque_minimo: int = 5) -> Produto:
        """Cadastra um produto novo. O(n) por causa da verificação de código repetido."""
        codigo = codigo.strip().upper()
        if self.buscar_por_codigo(codigo) is not None:
            raise ValueError(f"o código {codigo} já está cadastrado")
        if quantidade < 0 or preco <= 0 or estoque_minimo < 0:
            raise ValueError("quantidade e mínimo não podem ser negativos e o preço deve ser positivo")
        produto = Produto(codigo, nome, quantidade, preco, estoque_minimo)
        destino = self.ativos if quantidade > 0 else self.esgotados
        destino.inserir_fim(produto)   # O(1) com o ponteiro de fim
        return produto

    def remover_produto(self, codigo: str) -> Produto:
        """Remove o produto de vez (ex.: item descontinuado). O(n)."""
        codigo = codigo.strip().upper()
        for lista in (self.ativos, self.esgotados):
            removido = lista.remover_se(lambda p: p.codigo == codigo)
            if removido is not None:
                return removido
        raise KeyError(f"produto {codigo} não encontrado")

    # ------------------------------------------------------------------ buscas
    def buscar_por_codigo(self, codigo: str) -> Optional[Produto]:
        """Busca exata pelo código nas duas listas. O(n)."""
        codigo = codigo.strip().upper()
        produto = self.ativos.buscar(lambda p: p.codigo == codigo)
        if produto is None:
            produto = self.esgotados.buscar(lambda p: p.codigo == codigo)
        return produto

    def buscar_por_nome(self, trecho: str) -> list:
        """Produtos ativos cujo nome contém o trecho (sem diferenciar acentos/maiúsculas). O(n)."""
        alvo = normalizar_texto(trecho)
        return self.ativos.filtrar(lambda p: alvo in normalizar_texto(p.nome))

    # ------------------------------------------------------------------ movimentações
    def atualizar_quantidade(self, codigo: str, variacao: int) -> Produto:
        """Soma `variacao` ao estoque (positiva = entrada, negativa = saída). O(n).

        * saída que zera o estoque: o produto sai da lista ativa e vai para esgotados;
        * entrada em produto esgotado: ele volta para a lista ativa;
        * saída maior que o disponível: EstoqueInsuficienteError (nada é alterado).
        """
        codigo = codigo.strip().upper()
        produto = self.buscar_por_codigo(codigo)
        if produto is None:
            raise KeyError(f"produto {codigo} não encontrado")
        nova_quantidade = produto.quantidade + variacao
        if nova_quantidade < 0:
            raise EstoqueInsuficienteError(
                f"saída de {-variacao} un. de {produto.nome}, mas só há {produto.quantidade} em estoque")
        estava_esgotado = produto.quantidade == 0
        produto.quantidade = nova_quantidade
        if nova_quantidade == 0 and not estava_esgotado:
            self.ativos.remover_se(lambda p: p.codigo == codigo)      # sai da lista ativa
            self.esgotados.inserir_fim(produto)
        elif nova_quantidade > 0 and estava_esgotado:
            self.esgotados.remover_se(lambda p: p.codigo == codigo)   # volta para a ativa
            self.ativos.inserir_fim(produto)
        return produto

    def registrar_entrada(self, codigo: str, quantidade: int) -> Produto:
        if quantidade <= 0:
            raise ValueError("a entrada deve ser positiva")
        return self.atualizar_quantidade(codigo, quantidade)

    def registrar_saida(self, codigo: str, quantidade: int) -> Produto:
        if quantidade <= 0:
            raise ValueError("a saída deve ser positiva")
        return self.atualizar_quantidade(codigo, -quantidade)

    # ------------------------------------------------------------------ relatórios
    def listar_abaixo_do_minimo(self) -> list:
        """Produtos ATIVOS com quantidade menor que o próprio estoque mínimo. O(n)."""
        return self.ativos.filtrar(lambda p: p.abaixo_do_minimo)

    def valor_total(self) -> float:
        return sum(p.valor_em_estoque for p in self.ativos)


# ---------------------------------------------------------------------- simulação da semana
CADASTRO_INICIAL = [
    # código, nome, quantidade, preço unitário, estoque mínimo
    ("CIM-50", "Cimento CP-II 50 kg", 120, 38.90, 40),
    ("ARE-M3", "Areia média (m³)", 15, 145.00, 5),
    ("TIJ-8F", "Tijolo 8 furos (milheiro)", 6, 890.00, 2),
    ("VER-10", "Vergalhão CA-50 10 mm (12 m)", 80, 52.40, 30),
    ("TIN-18", "Tinta acrílica branca 18 L", 22, 289.90, 8),
    ("ARG-20", "Argamassa AC-II 20 kg", 60, 24.50, 25),
    ("CAN-25", "Cano PVC 25 mm (6 m)", 45, 19.90, 20),
    ("TOR-12", "Torneira de jardim 1/2\"", 12, 27.90, 5),
    ("FIO-25", "Fio flexível 2,5 mm (100 m)", 9, 239.00, 4),
    ("PRE-17", "Prego 17x27 (kg)", 30, 21.00, 10),
    ("LIX-100", "Lixa d'água grão 100", 150, 2.50, 50),
    ("REJ-01", "Rejunte flexível cinza 1 kg", 25, 14.90, 10),
]

# (operação, argumentos...) — "saida"/"entrada" (código, quantidade), "cadastrar" (...),
# "remover" (código, motivo), "buscar_nome" (trecho), "buscar_codigo" (código)
SEMANA = [
    ("Segunda-feira", [
        ("saida", "CIM-50", 15), ("saida", "ARG-20", 12), ("saida", "LIX-100", 20), ("saida", "TOR-12", 4),
    ]),
    ("Terça-feira", [
        ("saida", "CIM-50", 90), ("saida", "ARE-M3", 8), ("saida", "VER-10", 35), ("entrada", "FIO-25", 6),
    ]),
    ("Quarta-feira", [
        ("saida", "TOR-12", 8),
        ("cadastrar", "CXA-500", "Caixa d'água 500 L", 4, 389.00, 2),
        ("saida", "CAN-25", 28), ("saida", "TIN-18", 5),
    ]),
    ("Quinta-feira", [
        ("entrada", "CIM-50", 200), ("saida", "ARE-M3", 10), ("saida", "ARE-M3", 5), ("saida", "VER-10", 50),
    ]),
    ("Sexta-feira", [
        ("remover", "LIX-100", "fornecedor deixou de fabricar"),
        ("buscar_nome", "cano"), ("buscar_codigo", "TIN-18"),
        ("saida", "REJ-01", 18), ("saida", "PRE-17", 12),
    ]),
    ("Sábado", [
        ("entrada", "TOR-12", 20), ("entrada", "CAN-25", 30), ("saida", "CIM-50", 40), ("saida", "CXA-500", 1),
    ]),
]


def _executar_operacao(estoque: ControleEstoque, operacao: tuple) -> None:
    tipo = operacao[0]
    try:
        if tipo in ("saida", "entrada"):
            _, codigo, quantidade = operacao
            if tipo == "saida":
                produto = estoque.registrar_saida(codigo, quantidade)
            else:
                produto = estoque.registrar_entrada(codigo, quantidade)
            sinal = "-" if tipo == "saida" else "+"
            print(f"  {tipo:<8} {codigo:<8} {sinal}{quantidade:<4} {produto.nome:<30} "
                  f"-> {produto.quantidade} em estoque")
            if produto.quantidade == 0:
                print(f"           ESGOTADO: {produto.nome} saiu da lista ativa")
            elif tipo == "entrada" and produto.quantidade == quantidade:
                print(f"           {produto.nome} voltou para a lista ativa")
            elif produto.abaixo_do_minimo:
                print(f"           ALERTA: abaixo do mínimo ({produto.quantidade} < {produto.estoque_minimo})")
        elif tipo == "cadastrar":
            _, codigo, nome, quantidade, preco, minimo = operacao
            estoque.cadastrar(codigo, nome, quantidade, preco, minimo)
            print(f"  cadastro {codigo:<8} {nome} ({quantidade} un., {moeda(preco)}, mínimo {minimo})")
        elif tipo == "remover":
            _, codigo, motivo = operacao
            removido = estoque.remover_produto(codigo)
            print(f"  remoção  {codigo:<8} {removido.nome} ({motivo})")
        elif tipo == "buscar_nome":
            achados = estoque.buscar_por_nome(operacao[1])
            nomes = ", ".join(f"{p.codigo} {p.nome} ({p.quantidade} un.)" for p in achados) or "nenhum"
            print(f"  busca    nome contém '{operacao[1]}': {nomes}")
        elif tipo == "buscar_codigo":
            produto = estoque.buscar_por_codigo(operacao[1])
            if produto is None:
                texto = "não encontrado"
            else:
                texto = f"{produto.nome} - {produto.quantidade} un. a {moeda(produto.preco_unitario)}"
            print(f"  busca    código {operacao[1]}: {texto}")
    except (EstoqueInsuficienteError, KeyError, ValueError) as erro:
        print(f"  RECUSADO {operacao[1]:<8} {erro}")


def executar_demonstracao() -> None:
    cabecalho("SP06 - Controle de estoque da loja Casa & Obra (Lista encadeada)")
    estoque = ControleEstoque()
    for codigo, nome, quantidade, preco, minimo in CADASTRO_INICIAL:
        estoque.cadastrar(codigo, nome, quantidade, preco, minimo)
    print(f"Cadastro inicial: {len(estoque.ativos)} produtos, valor em estoque {moeda(estoque.valor_total())}.")

    for dia, operacoes in SEMANA:
        secao(dia)
        for operacao in operacoes:
            _executar_operacao(estoque, operacao)
        abaixo = estoque.listar_abaixo_do_minimo()
        print(f"  fim do dia: {len(estoque.ativos)} ativos | abaixo do mínimo: "
              f"{', '.join(p.codigo for p in abaixo) or 'nenhum'} | esgotados: "
              f"{', '.join(p.codigo for p in estoque.esgotados) or 'nenhum'}")

    secao("Fechamento da semana - produtos ativos (ordem da lista encadeada)")
    linhas = [[p.codigo, p.nome, p.quantidade, p.estoque_minimo, moeda(p.preco_unitario),
               moeda(p.valor_em_estoque), "REPOR" if p.abaixo_do_minimo else "ok"] for p in estoque.ativos]
    imprimir_tabela(["Código", "Produto", "Qtd", "Mín", "Preço un.", "Valor", "Situação"], linhas, "<<>>>><")
    print(f"\nValor total em estoque: {moeda(estoque.valor_total())}")
    abaixo = estoque.listar_abaixo_do_minimo()
    print("Abaixo do mínimo: "
          + (", ".join(f"{p.nome} ({p.quantidade}/{p.estoque_minimo})" for p in abaixo) or "nenhum"))
    print("Esgotados (fora da lista ativa): " + (", ".join(p.nome for p in estoque.esgotados) or "nenhum"))


if __name__ == "__main__":
    executar_demonstracao()
