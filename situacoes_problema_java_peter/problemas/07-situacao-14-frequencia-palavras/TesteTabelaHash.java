/** Testes executaveis da tabela hash e do contador de palavras. */
public class TesteTabelaHash {
    public static void main(String[] args) {
        testarContagemENormalizacao();
        testarColisaoPorEncadeamento();
        testarCasosDeErro();
        System.out.println("Todos os testes do problema 7 foram aprovados.");
    }

    private static void testarContagemENormalizacao() {
        ContadorPalavras contador = new ContadorPalavras();
        contador.processar("Java, java! Estruturas de dados; dados e Java.");

        verificar(contador.getTabela().frequenciaDe("java") == 3,
                "A palavra Java deveria aparecer tres vezes.");
        verificar(contador.getTabela().frequenciaDe("dados") == 2,
                "A palavra dados deveria aparecer duas vezes.");
        verificar(contador.getTabela().frequenciaDe("inexistente") == 0,
                "Palavra inexistente deveria ter frequencia zero.");
        verificar(contador.getTabela().palavrasDistintas() == 5,
                "Deveriam existir cinco palavras distintas.");
        verificar(contador.getTabela().totalOcorrencias() == 8,
                "Deveriam existir oito ocorrencias.");

        PalavraFrequencia[] maisFrequentes = contador.maisFrequentes(1);
        verificar(maisFrequentes.length == 1 && maisFrequentes[0].getPalavra().equals("java"),
                "A palavra mais frequente deveria ser java.");
    }

    private static void testarColisaoPorEncadeamento() {
        TabelaHash tabela = new TabelaHash(2);
        tabela.adicionar("a");
        tabela.adicionar("c");
        tabela.adicionar("a");

        verificar(tabela.frequenciaDe("a") == 2,
                "A frequencia de a deveria ser preservada apos colisao.");
        verificar(tabela.frequenciaDe("c") == 1,
                "A frequencia de c deveria ser preservada apos colisao.");
        verificar(tabela.palavrasDistintas() == 2,
                "A colisao nao deveria criar uma palavra distinta extra.");
    }

    private static void testarCasosDeErro() {
        esperarErro(() -> new TabelaHash(0), "capacidade zero");

        TabelaHash tabela = new TabelaHash();
        esperarErro(() -> tabela.adicionar(null), "palavra nula");
        esperarErro(() -> tabela.frequenciaDe(""), "palavra vazia");

        ContadorPalavras contador = new ContadorPalavras();
        esperarErro(() -> contador.processar(null), "texto nulo");
        esperarErro(() -> contador.maisFrequentes(-1), "limite negativo");
        contador.processar("!!! ...");
        verificar(contador.getTabela().palavrasDistintas() == 0,
                "Texto sem palavras deveria produzir uma tabela vazia.");
    }

    private static void esperarErro(Runnable operacao, String descricao) {
        try {
            operacao.run();
            throw new AssertionError("Deveria rejeitar: " + descricao);
        } catch (IllegalArgumentException erro) {
            // Erro esperado para o caso invalido.
        }
    }

    private static void verificar(boolean condicao, String mensagem) {
        if (!condicao) {
            throw new AssertionError(mensagem);
        }
    }
}
