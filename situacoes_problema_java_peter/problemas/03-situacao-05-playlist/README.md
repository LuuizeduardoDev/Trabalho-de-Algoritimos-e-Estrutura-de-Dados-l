## Problema 3 — Gerenciamento de Playlist de Musicas

O projeto implementa uma playlist com uma lista simplesmente encadeada manual.
Cada no armazena uma musica com titulo, artista e duracao em segundos.

### Operacoes implementadas

- insercao no inicio, no final e em qualquer posicao;
- remocao da primeira ocorrencia de um titulo, ignorando maiusculas e minusculas;
- listagem da playlist;
- busca por trecho do titulo ou do artista;
- reordenacao alfabetica pelo titulo.

As posicoes sao baseadas em zero. A busca e textual e nao diferencia maiusculas de
minusculas. Essas escolhas foram adotadas porque a especificacao nao define esses
detalhes.

### Compilacao e execucao

Na pasta `problema3`:

```bash
javac -d bin *.java
java -cp bin TestePlaylist
java -cp bin PlaylistApp
```

### Complexidade

- insercao no inicio e no final: O(1);
- insercao em uma posicao: O(n) no pior caso;
- remocao por titulo e busca: O(n);
- listagem: O(n);
- reordenacao por insercao dos nos: O(n²) no pior caso;
- espaco adicional da playlist: O(n).
