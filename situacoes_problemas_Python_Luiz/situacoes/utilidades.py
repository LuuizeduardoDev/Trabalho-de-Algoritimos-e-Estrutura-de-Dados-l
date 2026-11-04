"""Funções auxiliares das demonstrações: formatação de saída e normalização de texto.

Nada aqui implementa estrutura de dados; são apenas utilitários de exibição.
"""

from __future__ import annotations

import unicodedata

LARGURA = 78


def cabecalho(titulo: str) -> None:
    """Título principal de uma demonstração."""
    print()
    print("=" * LARGURA)
    print(titulo)
    print("=" * LARGURA)


def secao(titulo: str) -> None:
    """Subtítulo dentro de uma demonstração."""
    print()
    print(f"--- {titulo} " + "-" * max(3, LARGURA - len(titulo) - 5))


def numero(valor, casas: int = 0) -> str:
    """Número no padrão brasileiro: 12.345,67."""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def moeda(valor: float) -> str:
    """Valor em reais: R$ 1.234,56."""
    return "R$ " + numero(valor, 2)


def normalizar_texto(texto: str) -> str:
    """Minúsculas e sem acentos ("Café" -> "cafe"), para buscas e ordenação alfabética."""
    decomposto = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def imprimir_tabela(cabecalhos, linhas, alinhamento: str = None) -> None:
    """Imprime uma tabela de texto simples.

    alinhamento: uma letra por coluna, "<" (esquerda) ou ">" (direita).
    """
    colunas = len(cabecalhos)
    if alinhamento is None:
        alinhamento = "<" * colunas
    textos = [[str(celula) for celula in linha] for linha in linhas]
    larguras = [len(str(c)) for c in cabecalhos]
    for linha in textos:
        for i, celula in enumerate(linha):
            larguras[i] = max(larguras[i], len(celula))

    def montar(celulas):
        partes = [f"{celula:{alinhamento[i]}{larguras[i]}}" for i, celula in enumerate(celulas)]
        return "  ".join(partes).rstrip()

    print(montar([str(c) for c in cabecalhos]))
    print("  ".join("-" * largura for largura in larguras))
    for linha in textos:
        print(montar(linha))
