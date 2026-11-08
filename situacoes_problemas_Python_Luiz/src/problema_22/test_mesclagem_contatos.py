"""Testes da SP22 - Mesclagem de contatos (rode nesta pasta: python -m unittest -v).

O sorted() do Python aparece aqui só como GABARITO para conferir os resultados.
"""

import io
import random
import unittest
from contextlib import redirect_stdout

from merge_sort import intercalar, merge_sort
from mesclagem_contatos import COMERCIAL, FINANCEIRO, Contato, esta_ordenada, executar_demonstracao, \
    mesclar_sem_duplicatas


class TestMergeSort(unittest.TestCase):
    def test_contra_gabarito_crescente_e_decrescente(self):
        sorteio = random.Random(4)
        for _ in range(150):
            dados = [sorteio.randint(-50, 50) for _ in range(sorteio.randint(0, 60))]
            for decrescente in (False, True):
                lista = list(dados)
                merge_sort(lista, decrescente=decrescente)
                self.assertEqual(lista, sorted(dados, reverse=decrescente))

    def test_estavel_nos_dois_sentidos(self):
        sorteio = random.Random(5)
        registros = [(sorteio.randint(0, 5), indice) for indice in range(80)]
        for decrescente in (False, True):
            lista = list(registros)
            merge_sort(lista, chave=lambda r: r[0], decrescente=decrescente)
            self.assertEqual(lista, sorted(registros, key=lambda r: r[0], reverse=decrescente))

    def test_intercalar_duas_listas_ordenadas(self):
        resultado, metricas = intercalar([1, 4, 9], [2, 3, 10, 11])
        self.assertEqual(resultado, [1, 2, 3, 4, 9, 10, 11])
        self.assertLessEqual(metricas.comparacoes, 6)


class TestMesclagem(unittest.TestCase):
    def test_mesclagem_das_listas_da_demonstracao(self):
        unica, removidas, _ = mesclar_sem_duplicatas(COMERCIAL, FINANCEIRO)
        self.assertEqual((len(unica), len(removidas)), (34, 6))
        self.assertTrue(esta_ordenada(unica))
        self.assertEqual(sum(1 for c in unica if c.nome == "Ana Paula Souza"), 2)   # homônimos
        carlos = next(c for c in unica if c.nome == "Carlos Eduardo Nunes")
        self.assertEqual(carlos.departamentos, "Comercial + Financeiro")
        self.assertEqual(COMERCIAL[3].departamentos, "Comercial")                 # entrada intacta

    def test_casos_limite(self):
        contato = Contato("Ana", "ana@x.com", "1", "A")
        self.assertEqual(mesclar_sem_duplicatas([], [])[0], [])
        self.assertEqual(len(mesclar_sem_duplicatas([contato], [])[0]), 1)
        repetidos = [contato, Contato("ana", "ANA@x.com", "1", "A")]               # repetido na mesma lista
        self.assertEqual(len(mesclar_sem_duplicatas(repetidos, [contato])[0]), 1)


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP22", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
