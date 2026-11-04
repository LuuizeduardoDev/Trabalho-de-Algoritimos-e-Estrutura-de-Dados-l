"""SP13 – Cadastro de Usuários com Login Rápido.

Estrutura usada: Tabela hash com encadeamento -> tabela_hash.py

O que o enunciado pede e onde está:
  * tabela hash com tratamento de colisões (encadeamento) ... SistemaLogin.contas
  * cadastrar, autenticar (login), remover, listar .......... métodos de SistemaLogin
  * 20+ usuários e testes de colisão e autenticação ......... executar_demonstracao() (22 usuários)

Por que tabela hash: o login sempre procura UMA conta pela chave (e-mail ou
nome de usuário) e a ordem das contas não importa. A tabela hash leva direto
ao balde da chave: O(1) em média, mesmo com milhões de contas.

Segurança (como em sistemas reais):
  * a senha NUNCA é guardada; guarda-se um hash PBKDF2-SHA256 com um "sal"
    aleatório por usuário (hashlib/os/hmac são da biblioteca padrão e não
    fazem parte da estrutura avaliada);
  * a comparação usa hmac.compare_digest (tempo constante);
  * depois de 3 senhas erradas seguidas a conta é bloqueada (variação extra).
"""

from __future__ import annotations

import hashlib
import hmac
import os
import sys
from dataclasses import dataclass

from tabela_hash import TabelaHash
from merge_sort import merge_sort
from utilidades import cabecalho, configurar_terminal, imprimir_tabela, numero, secao

ITERACOES_PBKDF2 = 20_000   # baixo para a demonstração ficar rápida; produção usa 600.000+
MAX_TENTATIVAS = 3


@dataclass
class ContaUsuario:
    usuario: str
    nome: str
    sal: bytes
    hash_senha: bytes
    tentativas_erradas: int = 0
    bloqueada: bool = False


@dataclass
class ResultadoLogin:
    sucesso: bool
    mensagem: str


class SistemaLogin:
    """Contas guardadas numa tabela hash: chave = usuário normalizado."""

    def __init__(self, capacidade_inicial: int = 7, fator_carga_max: float = 0.75):
        self.contas = TabelaHash(capacidade_inicial, fator_carga_max)

    @staticmethod
    def normalizar(usuario: str) -> str:
        """E-mails não diferenciam maiúsculas: 'Ana@X.com ' e 'ana@x.com' são a mesma conta."""
        return usuario.strip().lower()

    @staticmethod
    def _hash_da_senha(senha: str, sal: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), sal, ITERACOES_PBKDF2)

    def cadastrar(self, usuario: str, nome: str, senha: str) -> ContaUsuario:
        """Cria a conta. O(1) em média. ValueError se o usuário já existir."""
        chave = self.normalizar(usuario)
        if not chave:
            raise ValueError("informe o usuário")
        if chave in self.contas:
            raise ValueError(f"o usuário {chave} já está cadastrado")
        if len(senha) < 6:
            raise ValueError("a senha precisa ter pelo menos 6 caracteres")
        sal = os.urandom(16)
        conta = ContaUsuario(chave, nome, sal, self._hash_da_senha(senha, sal))
        self.contas.inserir(chave, conta)
        return conta

    def autenticar(self, usuario: str, senha: str) -> ResultadoLogin:
        """Login: localiza a conta na tabela (O(1) médio) e confere a senha."""
        conta = self.contas.buscar(self.normalizar(usuario))
        if conta is None:
            return ResultadoLogin(False, "usuário não encontrado")
        if conta.bloqueada:
            return ResultadoLogin(False, "conta bloqueada por excesso de tentativas")
        if hmac.compare_digest(self._hash_da_senha(senha, conta.sal), conta.hash_senha):
            conta.tentativas_erradas = 0
            return ResultadoLogin(True, f"bem-vindo(a), {conta.nome}")
        conta.tentativas_erradas += 1
        if conta.tentativas_erradas >= MAX_TENTATIVAS:
            conta.bloqueada = True
            return ResultadoLogin(False, f"senha incorreta - conta BLOQUEADA após {MAX_TENTATIVAS} erros")
        restantes = MAX_TENTATIVAS - conta.tentativas_erradas
        return ResultadoLogin(False, f"senha incorreta ({restantes} tentativa(s) antes do bloqueio)")

    def desbloquear(self, usuario: str) -> bool:
        conta = self.contas.buscar(self.normalizar(usuario))
        if conta is None:
            return False
        conta.bloqueada = False
        conta.tentativas_erradas = 0
        return True

    def remover_conta(self, usuario: str) -> bool:
        """Exclui a conta. O(1) em média."""
        return self.contas.remover(self.normalizar(usuario))

    def listar_usuarios(self) -> list:
        """Usuários em ordem alfabética (a tabela hash não guarda ordem; ordenamos com Merge Sort)."""
        usuarios = list(self.contas.chaves())
        merge_sort(usuarios)
        return usuarios

    def __len__(self) -> int:
        return len(self.contas)


