"""Testes da SP08 - Autocomplete (rode nesta pasta: python -m unittest -v)."""

import io
import random
import unittest
from contextlib import redirect_stdout

from arvore_bst import ArvoreBST
from autocomplete_produtos import PRODUTOS, AutocompleteProdutos, executar_demonstracao
from utilidades import normalizar_texto


class TestArvoreBST(unittest.TestCase):
    def test_insercao_busca_e_percurso_em_ordem(self):
        arvore = ArvoreBST()
        for chave in [50, 30, 70, 20, 40, 60, 80]:
            self.assertTrue(arvore.inserir(chave, str(chave)))
        self.assertFalse(arvore.inserir(40, "quarenta"))        # repetida: só atualiza
        self.assertEqual(arvore.buscar(40), "quarenta")
        self.assertIsNone(arvore.buscar(45))
        self.assertEqual([c for c, _ in arvore.em_ordem()], [20, 30, 40, 50, 60, 70, 80])
        self.assertEqual(arvore.altura(), 3)
        self.assertEqual((arvore.minimo(), arvore.maximo()), (20, 80))

    def test_remocao_nos_tres_casos(self):
        arvore = ArvoreBST()
        for chave in [50, 30, 70, 20, 40, 60, 80, 65]:
            arvore.inserir(chave)
        self.assertTrue(arvore.remover(20))   # folha
        self.assertTrue(arvore.remover(60))   # um filho
        self.assertTrue(arvore.remover(50))   # dois filhos (raiz)
        self.assertFalse(arvore.remover(99))
        self.assertEqual([c for c, _ in arvore.em_ordem()], [30, 40, 65, 70, 80])
        self.assertEqual(len(arvore), 5)

    def test_insercao_ordenada_degenera(self):
        arvore = ArvoreBST()
        for chave in range(30):
            arvore.inserir(chave)
        self.assertEqual(arvore.altura(), 30)

    def test_aleatorio_contra_conjunto(self):
        sorteio = random.Random(1)
        for _ in range(50):
            arvore, referencia = ArvoreBST(), set()
            for _ in range(200):
                chave = sorteio.randint(0, 80)
                if sorteio.random() < 0.6:
                    self.assertEqual(arvore.inserir(chave), chave not in referencia)
                    referencia.add(chave)
                else:
                    self.assertEqual(arvore.remover(chave), chave in referencia)
                    referencia.discard(chave)
            self.assertEqual([c for c, _ in arvore.em_ordem()], sorted(referencia))


class TestAutocomplete(unittest.TestCase):
    def test_resultados_iguais_a_busca_ingenua(self):
        auto = AutocompleteProdutos(PRODUTOS)
        for prefixo in ["", "c", "ca", "caf", "café", "mouse", "pan", "smart", "z", "Fone de ouvido c"]:
            esperado = sorted((p for p in PRODUTOS if normalizar_texto(p).startswith(normalizar_texto(prefixo))),
                              key=normalizar_texto)
            sugestoes, _ = auto.sugerir(prefixo)
            self.assertEqual(sugestoes, esperado, prefixo)

    def test_percurso_limitado_e_limite(self):
        auto = AutocompleteProdutos(PRODUTOS)
        _, visitados = auto.sugerir("mouse")
        self.assertLess(visitados, len(PRODUTOS) // 4)
        sugestoes, _ = auto.sugerir("c", limite=3)
        self.assertEqual(len(sugestoes), 3)

    def test_nomes_repetidos_e_remocao(self):
        auto = AutocompleteProdutos(["Café"])
        self.assertFalse(auto.adicionar("CAFE"))
        self.assertTrue(auto.remover("café"))
        self.assertEqual(auto.sugerir("caf")[0], [])


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP08", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
