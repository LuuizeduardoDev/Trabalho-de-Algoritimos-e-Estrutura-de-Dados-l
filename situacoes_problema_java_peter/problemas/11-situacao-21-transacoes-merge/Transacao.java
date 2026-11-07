import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Locale;

/** Representa uma transacao bancaria registrada em um instante. */
public class Transacao {
    private static final DateTimeFormatter FORMATO =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss", Locale.ROOT);

    private final LocalDateTime dataHora;
    private final double valor;
    private final String descricao;

    public Transacao(LocalDateTime dataHora, double valor, String descricao) {
        if (dataHora == null) {
            throw new IllegalArgumentException("A data e hora nao podem ser nulas.");
        }
        if (!Double.isFinite(valor)) {
            throw new IllegalArgumentException("O valor deve ser um numero finito.");
        }
        if (descricao == null || descricao.trim().isEmpty()) {
            throw new IllegalArgumentException("A descricao nao pode ser vazia.");
        }

        this.dataHora = dataHora;
        this.valor = valor;
        this.descricao = descricao;
    }

    public LocalDateTime getDataHora() {
        return dataHora;
    }

    public double getValor() {
        return valor;
    }

    public String getDescricao() {
        return descricao;
    }

    @Override
    public String toString() {
        return dataHora.format(FORMATO) + " | R$ " + String.format(Locale.ROOT, "%.2f", valor)
                + " | " + descricao;
    }
}
