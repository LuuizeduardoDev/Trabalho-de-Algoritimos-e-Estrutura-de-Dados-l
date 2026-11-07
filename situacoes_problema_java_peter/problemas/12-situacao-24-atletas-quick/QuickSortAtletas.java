/** Ordena atletas com Quick Sort, usando o menor tempo como melhor resultado. */
public class QuickSortAtletas {

    private QuickSortAtletas() {
        // Classe utilitaria: nao deve ser instanciada.
    }

    /** Ordena o vetor recebido no proprio vetor. A complexidade media e O(n log n). */
    public static void ordenar(Atleta[] atletas) {
        if (atletas == null) {
            throw new IllegalArgumentException("O vetor de atletas nao pode ser nulo.");
        }

        validarAtletas(atletas);
        if (atletas.length < 2) {
            return;
        }
        quickSort(atletas, 0, atletas.length - 1);
    }

    private static void quickSort(Atleta[] atletas, int inicio, int fim) {
        int esquerda = inicio;
        int direita = fim;
        Atleta pivo = atletas[inicio + (fim - inicio) / 2];

        while (esquerda <= direita) {
            while (comparar(atletas[esquerda], pivo) < 0) {
                esquerda++;
            }
            while (comparar(atletas[direita], pivo) > 0) {
                direita--;
            }

            if (esquerda <= direita) {
                trocar(atletas, esquerda, direita);
                esquerda++;
                direita--;
            }
        }

        if (inicio < direita) {
            quickSort(atletas, inicio, direita);
        }
        if (esquerda < fim) {
            quickSort(atletas, esquerda, fim);
        }
    }

    private static void validarAtletas(Atleta[] atletas) {
        for (Atleta atleta : atletas) {
            if (atleta == null) {
                throw new IllegalArgumentException("O vetor nao pode conter atleta nulo.");
            }
        }
    }

    private static int comparar(Atleta primeiro, Atleta segundo) {
        int comparacaoTempo = Double.compare(primeiro.getTempo(), segundo.getTempo());
        if (comparacaoTempo != 0) {
            return comparacaoTempo;
        }

        int comparacaoNome = primeiro.getNome().compareToIgnoreCase(segundo.getNome());
        if (comparacaoNome != 0) {
            return comparacaoNome;
        }
        return primeiro.getNome().compareTo(segundo.getNome());
    }

    private static void trocar(Atleta[] atletas, int primeiro, int segundo) {
        Atleta auxiliar = atletas[primeiro];
        atletas[primeiro] = atletas[segundo];
        atletas[segundo] = auxiliar;
    }
}
