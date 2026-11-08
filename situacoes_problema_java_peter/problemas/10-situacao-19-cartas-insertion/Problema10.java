/** Demonstracao da insercao individual de novas cartas em uma mao ordenada. */
public class Problema10 {
    public static void main(String[] args) {
        if (args.length > 0) {
            System.out.println("Uso: java Problema10");
            return;
        }

        int[] valoresRecebidos = { 8, 3, 12, 5, 5, 1, 10, 7, 13, 2, 9, 4 };
        MaoCartas mao = new MaoCartas();

        System.out.println("Insercao de cartas em ordem crescente:");
        for (int i = 0; i < valoresRecebidos.length; i++) {
            Carta carta = new Carta(valoresRecebidos[i]);
            mao.inserir(carta);
            System.out.println("Recebida " + carta + " -> mao: " + mao);
        }
    }
}
