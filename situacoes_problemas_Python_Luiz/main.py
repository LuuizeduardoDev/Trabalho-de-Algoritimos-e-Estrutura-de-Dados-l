"""Main principal: executa todas as situações-problema de uma vez.

Como rodar (na pasta raiz do projeto, onde está este arquivo):
    python main.py

Cada situação-problema é executada dentro da própria pasta, do mesmo jeito
que seria rodando o arquivo principal sozinho. Isso evita conflito entre
módulos com o mesmo nome em pastas diferentes (utilidades.py, tabela_hash.py,
merge_sort.py...).
"""

import subprocess
import sys
from pathlib import Path

PASTA_SRC = Path(__file__).resolve().parent / "src"

# (pasta, arquivo principal), na ordem das situações-problema
PROBLEMAS = [
    ("problema_02", "fila_impressao.py"),
    ("problema_04", "verificador_expressoes.py"),
    ("problema_06", "controle_estoque.py"),
    ("problema_08", "autocomplete_produtos.py"),
    ("problema_10", "ranking_jogadores.py"),
    ("problema_12", "rede_social.py"),
    ("problema_13", "login_usuarios.py"),
    ("problema_16", "vitrine_produtos.py"),
    ("problema_18", "tarefas_prioridade.py"),
    ("problema_20", "ranking_vendedores.py"),
    ("problema_22", "mesclagem_contatos.py"),
    ("problema_23", "catalogo_ecommerce.py"),
]


def main() -> int:
    falhas = []

    for pasta, arquivo in PROBLEMAS:
        print()
        print("#" * 80)
        print("#  EXECUTANDO " + pasta + "/" + arquivo)
        print("#" * 80)
        sys.stdout.flush()

        resultado = subprocess.run(
            [sys.executable, arquivo],
            cwd=str(PASTA_SRC / pasta),
        )
        if resultado.returncode != 0:
            falhas.append(pasta)

    print()
    print("=" * 80)
    total = len(PROBLEMAS)
    print("Situações-problema executadas: " + str(total - len(falhas)) + " de " + str(total) + " sem erro.")
    if falhas:
        print("Com erro: " + ", ".join(falhas))
    print("=" * 80)
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
