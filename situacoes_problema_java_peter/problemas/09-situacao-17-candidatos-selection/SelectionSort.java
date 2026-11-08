/**
 * Selection Sort para candidatos.
 * A ordenacao e decrescente porque os maiores resultados sao os melhores.
 */
public class SelectionSort {

    private SelectionSort() {
        // Classe utilitaria: nao deve ser instanciada.
    }

    /** Ordena o vetor recebido no proprio vetor, da maior para a menor pontuacao. */
    public static void ordenar(Candidato[] candidatos) {
        validarLista(candidatos);

        for (int posicao = 0; posicao < candidatos.length - 1; posicao++) {
            int indiceMaior = posicao;

            // Procura o maior elemento restante para coloca-lo na posicao atual.
            for (int i = posicao + 1; i < candidatos.length; i++) {
                if (vemAntes(candidatos[i], candidatos[indiceMaior])) {
                    indiceMaior = i;
                }
            }

            if (indiceMaior != posicao) {
                Candidato temporario = candidatos[posicao];
                candidatos[posicao] = candidatos[indiceMaior];
                candidatos[indiceMaior] = temporario;
            }
        }
    }

    /**
     * Devolve os primeiros N candidatos de um vetor ja ordenado.
     * A ordenacao e validada para evitar extrair um Top-N incorreto.
     */
    public static Candidato[] extrairTopN(Candidato[] candidatosOrdenados, int n) {
        validarLista(candidatosOrdenados);
        if (n <= 0 || n > candidatosOrdenados.length) {
            throw new IllegalArgumentException(
                    "N deve estar entre 1 e " + candidatosOrdenados.length + ".");
        }

        for (int i = 1; i < candidatosOrdenados.length; i++) {
            if (vemAntes(candidatosOrdenados[i], candidatosOrdenados[i - 1])) {
                throw new IllegalArgumentException("A lista deve estar ordenada antes do Top-N.");
            }
        }

        Candidato[] topN = new Candidato[n];
        for (int i = 0; i < n; i++) {
            topN[i] = candidatosOrdenados[i];
        }
        return topN;
    }

    private static boolean vemAntes(Candidato primeiro, Candidato segundo) {
        if (primeiro.getPontuacao() != segundo.getPontuacao()) {
            return primeiro.getPontuacao() > segundo.getPontuacao();
        }
        // Desempate simples e deterministico, pois a especificacao nao o define.
        return primeiro.getNome().compareToIgnoreCase(segundo.getNome()) < 0;
    }

    private static void validarLista(Candidato[] candidatos) {
        if (candidatos == null || candidatos.length == 0) {
            throw new IllegalArgumentException("A lista de candidatos nao pode ser vazia.");
        }
        for (Candidato candidato : candidatos) {
            if (candidato == null) {
                throw new IllegalArgumentException("A lista nao pode conter candidato nulo.");
            }
        }
    }
}
