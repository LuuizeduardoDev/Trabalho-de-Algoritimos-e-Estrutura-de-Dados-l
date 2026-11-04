"""Testes da SP02 - Fila de impressão (rode nesta pasta: python -m unittest -v)."""

import io
import unittest
from contextlib import redirect_stdout

from fila import Fila
from fila_impressao import EVENTOS_DO_LABORATORIO, FilaDeImpressao, SimuladorLaboratorio, executar_demonstracao


class TestFila(unittest.TestCase):
    def test_primeiro_a_entrar_e_primeiro_a_sair(self):
        fila = Fila()
        for nome in ["Ana", "Bruno", "Carla"]:
            fila.enqueue(nome)
        self.assertEqual(fila.size(), 3)
        self.assertEqual(fila.front(), "Ana")
        self.assertEqual([fila.dequeue() for _ in range(3)], ["Ana", "Bruno", "Carla"])
        self.assertTrue(fila.is_empty())

    def test_fila_vazia_lanca_erro(self):
        fila = Fila()
        with self.assertRaises(IndexError):
            fila.dequeue()
        with self.assertRaises(IndexError):
            fila.front()

    def test_reutilizar_depois_de_esvaziar(self):
        fila = Fila([1, 2])
        fila.dequeue()
        fila.dequeue()
        fila.enqueue(3)
        self.assertEqual(list(fila), [3])
        self.assertEqual(fila.front(), 3)

    def test_listar_nao_remove(self):
        fila = Fila([1, 2, 3])
        self.assertEqual(list(fila), [1, 2, 3])
        self.assertEqual(len(fila), 3)


class TestFilaDeImpressao(unittest.TestCase):
    def test_imprime_na_ordem_de_chegada(self):
        fila = FilaDeImpressao()
        for aluno in ["Ana", "Bruno", "Carla"]:
            fila.enviar(aluno, "a.pdf", 2)
        self.assertEqual([fila.imprimir_proximo().aluno for _ in range(3)], ["Ana", "Bruno", "Carla"])

    def test_cancelar_ultimo_preserva_os_demais(self):
        fila = FilaDeImpressao()
        for aluno in ["Ana", "Bruno", "Carla", "Diego"]:
            fila.enviar(aluno, "a.pdf", 1)
        self.assertEqual(fila.cancelar_ultimo().aluno, "Diego")
        self.assertEqual([t.aluno for t in fila.listar()], ["Ana", "Bruno", "Carla"])
        self.assertIsNone(FilaDeImpressao().cancelar_ultimo())

    def test_simulacao_completa(self):
        simulador = SimuladorLaboratorio(mostrar=False)
        simulador.executar(EVENTOS_DO_LABORATORIO)
        numeros = [t.numero for t in simulador.impressos]
        self.assertEqual((simulador.enviados, len(simulador.cancelados), len(numeros)), (17, 2, 15))
        self.assertEqual(numeros, sorted(numeros))             # FIFO
        self.assertTrue(simulador.fila.esta_vazia())
        for anterior, atual in zip(simulador.impressos, simulador.impressos[1:]):
            self.assertGreaterEqual(atual.inicio, anterior.fim)   # uma impressão por vez

    def test_paginas_invalidas(self):
        with self.assertRaises(ValueError):
            FilaDeImpressao().enviar("Ana", "a.pdf", 0)


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP02", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
