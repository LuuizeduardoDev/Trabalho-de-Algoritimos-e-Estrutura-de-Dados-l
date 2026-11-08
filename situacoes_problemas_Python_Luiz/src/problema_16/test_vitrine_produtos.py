"""Testes da SP16 - Vitrine com Bubble Sort (rode nesta pasta: python -m unittest -v).

O sorted() do Python aparece aqui só como GABARITO para conferir os resultados.
"""

import io
import random
import unittest
from contextlib import redirect_stdout

from bubble_sort import bubble_sort
from vitrine_produtos import VITRINE, executar_demonstracao, ordenar_vitrine


class TestBubbleSort(unittest.TestCase):
    def test_contra_gabarito_crescente_e_decrescente(self):
        sorteio = random.Random(4)
        for _ in range(150):
            dados = [sorteio.randint(-50, 50) for _ in range(sorteio.randint(0, 60))]
            for decrescente in (False, True):
                lista = list(dados)
                bubble_sort(lista, decrescente=decrescente)
                self.assertEqual(lista, sorted(dados, reverse=decrescente))

    def test_casos_especiais(self):
        for dados in ([], [7], [2, 1], [3, 3, 3], list(range(20)), list(range(20, 0, -1))):
            lista = list(dados)
            bubble_sort(lista)
            self.assertEqual(lista, sorted(dados))

    def test_estavel_nos_dois_sentidos(self):
        sorteio = random.Random(5)
        registros = [(sorteio.randint(0, 5), indice) for indice in range(80)]
        for decrescente in (False, True):
            lista = list(registros)
            bubble_sort(lista, chave=lambda r: r[0], decrescente=decrescente)
            self.assertEqual(lista, sorted(registros, key=lambda r: r[0], reverse=decrescente))

    def test_para_cedo_quando_ja_esta_ordenado(self):
        metricas = bubble_sort(list(range(100)))
        self.assertEqual((metricas.passadas, metricas.comparacoes, metricas.trocas), (1, 99, 0))

    def test_pior_caso(self):
        metricas = bubble_sort(list(range(10, 0, -1)))
        self.assertEqual((metricas.comparacoes, metricas.trocas), (45, 45))


class TestVitrine(unittest.TestCase):
    def test_crescente_decrescente_e_estavel(self):
        crescente, _ = ordenar_vitrine(VITRINE, crescente=True)
        decrescente, _ = ordenar_vitrine(VITRINE, crescente=False)
        self.assertEqual([p.preco for p in crescente], sorted(p.preco for p in VITRINE))
        self.assertEqual([p.preco for p in decrescente], sorted((p.preco for p in VITRINE), reverse=True))
        empatados = [p.nome for p in crescente if p.preco == 39.90]
        self.assertEqual(empatados, ["Caneca personalizada", "Chaveiro de couro"])
        self.assertEqual(VITRINE[0].nome, "Fone de ouvido bluetooth")   # original intacta


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP16", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
