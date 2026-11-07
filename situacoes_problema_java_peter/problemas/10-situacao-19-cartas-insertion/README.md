# Problema 10 — Inserção de novas cartas em uma mão ordenada

O programa insere cada carta assim que ela é recebida, deslocando as cartas
maiores para abrir espaço na posição correta. A mão permanece ordenada após
cada operação.

## Decisões para pontos não especificados

- A ordem escolhida é crescente, pois a especificação não define crescente ou decrescente.
- Cada carta possui somente um valor, pois naipe e identificador não foram exigidos.
- Cartas com o mesmo valor são mantidas na ordem de chegada.
- Valores inteiros não são limitados a uma faixa, pois a especificação não define os valores válidos.
- A demonstração usa 12 cartas, dentro do intervalo exigido de 10 a 13 cartas.

## Compilação e execução

No diretório `problema10`, execute:

```text
javac -encoding UTF-8 -d out *.java
java -cp out Problema10
java -cp out TesteMaoCartas
```

Exemplo resumido de saída:

```text
Recebida Carta(8) -> mao: [8]
Recebida Carta(3) -> mao: [3, 8]
Recebida Carta(5) -> mao: [3, 5, 8]
...
Recebida Carta(4) -> mao: [1, 2, 3, 4, 5, 5, 7, 8, 9, 10, 12, 13]
```

## Complexidade

Cada inserção pode deslocar todas as cartas da mão, portanto custa `O(n)` no
pior caso. Para `n` cartas recebidas, a sequência completa custa `O(n²)` no
pior caso. O vetor interno usa `O(n)` espaço.
