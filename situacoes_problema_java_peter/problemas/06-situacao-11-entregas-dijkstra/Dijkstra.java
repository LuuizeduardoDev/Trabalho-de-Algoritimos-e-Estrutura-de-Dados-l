/** Implementacao do algoritmo de Dijkstra para pesos nao negativos. */
public final class Dijkstra {
    private Dijkstra() {
        // Classe utilitaria.
    }

    public static Rota encontrar(GrafoPonderado grafo, String origem, String destino) {
        if (grafo == null) {
            throw new IllegalArgumentException("O grafo nao pode ser nulo.");
        }
        if (origem == null || destino == null) {
            throw new IllegalArgumentException("Origem e destino sao obrigatorios.");
        }

        int indiceOrigem = exigirIndice(grafo, origem);
        int indiceDestino = exigirIndice(grafo, destino);
        int quantidade = grafo.tamanho();
        double[] distancias = new double[quantidade];
        int[] anteriores = new int[quantidade];
        boolean[] visitados = new boolean[quantidade];

        for (int i = 0; i < quantidade; i++) {
            distancias[i] = Double.POSITIVE_INFINITY;
            anteriores[i] = -1;
        }
        distancias[indiceOrigem] = 0;

        for (int passo = 0; passo < quantidade; passo++) {
            int atual = selecionarMenorNaoVisitado(distancias, visitados);
            if (atual == -1) {
                break;
            }
            visitados[atual] = true;

            GrafoPonderado.Aresta aresta = grafo.primeiraAresta(atual);
            while (aresta != null) {
                if (!visitados[aresta.destino]) {
                    double novaDistancia = distancias[atual] + aresta.peso;
                    if (novaDistancia < distancias[aresta.destino]) {
                        distancias[aresta.destino] = novaDistancia;
                        anteriores[aresta.destino] = atual;
                    }
                }
                aresta = aresta.proxima;
            }
        }

        if (Double.isInfinite(distancias[indiceDestino])) {
            return Rota.semCaminho();
        }
        return Rota.encontrada(reconstruirCaminho(grafo, anteriores, indiceOrigem,
                indiceDestino), distancias[indiceDestino]);
    }

    private static int selecionarMenorNaoVisitado(double[] distancias,
            boolean[] visitados) {
        int menor = -1;
        for (int i = 0; i < distancias.length; i++) {
            if (!visitados[i] && (menor == -1 || distancias[i] < distancias[menor])) {
                menor = i;
            }
        }
        return menor;
    }

    private static String[] reconstruirCaminho(GrafoPonderado grafo, int[] anteriores,
            int origem, int destino) {
        int[] indicesInvertidos = new int[grafo.tamanho()];
        int quantidade = 0;
        int atual = destino;
        while (atual != -1) {
            indicesInvertidos[quantidade++] = atual;
            if (atual == origem) {
                break;
            }
            atual = anteriores[atual];
        }

        String[] caminho = new String[quantidade];
        for (int i = 0; i < quantidade; i++) {
            caminho[i] = grafo.nomeDoVertice(indicesInvertidos[quantidade - 1 - i]);
        }
        return caminho;
    }

    private static int exigirIndice(GrafoPonderado grafo, String nome) {
        int indice = grafo.indiceDoVertice(nome);
        if (indice == -1) {
            throw new IllegalArgumentException("Vertice inexistente: " + nome);
        }
        return indice;
    }
}
