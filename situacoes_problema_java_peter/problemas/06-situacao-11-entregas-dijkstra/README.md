# Problema 6 — Roteamento de entrega de mercadorias

O projeto representa uma cidade como um grafo ponderado e nao direcionado. Os vertices sao pontos de entrega e os pesos das conexoes representam o custo de deslocamento.

## Estrutura

- `GrafoPonderado.java`: lista de adjacencia implementada manualmente com nos encadeados;
- `Dijkstra.java`: algoritmo de Dijkstra para pesos nao negativos;
- `Rota.java`: resultado de uma consulta, com caminho e custo;
- `Problema6.java`: demonstracao com 10 vertices e quatro pares de origem e destino;
- `TesteDijkstra.java`: testes de rotas, vertices desconectados e entradas invalidas.

Nao sao utilizadas `HashMap`, `PriorityQueue` ou outra implementacao pronta de grafo. A busca do menor vertice ainda nao visitado e feita linearmente, mantendo a implementacao didatica.

## Decisoes para pontos nao especificados

- O grafo e nao direcionado: uma conexao pode ser percorrida nos dois sentidos.
- Os pesos sao custos nao negativos; a demonstracao usa valores inteiros, embora a classe aceite `double`.
- Quando nao existe caminho, `Dijkstra.encontrar` devolve uma `Rota` sem caminho, em vez de lancar erro.
- Vertices inexistentes, nomes vazios, pesos negativos e capacidade invalida geram erro.

## Compilacao e execucao

No diretorio `problema6`:

```text
javac -encoding UTF-8 -d out *.java
java -cp out Problema6
java -cp out TesteDijkstra
```

Exemplo de resultado:

```text
Centro de Distribuicao -> Aeroporto: Centro de Distribuicao -> Sul -> Industrial -> Porto -> Aeroporto | custo total: 11.0
```

## Complexidade

Com lista de adjacencia e selecao linear do menor vertice, Dijkstra possui complexidade de tempo `O(V² + E)` e espaco `O(V + E)`, onde `V` e o numero de vertices e `E` o numero de conexoes direcionais armazenadas.
