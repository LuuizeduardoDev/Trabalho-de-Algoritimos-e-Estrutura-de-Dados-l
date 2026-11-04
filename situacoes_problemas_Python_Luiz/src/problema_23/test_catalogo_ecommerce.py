"""Testes da SP23 - Catálogo com Quick Sort (rode nesta pasta: python -m unittest -v).

O sorted() do Python aparece aqui só como GABARITO para conferir os resultados.
"""

import io
import random
import sys
import unittest
from contextlib import redirect_stdout

from catalogo_ecommerce import CRITERIOS, carregar_catalogo, executar_demonstracao, gerar_catalogo, \
    ordenar_catalogo
from quick_sort import quick_sort


class TestQuickSort(unittest.TestCase):
    def test_contra_gabarito_crescente_e_decrescente(self):
        sorteio = random.Random(4)
        for _ in range(150):
            dados = [sorteio.randint(-50, 50) for _ in range(sorteio.randint(0, 60))]
            for decrescente in (False, True):
                lista = list(dados)
                quick_sort(lista, decrescente=decrescente)
                self.assertEqual(lista, sorted(dados, reverse=decrescente))

    def test_casos_especiais(self):
        for dados in ([], [7], [2, 1], [3, 3, 3], list(range(20)), list(range(20, 0, -1))):
            lista = list(dados)
            quick_sort(lista)
            self.assertEqual(lista, sorted(dados))

    def test_nao_estoura_a_recursao(self):
        limite = sys.getrecursionlimit()
        sys.setrecursionlimit(120)   # a pilha do Quick Sort deve ficar O(log n)
        try:
            for dados in (list(range(20000)), list(range(20000, 0, -1)), [1] * 20000):
                lista = list(dados)
                quick_sort(lista)
                self.assertEqual(lista, sorted(dados))
        finally:
            sys.setrecursionlimit(limite)


class TestCatalogo(unittest.TestCase):
    def test_catalogo_do_arquivo_e_criterios(self):
        catalogo = carregar_catalogo()
        self.assertGreaterEqual(len(catalogo), 100)
        for rotulo, chave in CRITERIOS:
            ordenado, _ = ordenar_catalogo(catalogo, rotulo)
            self.assertEqual([chave(p) for p in ordenado], sorted(chave(p) for p in catalogo), rotulo)
        with self.assertRaises(ValueError):
            ordenar_catalogo(catalogo, "Cor")

    def test_geracao_deterministica(self):
        self.assertEqual([p.nome for p in gerar_catalogo(50)], [p.nome for p in gerar_catalogo(50)])


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP23", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
