/** Bubble Sort otimizado para ordenar notas em ordem crescente. */
public class BubbleSortNotas {
    public static final int MAX_ALUNOS = 30;

    private BubbleSortNotas() {
        // Classe utilitaria.
    }

    /** Ordena o vetor recebido e interrompe quando uma passagem nao troca nada. */
    public static EstatisticasOrdenacao ordenar(NotaAluno[] notas) {
        validarVetor(notas);
        EstatisticasOrdenacao estatisticas = new EstatisticasOrdenacao();

        for (int fim = notas.length - 1; fim > 0; fim--) {
            boolean houveTroca = false;

            for (int i = 0; i < fim; i++) {
                estatisticas.registrarComparacao();
                if (comparar(notas[i], notas[i + 1]) > 0) {
                    trocar(notas, i, i + 1);
                    estatisticas.registrarTroca();
                    houveTroca = true;
                }
            }

            if (!houveTroca) {
                break;
            }
        }
        return estatisticas;
    }

    static int comparar(NotaAluno primeira, NotaAluno segunda) {
        int comparacaoNota = Double.compare(primeira.getNota(), segunda.getNota());
        if (comparacaoNota != 0) {
            return comparacaoNota;
        }
        return primeira.getAluno().compareToIgnoreCase(segunda.getAluno());
    }

    static void trocar(NotaAluno[] notas, int primeiro, int segundo) {
        NotaAluno temporaria = notas[primeiro];
        notas[primeiro] = notas[segundo];
        notas[segundo] = temporaria;
    }

    static void validarVetor(NotaAluno[] notas) {
        if (notas == null) {
            throw new IllegalArgumentException("O vetor de notas nao pode ser nulo.");
        }
        if (notas.length > MAX_ALUNOS) {
            throw new IllegalArgumentException("A turma nao pode ter mais de 30 alunos.");
        }
        for (NotaAluno nota : notas) {
            if (nota == null) {
                throw new IllegalArgumentException("O vetor nao pode conter aluno nulo.");
            }
        }
    }
}
