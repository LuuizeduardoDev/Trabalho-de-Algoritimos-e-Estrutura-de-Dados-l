"""Testes da SP12 - Rede de amizades (rode nesta pasta: python -m unittest -v)."""

import io
import unittest
from contextlib import redirect_stdout

from grafo import Grafo
from rede_social import executar_demonstracao, montar_rede


class TestGrafo(unittest.TestCase):
    def setUp(self):
        self.grafo = Grafo()
        for a, b in [("A", "B"), ("B", "C"), ("C", "D"), ("A", "E"), ("E", "D"), ("X", "Y")]:
            self.grafo.adicionar_aresta(a, b)

    def test_arestas_nao_direcionadas(self):
        self.assertTrue(self.grafo.tem_aresta("B", "A"))
        self.assertFalse(self.grafo.adicionar_aresta("B", "A"))   # repetida
        self.assertEqual(self.grafo.num_arestas(), 6)
        self.assertEqual(self.grafo.vizinhos("A"), ["B", "E"])
        with self.assertRaises(ValueError):
            self.grafo.adicionar_aresta("A", "A")
        with self.assertRaises(KeyError):
            self.grafo.vizinhos("Z")

    def test_bfs_e_menor_caminho(self):
        self.assertEqual(self.grafo.busca_em_largura("A"),
                         [("A", 0), ("B", 1), ("E", 1), ("C", 2), ("D", 2)])
        self.assertEqual(self.grafo.caminho_mais_curto("A", "D"), ["A", "E", "D"])
        self.assertIsNone(self.grafo.caminho_mais_curto("A", "X"))
        self.assertEqual(self.grafo.caminho_mais_curto("C", "C"), ["C"])

    def test_remover_aresta_e_componentes(self):
        self.assertEqual(len(self.grafo.componentes()), 2)
        self.assertTrue(self.grafo.remover_aresta("X", "Y"))
        self.assertFalse(self.grafo.tem_aresta("Y", "X"))
        self.assertEqual(len(self.grafo.componentes()), 3)

    def test_grafo_direcionado_com_pesos(self):
        grafo = Grafo(direcionado=True)
        grafo.adicionar_aresta("Centro", "Bairro A", 7)
        self.assertTrue(grafo.tem_aresta("Centro", "Bairro A"))
        self.assertFalse(grafo.tem_aresta("Bairro A", "Centro"))
        self.assertEqual(grafo.vizinhos_com_peso("Centro"), [("Bairro A", 7)])


class TestRedeSocial(unittest.TestCase):
    def setUp(self):
        self.rede = montar_rede()

    def test_amigos_e_amigos_em_comum(self):
        self.assertEqual(self.rede.amigos("Ana"), ["Bruno", "Carla", "Daniel"])
        self.assertEqual(self.rede.amigos_em_comum("Ana", "Eduarda"), ["Bruno", "Daniel"])
        self.assertEqual(self.rede.amigos_em_comum("Ana", "Hugo"), [])

    def test_graus_de_separacao(self):
        self.assertEqual(self.rede.grau_de_separacao("Ana", "Bruno")[0], 1)
        self.assertEqual(self.rede.grau_de_separacao("Ana", "Paulo")[0], 8)
        self.assertEqual(self.rede.grau_de_separacao("Ana", "Sofia"), (None, None))
        self.rede.adicionar_amizade("Daniel", "Paulo")
        self.assertEqual(self.rede.grau_de_separacao("Ana", "Paulo"), (2, ["Ana", "Daniel", "Paulo"]))

    def test_sugestoes_e_componentes(self):
        self.assertEqual(self.rede.sugerir_conexoes("Ana"), [("Eduarda", 2), ("Felipe", 1)])
        self.assertEqual(self.rede.sugerir_conexoes("Tiago"), [])
        self.assertEqual(len(self.rede.estatisticas()[4]), 3)


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP12", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
