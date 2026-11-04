"""Testes das 12 situações-problema (python -m unittest)."""

import io
import random
import unittest
from contextlib import redirect_stdout
from importlib import import_module

from situacoes import SITUACOES
from situacoes.sp02_fila_impressao import EVENTOS_DO_LABORATORIO, FilaDeImpressao, SimuladorLaboratorio
from situacoes.sp04_verificador_expressoes import verificar_expressao
from situacoes.sp06_controle_estoque import ControleEstoque, EstoqueInsuficienteError
from situacoes.sp08_autocomplete import PRODUTOS, AutocompleteProdutos
from situacoes.sp10_ranking_jogadores import RankingJogadores
from situacoes.sp12_rede_social import montar_rede
from situacoes.sp13_login_usuarios import USUARIOS, SistemaLogin
from situacoes.sp16_vitrine_bubble import VITRINE, ordenar_vitrine
from situacoes.sp18_tarefas_selection import TAREFAS_DA_MANHA, Tarefa, organizar_por_prioridade
from situacoes.sp20_vendedores_insertion import Vendedor, atualizar_ranking, comparar_entradas
from situacoes.sp22_contatos_merge import (COMERCIAL, FINANCEIRO, Contato, esta_ordenada,
                                           mesclar_sem_duplicatas)
from situacoes.sp23_catalogo_quick import CRITERIOS, carregar_catalogo, gerar_catalogo, ordenar_catalogo
from situacoes.utilidades import normalizar_texto


class TestSP02FilaImpressao(unittest.TestCase):
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


class TestSP04Expressoes(unittest.TestCase):
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


class TestSP06Estoque(unittest.TestCase):
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


class TestSP08Autocomplete(unittest.TestCase):
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


class TestSP10Ranking(unittest.TestCase):
    def test_top_k_e_posicoes_contra_busca_ingenua(self):
        sorteio = random.Random(8)
        ranking, pontos = RankingJogadores(), {}
        for numero in range(60):
            nome = f"jogador{numero:02d}"
            pontos[nome] = sorteio.randint(0, 500)
            ranking.registrar(nome, pontos[nome])
        for _ in range(400):
            nome = sorteio.choice(list(pontos))
            pontos[nome] = ranking.somar_pontos(nome, sorteio.randint(-80, 80))
        esperado = sorted(pontos.items(), key=lambda par: (-par[1], par[0]))
        self.assertEqual([(n, p) for _, n, p in ranking.top(10)], esperado[:10])
        for posicao, (nome, _) in enumerate(esperado, start=1):
            self.assertEqual(ranking.posicao(nome), posicao)
        self.assertTrue(ranking.arvore.esta_balanceada())

    def test_desempate_por_nome_e_remocao(self):
        ranking = RankingJogadores()
        for nome, pontos in [("Zeca", 100), ("Ana", 100), ("Bia", 150)]:
            ranking.registrar(nome, pontos)
        self.assertEqual([n for _, n, _ in ranking.top(3)], ["Bia", "Ana", "Zeca"])
        ranking.remover("Bia")
        self.assertEqual(ranking.jogador_na_posicao(1), ("Ana", 100))
        with self.assertRaises(ValueError):
            ranking.registrar("Ana", 10)
        with self.assertRaises(KeyError):
            ranking.pontos("Bia")


class TestSP12RedeSocial(unittest.TestCase):
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


class TestSP13Login(unittest.TestCase):
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


class TestSP16SP18SP20Ordenacoes(unittest.TestCase):
    def test_vitrine_crescente_decrescente_e_estavel(self):
        crescente, _ = ordenar_vitrine(VITRINE, crescente=True)
        decrescente, _ = ordenar_vitrine(VITRINE, crescente=False)
        self.assertEqual([p.preco for p in crescente], sorted(p.preco for p in VITRINE))
        self.assertEqual([p.preco for p in decrescente], sorted((p.preco for p in VITRINE), reverse=True))
        empatados = [p.nome for p in crescente if p.preco == 39.90]
        self.assertEqual(empatados, ["Caneca personalizada", "Chaveiro de couro"])
        self.assertEqual(VITRINE[0].nome, "Fone de ouvido bluetooth")   # original intacta

    def test_tarefas_por_prioridade_com_desempate(self):
        agenda, metricas = organizar_por_prioridade(TAREFAS_DA_MANHA)
        chaves = [(-t.prioridade, t.codigo) for t in agenda]
        self.assertEqual(chaves, sorted(chaves))
        self.assertLessEqual(metricas.trocas, len(agenda) - 1)
        with self.assertRaises(ValueError):
            Tarefa(99, "inválida", 6, 10)

    def test_ranking_de_vendedores(self):
        ranking = [Vendedor("B", 100.0), Vendedor("A", 300.0), Vendedor("C", 100.0)]
        atualizar_ranking(ranking)
        self.assertEqual([v.nome for v in ranking], ["A", "B", "C"])   # empate: mantém a ordem anterior
        ordenada, quase, aleatoria = comparar_entradas(300)
        self.assertEqual(ordenada.comparacoes, 299)
        self.assertLess(quase.comparacoes, aleatoria.comparacoes)


class TestSP22Contatos(unittest.TestCase):
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


class TestSP23Catalogo(unittest.TestCase):
    def test_catalogo_do_arquivo_e_criterios(self):
        catalogo = carregar_catalogo()
        self.assertGreaterEqual(len(catalogo), 100)
        for rotulo, chave in CRITERIOS:
            ordenado, _ = ordenar_catalogo(catalogo, rotulo)
            self.assertEqual([chave(p) for p in ordenado], sorted(chave(p) for p in catalogo), rotulo)
        with self.assertRaises(ValueError):
            ordenar_catalogo(catalogo, "Cor")

    def test_geracao_deterministica(self):
        self.assertEqual([p.nome for p in gerar_catalogo(50)], [p.nome for p in gerar_catalogo(50)])


class TestDemonstracoes(unittest.TestCase):
    def test_todas_as_demonstracoes_rodam(self):
        for codigo, _, _, nome_modulo in SITUACOES:
            saida = io.StringIO()
            with redirect_stdout(saida):
                import_module(nome_modulo).executar_demonstracao()
            self.assertIn(codigo, saida.getvalue(), codigo)


if __name__ == "__main__":
    unittest.main()
