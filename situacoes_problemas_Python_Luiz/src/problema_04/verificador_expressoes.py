"""SP04 – Verificação de Expressões com Parênteses, Colchetes e Chaves.

Estrutura usada: Pilha (LIFO) -> pilha.py

O que o enunciado pede e onde está:
  * função que recebe uma string e diz se está balanceada .. verificar_expressao()
  * suporte a (), [] e {} ................................... ABERTURAS / FECHAMENTOS
  * testes com expressões válidas e inválidas ............... EXPRESSOES_DE_TESTE
  * posição do primeiro desbalanceamento (valorizado) ....... ResultadoVerificacao.posicao

Por que pilha: o ÚLTIMO símbolo aberto precisa ser o PRIMEIRO a ser fechado.
Cada abertura é empilhada; cada fechamento precisa casar com o topo da pilha.
É exatamente a regra LIFO.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional

from pilha import Pilha
from utilidades import cabecalho, configurar_terminal, secao

ABERTURAS = "([{"
FECHAMENTOS = ")]}"   # FECHAMENTOS[i] fecha ABERTURAS[i]


@dataclass
class ResultadoVerificacao:
    balanceada: bool
    posicao: Optional[int] = None   # posição do 1º problema (1 = primeiro caractere)
    mensagem: str = "expressão balanceada"


def verificar_expressao(expressao: str, ignorar_strings: bool = False, passos: list = None) -> ResultadoVerificacao:
    """Diz se (), [] e {} estão balanceados e onde está o primeiro erro.

    Tempo O(n) — cada caractere é visto uma vez e cada push/pop é O(1).
    Espaço O(n) no pior caso (todas as aberturas empilhadas).

    ignorar_strings: em trechos de código, ignora símbolos dentro de aspas
                     (ex.: print(":)") é válido).
    passos: se uma lista for passada, recebe a descrição de cada push/pop
            (usado para mostrar a pilha passo a passo).
    """
    pilha = Pilha()          # guarda pares (símbolo de abertura, posição)
    aspas_abertas = None     # aspas que abriram a string atual
    posicao_aspas = 0
    escapado = False

    for indice, caractere in enumerate(expressao):
        posicao = indice + 1

        if ignorar_strings:
            if aspas_abertas is not None:          # estamos dentro de uma string
                if escapado:
                    escapado = False
                elif caractere == "\\":
                    escapado = True
                elif caractere == aspas_abertas:
                    aspas_abertas = None
                continue
            if caractere in "\"'":
                aspas_abertas, posicao_aspas = caractere, posicao
                continue

        if caractere in ABERTURAS:
            pilha.push((caractere, posicao))
            if passos is not None:
                passos.append(f"pos {posicao:>2}: '{caractere}' -> push   pilha: {_mostrar(pilha)}")
        elif caractere in FECHAMENTOS:
            esperado = ABERTURAS[FECHAMENTOS.index(caractere)]
            if pilha.is_empty():
                return ResultadoVerificacao(
                    False, posicao, f"'{caractere}' fecha um símbolo que nunca foi aberto")
            abertura, posicao_abertura = pilha.pop()
            if passos is not None:
                passos.append(f"pos {posicao:>2}: '{caractere}' -> pop '{abertura}' pilha: {_mostrar(pilha)}")
            if abertura != esperado:
                fechamento_correto = FECHAMENTOS[ABERTURAS.index(abertura)]
                return ResultadoVerificacao(
                    False, posicao,
                    f"esperava '{fechamento_correto}' para fechar o '{abertura}' da posição "
                    f"{posicao_abertura}, mas encontrou '{caractere}'")

    if aspas_abertas is not None:
        return ResultadoVerificacao(False, posicao_aspas, f"texto entre aspas ({aspas_abertas}) nunca foi fechado")

    if not pilha.is_empty():
        # O primeiro desbalanceamento é a abertura MAIS ANTIGA que ficou sem par,
        # ou seja, a do fundo da pilha.
        sem_par = pilha.size()
        while pilha.size() > 1:
            pilha.pop()
        abertura, posicao_abertura = pilha.pop()
        extra = f" ({sem_par} símbolos ficaram sem fechamento)" if sem_par > 1 else ""
        return ResultadoVerificacao(
            False, posicao_abertura, f"o '{abertura}' aberto aqui nunca foi fechado{extra}")

    return ResultadoVerificacao(True)


def _mostrar(pilha: Pilha) -> str:
    """Conteúdo da pilha da base para o topo, só com os símbolos."""
    simbolos = [simbolo for simbolo, _ in pilha]   # a iteração vai do topo para a base
    simbolos.reverse()
    return "[" + " ".join(simbolos) + "]" if simbolos else "[] (vazia)"


def apontar(expressao: str, posicao: int, recuo: int) -> str:
    """Linha com um ^ embaixo do caractere da posição informada."""
    return " " * (recuo + posicao - 1) + "^"


# ---------------------------------------------------------------------- testes da demonstração
EXPRESSOES_DE_TESTE = [
    # (expressão, ignorar_strings)
    ("{ [ ( ) ] }", False),                       # exemplos do enunciado
    ("( [ ) ]", False),
    ("((()))", False),
    ("([)]", False),
    ("(a + b) * [c - d] / {e + f}", False),      # expressões matemáticas
    ("{[(x + y) * 2] - (z / 3)}", False),
    ("((a + b) * c", False),
    ("a + b) * (c", False),
    ("{[}]", False),
    ("", False),
    ("if (v[i] > 0) { soma += v[i]; }", False),  # trechos de código
    ('print("sorriso :)")', False),
    ('print("sorriso :)")', True),
]


def executar_demonstracao() -> None:
    cabecalho("SP04 - Verificação de parênteses, colchetes e chaves (Pilha)")

    secao("Pilha passo a passo para  { [ ( ) ] }")
    passos = []
    verificar_expressao("{ [ ( ) ] }", passos=passos)
    for passo in passos:
        print("  " + passo)
    print("  fim: pilha vazia -> expressão balanceada")

    secao("Testes")
    validas = invalidas = 0
    for expressao, ignorar in EXPRESSOES_DE_TESTE:
        resultado = verificar_expressao(expressao, ignorar_strings=ignorar)
        rotulo = "(ignorando texto entre aspas)" if ignorar else ""
        mostrada = expressao if expressao else "(vazia)"
        if resultado.balanceada:
            validas += 1
            print(f"  VÁLIDA    {mostrada}  {rotulo}".rstrip())
        else:
            invalidas += 1
            print(f"  INVÁLIDA  {mostrada}  {rotulo}".rstrip())
            print(apontar(expressao, resultado.posicao, recuo=12))
            print(f"            posição {resultado.posicao}: {resultado.mensagem}")
    print(f"\n{validas} válidas e {invalidas} inválidas de {len(EXPRESSOES_DE_TESTE)} expressões testadas.")


def modo_interativo() -> None:
    print("\nDigite expressões para verificar (linha vazia para sair).")
    while True:
        try:
            expressao = input("expressão> ")
        except EOFError:
            break
        if not expressao:
            break
        resultado = verificar_expressao(expressao, ignorar_strings=True)
        if resultado.balanceada:
            print("  OK: balanceada")
        else:
            print(apontar(expressao, resultado.posicao, recuo=11))
            print(f"  ERRO na posição {resultado.posicao}: {resultado.mensagem}")


if __name__ == "__main__":
    configurar_terminal()
    executar_demonstracao()
    if "-i" in sys.argv[1:]:
        modo_interativo()
