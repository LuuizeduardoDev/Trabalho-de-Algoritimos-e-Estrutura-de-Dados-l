# Problema 5 — Índice de CPF para Sistema de RH

Implementação de uma árvore AVL manual para indexar funcionários pelo CPF.

## Arquivos

- `Funcionario.java`: dados do funcionário e validação do CPF;
- `ArvoreAVL.java`: inserção, busca, remoção, rotações, altura e fatores de balanceamento;
- `SistemaRH.java`: demonstração com 25 funcionários, buscas, remoções e erros;
- `TesteArvoreAVL.java`: testes executáveis das rotações, operações e casos inválidos.

## Compilação e execução

Na pasta `problema5`:

```bash
javac -d bin *.java
java -cp bin SistemaRH
java -cp bin TesteArvoreAVL
```

## Exemplo de saída

```text
Funcionarios cadastrados: 25
Altura da arvore: 5
Fator da raiz: 0
Arvore balanceada? true
CPF 10000000013 encontrado
CPF 99999999999 nao encontrado
CPF 10000000010 removido.
Balanceada apos a operacao? true
```

Os dados de entrada são definidos no próprio `SistemaRH`, pois a especificação não exige uma interface de leitura.

## Decisões para pontos não especificados

- O CPF é armazenado como texto com exatamente 11 dígitos, sem pontuação.
- CPF duplicado é rejeitado com `IllegalArgumentException`.
- Busca de CPF inexistente retorna `null`; remoção inexistente retorna `false`.
- A altura de uma árvore vazia é 0 e a de uma folha é 1.
- A demonstração remove dois funcionários existentes e tenta remover um CPF inexistente.

## Justificativa e complexidade

A AVL foi escolhida porque mantém a diferença entre as alturas das subárvores em no máximo 1. As rotações simples e duplas preservam a busca binária e mantêm a altura em `O(log n)` no pior caso. Inserção, busca e remoção custam `O(log n)`. A verificação completa de balanceamento e a listagem em ordem custam `O(n)`, e a árvore utiliza `O(n)` espaço.