# ---------------------------------------------------------------------- dados
USUARIOS = [
    ("ana.souza@exemplo.com.br", "Ana Souza", "Sol@2024!"),
    ("bruno.lima@exemplo.com.br", "Bruno Lima", "Bru#1990x"),
    ("carla.dias@exemplo.com.br", "Carla Dias", "Carla$123"),
    ("daniel_rocha", "Daniel Rocha", "rocha.D99"),
    ("eduarda.mendes@exemplo.com.br", "Eduarda Mendes", "Duda!2025"),
    ("felipe.araujo@exemplo.com.br", "Felipe Araújo", "Fel1pe#A"),
    ("gabi.nunes", "Gabriela Nunes", "gabiN@77"),
    ("hugo.martins@exemplo.com.br", "Hugo Martins", "Hugo2024$"),
    ("isabela.freitas@exemplo.com.br", "Isabela Freitas", "IsaF!888"),
    ("joao.pedro@exemplo.com.br", "João Pedro", "JP_2003jp"),
    ("karina.alves@exemplo.com.br", "Karina Alves", "Kah*4567"),
    ("lucas.ferreira@exemplo.com.br", "Lucas Ferreira", "Luc@s321"),
    ("mari.costa", "Mariana Costa", "MariC#09"),
    ("nicolas.barros@exemplo.com.br", "Nicolas Barros", "Nico!B55"),
    ("olivia.mendes@exemplo.com.br", "Olívia Mendes", "Oli#v1a2"),
    ("paulo.vieira@exemplo.com.br", "Paulo Vieira", "PV@2020p"),
    ("rafa.teixeira", "Rafael Teixeira", "Rafa$T44"),
    ("sofia.ramos@exemplo.com.br", "Sofia Ramos", "S0fia!R1"),
    ("tiago.lopes@exemplo.com.br", "Tiago Lopes", "T1ag0#L"),
    ("vitoria.campos@exemplo.com.br", "Vitória Campos", "Vic@mpo5"),
    ("wesley.santos@exemplo.com.br", "Wesley Santos", "W3sley!S"),
    ("yasmin.oliveira@exemplo.com.br", "Yasmin Oliveira", "Yas#2001"),
]


