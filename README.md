# Trabalho de Algoritmos e Estruturas de Dados I

Trabalho prático da disciplina do professor Hilson Silva, no semestre 2026/2. O repositório reúne 24 situações-problema que aplicam estruturas de dados, buscas em grafos e algoritmos de ordenação a cenários como atendimento em clínicas, controle de estoque e classificação de atletas.

Peter Vinicios implementou 12 situações em Java e Luiz Eduardo implementou as outras 12 em Python. Cada situação tem uma demonstração e testes automatizados. As estruturas e os algoritmos estudados foram implementados manualmente, com apoio das bibliotecas padrão das duas linguagens.

## Situações-problema

| Nº no enunciado | Situação-problema | Estrutura ou algoritmo principal | Implementação |
| ---: | --- | --- | --- |
| 01 | Atendimento em clínica médica | Fila FIFO | Java |
| 02 | Fila de impressão do laboratório | Fila FIFO | Python |
| 03 | Desfazer ações em um editor de texto | Pilha LIFO | Java |
| 04 | Verificação de parênteses, colchetes e chaves | Pilha LIFO | Python |
| 05 | Gerenciamento de playlist | Lista simplesmente encadeada | Java |
| 06 | Controle de estoque | Lista encadeada | Python |
| 07 | Cadastro e busca de alunos | Árvore binária de busca (BST) | Java |
| 08 | Autocompletar nomes de produtos | Árvore binária de busca (BST) | Python |
| 09 | Índice de CPF para um sistema de RH | Árvore AVL | Java |
| 10 | Ranking de jogadores | Árvore AVL e tabela hash | Python |
| 11 | Roteamento de entregas | Grafo ponderado e algoritmo de Dijkstra | Java |
| 12 | Rede de amizades | Grafo e busca em largura (BFS) | Python |
| 13 | Cadastro e login de usuários | Tabela hash | Python |
| 14 | Frequência de palavras | Tabela hash com encadeamento | Java |
| 15 | Ordenação de notas | Bubble Sort, Selection Sort e Insertion Sort | Java |
| 16 | Vitrine de produtos ordenada por preço | Bubble Sort | Python |
| 17 | Seleção de candidatos | Selection Sort | Java |
| 18 | Ordenação de tarefas por prioridade | Selection Sort | Python |
| 19 | Inserção ordenada de cartas | Insertion Sort | Java |
| 20 | Ranking de vendedores | Insertion Sort | Python |
| 21 | Ordenação de transações bancárias | Merge Sort | Java |
| 22 | Mesclagem de listas de contatos | Intercalação (merge) | Python |
| 23 | Catálogo de comércio eletrônico | Comparação entre Quick Sort e Merge Sort | Python |
| 24 | Classificação de atletas | Quick Sort | Java |

## Como executar

Os exemplos de cada linguagem partem da raiz do repositório. O projeto usa apenas as bibliotecas padrão do Java e do Python.

### Java

Com o JDK 17 instalado, compile os arquivos e abra o menu pelo PowerShell.

```powershell
cd situacoes_problema_java_peter
New-Item -ItemType Directory -Force out | Out-Null
javac -encoding UTF-8 -d out Main.java (Get-ChildItem -Path problemas -Recurse -File -Filter *.java).FullName
java -cp out Main
```

No menu, as opções `1` a `12` executam uma demonstração, `13` roda os testes, `14` executa todas as demonstrações e `0` encerra. As opções `1` a `12` correspondem ao primeiro número no nome das pastas em `problemas/`. Por exemplo, a opção `5` abre a situação `09` do enunciado, sobre o índice de CPF.

Na pasta `situacoes_problema_java_peter`, também é possível executar diretamente a demonstração do exemplo, todas as demonstrações ou os 12 conjuntos de testes.

```powershell
java -cp out Main 5
java -cp out Main demonstracoes
java -cp out Main testes
```

### Python

Com o Python 3.7 ou superior instalado, execute todas as demonstrações com o comando abaixo. No Linux e no macOS, use `python3` se esse for o nome do comando instalado.

```bash
python situacoes_problemas_Python_Luiz/main.py
```

Para rodar uma demonstração individual e seus testes, use a pasta da situação. O exemplo abaixo usa a fila de impressão.

```bash
cd situacoes_problemas_Python_Luiz/src/problema_02
python fila_impressao.py
python -m unittest -v
```

Para rodar os 87 testes da parte em Python, execute `python -m unittest -v` em cada uma das 12 pastas em `src/`.

As situações `04`, `08` e `13` também aceitam `-i` para abrir o modo interativo. Na pasta da situação `04`, por exemplo, execute `python verificador_expressoes.py -i`.
