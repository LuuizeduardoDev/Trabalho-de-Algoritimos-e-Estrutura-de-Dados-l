"""Testes da SP13 - Cadastro e login (rode nesta pasta: python -m unittest -v)."""

import io
import random
import unittest
from contextlib import redirect_stdout

from login_usuarios import USUARIOS, SistemaLogin, executar_demonstracao
from tabela_hash import TabelaHash


class TestTabelaHash(unittest.TestCase):
    def test_operacoes_basicas(self):
        tabela = TabelaHash()
        self.assertTrue(tabela.inserir("ana", 1))
        self.assertFalse(tabela.inserir("ana", 2))      # atualiza
        tabela["bia"] = 3
        self.assertEqual(tabela.buscar("ana"), 2)
        self.assertEqual(tabela["bia"], 3)
        self.assertIn("bia", tabela)
        self.assertIsNone(tabela.buscar("caio"))
        self.assertTrue(tabela.remover("ana"))
        self.assertFalse(tabela.remover("ana"))
        self.assertEqual(len(tabela), 1)
        with self.assertRaises(KeyError):
            tabela["ana"]
        with self.assertRaises(KeyError):
            del tabela["ana"]

    def test_funcao_hash_deterministica(self):
        self.assertEqual(TabelaHash.funcao_hash("abc"), 96354)   # mesmo valor do String.hashCode() do Java
        self.assertEqual(TabelaHash.funcao_hash(42), 42)
        self.assertNotEqual(TabelaHash.funcao_hash((1, 2)), TabelaHash.funcao_hash((2, 1)))

    def test_colisoes_com_encadeamento(self):
        tabela = TabelaHash(capacidade=1, fator_carga_max=None)   # tudo cai no mesmo balde
        for numero in range(10):
            tabela.inserir(f"chave{numero}", numero)
        self.assertEqual(tabela.maior_cadeia(), 10)
        self.assertEqual(tabela.colisoes(), 9)
        for numero in range(10):
            self.assertEqual(tabela.buscar(f"chave{numero}"), numero)
        self.assertTrue(tabela.remover("chave5"))
        self.assertEqual(len(tabela.cadeia(0)), 9)

    def test_redimensionamento_preserva_itens(self):
        tabela = TabelaHash(capacidade=7, fator_carga_max=0.75)
        eventos = []
        tabela.ao_redimensionar = lambda antiga, nova: eventos.append((antiga, nova))
        for numero in range(100):
            tabela.inserir(f"usuario{numero}", numero)
        self.assertEqual(eventos[0], (7, 17))
        self.assertLessEqual(tabela.fator_carga(), 0.75)
        self.assertEqual(sum(tabela.tamanhos_das_cadeias()), 100)
        self.assertTrue(all(tabela.buscar(f"usuario{n}") == n for n in range(100)))

    def test_aleatorio_contra_dict(self):
        sorteio = random.Random(3)
        tabela, referencia = TabelaHash(capacidade=3), {}
        for _ in range(3000):
            chave = sorteio.choice([sorteio.randint(-20, 200), f"k{sorteio.randint(0, 150)}"])
            if sorteio.random() < 0.6:
                tabela.inserir(chave, chave)
                referencia[chave] = chave
            else:
                self.assertEqual(tabela.remover(chave), chave in referencia)
                referencia.pop(chave, None)
        self.assertEqual(len(tabela), len(referencia))
        self.assertEqual({k: v for k, v in tabela.itens()}, referencia)


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sistema = SistemaLogin(capacidade_inicial=7)
        for usuario, nome, senha in USUARIOS:
            cls.sistema.cadastrar(usuario, nome, senha)

    def test_cadastro_com_colisoes_e_redimensionamento(self):
        tabela = self.sistema.contas
        self.assertGreaterEqual(len(self.sistema), 20)
        self.assertGreater(tabela.redimensionamentos, 0)
        self.assertGreater(tabela.colisoes(), 0)

    def test_autenticacao(self):
        self.assertTrue(self.sistema.autenticar("ana.souza@exemplo.com.br", "Sol@2024!").sucesso)
        self.assertTrue(self.sistema.autenticar("  ANA.SOUZA@exemplo.com.br", "Sol@2024!").sucesso)
        self.assertFalse(self.sistema.autenticar("ana.souza@exemplo.com.br", "sol@2024!").sucesso)
        self.assertFalse(self.sistema.autenticar("ninguem@exemplo.com.br", "qualquer").sucesso)

    def test_bloqueio_remocao_e_duplicata(self):
        sistema = SistemaLogin()
        sistema.cadastrar("teste", "Teste", "segredo1")
        for _ in range(3):
            sistema.autenticar("teste", "errada")
        self.assertFalse(sistema.autenticar("teste", "segredo1").sucesso)   # bloqueada
        sistema.desbloquear("teste")
        self.assertTrue(sistema.autenticar("teste", "segredo1").sucesso)
        with self.assertRaises(ValueError):
            sistema.cadastrar("TESTE", "Outro", "segredo2")
        with self.assertRaises(ValueError):
            sistema.cadastrar("novo", "Novo", "123")                       # senha curta
        self.assertTrue(sistema.remover_conta("teste"))
        self.assertFalse(sistema.autenticar("teste", "segredo1").sucesso)

    def test_senha_nao_fica_guardada(self):
        conta = self.sistema.contas.buscar("ana.souza@exemplo.com.br")
        self.assertNotIn(b"Sol@2024!", conta.hash_senha)
        self.assertEqual(len(conta.hash_senha), 32)


class TestDemonstracao(unittest.TestCase):
    def test_demonstracao_roda_sem_erro(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            executar_demonstracao()
        self.assertIn("SP13", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
