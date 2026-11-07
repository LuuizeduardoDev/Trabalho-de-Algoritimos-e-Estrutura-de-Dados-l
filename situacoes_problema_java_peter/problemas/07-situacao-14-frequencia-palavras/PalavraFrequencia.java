/** Representa uma palavra e a quantidade de vezes em que ela apareceu. */
public class PalavraFrequencia {
    private final String palavra;
    private final int frequencia;

    public PalavraFrequencia(String palavra, int frequencia) {
        this.palavra = palavra;
        this.frequencia = frequencia;
    }

    public String getPalavra() {
        return palavra;
    }

    public int getFrequencia() {
        return frequencia;
    }

    @Override
    public String toString() {
        return palavra + " -> " + frequencia;
    }
}
