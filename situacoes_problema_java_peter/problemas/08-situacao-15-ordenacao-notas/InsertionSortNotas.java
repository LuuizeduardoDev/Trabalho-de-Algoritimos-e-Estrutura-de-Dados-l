/** Insertion Sort usado como referencia para a comparacao de estatisticas. */
public class InsertionSortNotas {
    private InsertionSortNotas() {
        // Classe utilitaria.
    }

    /** Usa trocas adjacentes para que as trocas sejam contabilizadas diretamente. */
    public static EstatisticasOrdenacao ordenar(NotaAluno[] notas) {
        BubbleSortNotas.validarVetor(notas);
        EstatisticasOrdenacao estatisticas = new EstatisticasOrdenacao();

        for (int i = 1; i < notas.length; i++) {
            int posicao = i;
            while (posicao > 0) {
                estatisticas.registrarComparacao();
                if (BubbleSortNotas.comparar(notas[posicao - 1], notas[posicao]) <= 0) {
                    break;
                }
                BubbleSortNotas.trocar(notas, posicao - 1, posicao);
                estatisticas.registrarTroca();
                posicao--;
            }
        }
        return estatisticas;
    }
}
