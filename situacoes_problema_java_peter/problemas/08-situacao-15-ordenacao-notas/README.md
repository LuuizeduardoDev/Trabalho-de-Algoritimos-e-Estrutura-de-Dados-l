## Problema 8 — Ordenação de Notas de uma Turma Pequena

O projeto ordena registros de aluno e nota usando Bubble Sort otimizado. A
ordenação é crescente pela nota; em caso de empate, o nome do aluno é usado
como critério secundário para deixar o resultado determinístico.

### Estrutura

- `NotaAluno.java`: registro de um aluno e sua nota;
- `EstatisticasOrdenacao.java`: contagem de comparações e trocas;
- `BubbleSortNotas.java`: Bubble Sort com parada antecipada quando uma passagem
  não realiza trocas;
- `SelectionSortNotas.java` e `InsertionSortNotas.java`: algoritmos de
  referência para a comparação solicitada;
- `Problema8.java`: demonstração com oito alunos;
- `TesteOrdenacaoNotas.java`: testes normais, parada antecipada e casos de erro.

### Decisões para pontos não especificados

- As notas são ordenadas em ordem crescente.
- A nota válida está no intervalo de 0 a 10.
- A turma aceita de zero a 30 alunos; o vetor vazio é válido.
- Empates de nota são resolvidos pelo nome do aluno, ignorando diferença entre
  maiúsculas e minúsculas.
- A comparação utiliza Selection Sort e Insertion Sort, escolhidos por serem
  algoritmos simples e estudados junto com Bubble Sort. No Insertion Sort foram
  usadas trocas adjacentes para manter a contagem de trocas diretamente
  comparável.

### Compilação e execução

Na pasta `problema8`:

```bash
javac -encoding UTF-8 -d out *.java
java -cp out Problema8
java -cp out TesteOrdenacaoNotas
```

### Complexidade

- Bubble Sort otimizado: O(n²) no pior caso, O(n) no melhor caso; espaço O(1).
- Selection Sort: O(n²) em qualquer caso; espaço O(1).
- Insertion Sort: O(n²) no pior caso e O(n) no melhor caso; espaço O(1).

As contagens são de comparações entre registros e trocas físicas de posições.
