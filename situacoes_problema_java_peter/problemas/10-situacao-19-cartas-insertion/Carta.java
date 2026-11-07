/** Representa uma carta usando somente o valor exigido pela especificacao. */
public class Carta {
    private final int valor;

    public Carta(int valor) {
        this.valor = valor;
    }

    public int getValor() {
        return valor;
    }

    @Override
    public String toString() {
        return "Carta(" + valor + ")";
    }
}
