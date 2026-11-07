# Problema 11 — Ordenação de histórico de transações bancárias

O programa ordena um histórico de transações usando **Merge Sort**, em ordem cronológica crescente. Cada transação possui data e hora, valor e descrição.

## Decisões para pontos não especificados

- A data e hora usam `LocalDateTime` no formato `yyyy-MM-dd HH:mm:ss`.
- A ordenação é crescente, da transação mais antiga para a mais recente.
- Transações no mesmo segundo permanecem na ordem em que foram registradas.
- Listas vazias, transações nulas e dados de transação inválidos geram `IllegalArgumentException`.
- O valor é armazenado como `double`, suficiente para a demonstração acadêmica solicitada.

## Compilação e execução

No diretório `problema11`, execute:

```text
javac -encoding UTF-8 -d out *.java
java -cp out Problema11
java -cp out TesteMergeSortTransacoes
```

O programa demonstrativo gera 50 transações e inclui duas transações no mesmo segundo para evidenciar a estabilidade.

## Complexidade

O Merge Sort possui complexidade de tempo `O(n log n)` e usa `O(n)` de espaço auxiliar. A divisão do vetor é recursiva e a intercalação escolhe primeiro o elemento da metade esquerda em caso de empate, preservando a estabilidade.
