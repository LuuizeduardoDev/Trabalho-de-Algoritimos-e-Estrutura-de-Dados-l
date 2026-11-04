"""Testes da SP18 - Tarefas com Selection Sort (rode nesta pasta: python -m unittest -v).

O sorted() do Python aparece aqui só como GABARITO para conferir os resultados.
"""

import io
import random
import unittest
from contextlib import redirect_stdout

from selection_sort import selection_sort
from tarefas_prioridade import TAREFAS_DA_MANHA, Tarefa, executar_demonstracao, organizar_por_prioridade


class TestSelectionSort(unittest.TestCase):
    def test_contra_gabarito_crescente_e_decrescente(self):
        sorteio = random.Random(4)
        for _ in range(150):
            dados = [sorteio.randint(-50, 50) for _ in range(sorteio.randint(0, 60))]
            for decrescente in (False, True):
                lista = list(dados)
                selection_sort(lista, decrescente=decrescente)
                self.assertEqual(lista, sorted(dados, reverse=decrescente))

    def test_casos_especiais(self):
        for dados in ([], [7], [2, 1], [3, 3, 3], list(range(20)), list(range(20, 0, -1))):
            lista = list(dados)
            selection_sort(lista)
            self.assertEqual(lista, sorted(dados))

    def test_comparacoes_fixas_e_poucas_trocas(self):
        dados = [random.Random(6).random() for _ in range(50)]
        metricas = selection_sort(dados)
        self.assertEqual(metricas.comparacoes, 50 * 49 // 2)
        self.assertLessEqual(metricas.trocas, 49)


class TestTarefas(unittest.TestCase):
    def test_tarefas_por_prioridade_com_desempate(self):
        agenda, metricas = organizar_por_prioridade(TAREFAS_DA_MANHA)
        chaves = [(-t.prioridade, t.codigo) for t in agenda]
        self.assertEqual(chaves, sorted(chaves))
        self.assertLessEqual(metricas.trocas, len(agenda) - 1)
        with self.assertRaises(ValueError):
            Tarefa(99, "inválida", 6, 10)


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP18", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
