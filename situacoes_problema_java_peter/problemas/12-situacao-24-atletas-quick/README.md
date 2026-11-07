# Problema 12 — Classificação de Resultados de uma Competição Esportiva

## Decisão adotada

A especificação permite usar tempo ou pontuação e não define qual direção é melhor. Foi escolhida uma corrida por tempo: o menor tempo representa a melhor colocação. Em caso de empate, o nome é usado como segundo critério, em ordem alfabética, para deixar a classificação determinística. Essa é uma decisão de implementação, não um novo requisito oficial.

## Implementação

- `Atleta`: registro com nome e tempo em segundos, validando nome não vazio e tempo finito não negativo.
- `QuickSortAtletas`: Quick Sort manual, com pivô no elemento central, particionamento por dois índices e chamadas recursivas.
- `Problema12`: demonstração com 30 atletas, classificação final e pódio.
- `TesteQuickSortAtletas`: testes de ordenação, empate, vetor vazio, entradas inválidas e pódio com menos de três atletas.

Não são utilizadas estruturas prontas de ordenação. O vetor de `Atleta` é ordenado no próprio lugar.

Complexidade média do Quick Sort: O(n log n) em tempo e O(log n) de espaço de pilha. No pior caso, o tempo pode ser O(n²) e a pilha pode chegar a O(n).

## Compilação e execução

No diretório `problema12`:

```text
javac -d out *.java
java -cp out Problema12
java -cp out TesteQuickSortAtletas
```

A execução de `Problema12` imprime a classificação completa de 30 atletas e os três primeiros colocados. Com os dados fornecidos, Paulo, Ursula e Davi formam o pódio, de acordo com os menores tempos.

Exemplo resumido de saída:

```text
Classificacao final:
 1o lugar - Paulo - 57.84 s
 2o lugar - Ursula - 58.41 s
 3o lugar - Davi - 58.75 s
...
30o lugar - Tiago - 68.02 s

Podio:
1o lugar - Paulo - 57.84 s
2o lugar - Ursula - 58.41 s
3o lugar - Davi - 58.75 s
```
