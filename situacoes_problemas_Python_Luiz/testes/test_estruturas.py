"""Testes das estruturas de dados (python -m unittest)."""

import math
import random
import unittest

from estruturas import ArvoreAVL, ArvoreBST, Fila, Grafo, ListaEncadeada, Pilha, TabelaHash


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


class TestArvoreAVL(unittest.TestCase):
    def _raiz(self, chaves):
        arvore = ArvoreAVL()
        for chave in chaves:
            arvore.inserir(chave)
        return arvore

    def test_quatro_casos_de_rotacao(self):
        casos = {"ll": [30, 20, 10], "rr": [10, 20, 30], "lr": [30, 10, 20], "rl": [10, 30, 20]}
        for caso, chaves in casos.items():
            arvore = self._raiz(chaves)
            self.assertEqual(arvore.raiz.chave, 20, caso)
            self.assertEqual(getattr(arvore.rotacoes, caso), 1, caso)
            self.assertEqual(arvore.altura(), 2)

    def test_insercao_ordenada_continua_balanceada(self):
        arvore = self._raiz(range(1, 1001))
        self.assertTrue(arvore.esta_balanceada())
        self.assertLessEqual(arvore.altura(), 1.44 * math.log2(1000 + 2))
        self.assertEqual(arvore.altura(), 10)   # 1000 chaves: altura mínima possível

    def test_remocao_rebalanceia(self):
        arvore = self._raiz(range(1, 32))       # árvore perfeita com 31 nós
        for chave in range(1, 16):
            self.assertTrue(arvore.remover(chave))
            self.assertTrue(arvore.esta_balanceada())
        self.assertFalse(arvore.remover(1))
        self.assertEqual([c for c, _ in arvore.em_ordem()], list(range(16, 32)))

    def test_posicao_k_esimo_e_primeiros(self):
        arvore = self._raiz([40, 10, 30, 20, 50])
        self.assertEqual(arvore.posicao(10), 1)
        self.assertEqual(arvore.posicao(50), 5)
        self.assertIsNone(arvore.posicao(35))
        self.assertEqual(arvore.k_esimo(3)[0], 30)
        self.assertEqual([c for c, _ in arvore.primeiros(2)], [10, 20])
        with self.assertRaises(IndexError):
            arvore.k_esimo(6)

    def test_aleatorio_mantem_todas_as_regras(self):
        sorteio = random.Random(2)
        for _ in range(40):
            arvore, referencia = ArvoreAVL(), set()
            for _ in range(250):
                chave = sorteio.randint(0, 120)
                if sorteio.random() < 0.6:
                    arvore.inserir(chave, chave * 2)
                    referencia.add(chave)
                else:
                    self.assertEqual(arvore.remover(chave), chave in referencia)
                    referencia.discard(chave)
            self.assertTrue(arvore.esta_balanceada())
            ordenadas = sorted(referencia)
            self.assertEqual([c for c, _ in arvore.em_ordem()], ordenadas)
            for posicao, chave in enumerate(ordenadas, start=1):
                self.assertEqual(arvore.posicao(chave), posicao)
                self.assertEqual(arvore.buscar(chave), chave * 2)


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
        self.assertEqual(TabelaHash.funcao_hash("abc"), TabelaHash.funcao_hash("abc"))
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


if __name__ == "__main__":
    unittest.main()
