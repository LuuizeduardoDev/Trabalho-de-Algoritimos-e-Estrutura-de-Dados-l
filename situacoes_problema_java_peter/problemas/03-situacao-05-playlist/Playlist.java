import java.util.Locale;

/**
 * Playlist baseada em uma lista simplesmente encadeada implementada manualmente.
 * As posicoes usadas pela classe sao baseadas em zero.
 */
public class Playlist {
    private static class No {
        private final Musica musica;
        private No proximo;

        private No(Musica musica) {
            this.musica = musica;
        }
    }

    private final String nome;
    private No inicio;
    private No fim;
    private int tamanho;

    public Playlist(String nome) {
        if (nome == null || nome.trim().isEmpty()) {
            throw new IllegalArgumentException("O nome da playlist nao pode ser vazio.");
        }
        this.nome = nome.trim();
    }

    public String getNome() {
        return nome;
    }

    public int tamanho() {
        return tamanho;
    }

    public boolean estaVazia() {
        return tamanho == 0;
    }

    /** Insere uma musica na primeira posicao. */
    public void inserirInicio(Musica musica) {
        validarMusica(musica);
        No novo = new No(musica);
        novo.proximo = inicio;
        inicio = novo;

        if (fim == null) {
            fim = novo;
        }
        tamanho++;
    }

    /** Insere uma musica na ultima posicao. */
    public void inserirFinal(Musica musica) {
        validarMusica(musica);
        No novo = new No(musica);

        if (fim == null) {
            inicio = novo;
            fim = novo;
        } else {
            fim.proximo = novo;
            fim = novo;
        }
        tamanho++;
    }

    /**
     * Insere uma musica na posicao indicada, aceitando tambem inicio e final.
     * A posicao final valida e igual ao tamanho atual.
     */
    public void inserir(Musica musica, int posicao) {
        validarMusica(musica);
        if (posicao < 0 || posicao > tamanho) {
            throw new IndexOutOfBoundsException("Posicao invalida: " + posicao);
        }

        if (posicao == 0) {
            inserirInicio(musica);
            return;
        }
        if (posicao == tamanho) {
            inserirFinal(musica);
            return;
        }

        No anterior = inicio;
        for (int indice = 1; indice < posicao; indice++) {
            anterior = anterior.proximo;
        }

        No novo = new No(musica);
        novo.proximo = anterior.proximo;
        anterior.proximo = novo;
        tamanho++;
    }

    /** Remove a primeira musica cujo titulo coincide, ignorando maiusculas. */
    public boolean removerPorTitulo(String titulo) {
        validarTexto(titulo, "O titulo para remocao nao pode ser vazio.");

        No anterior = null;
        No atual = inicio;
        while (atual != null) {
            if (atual.musica.getTitulo().equalsIgnoreCase(titulo.trim())) {
                if (anterior == null) {
                    inicio = atual.proximo;
                } else {
                    anterior.proximo = atual.proximo;
                }

                if (atual == fim) {
                    fim = anterior;
                }
                tamanho--;
                return true;
            }
            anterior = atual;
            atual = atual.proximo;
        }
        return false;
    }

    /** Retorna uma copia dos elementos na ordem atual da playlist. */
    public Musica[] listar() {
        Musica[] musicas = new Musica[tamanho];
        No atual = inicio;
        int indice = 0;
        while (atual != null) {
            musicas[indice++] = atual.musica;
            atual = atual.proximo;
        }
        return musicas;
    }

    /** Busca por trecho no titulo ou no artista, sem diferenciar maiusculas. */
    public Musica[] buscar(String criterio) {
        validarTexto(criterio, "O criterio de busca nao pode ser vazio.");
        String busca = criterio.trim().toLowerCase(Locale.ROOT);

        int quantidadeEncontrada = 0;
        No atual = inicio;
        while (atual != null) {
            if (corresponde(atual.musica, busca)) {
                quantidadeEncontrada++;
            }
            atual = atual.proximo;
        }

        Musica[] resultado = new Musica[quantidadeEncontrada];
        atual = inicio;
        int indice = 0;
        while (atual != null) {
            if (corresponde(atual.musica, busca)) {
                resultado[indice++] = atual.musica;
            }
            atual = atual.proximo;
        }
        return resultado;
    }

    /** Reordena a lista alfabeticamente pelo titulo usando insercao de nos. */
    public void reordenarPorTitulo() {
        No listaOrdenada = null;
        No atual = inicio;

        while (atual != null) {
            No proximo = atual.proximo;
            if (listaOrdenada == null || vemAntes(atual, listaOrdenada)) {
                atual.proximo = listaOrdenada;
                listaOrdenada = atual;
            } else {
                No cursor = listaOrdenada;
                while (cursor.proximo != null && !vemAntes(atual, cursor.proximo)) {
                    cursor = cursor.proximo;
                }
                atual.proximo = cursor.proximo;
                cursor.proximo = atual;
            }
            atual = proximo;
        }

        inicio = listaOrdenada;
        fim = null;
        atual = inicio;
        while (atual != null) {
            fim = atual;
            atual = atual.proximo;
        }
    }

    private boolean corresponde(Musica musica, String busca) {
        return musica.getTitulo().toLowerCase(Locale.ROOT).contains(busca)
                || musica.getArtista().toLowerCase(Locale.ROOT).contains(busca);
    }

    private boolean vemAntes(No primeiro, No segundo) {
        return primeiro.musica.getTitulo().compareToIgnoreCase(
                segundo.musica.getTitulo()) < 0;
    }

    private void validarMusica(Musica musica) {
        if (musica == null) {
            throw new IllegalArgumentException("A playlist nao aceita musica null.");
        }
    }

    private void validarTexto(String texto, String mensagem) {
        if (texto == null || texto.trim().isEmpty()) {
            throw new IllegalArgumentException(mensagem);
        }
    }
}
