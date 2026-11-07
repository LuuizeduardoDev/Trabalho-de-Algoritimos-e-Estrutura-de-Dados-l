/** Representa uma musica da playlist. */
public class Musica {
    private final String titulo;
    private final String artista;
    private final int duracaoSegundos;

    public Musica(String titulo, String artista, int duracaoSegundos) {
        if (titulo == null || titulo.trim().isEmpty()) {
            throw new IllegalArgumentException("O titulo da musica nao pode ser vazio.");
        }
        if (artista == null || artista.trim().isEmpty()) {
            throw new IllegalArgumentException("O artista da musica nao pode ser vazio.");
        }
        if (duracaoSegundos < 0) {
            throw new IllegalArgumentException("A duracao nao pode ser negativa.");
        }

        this.titulo = titulo.trim();
        this.artista = artista.trim();
        this.duracaoSegundos = duracaoSegundos;
    }

    public String getTitulo() {
        return titulo;
    }

    public String getArtista() {
        return artista;
    }

    public int getDuracaoSegundos() {
        return duracaoSegundos;
    }

    public String getDuracaoFormatada() {
        int minutos = duracaoSegundos / 60;
        int segundos = duracaoSegundos % 60;
        return minutos + ":" + (segundos < 10 ? "0" : "") + segundos;
    }

    @Override
    public String toString() {
        return titulo + " - " + artista + " (" + getDuracaoFormatada() + ")";
    }
}
