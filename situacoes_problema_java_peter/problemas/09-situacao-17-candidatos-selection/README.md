# Problema 9 — Seleção dos melhores candidatos

O programa ordena candidatos pela pontuação da prova usando **Selection Sort** e, depois, extrai o Top-N.

## Decisões para pontos não especificados

- A pontuação foi representada por `double`, permitindo notas inteiras ou decimais.
- A ordem é decrescente: a maior pontuação ocupa a primeira posição.
- Em caso de empate, o nome é usado em ordem alfabética apenas para tornar o resultado determinístico.
- O exemplo utiliza `N = 5`; o programa aceita outro valor inteiro como primeiro argumento.

## Compilação e execução

No diretório `problema9`, execute:

```text
javac -encoding UTF-8 -d out *.java
java -cp out Problema9
java -cp out Problema9 3
java -cp out TesteSelecaoCandidatos
```

O exemplo contém 15 candidatos, incluindo pontuações empatadas. `N` deve estar entre 1 e 15.

## Complexidade

O Selection Sort realiza `O(n²)` comparações e usa `O(1)` espaço auxiliar, além do vetor de entrada. A extração do Top-N percorre `N` posições e usa `O(N)` espaço para o novo vetor.
