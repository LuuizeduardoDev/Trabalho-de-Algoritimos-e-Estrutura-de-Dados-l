"""Trabalho Prático - Estrutura de Dados I (2026-2) - Prof. Hilson Silva.

Parte de Luiz Eduardo: SP02, SP04, SP06, SP08, SP10, SP12, SP13, SP16, SP18,
SP20, SP22 e SP23.

Como usar:
    python main.py            -> menu
    python main.py sp04       -> demonstração da SP04
    python main.py sp04 -i    -> demonstração + modo interativo (SP04, SP08 e SP13)
    python main.py todas      -> todas as demonstrações em sequência
"""

from __future__ import annotations

import sys
from importlib import import_module

from situacoes import SITUACOES


def _configurar_saida() -> None:
    """Evita erro de acentuação em terminais antigos do Windows."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass


def _encontrar(texto: str):
    """Aceita 'sp4', 'SP04', '4', '04'... e devolve a linha de SITUACOES."""
    digitos = "".join(c for c in texto if c.isdigit())
    if not digitos:
        return None
    codigo = f"SP{int(digitos):02d}"
    for situacao in SITUACOES:
        if situacao[0] == codigo:
            return situacao
    return None


def executar(situacao, interativo: bool = False) -> None:
    codigo, _, _, nome_modulo = situacao
    modulo = import_module(nome_modulo)
    modulo.executar_demonstracao()
    if interativo:
        if hasattr(modulo, "modo_interativo"):
            modulo.modo_interativo()
        else:
            print(f"\n(A {codigo} não tem modo interativo.)")


def executar_todas() -> None:
    for situacao in SITUACOES:
        executar(situacao)


def menu() -> None:
    while True:
        print()
        print("=" * 66)
        print(" TRABALHO PRÁTICO - ESTRUTURA DE DADOS I (2026-2)")
        print(" Parte de Luiz Eduardo - 12 situações-problema")
        print("=" * 66)
        for numero, (codigo, titulo, estrutura, _) in enumerate(SITUACOES, start=1):
            print(f" {numero:>2}) {codigo}  {titulo:<34} {estrutura}")
        print("  T) Rodar todas as demonstrações")
        print("  0) Sair")
        try:
            escolha = input("Escolha: ").strip().lower()
        except EOFError:
            return
        if escolha in ("0", "sair", "s"):
            return
        if escolha == "t":
            executar_todas()
        elif escolha.isdigit() and 1 <= int(escolha) <= len(SITUACOES):
            situacao = SITUACOES[int(escolha) - 1]
            executar(situacao)
            modulo = import_module(situacao[3])
            if hasattr(modulo, "modo_interativo"):
                try:
                    resposta = input("\nTestar no modo interativo? (s/N) ").strip().lower()
                except EOFError:
                    return
                if resposta == "s":
                    modulo.modo_interativo()
        else:
            print("Opção inválida.")
            continue
        try:
            input("\nEnter para voltar ao menu...")
        except EOFError:
            return


def main(argumentos: list) -> int:
    _configurar_saida()
    if not argumentos:
        menu()
        return 0
    if argumentos[0].lower() in ("todas", "todos", "all"):
        executar_todas()
        return 0
    situacao = _encontrar(argumentos[0])
    if situacao is None:
        codigos = ", ".join(s[0] for s in SITUACOES)
        print(f"Situação-problema não encontrada: {argumentos[0]}. Disponíveis: {codigos}")
        return 1
    executar(situacao, interativo="-i" in argumentos[1:])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
