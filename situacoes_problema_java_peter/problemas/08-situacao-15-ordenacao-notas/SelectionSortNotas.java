/** Selection Sort usado como referencia para a comparacao de estatisticas. */
public class SelectionSortNotas {
    private SelectionSortNotas() {
        // Classe utilitaria.
    }

    public static EstatisticasOrdenacao ordenar(NotaAluno[] notas) {
        BubbleSortNotas.validarVetor(notas);
        EstatisticasOrdenacao estatisticas = new EstatisticasOrdenacao();

        for (int inicio = 0; inicio < notas.length - 1; inicio++) {
            int menor = inicio;
            for (int i = inicio + 1; i < notas.length; i++) {
                estatisticas.registrarComparacao();
                if (BubbleSortNotas.comparar(notas[i], notas[menor]) < 0) {
                    menor = i;
                }
            }
            if (menor != inicio) {
                BubbleSortNotas.trocar(notas, inicio, menor);
                estatisticas.registrarTroca();
            }
        }
        return estatisticas;
    }
}
