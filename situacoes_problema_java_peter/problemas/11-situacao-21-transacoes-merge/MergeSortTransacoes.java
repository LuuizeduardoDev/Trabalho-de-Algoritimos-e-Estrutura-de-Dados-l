import java.time.LocalDateTime;

/** Merge Sort estavel para ordenar transacoes em ordem cronologica. */
public final class MergeSortTransacoes {
    private MergeSortTransacoes() {
        // Classe utilitaria: nao deve ser instanciada.
    }

    /** Ordena o vetor no proprio vetor, da transacao mais antiga para a mais recente. */
    public static void ordenar(Transacao[] transacoes) {
        validarLista(transacoes);
        Transacao[] auxiliar = new Transacao[transacoes.length];
        ordenar(transacoes, auxiliar, 0, transacoes.length - 1);
    }

    private static void ordenar(Transacao[] transacoes, Transacao[] auxiliar,
            int inicio, int fim) {
        if (inicio >= fim) {
            return;
        }

        int meio = inicio + (fim - inicio) / 2;
        ordenar(transacoes, auxiliar, inicio, meio);
        ordenar(transacoes, auxiliar, meio + 1, fim);
        intercalar(transacoes, auxiliar, inicio, meio, fim);
    }

    private static void intercalar(Transacao[] transacoes, Transacao[] auxiliar,
            int inicio, int meio, int fim) {
        for (int i = inicio; i <= fim; i++) {
            auxiliar[i] = transacoes[i];
        }

        int esquerda = inicio;
        int direita = meio + 1;

        for (int posicao = inicio; posicao <= fim; posicao++) {
            if (esquerda > meio) {
                transacoes[posicao] = auxiliar[direita++];
            } else if (direita > fim) {
                transacoes[posicao] = auxiliar[esquerda++];
            } else if (vemAntesOuNoMesmoInstante(auxiliar[esquerda], auxiliar[direita])) {
                // Em empate, escolhe a metade esquerda para preservar a estabilidade.
                transacoes[posicao] = auxiliar[esquerda++];
            } else {
                transacoes[posicao] = auxiliar[direita++];
            }
        }
    }

    private static boolean vemAntesOuNoMesmoInstante(Transacao primeira, Transacao segunda) {
        LocalDateTime instante1 = primeira.getDataHora();
        LocalDateTime instante2 = segunda.getDataHora();
        return !instante1.isAfter(instante2);
    }

    private static void validarLista(Transacao[] transacoes) {
        if (transacoes == null || transacoes.length == 0) {
            throw new IllegalArgumentException("A lista de transacoes nao pode ser vazia.");
        }
        for (Transacao transacao : transacoes) {
            if (transacao == null) {
                throw new IllegalArgumentException("A lista nao pode conter transacao nula.");
            }
        }
    }
}
