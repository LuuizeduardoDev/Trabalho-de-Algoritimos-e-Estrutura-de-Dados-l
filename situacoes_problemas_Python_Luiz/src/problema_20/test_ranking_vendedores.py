"""Testes da SP20 - Ranking de vendedores com Insertion Sort (rode nesta pasta: python -m unittest -v).

O sorted() do Python aparece aqui só como GABARITO para conferir os resultados.
"""

import io
import random
import unittest
from contextlib import redirect_stdout

from insertion_sort import inserir_em_ordem, insertion_sort
from ranking_vendedores import Vendedor, atualizar_ranking, comparar_entradas, executar_demonstracao


class TestInsertionSort(unittest.TestCase):
    def test_contra_gabarito_crescente_e_decrescente(self):
        sorteio = random.Random(4)
        for _ in range(150):
            dados = [sorteio.randint(-50, 50) for _ in range(sorteio.randint(0, 60))]
            for decrescente in (False, True):
                lista = list(dados)
                insertion_sort(lista, decrescente=decrescente)
                self.assertEqual(lista, sorted(dados, reverse=decrescente))

    def test_estavel_nos_dois_sentidos(self):
        sorteio = random.Random(5)
        registros = [(sorteio.randint(0, 5), indice) for indice in range(80)]
        for decrescente in (False, True):
            lista = list(registros)
            insertion_sort(lista, chave=lambda r: r[0], decrescente=decrescente)
            self.assertEqual(lista, sorted(registros, key=lambda r: r[0], reverse=decrescente))

    def test_linear_em_lista_ordenada(self):
        metricas = insertion_sort(list(range(1000)))
        self.assertEqual((metricas.comparacoes, metricas.trocas), (999, 0))

    def test_inserir_em_ordem(self):
        mao = []
        for carta in [5, 2, 8, 2, 9, 1]:
            inserir_em_ordem(mao, carta)
        self.assertEqual(mao, [1, 2, 2, 5, 8, 9])
        self.assertEqual(inserir_em_ordem(mao, 6), 4)


class TestRankingVendedores(unittest.TestCase):
    def test_ranking_e_comparacao_de_entradas(self):
        ranking = [Vendedor("B", 100.0), Vendedor("A", 300.0), Vendedor("C", 100.0)]
        atualizar_ranking(ranking)
        self.assertEqual([v.nome for v in ranking], ["A", "B", "C"])   # empate: mantém a ordem anterior
        ordenada, quase, aleatoria = comparar_entradas(300)
        self.assertEqual(ordenada.comparacoes, 299)
        self.assertLess(quase.comparacoes, aleatoria.comparacoes)


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP20", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
