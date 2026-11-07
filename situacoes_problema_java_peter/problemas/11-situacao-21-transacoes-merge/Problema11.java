import java.time.LocalDateTime;

/** Programa demonstrativo da ordenacao de um historico bancario. */
public class Problema11 {
    private static final int QUANTIDADE_TRANSACOES = 50;

    public static void main(String[] args) {
        try {
            if (args.length != 0) {
                throw new IllegalArgumentException("Este programa nao recebe argumentos.");
            }

            Transacao[] historico = criarHistoricoDeExemplo();
            MergeSortTransacoes.ordenar(historico);

            System.out.println("Historico ordenado por data e hora (" + historico.length
                    + " transacoes):");
            for (int i = 0; i < historico.length; i++) {
                System.out.println((i + 1) + ". " + historico[i]);
            }
        } catch (IllegalArgumentException erro) {
            System.out.println("Erro: " + erro.getMessage());
        }
    }

    /** Gera dados deterministas para que a demonstracao seja reproduzivel. */
    private static Transacao[] criarHistoricoDeExemplo() {
        Transacao[] transacoes = new Transacao[QUANTIDADE_TRANSACOES];
        LocalDateTime inicio = LocalDateTime.of(2026, 10, 1, 9, 0, 0);

        for (int i = 0; i < transacoes.length; i++) {
            int deslocamentoEmMinutos = (i * 17) % 720;
            LocalDateTime dataHora = inicio.plusMinutes(deslocamentoEmMinutos);
            double valor = 35.0 + (i * 13.75);
            transacoes[i] = new Transacao(dataHora, valor, "Compra ou transferencia " + (i + 1));
        }

        // Mesmo instante: a ordem "Pagamento 1" e "Pagamento 2" deve permanecer.
        transacoes[0] = new Transacao(inicio.plusHours(5), 120.00, "Pagamento 1");
        transacoes[1] = new Transacao(inicio.plusHours(5), 85.50, "Pagamento 2");
        return transacoes;
    }
}
