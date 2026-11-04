"""SP20 – Atualização de Ranking de Vendedores do Mês.

Algoritmo usado: Insertion Sort -> ordenacao/insertion_sort.py

O que o enunciado pede e onde está:
  * Insertion Sort em lista de vendedores (nome + total) .. atualizar_ranking()
  * simulação de atualizações diárias ao longo de uma semana executar_demonstracao()
  * comparação: lista já ordenada x lista aleatória ...... comparar_entradas()

Por que Insertion Sort: o ranking de ontem já está ordenado e as vendas de um
dia mudam pouco o total acumulado do mês. A lista chega QUASE ORDENADA, e é
aí que o Insertion Sort brilha: ele custa O(n + k), onde k é o número de pares
fora de ordem. Cada vendedor só anda as poucas posições que realmente mudou.
Ele também é ESTÁVEL: num empate de total, quem estava à frente ontem continua
à frente.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):  # permite rodar este arquivo diretamente
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from estruturas.tabela_hash import TabelaHash
from ordenacao.insertion_sort import insertion_sort
from situacoes.utilidades import cabecalho, imprimir_tabela, moeda, numero, secao


@dataclass
class Vendedor:
    nome: str
    total_vendas: float   # acumulado no mês


def atualizar_ranking(ranking: list):
    """Reordena NO PRÓPRIO LUGAR a lista do dia anterior (maior total primeiro)."""
    return insertion_sort(ranking, chave=lambda v: v.total_vendas, decrescente=True)


VENDEDORES = [   # total acumulado do mês até o domingo
    ("Adriana", 48_350.00), ("Bernardo", 31_200.00), ("Cláudia", 55_870.00),
    ("Davi", 27_640.00), ("Elaine", 42_910.00), ("Fábio", 38_450.00),
    ("Giovana", 61_020.00), ("Heitor", 22_380.00), ("Ingrid", 45_600.00),
    ("Jonas", 35_090.00), ("Larissa", 50_730.00), ("Murilo", 29_980.00),
]
DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]


def _vendas_do_dia(sorteio: random.Random, vendedores: list) -> list:
    """Venda de cada vendedor no dia (alguns de folga vendem zero)."""
    return [0.0 if sorteio.random() < 0.15 else round(sorteio.uniform(400, 6_500), 2) for _ in vendedores]


def comparar_entradas(n: int, semente: int = 1):
    """Mede o Insertion Sort em três entradas de mesmo conteúdo para n vendedores.

    Devolve as métricas para: (já ordenada, ranking de ontem + vendas do dia, aleatória).
    """
    sorteio = random.Random(semente)
    base = [Vendedor(f"V{i:05d}", round(sorteio.uniform(10_000, 80_000), 2)) for i in range(n)]
    atualizar_ranking(base)                                   # "ranking de ontem"
    ja_ordenada = list(base)
    m_ordenada = atualizar_ranking(ja_ordenada)

    hoje = [Vendedor(v.nome, v.total_vendas) for v in base]   # mesma ordem de ontem...
    for v in hoje:                                            # ...com as vendas de hoje
        v.total_vendas += 0.0 if sorteio.random() < 0.15 else round(sorteio.uniform(400, 6_500), 2)
    aleatoria = list(hoje)
    sorteio.shuffle(aleatoria)
    m_quase = atualizar_ranking(hoje)
    m_aleatoria = atualizar_ranking(aleatoria)
    return m_ordenada, m_quase, m_aleatoria


def executar_demonstracao() -> None:
    cabecalho("SP20 - Ranking de vendedores do mês atualizado todo dia (Insertion Sort)")
    ranking = [Vendedor(nome, total) for nome, total in VENDEDORES]
    metricas = atualizar_ranking(ranking)
    print(f"{len(ranking)} vendedores. Ranking inicial montado a partir da ordem alfabética: "
          f"{metricas.comparacoes} comparações, {metricas.trocas} deslocamentos.")

    sorteio = random.Random(42)
    resumo = []
    for dia in DIAS:
        posicao_ontem = TabelaHash()
        for posicao, vendedor in enumerate(ranking, start=1):
            posicao_ontem[vendedor.nome] = posicao
        vendas = _vendas_do_dia(sorteio, ranking)
        for vendedor, venda in zip(ranking, vendas):
            vendedor.total_vendas += venda             # a lista continua na ordem de ontem

        embaralhada = list(ranking)                    # mesmos dados, ordem aleatória
        random.Random(dia).shuffle(embaralhada)
        m_aleatoria = atualizar_ranking(embaralhada)
        m_dia = atualizar_ranking(ranking)             # o caso real: lista de ontem
        resumo.append([dia, m_dia.comparacoes, m_dia.trocas, m_aleatoria.comparacoes, m_aleatoria.trocas])

        secao(f"{dia}: vendas lançadas, ranking reordenado")
        partes = []
        for posicao, vendedor in enumerate(ranking[:5], start=1):
            mudanca = posicao_ontem[vendedor.nome] - posicao
            seta = f"+{mudanca}" if mudanca > 0 else (str(mudanca) if mudanca < 0 else "=")
            partes.append(f"{posicao}º {vendedor.nome} {moeda(vendedor.total_vendas)} ({seta})")
        print("  Top-5: " + " | ".join(partes))
        print(f"  Insertion Sort na lista de ontem: {m_dia.comparacoes} comparações e "
              f"{m_dia.trocas} deslocamentos (mesmos dados embaralhados: "
              f"{m_aleatoria.comparacoes} e {m_aleatoria.trocas})")

    secao("Ranking ao fim da semana")
    imprimir_tabela(["Pos.", "Vendedor", "Total no mês"],
                    [[f"{i}º", v.nome, moeda(v.total_vendas)] for i, v in enumerate(ranking, start=1)], "><>")

    secao("Custo diário: lista de ontem x mesmos dados em ordem aleatória (n = 12)")
    imprimir_tabela(["Dia", "Comp. (ontem)", "Desloc. (ontem)", "Comp. (aleatória)", "Desloc. (aleatória)"],
                    resumo, "<>>>>")

    secao("Comparação de desempenho com mais vendedores")
    linhas = []
    for n in (100, 500, 1_000, 2_000):
        ordenada, quase, aleatoria = comparar_entradas(n)
        linhas.append([numero(n), numero(ordenada.comparacoes), numero(quase.comparacoes),
                       numero(aleatoria.comparacoes),
                       f"{numero(aleatoria.comparacoes / quase.comparacoes, 1)}x",
                       f"{numero(quase.tempo_ms, 1)} ms", f"{numero(aleatoria.tempo_ms, 1)} ms"])
    imprimir_tabela(["n", "Comp. já ordenada", "Comp. ontem+hoje", "Comp. aleatória", "Diferença",
                     "Tempo ontem+hoje", "Tempo aleatória"], linhas, ">>>>>>>")
    print("Já ordenada: n-1 comparações, O(n). Ontem + vendas de hoje: O(n + k), k = ultrapassagens do dia.")
    print("Aleatória: cerca de n²/4 comparações, O(n²). A vantagem cresce com n.")


if __name__ == "__main__":
    executar_demonstracao()
