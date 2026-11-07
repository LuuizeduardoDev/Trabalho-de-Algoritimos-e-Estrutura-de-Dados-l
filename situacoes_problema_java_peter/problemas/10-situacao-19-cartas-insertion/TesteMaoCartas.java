/** Testes das insercoes ordenadas e dos casos de erro do problema 10. */
public class TesteMaoCartas {
    public static void main(String[] args) {
        testarInsercaoOrdenada();
        testarValoresIguais();
        testarCrescimentoDaMao();
        testarErros();
        System.out.println("Todos os testes do problema 10 passaram.");
    }

    private static void testarInsercaoOrdenada() {
        MaoCartas mao = new MaoCartas();
        int[] valores = { 8, 3, 12, 1, 7 };
        for (int valor : valores) {
            mao.inserir(new Carta(valor));
        }

        exigir(mao.toString().equals("[1, 3, 7, 8, 12]"),
                "A mao nao foi ordenada corretamente.");
        exigir(mao.tamanho() == 5, "O tamanho da mao esta incorreto.");
    }

    private static void testarValoresIguais() {
        MaoCartas mao = new MaoCartas();
        Carta primeira = new Carta(5);
        Carta segunda = new Carta(5);
        mao.inserir(primeira);
        mao.inserir(segunda);

        exigir(mao.get(0) == primeira, "A primeira carta igual deve permanecer primeiro.");
        exigir(mao.get(1) == segunda, "A segunda carta igual deve permanecer depois.");
    }

    private static void testarCrescimentoDaMao() {
        MaoCartas mao = new MaoCartas();
        for (int i = 0; i < 14; i++) {
            mao.inserir(new Carta(14 - i));
        }

        exigir(mao.tamanho() == 14, "A mao deveria crescer quando a capacidade acabasse.");
        exigir(mao.get(0).getValor() == 1, "O menor valor deveria estar no inicio.");
        exigir(mao.get(13).getValor() == 14, "O maior valor deveria estar no final.");
    }

    private static void testarErros() {
        MaoCartas mao = new MaoCartas();
        esperarErro(() -> mao.inserir(null));
        esperarErro(() -> mao.get(0));
    }

    private static void esperarErro(Runnable operacao) {
        try {
            operacao.run();
            throw new AssertionError("Era esperada uma entrada invalida.");
        } catch (IllegalArgumentException | IndexOutOfBoundsException esperado) {
            // Comportamento esperado para o caso de erro.
        }
    }

    private static void exigir(boolean condicao, String mensagem) {
        if (!condicao) {
            throw new AssertionError(mensagem);
        }
    }
}
