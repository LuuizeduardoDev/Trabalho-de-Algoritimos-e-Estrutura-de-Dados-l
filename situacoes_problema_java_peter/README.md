# Trabalho de Algoritmos e Estruturas de Dados I

Projeto acadêmico em Java com 12 problemas independentes de algoritmos e estruturas de dados. Cada problema possui uma implementação, uma demonstração e testes automatizados.

## Problemas implementados

| Nº | Situação | Tema | Estrutura ou algoritmo principal |
|---:|---:|---|---|
| 1 | 01 | Atendimento de uma clínica médica | Fila FIFO manual |
| 2 | 03 | Desfazer ações em um editor de texto | Pilha LIFO manual |
| 3 | 05 | Gerenciamento de playlist | Lista simplesmente encadeada |
| 4 | 07 | Cadastro e busca de alunos | Árvore Binária de Busca (BST) |
| 5 | 09 | Índice de CPF para um sistema de RH | Árvore AVL |
| 6 | 11 | Roteamento de entregas | Grafo ponderado e Dijkstra |
| 7 | 14 | Frequência de palavras | Tabela hash com encadeamento |
| 8 | 15 | Ordenação de notas | Bubble Sort, Selection Sort e Insertion Sort |
| 9 | 17 | Seleção de candidatos | Selection Sort |
| 10 | 19 | Inserção ordenada de cartas | Insertion Sort |
| 11 | 21 | Ordenação de transações bancárias | Merge Sort |
| 12 | 24 | Classificação de atletas | Quick Sort |

As estruturas solicitadas são implementadas manualmente, sem o uso de implementações prontas como `Stack`, `Queue`, `LinkedList`, `HashMap`, `TreeMap` ou `TreeSet`.

## Tecnologias

- Java 17;
- `javac` para compilação;
- classes da biblioteca padrão do Java, quando necessárias;
- PowerShell nos comandos de execução da raiz do projeto.

Não há dependências externas, gerenciador de pacotes ou variáveis de ambiente obrigatórias.

## Pré-requisitos

- JDK 17 ou versão compatível instalada;
- terminal aberto na raiz do projeto.

A versão utilizada nos testes do projeto é o OpenJDK Temurin 17.0.20.

## Instalação e compilação

Na raiz do projeto, execute:

```powershell
New-Item -ItemType Directory -Force out | Out-Null
javac -encoding UTF-8 -d out Main.java (Get-ChildItem -Recurse -Filter *.java | Where-Object { $_.Name -ne 'Main.java' }).FullName
```

Os arquivos compilados são gerados no diretório `out/`.

## Como executar

### Menu interativo

```powershell
java -cp out Main
```

Opções disponíveis:

| Opção | Ação |
|---:|---|
| 1 a 12 | Executa a demonstração do problema escolhido |
| 13 | Executa os testes automatizados dos 12 problemas |
| 14 | Executa todas as demonstrações |
| 0 | Encerra o programa |

### Execução direta

Também é possível executar uma opção sem abrir o menu:

```powershell
java -cp out Main 5
java -cp out Main testes
java -cp out Main demonstracoes
```

O primeiro comando executa a demonstração do problema 5. Os demais executam todos os testes ou todas as demonstrações, respectivamente.

## Testes

Para executar todos os testes:

```powershell
java -cp out Main testes
```

Uma execução aprovada termina com um resumo semelhante a:

```text
Resumo: 12 de 12 conjuntos de testes executados sem falha.
```

Cada diretório de problema também contém uma classe de teste independente e um `README.md` com detalhes específicos da implementação.

## Estrutura do projeto

```text
.
├── Main.java                              # Menu, demonstrações e testes centralizados
├── especificacao-requisitos-12-projetos-java.md
├── problemas/
│   ├── 01-situacao-01-clinica/
│   ├── 02-situacao-03-editor-undo/
│   ├── ...
│   └── 12-situacao-24-atletas-quick/
└── out/                                   # Arquivos gerados pela compilação
```


