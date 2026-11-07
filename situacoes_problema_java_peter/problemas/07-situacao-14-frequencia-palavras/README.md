## Problema 7 — Contagem de Frequência de Palavras em um Texto

O projeto processa o preâmbulo da Constituição da República Federativa do Brasil,
conta a frequência das palavras
e exibe as dez palavras mais frequentes e o total de palavras distintas.

### Estrutura

- `TabelaHash.java`: tabela hash manual com encadeamento para tratar colisões;
- `PalavraFrequencia.java`: representa um par palavra–contagem;
- `ContadorPalavras.java`: extrai palavras e ordena o resultado para a apresentação;
- `Problema7.java`: demonstração com um texto real (preâmbulo da Constituição);
- `TesteTabelaHash.java`: testes de contagem, colisão e casos de erro.

Não são utilizadas `HashMap`, `Hashtable` ou outra tabela hash pronta.

### Decisões para pontos não especificados

- palavras são convertidas para minúsculas, mas os acentos são preservados;
- pontuação é ignorada;
- palavras com hífen são mantidas como uma única palavra;
- são apresentadas as dez palavras mais frequentes;
- em caso de empate, as palavras são apresentadas em ordem alfabética;
- texto nulo, palavra nula/vazia, capacidade inválida e limite negativo são rejeitados;
- texto sem palavras resulta em zero palavras distintas e zero ocorrências.

### Compilação e execução

Na pasta `problema7`:

```bash
javac -encoding UTF-8 -d bin *.java
java -cp bin Problema7
java -cp bin TesteTabelaHash
```

### Exemplo de saída

```text
Palavras mais frequentes:
- a: 8
- e: 5
...
Total de palavras distintas: 64
```

Os valores exatos são produzidos pelo programa a partir do texto constante em
`Problema7.java`.

### Complexidade

- inserção e busca: O(1) em média e O(n) no pior caso;
- contagem do texto: O(t) em média, onde `t` é o número de palavras;
- listagem das palavras distintas: O(n), onde `n` é a quantidade de palavras distintas;
- ordenação das frequências para apresentação: O(n²), usando ordenação por inserção;
- espaço da tabela: O(n + m), onde `m` é a capacidade da tabela.
