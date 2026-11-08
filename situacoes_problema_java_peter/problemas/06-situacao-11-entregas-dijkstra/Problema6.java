import java.util.Locale;

/** Demonstracao do roteamento de entregas com Dijkstra. */
public class Problema6 {
    public static void main(String[] args) {
        try {
            if (args.length != 0) {
                throw new IllegalArgumentException("Este programa nao recebe argumentos.");
            }

            GrafoPonderado cidade = criarMapaDeExemplo();
            System.out.println("Rotas de menor custo:");
            imprimirRota(cidade, "Centro de Distribuicao", "Aeroporto");
            imprimirRota(cidade, "Centro de Distribuicao", "Porto");
            imprimirRota(cidade, "Universidade", "Industrial");
            imprimirRota(cidade, "Norte", "Mercado");
        } catch (IllegalArgumentException | IllegalStateException erro) {
            System.out.println("Erro: " + erro.getMessage());
        }
    }

    private static void imprimirRota(GrafoPonderado cidade, String origem, String destino) {
        Rota rota = Dijkstra.encontrar(cidade, origem, destino);
        if (rota.existeCaminho()) {
            System.out.println(origem + " -> " + destino + ": " + rota.formatarCaminho()
                    + " | custo total: "
                    + String.format(Locale.ROOT, "%.1f", rota.getCusto()));
        } else {
            System.out.println(origem + " -> " + destino + ": nenhum caminho");
        }
    }

    /** Mapa com 10 pontos e pesos inteiros representando custo de deslocamento. */
    static GrafoPonderado criarMapaDeExemplo() {
        GrafoPonderado cidade = new GrafoPonderado(10);
        cidade.adicionarVertice("Centro de Distribuicao");
        cidade.adicionarVertice("Norte");
        cidade.adicionarVertice("Sul");
        cidade.adicionarVertice("Leste");
        cidade.adicionarVertice("Oeste");
        cidade.adicionarVertice("Industrial");
        cidade.adicionarVertice("Mercado");
        cidade.adicionarVertice("Porto");
        cidade.adicionarVertice("Aeroporto");
        cidade.adicionarVertice("Universidade");

        cidade.adicionarConexao("Centro de Distribuicao", "Norte", 4);
        cidade.adicionarConexao("Centro de Distribuicao", "Sul", 2);
        cidade.adicionarConexao("Norte", "Leste", 3);
        cidade.adicionarConexao("Norte", "Oeste", 5);
        cidade.adicionarConexao("Sul", "Leste", 6);
        cidade.adicionarConexao("Sul", "Industrial", 3);
        cidade.adicionarConexao("Leste", "Mercado", 2);
        cidade.adicionarConexao("Oeste", "Mercado", 1);
        cidade.adicionarConexao("Industrial", "Porto", 4);
        cidade.adicionarConexao("Mercado", "Porto", 3);
        cidade.adicionarConexao("Mercado", "Aeroporto", 7);
        cidade.adicionarConexao("Porto", "Aeroporto", 2);
        cidade.adicionarConexao("Oeste", "Universidade", 4);
        cidade.adicionarConexao("Universidade", "Aeroporto", 6);
        return cidade;
    }
}
