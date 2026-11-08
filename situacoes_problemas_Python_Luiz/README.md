## Situações-problema em Python – Luiz Eduardo

Parte de Luiz Eduardo no Trabalho Prático de Algoritmos e Estrutura de Dados I (Prof. Hilson Silva, 2026-2):
as situações-problema 02, 04, 06, 08, 10, 12, 13, 16, 18, 20, 22 e 23.

## Tecnologias Utilizadas

* **Python 3** (versão 3.7 ou mais nova; testado nas versões 3.11, 3.12 e 3.13)
* Apenas a biblioteca padrão do Python: não é preciso instalar nada.

## Sobre o Projeto

Cada situação-problema fica em uma pasta própria dentro de `src/` e roda sozinha: a pasta tem o arquivo
principal, as estruturas ou algoritmos que ele usa e um arquivo de testes (`test_*.py`).

Todas as estruturas e todos os algoritmos foram implementados do zero. Não usamos `collections.deque`,
`heapq`, `sorted()`/`list.sort()` nem `dict` no lugar das estruturas estudadas. A lista nativa do Python
serve apenas como vetor base, como o enunciado permite (item 5.4).

| Pasta | Situação-problema | Estrutura / algoritmo | Arquivo principal |
|---|---|---|---|
| `src/problema_02` | Fila de impressão do laboratório | Fila | `fila_impressao.py` |
| `src/problema_04` | Verificação de (), [] e {} | Pilha | `verificador_expressoes.py` |
| `src/problema_06` | Controle de estoque | Lista encadeada | `controle_estoque.py` |
| `src/problema_08` | Autocomplete de produtos | Árvore BST | `autocomplete_produtos.py` |
| `src/problema_10` | Ranking de jogadores | Árvore AVL + tabela hash | `ranking_jogadores.py` |
| `src/problema_12` | Rede de amizades | Grafo + BFS | `rede_social.py` |
| `src/problema_13` | Cadastro e login de usuários | Tabela hash | `login_usuarios.py` |
| `src/problema_16` | Vitrine ordenada por preço | Bubble Sort | `vitrine_produtos.py` |
| `src/problema_18` | Tarefas por prioridade | Selection Sort | `tarefas_prioridade.py` |
| `src/problema_20` | Ranking de vendedores | Insertion Sort | `ranking_vendedores.py` |
| `src/problema_22` | Mesclagem de contatos | Merge (intercalação) | `mesclagem_contatos.py` |
| `src/problema_23` | Catálogo de e-commerce | Quick Sort x Merge Sort | `catalogo_ecommerce.py` |

## Como Executar

1. Abra o terminal na pasta do problema (ex.: `src/problema_02`).
2. Rode o arquivo principal:
   ```bash
   python fila_impressao.py
   ```
3. As SPs 04, 08 e 13 também têm modo interativo: acrescente `-i` no final do comando
   (ex.: `python verificador_expressoes.py -i`).

No Linux e no macOS, use `python3` no lugar de `python`.

## Testes

Cada pasta tem seus próprios testes automatizados (87 no total). Para rodar, abra o terminal na pasta do
problema e digite:

```bash
python -m unittest -v
```

O relatório técnico (justificativa, complexidade e exemplos de entrada e saída de cada SP) é entregue à parte.
