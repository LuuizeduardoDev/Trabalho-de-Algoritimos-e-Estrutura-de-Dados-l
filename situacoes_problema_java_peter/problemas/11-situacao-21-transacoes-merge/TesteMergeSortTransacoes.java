import java.time.LocalDateTime;

/** Testes do Merge Sort, incluindo estabilidade e entradas invalidas. */
public class TesteMergeSortTransacoes {
    public static void main(String[] args) {
        testarOrdenacaoComMaisDe50Transacoes();
        testarEstabilidadeNoMesmoSegundo();
        testarErros();
        System.out.println("Todos os testes do problema 11 passaram.");
    }

    private static void testarOrdenacaoComMaisDe50Transacoes() {
        Transacao[] transacoes = new Transacao[50];
        LocalDateTime inicio = LocalDateTime.of(2026, 1, 1, 0, 0);

        for (int i = 0; i < transacoes.length; i++) {
            transacoes[i] = new Transacao(inicio.plusMinutes((i * 23) % 500), i + 1,
                    "Transacao " + i);
        }

        MergeSortTransacoes.ordenar(transacoes);
        for (int i = 1; i < transacoes.length; i++) {
            exigir(!transacoes[i - 1].getDataHora().isAfter(transacoes[i].getDataHora()),
                    "O vetor nao foi ordenado cronologicamente.");
        }
    }

    private static void testarEstabilidadeNoMesmoSegundo() {
        LocalDateTime instante = LocalDateTime.of(2026, 2, 10, 14, 30, 45);
        Transacao primeira = new Transacao(instante, 10, "Primeira");
        Transacao segunda = new Transacao(instante, 20, "Segunda");
        Transacao anterior = new Transacao(instante.minusSeconds(1), 5, "Anterior");

        Transacao[] transacoes = { segunda, primeira, anterior };
        MergeSortTransacoes.ordenar(transacoes);

        exigir(transacoes[0] == anterior, "A transacao anterior deveria vir primeiro.");
        exigir(transacoes[1] == segunda, "A ordem original do empate deveria ser preservada.");
        exigir(transacoes[2] == primeira, "A ordem original do empate deveria ser preservada.");
    }

    private static void testarErros() {
        esperarErro(() -> MergeSortTransacoes.ordenar(null));
        esperarErro(() -> MergeSortTransacoes.ordenar(new Transacao[0]));
        esperarErro(() -> MergeSortTransacoes.ordenar(new Transacao[] { null }));
        esperarErro(() -> new Transacao(null, 10, "Descricao"));
        esperarErro(() -> new Transacao(LocalDateTime.now(), 10, ""));
    }

    private static void esperarErro(Runnable operacao) {
        try {
            operacao.run();
            throw new AssertionError("Era esperada uma entrada invalida.");
        } catch (IllegalArgumentException esperado) {
            // Comportamento esperado para o caso de erro.
        }
    }

    private static void exigir(boolean condicao, String mensagem) {
        if (!condicao) {
            throw new AssertionError(mensagem);
        }
    }
}
