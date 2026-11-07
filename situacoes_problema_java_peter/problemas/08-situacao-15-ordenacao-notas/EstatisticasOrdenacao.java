/** Guarda as comparacoes e trocas realizadas por um algoritmo de ordenacao. */
public class EstatisticasOrdenacao {
    private long comparacoes;
    private long trocas;

    void registrarComparacao() {
        comparacoes++;
    }

    void registrarTroca() {
        trocas++;
    }

    public long getComparacoes() {
        return comparacoes;
    }

    public long getTrocas() {
        return trocas;
    }

    @Override
    public String toString() {
        return "comparacoes=" + comparacoes + ", trocas=" + trocas;
    }
}
