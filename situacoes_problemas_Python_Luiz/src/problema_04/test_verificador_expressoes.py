"""Testes da SP04 - Verificação de expressões (rode nesta pasta: python -m unittest -v)."""

import io
import unittest
from contextlib import redirect_stdout

from pilha import Pilha
from verificador_expressoes import executar_demonstracao, verificar_expressao


class TestPilha(unittest.TestCase):
    def test_ultimo_a_entrar_e_primeiro_a_sair(self):
        pilha = Pilha()
        for valor in range(5):
            pilha.push(valor)
        self.assertEqual(pilha.peek(), 4)
        self.assertEqual(list(pilha), [4, 3, 2, 1, 0])   # topo -> base
        self.assertEqual([pilha.pop() for _ in range(5)], [4, 3, 2, 1, 0])
        self.assertTrue(pilha.is_empty())

    def test_pilha_vazia_lanca_erro(self):
        with self.assertRaises(IndexError):
            Pilha().pop()
        with self.assertRaises(IndexError):
            Pilha().peek()


class TestVerificador(unittest.TestCase):
    def test_exemplos_do_enunciado(self):
        self.assertTrue(verificar_expressao("{ [ ( ) ] }").balanceada)
        self.assertTrue(verificar_expressao("((()))").balanceada)
        self.assertFalse(verificar_expressao("( [ ) ]").balanceada)
        self.assertFalse(verificar_expressao("([)]").balanceada)

    def test_posicao_do_primeiro_erro(self):
        self.assertEqual(verificar_expressao("( [ ) ]").posicao, 5)
        self.assertEqual(verificar_expressao("a + b)").posicao, 6)
        self.assertEqual(verificar_expressao("((a + b) * c").posicao, 1)
        self.assertIsNone(verificar_expressao("").posicao)

    def test_ignorar_texto_entre_aspas(self):
        codigo = 'print("sorriso :)")'
        self.assertFalse(verificar_expressao(codigo).balanceada)
        self.assertTrue(verificar_expressao(codigo, ignorar_strings=True).balanceada)
        self.assertFalse(verificar_expressao('print("aberto)', ignorar_strings=True).balanceada)


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP04", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