def executar_demonstracao() -> None:
    cabecalho("SP13 - Cadastro de usuários com login rápido (Tabela hash com encadeamento)")
    sistema = SistemaLogin(capacidade_inicial=7)
    sistema.contas.ao_redimensionar = lambda antiga, nova: print(
        f"  rehash: fator de carga passou de 0,75 -> tabela cresce de {antiga} para {nova} baldes")

    secao(f"Cadastro de {len(USUARIOS)} usuários (tabela começa com 7 baldes)")
    for usuario, nome, senha in USUARIOS:
        sistema.cadastrar(usuario, nome, senha)
    tabela = sistema.contas
    print(f"  {len(sistema)} contas | {tabela.capacidade} baldes | fator de carga "
          f"{numero(tabela.fator_carga(), 2)} | redimensionamentos: {tabela.redimensionamentos}")

    secao("Como as contas ficaram distribuídas")
    tamanhos = tabela.tamanhos_das_cadeias()
    print(f"  Baldes ocupados: {tabela.baldes_ocupados()} de {tabela.capacidade} | "
          f"colisões: {tabela.colisoes()} contas dividem balde | maior cadeia: {tabela.maior_cadeia()}")
    print("  Baldes com colisão (as contas ficam encadeadas no mesmo balde):")
    for indice, tamanho in enumerate(tamanhos):
        if tamanho >= 2:
            print(f"    balde {indice:>2}: " + " -> ".join(tabela.cadeia(indice)))
    exemplo = next(indice for indice, tamanho in enumerate(tamanhos) if tamanho >= 2)
    primeira, segunda = tabela.cadeia(exemplo)[:2]
    print("  Por que colidem? hash(chave) mod capacidade dá o mesmo balde:")
    for chave in (primeira, segunda):
        h = tabela.funcao_hash(chave)
        print(f"    hash('{chave}') = {h:>10} -> {h} mod {tabela.capacidade} = {h % tabela.capacidade}")

    secao("Testes de autenticação")
    testes = [
        ("ana.souza@exemplo.com.br", "Sol@2024!", "senha correta"),
        ("ANA.SOUZA@exemplo.com.br ", "Sol@2024!", "mesmo e-mail em maiúsculas e com espaço"),
        ("joao.pedro@exemplo.com.br", "jp_2003jp", "senha com maiúscula/minúscula trocada"),
        ("joaopedro@exemplo.com.br", "JP_2003jp", "usuário digitado errado"),
        ("gabi.nunes", "gabiN@77", "login por nome de usuário"),
    ]
    linhas = []
    for usuario, senha, situacao in testes:
        resultado = sistema.autenticar(usuario, senha)
        linhas.append([usuario.strip(), situacao, "OK" if resultado.sucesso else "NEGADO", resultado.mensagem])
    imprimir_tabela(["Usuário", "Situação", "Login", "Mensagem"], linhas)

    secao("Bloqueio após 3 senhas erradas")
    alvo = "hugo.martins@exemplo.com.br"
    for senha in ["hugo2024", "Hugo2023$", "Hugo2025$", "Hugo2024$"]:
        resultado = sistema.autenticar(alvo, senha)
        print(f"  {'OK    ' if resultado.sucesso else 'NEGADO'}  senha '{senha}': {resultado.mensagem}")
    sistema.desbloquear(alvo)
    resultado = sistema.autenticar(alvo, "Hugo2024$")
    print(f"  {'OK    ' if resultado.sucesso else 'NEGADO'}  após o suporte desbloquear: {resultado.mensagem}")

    secao("Cadastro repetido e remoção de conta")
    try:
        sistema.cadastrar("Carla.Dias@exemplo.com.br", "Outra Carla", "qualquer123")
    except ValueError as erro:
        print(f"  cadastro recusado: {erro}")
    usuario = "tiago.lopes@exemplo.com.br"
    print(f"  remover {usuario}: {'removida' if sistema.remover_conta(usuario) else 'não existia'} "
          f"({len(sistema)} contas)")
    print(f"  login depois da remoção: {sistema.autenticar(usuario, 'T1ag0#L').mensagem}")
    print(f"  remover de novo: {'removida' if sistema.remover_conta(usuario) else 'não existia'}")

    secao("Listagem (opcional): primeiros usuários em ordem alfabética")
    for usuario in sistema.listar_usuarios()[:6]:
        print(f"  {usuario}")
    print(f"  ... {len(sistema)} contas no total")


def modo_interativo() -> None:
    sistema = SistemaLogin()
    for usuario, nome, senha in USUARIOS:
        sistema.cadastrar(usuario, nome, senha)
    print(f"\n{len(sistema)} contas carregadas (ex.: ana.souza@exemplo.com.br / Sol@2024!).")
    print("Tente fazer login (usuário vazio para sair).")
    while True:
        try:
            usuario = input("usuário> ")
            if not usuario:
                break
            senha = input("senha> ")
        except EOFError:
            break
        resultado = sistema.autenticar(usuario, senha)
        print(f"  {'OK' if resultado.sucesso else 'NEGADO'}: {resultado.mensagem}")


if __name__ == "__main__":
    configurar_terminal()
    executar_demonstracao()
    if "-i" in sys.argv[1:]:
        modo_interativo()
