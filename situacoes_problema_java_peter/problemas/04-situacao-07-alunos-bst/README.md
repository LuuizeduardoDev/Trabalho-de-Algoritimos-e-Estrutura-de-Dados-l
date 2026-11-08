# Problema 4 — Cadastro e Busca de Alunos por Matrícula

## Estrutura utilizada

O cadastro usa uma Árvore Binária de Busca (BST) implementada manualmente em `ArvoreAlunos`.
Cada nó armazena matrícula, nome e curso. Matrículas menores ficam na subárvore esquerda
e matrículas maiores ficam na subárvore direita.

## Decisões para pontos não especificados

- Matrículas duplicadas não são inseridas; `inserir` retorna `false`.
- Busca ou remoção de matrícula inexistente retornam `null` ou `false`, respectivamente.
- A matrícula é representada por um número inteiro positivo.
- A classe `Problema4` usa dados fixos para demonstrar o funcionamento, incluindo 20 alunos.

## Compilação e execução

Na pasta `problema4`, execute:

```text
javac -d bin *.java
java -cp bin Problema4
java -cp bin TesteArvoreAlunos
```

## Exemplo de saída

```text
=== Cadastro concluido ===
Total de alunos: 20

=== Buscas ===
Aluno encontrado: Matricula: 202315 | Nome: Carla Mendes | Curso: Ciencia da Computacao
Matricula 202399 nao encontrada.

=== Remocoes ===
Matricula 202305 removida com sucesso.
Nao foi possivel remover: matricula 202399 inexistente.
```

O percurso em ordem imprime as matrículas em ordem crescente, antes e depois da remoção.

## Complexidade

- Inserção e busca: `O(h)`, onde `h` é a altura da árvore.
- Remoção: `O(h)`.
- Percurso em ordem: `O(n)`.
- Espaço adicional das operações: `O(h)` devido à estrutura da árvore e à recursão da remoção.
