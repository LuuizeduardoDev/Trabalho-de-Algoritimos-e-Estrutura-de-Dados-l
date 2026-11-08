"""Testes da SP06 - Controle de estoque (rode nesta pasta: python -m unittest -v)."""

import io
import unittest
from contextlib import redirect_stdout

from controle_estoque import ControleEstoque, EstoqueInsuficienteError, executar_demonstracao
from lista_encadeada import ListaEncadeada


class TestListaEncadeada(unittest.TestCase):
    def test_insercoes_em_qualquer_posicao(self):
        lista = ListaEncadeada([1, 2, 3])
        lista.inserir_inicio(0)
        lista.inserir_fim(4)
        lista.inserir_em(2, 9)
        lista.inserir_em(len(lista), 5)
        self.assertEqual(list(lista), [0, 1, 9, 2, 3, 4, 5])

    def test_remocoes_atualizam_inicio_e_fim(self):
        lista = ListaEncadeada([1, 2, 3, 4])
        self.assertEqual(lista.remover_se(lambda v: v == 4), 4)   # remove o último
        lista.inserir_fim(5)                                       # o fim foi atualizado
        self.assertEqual(list(lista), [1, 2, 3, 5])
        self.assertEqual(lista.remover_inicio(), 1)
        self.assertEqual(lista.remover_em(1), 3)
        self.assertEqual(list(lista), [2, 5])
        self.assertIsNone(lista.remover_se(lambda v: v == 99))

    def test_buscas(self):
        lista = ListaEncadeada(["ana", "bia", "caio", "bruno"])
        self.assertEqual(lista.buscar(lambda v: v.startswith("b")), "bia")
        self.assertEqual(lista.filtrar(lambda v: v.startswith("b")), ["bia", "bruno"])
        self.assertEqual(lista.indice(lambda v: v == "caio"), 2)
        self.assertEqual(lista.indice(lambda v: v == "zeca"), -1)
        self.assertEqual(lista.obter(3), "bruno")

    def test_posicoes_invalidas(self):
        lista = ListaEncadeada([1])
        for operacao in (lambda: lista.inserir_em(3, 0), lambda: lista.remover_em(1),
                         lambda: lista.obter(-1), lambda: ListaEncadeada().remover_inicio()):
            with self.assertRaises(IndexError):
                operacao()


class TestControleEstoque(unittest.TestCase):
    def setUp(self):
        self.estoque = ControleEstoque()
        self.estoque.cadastrar("CIM-50", "Cimento CP-II 50 kg", 10, 38.90, 5)
        self.estoque.cadastrar("TOR-12", "Torneira de jardim", 3, 27.90, 2)

    def test_esgotado_sai_da_lista_ativa_e_volta_com_entrada(self):
        self.estoque.registrar_saida("TOR-12", 3)
        self.assertEqual([p.codigo for p in self.estoque.ativos], ["CIM-50"])
        self.assertEqual([p.codigo for p in self.estoque.esgotados], ["TOR-12"])
        self.estoque.registrar_entrada("tor-12", 5)
        self.assertEqual([p.codigo for p in self.estoque.ativos], ["CIM-50", "TOR-12"])
        self.assertTrue(self.estoque.esgotados.esta_vazia())

    def test_saida_maior_que_o_estoque_e_recusada(self):
        with self.assertRaises(EstoqueInsuficienteError):
            self.estoque.registrar_saida("CIM-50", 11)
        self.assertEqual(self.estoque.buscar_por_codigo("CIM-50").quantidade, 10)

    def test_buscas_minimo_e_remocao(self):
        self.assertEqual(len(self.estoque.buscar_por_nome("CIMENTO")), 1)
        self.estoque.registrar_saida("CIM-50", 6)
        self.assertEqual([p.codigo for p in self.estoque.listar_abaixo_do_minimo()], ["CIM-50"])
        self.assertEqual(self.estoque.remover_produto("CIM-50").codigo, "CIM-50")
        self.assertIsNone(self.estoque.buscar_por_codigo("CIM-50"))
        with self.assertRaises(KeyError):
            self.estoque.remover_produto("CIM-50")
        with self.assertRaises(ValueError):
            self.estoque.cadastrar("tor-12", "Repetido", 1, 1.0)


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP06", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
