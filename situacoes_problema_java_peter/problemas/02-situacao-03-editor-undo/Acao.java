/**
 * Registro de uma acao. O estado anterior e mantido para que o undo possa
 * restaurar exatamente o editor, inclusive sua formatacao.
 */
public final class Acao {
    private final TipoAcao tipo;
    private final String descricao;
    private final EstadoEditor estadoAnterior;
    private final EstadoEditor estadoPosterior;

    public Acao(TipoAcao tipo, String descricao, EstadoEditor estadoAnterior,
            EstadoEditor estadoPosterior) {
        if (tipo == null) {
            throw new IllegalArgumentException("O tipo da acao nao pode ser null.");
        }
        if (descricao == null || descricao.trim().isEmpty()) {
            throw new IllegalArgumentException("A descricao da acao nao pode ser vazia.");
        }
        if (estadoAnterior == null || estadoPosterior == null) {
            throw new IllegalArgumentException("A acao deve possuir os dois estados.");
        }
        this.tipo = tipo;
        this.descricao = descricao;
        this.estadoAnterior = estadoAnterior;
        this.estadoPosterior = estadoPosterior;
    }

    public TipoAcao getTipo() {
        return tipo;
    }

    public String getDescricao() {
        return descricao;
    }

    public EstadoEditor getEstadoAnterior() {
        return estadoAnterior;
    }

    public EstadoEditor getEstadoPosterior() {
        return estadoPosterior;
    }

    @Override
    public String toString() {
        return tipo + ": " + descricao;
    }
}
