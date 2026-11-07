/**
 * Grafo ponderado representado por uma lista de adjacencia manual.
 * As conexoes deste projeto sao nao direcionadas.
 */
public final class GrafoPonderado {
    static final class Aresta {
        final int destino;
        final double peso;
        final Aresta proxima;

        private Aresta(int destino, double peso, Aresta proxima) {
            this.destino = destino;
            this.peso = peso;
            this.proxima = proxima;
        }
    }

    private final String[] nomes;
    private final Aresta[] adjacencias;
    private int quantidadeVertices;

    public GrafoPonderado(int capacidadeMaxima) {
        if (capacidadeMaxima <= 0) {
            throw new IllegalArgumentException("A capacidade deve ser positiva.");
        }
        nomes = new String[capacidadeMaxima];
        adjacencias = new Aresta[capacidadeMaxima];
    }

    public void adicionarVertice(String nome) {
        String nomeValido = validarNome(nome);
        if (quantidadeVertices == nomes.length) {
            throw new IllegalStateException("A capacidade maxima de vertices foi atingida.");
        }
        if (indiceDoVertice(nomeValido) != -1) {
            throw new IllegalArgumentException("O vertice ja existe: " + nomeValido);
        }

        nomes[quantidadeVertices] = nomeValido;
        quantidadeVertices++;
    }

    /** Adiciona uma conexao nos dois sentidos, com peso nao negativo. */
    public void adicionarConexao(String origem, String destino, double peso) {
        if (!Double.isFinite(peso) || peso < 0) {
            throw new IllegalArgumentException("O peso deve ser um numero nao negativo.");
        }

        int indiceOrigem = exigirIndice(origem);
        int indiceDestino = exigirIndice(destino);
        adjacencias[indiceOrigem] = new Aresta(indiceDestino, peso,
                adjacencias[indiceOrigem]);
        adjacencias[indiceDestino] = new Aresta(indiceOrigem, peso,
                adjacencias[indiceDestino]);
    }

    int tamanho() {
        return quantidadeVertices;
    }

    String nomeDoVertice(int indice) {
        return nomes[indice];
    }

    int indiceDoVertice(String nome) {
        if (nome == null) {
            return -1;
        }
        for (int i = 0; i < quantidadeVertices; i++) {
            if (nomes[i].equals(nome.trim())) {
                return i;
            }
        }
        return -1;
    }

    Aresta primeiraAresta(int indice) {
        return adjacencias[indice];
    }

    private int exigirIndice(String nome) {
        String nomeValido = validarNome(nome);
        int indice = indiceDoVertice(nomeValido);
        if (indice == -1) {
            throw new IllegalArgumentException("Vertice inexistente: " + nomeValido);
        }
        return indice;
    }

    private static String validarNome(String nome) {
        if (nome == null || nome.trim().isEmpty()) {
            throw new IllegalArgumentException("O nome do vertice nao pode ser vazio.");
        }
        return nome.trim();
    }
}
