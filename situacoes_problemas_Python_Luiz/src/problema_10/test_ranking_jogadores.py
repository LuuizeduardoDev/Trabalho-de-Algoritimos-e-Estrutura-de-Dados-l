"""Testes da SP10 - Ranking de jogadores (rode nesta pasta: python -m unittest -v)."""

import io
import math
import random
import unittest
from contextlib import redirect_stdout

from arvore_avl import ArvoreAVL
from ranking_jogadores import RankingJogadores, executar_demonstracao


class TestArvoreAVL(unittest.TestCase):
    def _arvore(self, chaves):
        arvore = ArvoreAVL()
        for chave in chaves:
            arvore.inserir(chave)
        return arvore

    def test_quatro_casos_de_rotacao(self):
        casos = {"ll": [30, 20, 10], "rr": [10, 20, 30], "lr": [30, 10, 20], "rl": [10, 30, 20]}
        for caso, chaves in casos.items():
            arvore = self._arvore(chaves)
            self.assertEqual(arvore.raiz.chave, 20, caso)
            self.assertEqual(getattr(arvore.rotacoes, caso), 1, caso)
            self.assertEqual(arvore.altura(), 2)

    def test_insercao_ordenada_continua_balanceada(self):
        arvore = self._arvore(range(1, 1001))
        self.assertTrue(arvore.esta_balanceada())
        self.assertLessEqual(arvore.altura(), 1.44 * math.log2(1000 + 2))
        self.assertEqual(arvore.altura(), 10)   # 1000 chaves: altura mínima possível

    def test_remocao_rebalanceia(self):
        arvore = self._arvore(range(1, 32))       # árvore perfeita com 31 nós
        for chave in range(1, 16):
            self.assertTrue(arvore.remover(chave))
            self.assertTrue(arvore.esta_balanceada())
        self.assertFalse(arvore.remover(1))
        self.assertEqual([c for c, _ in arvore.em_ordem()], list(range(16, 32)))

    def test_posicao_k_esimo_e_primeiros(self):
        arvore = self._arvore([40, 10, 30, 20, 50])
        self.assertEqual(arvore.posicao(10), 1)
        self.assertEqual(arvore.posicao(50), 5)
        self.assertIsNone(arvore.posicao(35))
        self.assertEqual(arvore.k_esimo(3)[0], 30)
        self.assertEqual([c for c, _ in arvore.primeiros(2)], [10, 20])
        with self.assertRaises(IndexError):
            arvore.k_esimo(6)

    def test_aleatorio_mantem_todas_as_regras(self):
        sorteio = random.Random(2)
        for _ in range(40):
            arvore, referencia = ArvoreAVL(), set()
            for _ in range(250):
                chave = sorteio.randint(0, 120)
                if sorteio.random() < 0.6:
                    arvore.inserir(chave, chave * 2)
                    referencia.add(chave)
                else:
                    self.assertEqual(arvore.remover(chave), chave in referencia)
                    referencia.discard(chave)
            self.assertTrue(arvore.esta_balanceada())
            ordenadas = sorted(referencia)
            self.assertEqual([c for c, _ in arvore.em_ordem()], ordenadas)
            for posicao, chave in enumerate(ordenadas, start=1):
                self.assertEqual(arvore.posicao(chave), posicao)
                self.assertEqual(arvore.buscar(chave), chave * 2)


class TestRanking(unittest.TestCase):
    def test_top_k_e_posicoes_contra_busca_ingenua(self):
        sorteio = random.Random(8)
        ranking, pontos = RankingJogadores(), {}
        for numero in range(60):
            nome = f"jogador{numero:02d}"
            pontos[nome] = sorteio.randint(0, 500)
            ranking.registrar(nome, pontos[nome])
        for _ in range(400):
            nome = sorteio.choice(list(pontos))
            pontos[nome] = ranking.somar_pontos(nome, sorteio.randint(-80, 80))
        esperado = sorted(pontos.items(), key=lambda par: (-par[1], par[0]))
        self.assertEqual([(n, p) for _, n, p in ranking.top(10)], esperado[:10])
        for posicao, (nome, _) in enumerate(esperado, start=1):
            self.assertEqual(ranking.posicao(nome), posicao)
        self.assertTrue(ranking.arvore.esta_balanceada())

    def test_desempate_por_nome_e_remocao(self):
        ranking = RankingJogadores()
        for nome, pontos in [("Zeca", 100), ("Ana", 100), ("Bia", 150)]:
            ranking.registrar(nome, pontos)
        self.assertEqual([n for _, n, _ in ranking.top(3)], ["Bia", "Ana", "Zeca"])
        ranking.remover("Bia")
        self.assertEqual(ranking.jogador_na_posicao(1), ("Ana", 100))
        with self.assertRaises(ValueError):
            ranking.registrar("Ana", 10)
        with self.assertRaises(KeyError):
            ranking.pontos("Bia")


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP10", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
