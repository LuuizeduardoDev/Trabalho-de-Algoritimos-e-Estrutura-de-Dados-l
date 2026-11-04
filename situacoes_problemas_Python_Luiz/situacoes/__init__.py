"""Situações-problema (SPs) do trabalho.

Cada módulo tem a função executar_demonstracao() e, alguns, modo_interativo().
Para incluir as SPs do Peter no menu, basta acrescentar uma linha em SITUACOES.
"""

SITUACOES = [
    # (código, título, estrutura ou algoritmo, módulo)
    ("SP02", "Fila de impressão do laboratório", "Fila", "situacoes.sp02_fila_impressao"),
    ("SP04", "Verificação de (), [] e {}", "Pilha", "situacoes.sp04_verificador_expressoes"),
    ("SP06", "Controle de estoque da loja", "Lista encadeada", "situacoes.sp06_controle_estoque"),
    ("SP08", "Autocomplete de produtos", "Árvore BST", "situacoes.sp08_autocomplete"),
    ("SP10", "Ranking de jogadores", "Árvore AVL", "situacoes.sp10_ranking_jogadores"),
    ("SP12", "Rede de amizades", "Grafo + BFS", "situacoes.sp12_rede_social"),
    ("SP13", "Cadastro e login de usuários", "Tabela hash", "situacoes.sp13_login_usuarios"),
    ("SP16", "Vitrine ordenada por preço", "Bubble Sort", "situacoes.sp16_vitrine_bubble"),
    ("SP18", "Tarefas por prioridade", "Selection Sort", "situacoes.sp18_tarefas_selection"),
    ("SP20", "Ranking de vendedores", "Insertion Sort", "situacoes.sp20_vendedores_insertion"),
    ("SP22", "Mesclagem de contatos", "Merge (intercalação)", "situacoes.sp22_contatos_merge"),
    ("SP23", "Catálogo de e-commerce", "Quick Sort", "situacoes.sp23_catalogo_quick"),
]
