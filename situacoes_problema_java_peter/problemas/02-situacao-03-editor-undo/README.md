## Problema 2 — Sistema de Desfazer (Undo)

O projeto implementa um editor de texto simples com uma pilha encadeada manual
de acoes. A pilha segue o comportamento LIFO: a acao mais recente e desfeita
primeiro.

### Operacoes implementadas

- digitacao no final do texto;
- exclusao de um intervalo `[inicio, fim)`;
- formatacao para texto normal, maiusculas ou minusculas;
- desfazer com restauracao do estado anterior completo;
- tratamento de historico vazio e entradas invalidas.

Cada `Acao` armazena seu tipo, uma descricao, o estado anterior e o estado
posterior. O `redo` nao foi implementado porque e opcional na especificacao.

Como a especificacao nao define o modelo do editor nem as formatacoes, foram
escolhidas as operacoes mais simples: a digitacao ocorre no final e a
formatacao altera o texto inteiro. Essas escolhas sao apenas decisoes de
implementacao para a simulacao.

### Compilacao e execucao

Na pasta `problema2`:

```bash
javac -d bin *.java
java -cp bin TesteEditorTexto
java -cp bin Problema2
```

`Problema2` executa 12 acoes, imprime o estado apos cada uma e desfaz todas
passo a passo. `TesteEditorTexto` verifica a pilha LIFO, as tres operacoes do
editor e os casos de erro.

Exemplo de trecho da saida:

```text
12. texto=" mundo bem-vindo ao editor!", formato=MINUSCULAS
Desfeito -> texto=" MUNDO BEM-VINDO AO EDITOR!", formato=MAIUSCULAS
...
Desfeito -> texto="", formato=NORMAL
Sem mais acoes para desfazer: true
```

### Complexidade

- `push`, `pop` e `desfazer`: O(1), sem contar a copia do texto feita pela operacao;
- digitacao e exclusao: O(n), pois criam o novo texto;
- formatacao: O(n), pois percorre o texto;
- espaco do historico: O(k + tamanho dos estados armazenados), para `k` acoes.
