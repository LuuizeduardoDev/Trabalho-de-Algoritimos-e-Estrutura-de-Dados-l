"""Testes dos algoritmos de ordenação (python -m unittest).

O sorted() do Python aparece aqui só como GABARITO para conferir os resultados;
as implementações em ordenacao/ não o usam.
"""

import random
import sys
import unittest

from ordenacao import (bubble_sort, inserir_em_ordem, insertion_sort, intercalar, merge_sort, quick_sort,
                       selection_sort)

TODOS = [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort]
ESTAVEIS = [bubble_sort, insertion_sort, merge_sort]


class TestCorretude(unittest.TestCase):
    def test_contra_gabarito_crescente_e_decrescente(self):
        sorteio = random.Random(4)
        for _ in range(150):
            dados = [sorteio.randint(-50, 50) for _ in range(sorteio.randint(0, 60))]
            for algoritmo in TODOS:
                for decrescente in (False, True):
                    lista = list(dados)
                    algoritmo(lista, decrescente=decrescente)
                    self.assertEqual(lista, sorted(dados, reverse=decrescente), algoritmo.__name__)

    def test_casos_especiais(self):
        for algoritmo in TODOS:
            for dados in ([], [7], [2, 1], [3, 3, 3], list(range(20)), list(range(20, 0, -1))):
                lista = list(dados)
                algoritmo(lista)
                self.assertEqual(lista, sorted(dados), algoritmo.__name__)

    def test_chave_personalizada(self):
        palavras = ["banana", "kiwi", "abacaxi", "uva", "maçã"]
        for algoritmo in TODOS:
            lista = list(palavras)
            algoritmo(lista, chave=len)
            self.assertEqual([len(p) for p in lista], sorted(len(p) for p in palavras))


class TestEstabilidade(unittest.TestCase):
    def test_empates_mantem_a_ordem_original(self):
        sorteio = random.Random(5)
        registros = [(sorteio.randint(0, 5), indice) for indice in range(80)]
        for algoritmo in ESTAVEIS:
            for decrescente in (False, True):
                lista = list(registros)
                algoritmo(lista, chave=lambda r: r[0], decrescente=decrescente)
                esperado = sorted(registros, key=lambda r: r[0], reverse=decrescente)  # sorted é estável
                self.assertEqual(lista, esperado, (algoritmo.__name__, decrescente))


class TestMetricas(unittest.TestCase):
    def test_bubble_para_cedo_quando_ja_esta_ordenado(self):
        metricas = bubble_sort(list(range(100)))
        self.assertEqual((metricas.passadas, metricas.comparacoes, metricas.trocas), (1, 99, 0))

    def test_bubble_pior_caso(self):
        metricas = bubble_sort(list(range(10, 0, -1)))
        self.assertEqual((metricas.comparacoes, metricas.trocas), (45, 45))

    def test_selection_faz_no_maximo_n_menos_1_trocas(self):
        dados = [random.Random(6).random() for _ in range(50)]
        metricas = selection_sort(dados)
        self.assertEqual(metricas.comparacoes, 50 * 49 // 2)
        self.assertLessEqual(metricas.trocas, 49)

    def test_insertion_linear_em_lista_ordenada(self):
        metricas = insertion_sort(list(range(1000)))
        self.assertEqual((metricas.comparacoes, metricas.trocas), (999, 0))

    def test_quick_sort_nao_estoura_recursao(self):
        limite = sys.getrecursionlimit()
        sys.setrecursionlimit(120)   # a pilha do Quick Sort deve ficar O(log n)
        try:
            for dados in (list(range(20000)), list(range(20000, 0, -1)), [1] * 20000):
                lista = list(dados)
                quick_sort(lista)
                self.assertEqual(lista, sorted(dados))
        finally:
            sys.setrecursionlimit(limite)


class TestAuxiliares(unittest.TestCase):
    def test_intercalar_duas_listas_ordenadas(self):
        resultado, metricas = intercalar([1, 4, 9], [2, 3, 10, 11])
        self.assertEqual(resultado, [1, 2, 3, 4, 9, 10, 11])
        self.assertLessEqual(metricas.comparacoes, 6)

    def test_inserir_em_ordem(self):
        mao = []
        for carta in [5, 2, 8, 2, 9, 1]:
            inserir_em_ordem(mao, carta)
        self.assertEqual(mao, [1, 2, 2, 5, 8, 9])
        self.assertEqual(inserir_em_ordem(mao, 6), 4)


if __name__ == "__main__":
    unittest.main()
