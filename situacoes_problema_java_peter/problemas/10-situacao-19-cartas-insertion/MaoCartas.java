/**
 * Mao ordenada de cartas.
 * A insercao desloca os elementos maiores uma posicao para a direita e coloca
 * a nova carta no primeiro ponto em que a ordem crescente e preservada.
 */
public class MaoCartas {
    private Carta[] cartas;
    private int quantidade;

    public MaoCartas() {
        cartas = new Carta[13];
        quantidade = 0;
    }

    /** Insere uma carta na posicao correta, mantendo a mao em ordem crescente. */
    public void inserir(Carta carta) {
        if (carta == null) {
            throw new IllegalArgumentException("A carta nao pode ser nula.");
        }

        garantirCapacidade();

        int posicao = quantidade;
        // Valores iguais nao sao deslocados, preservando a ordem de chegada.
        while (posicao > 0
                && cartas[posicao - 1].getValor() > carta.getValor()) {
            cartas[posicao] = cartas[posicao - 1];
            posicao--;
        }

        cartas[posicao] = carta;
        quantidade++;
    }

    public int tamanho() {
        return quantidade;
    }

    public Carta get(int indice) {
        if (indice < 0 || indice >= quantidade) {
            throw new IndexOutOfBoundsException("Indice invalido: " + indice);
        }
        return cartas[indice];
    }

    private void garantirCapacidade() {
        if (quantidade < cartas.length) {
            return;
        }

        Carta[] novaMao = new Carta[cartas.length * 2];
        for (int i = 0; i < cartas.length; i++) {
            novaMao[i] = cartas[i];
        }
        cartas = novaMao;
    }

    @Override
    public String toString() {
        StringBuilder resultado = new StringBuilder("[");
        for (int i = 0; i < quantidade; i++) {
            if (i > 0) {
                resultado.append(", ");
            }
            resultado.append(cartas[i].getValor());
        }
        return resultado.append("]").toString();
    }
}
