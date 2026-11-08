/** Testes do grafo ponderado e do algoritmo de Dijkstra. */
public class TesteDijkstra {
    public static void main(String[] args) {
        testarRotasDoMapa();
        testarVerticeDesconectado();
        testarEntradasInvalidas();
        System.out.println("Todos os testes do problema 6 passaram.");
    }

    private static void testarRotasDoMapa() {
        GrafoPonderado cidade = Problema6.criarMapaDeExemplo();

        Rota paraAeroporto = Dijkstra.encontrar(cidade, "Centro de Distribuicao", "Aeroporto");
        exigir(paraAeroporto.existeCaminho(), "Deveria existir rota para o aeroporto.");
        exigir(Math.abs(paraAeroporto.getCusto() - 11.0) < 0.0001,
                "O custo para o aeroporto deveria ser 11.");
        exigir(paraAeroporto.quantidadeDePontos() == 5,
                "A rota para o aeroporto deveria conter cinco pontos.");

        Rota paraIndustrial = Dijkstra.encontrar(cidade, "Universidade", "Industrial");
        exigir(Math.abs(paraIndustrial.getCusto() - 12.0) < 0.0001,
                "O custo para a regiao industrial deveria ser 12.");
    }

    private static void testarVerticeDesconectado() {
        GrafoPonderado grafo = new GrafoPonderado(2);
        grafo.adicionarVertice("A");
        grafo.adicionarVertice("B");

        Rota rota = Dijkstra.encontrar(grafo, "A", "B");
        exigir(!rota.existeCaminho(), "Vertices desconectados nao devem gerar uma rota.");
        esperarErro(rota::getCusto);
    }

    private static void testarEntradasInvalidas() {
        GrafoPonderado grafo = new GrafoPonderado(1);
        grafo.adicionarVertice("A");

        esperarErro(() -> new GrafoPonderado(0));
        esperarErro(() -> grafo.adicionarVertice("A"));
        esperarErro(() -> grafo.adicionarConexao("A", "B", 2));
        esperarErro(() -> grafo.adicionarConexao("A", "A", -1));
        esperarErro(() -> Dijkstra.encontrar(grafo, "A", "B"));
        esperarErro(() -> Dijkstra.encontrar(null, "A", "A"));
    }

    private static void esperarErro(Runnable operacao) {
        try {
            operacao.run();
            throw new AssertionError("Era esperada uma entrada invalida.");
        } catch (IllegalArgumentException | IllegalStateException | IndexOutOfBoundsException esperado) {
            // Comportamento esperado para o caso de erro.
        }
    }

    private static void exigir(boolean condicao, String mensagem) {
        if (!condicao) {
            throw new AssertionError(mensagem);
        }
    }
}
