"""SP10 – Ranking de Jogadores em um Jogo Online.

Estruturas usadas:
  * Árvore AVL -> estruturas/arvore_avl.py (o ranking em si)
  * Tabela hash -> estruturas/tabela_hash.py (índice nome -> pontuação atual)

O que o enunciado pede e onde está:
  * AVL ordenada por pontuação, com desempate pelo nome ... chave (-pontos, nome)
  * inserção/atualização de pontuação e consulta Top-K .... RankingJogadores
  * simulação de 30 jogadores com atualizações ............ executar_demonstracao()

Decisões de projeto:
  * Chave composta (-pontos, nome): o percurso EM ORDEM da AVL já sai do maior
    para o menor placar e, no empate, em ordem alfabética. Top-K = os K
    primeiros do percurso: O(log n + K).
  * Atualizar a pontuação muda a CHAVE do jogador, e chave de árvore não pode
    ser alterada no lugar (quebraria a ordem). Então atualizar = remover a
    chave antiga + inserir a nova, as duas O(log n) com rebalanceamento.
  * Para achar a chave antiga sem percorrer a árvore, uma tabela hash guarda
    nome -> pontuação atual (busca O(1) em média).
  * Os nós da AVL guardam o tamanho da subárvore, então a posição de qualquer
    jogador ("você está em 17º") sai em O(log n).
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

if __package__ in (None, ""):  # permite rodar este arquivo diretamente
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from estruturas.arvore_avl import ArvoreAVL
from estruturas.tabela_hash import TabelaHash
from situacoes.utilidades import cabecalho, imprimir_tabela, numero, secao


class RankingJogadores:
    """Ranking de jogadores mantido em uma AVL."""

    def __init__(self):
        self.arvore = ArvoreAVL()             # chave (-pontos, nome) -> nome
        self._pontos_por_nome = TabelaHash()  # nome -> pontos atuais
        self.atualizacoes = 0

    @staticmethod
    def _chave(nome: str, pontos: int) -> tuple:
        return (-pontos, nome)   # mais pontos = chave menor = aparece antes

    def registrar(self, nome: str, pontos: int = 0) -> None:
        """Novo jogador no ranking. O(log n)."""
        if nome in self._pontos_por_nome:
            raise ValueError(f"o jogador {nome} já está no ranking")
        if pontos < 0:
            raise ValueError("a pontuação não pode ser negativa")
        self.arvore.inserir(self._chave(nome, pontos), nome)
        self._pontos_por_nome[nome] = pontos

    def atualizar(self, nome: str, novos_pontos: int) -> None:
        """Troca a pontuação: remove a chave antiga e insere a nova. O(log n)."""
        antigos = self.pontos(nome)
        novos_pontos = max(0, novos_pontos)
        self.arvore.remover(self._chave(nome, antigos))
        self.arvore.inserir(self._chave(nome, novos_pontos), nome)
        self._pontos_por_nome[nome] = novos_pontos
        self.atualizacoes += 1

    def somar_pontos(self, nome: str, variacao: int) -> int:
        """Soma (ou subtrai) pontos; a pontuação nunca fica negativa. O(log n)."""
        novos = max(0, self.pontos(nome) + variacao)
        self.atualizar(nome, novos)
        return novos

    def remover(self, nome: str) -> None:
        """Tira o jogador do ranking (ex.: conta banida). O(log n)."""
        pontos = self.pontos(nome)
        self.arvore.remover(self._chave(nome, pontos))
        self._pontos_por_nome.remover(nome)

    def pontos(self, nome: str) -> int:
        pontos = self._pontos_por_nome.buscar(nome)
        if pontos is None:
            raise KeyError(f"jogador {nome} não está no ranking")
        return pontos

    def top(self, k: int) -> list:
        """Os k melhores como (posição, nome, pontos). O(log n + k)."""
        return [(posicao, nome, -chave[0])
                for posicao, (chave, nome) in enumerate(self.arvore.primeiros(k), start=1)]

    def posicao(self, nome: str) -> int:
        """Colocação atual do jogador (1 = líder). O(log n)."""
        return self.arvore.posicao(self._chave(nome, self.pontos(nome)))

    def jogador_na_posicao(self, posicao: int) -> tuple:
        """(nome, pontos) de quem ocupa a colocação informada. O(log n)."""
        chave, nome = self.arvore.k_esimo(posicao)
        return nome, -chave[0]

    def nomes(self) -> list:
        return list(self._pontos_por_nome.chaves())

    def __len__(self) -> int:
        return len(self.arvore)


# ---------------------------------------------------------------------- simulação
JOGADORES = [
    "ShadowWolf", "PixelQueen", "NeoBlade", "LunaStorm", "IronFang", "CyberNina",
    "DarkPhoenix", "TurboTaco", "MysticRay", "FrostByte", "NovaStrike", "BlazeKing",
    "SilverFox", "QuantumLeo", "RubyRage", "AquaMaru", "VortexVini", "EchoHunter",
    "ZeroGravity", "MegaMila", "ToxicTiger", "OrbitOlga", "CrimsonCris", "JadeJaguar",
    "HyperHugo", "PandaPower", "RocketRafa", "StellarSofi", "BitBruna", "GamaGabi",
]


def _pontuacoes_iniciais(semente: int = 10) -> list:
    sorteio = random.Random(semente)
    pontuacoes = [(nome, sorteio.randrange(900, 2100, 5)) for nome in JOGADORES]
    # empate proposital para mostrar o desempate pelo nome
    pontuacoes[2] = ("NeoBlade", 1985)
    pontuacoes[3] = ("LunaStorm", 1985)
    return pontuacoes


def _imprimir_top(ranking: RankingJogadores, k: int) -> None:
    linhas = [[f"{posicao}º", nome, numero(pontos)] for posicao, nome, pontos in ranking.top(k)]
    imprimir_tabela(["Pos.", "Jogador", "Pontos"], linhas, "><>")


def executar_demonstracao() -> None:
    cabecalho("SP10 - Ranking de jogadores de um jogo online (Árvore AVL)")
    ranking = RankingJogadores()
    for nome, pontos in _pontuacoes_iniciais():
        ranking.registrar(nome, pontos)
    print(f"{len(ranking)} jogadores cadastrados. Altura da AVL: {ranking.arvore.altura()} "
          f"(rotações feitas no cadastro: {ranking.arvore.rotacoes.total}).")

    secao("Top-10 inicial")
    _imprimir_top(ranking, 10)
    print("NeoBlade e LunaStorm empatam com 1.985 pontos; o desempate pelo nome põe LunaStorm à frente.")

    sorteio = random.Random(2026)
    for rodada in range(1, 6):
        antes = TabelaHash()  # posição de cada um antes da rodada (para achar quem mais subiu)
        for nome in ranking.nomes():
            antes[nome] = ranking.posicao(nome)

        eventos = []
        if rodada == 3:
            ranking.registrar("NovatoNix", 1600)
            eventos.append("NovatoNix entrou no jogo com 1.600 pontos")
        if rodada == 4:
            ranking.remover("ToxicTiger")
            eventos.append("ToxicTiger foi banido por trapaça e saiu do ranking")

        participantes = ranking.nomes()
        for _ in range(6):   # 6 partidas por rodada = 12 atualizações de pontuação
            vencedor, perdedor = sorteio.sample(participantes, 2)
            ranking.somar_pontos(vencedor, sorteio.randint(25, 60))
            ranking.somar_pontos(perdedor, -sorteio.randint(10, 30))

        subida, quem = 0, None
        for nome in ranking.nomes():
            if nome in antes and antes[nome] - ranking.posicao(nome) > subida:
                subida, quem = antes[nome] - ranking.posicao(nome), nome

        secao(f"Rodada {rodada}: 6 partidas, 12 atualizações de pontuação")
        for evento in eventos:
            print(f"  {evento}")
        top5 = ", ".join(f"{p}º {n} ({numero(pts)})" for p, n, pts in ranking.top(5))
        print(f"  Top-5: {top5}")
        if quem:
            print(f"  Quem mais subiu: {quem}, {subida} posições (agora {ranking.posicao(quem)}º)")

    secao("Ranking final - Top-10")
    _imprimir_top(ranking, 10)

    secao("Consultas por posição (tamanho das subárvores, O(log n))")
    for nome in ["PandaPower", "NovatoNix", "BitBruna"]:
        print(f"  {nome} está em {ranking.posicao(nome)}º com {numero(ranking.pontos(nome))} pontos")
    nome, pontos = ranking.jogador_na_posicao(15)
    print(f"  Quem está em 15º? {nome} ({numero(pontos)} pontos)")

    secao("A árvore continua balanceada?")
    n = len(ranking)
    arvore = ranking.arvore
    fatores = [fator for _, _, fator in arvore.fatores_de_balanceamento()]
    print(f"  Jogadores: {n} | atualizações de pontuação: {ranking.atualizacoes} "
          f"(cada uma = 1 remoção + 1 inserção na AVL)")
    print(f"  Altura: {arvore.altura()} | mínima possível: {math.ceil(math.log2(n + 1))} | "
          f"limite teórico da AVL: {numero(1.44 * math.log2(n + 2), 1)}")
    print(f"  Fatores de balanceamento encontrados: de {min(fatores)} a {max(fatores)}")
    print(f"  Verificação completa (ordem, alturas, fatores): "
          f"{'OK' if arvore.esta_balanceada() else 'FALHOU'}")
    print(f"  Rotações desde o início: {arvore.rotacoes}")


if __name__ == "__main__":
    executar_demonstracao()
