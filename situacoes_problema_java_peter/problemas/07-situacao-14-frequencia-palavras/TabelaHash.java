/**
 * Tabela hash manual para associar cada palavra a sua frequencia.
 * As colisoes sao resolvidas por encadeamento em nos proprios.
 */
public class TabelaHash {
    private static class Entrada {
        private final String palavra;
        private int frequencia;
        private Entrada proxima;

        private Entrada(String palavra, Entrada proxima) {
            this.palavra = palavra;
            this.frequencia = 1;
            this.proxima = proxima;
        }
    }

    private final Entrada[] tabela;
    private int palavrasDistintas;
    private int totalOcorrencias;

    public TabelaHash() {
        this(101);
    }

    /** Permite usar uma tabela pequena nos testes de colisao. */
    public TabelaHash(int capacidade) {
        if (capacidade <= 0) {
            throw new IllegalArgumentException("A capacidade deve ser positiva.");
        }
        tabela = new Entrada[capacidade];
    }

    /** Adiciona uma ocorrencia da palavra. */
    public void adicionar(String palavra) {
        validarPalavra(palavra);

        int indice = indiceDa(palavra);
        Entrada atual = tabela[indice];
        while (atual != null) {
            if (atual.palavra.equals(palavra)) {
                atual.frequencia++;
                totalOcorrencias++;
                return;
            }
            atual = atual.proxima;
        }

        tabela[indice] = new Entrada(palavra, tabela[indice]);
        palavrasDistintas++;
        totalOcorrencias++;
    }

    /** Retorna a frequencia da palavra ou zero quando ela nao foi encontrada. */
    public int frequenciaDe(String palavra) {
        validarPalavra(palavra);

        Entrada atual = tabela[indiceDa(palavra)];
        while (atual != null) {
            if (atual.palavra.equals(palavra)) {
                return atual.frequencia;
            }
            atual = atual.proxima;
        }
        return 0;
    }

    public int palavrasDistintas() {
        return palavrasDistintas;
    }

    public int totalOcorrencias() {
        return totalOcorrencias;
    }

    /** Copia os pares armazenados para um vetor, sem expor os nos da tabela. */
    public PalavraFrequencia[] listarFrequencias() {
        PalavraFrequencia[] resultado = new PalavraFrequencia[palavrasDistintas];
        int posicao = 0;

        for (Entrada inicio : tabela) {
            Entrada atual = inicio;
            while (atual != null) {
                resultado[posicao++] = new PalavraFrequencia(atual.palavra, atual.frequencia);
                atual = atual.proxima;
            }
        }
        return resultado;
    }

    private int indiceDa(String palavra) {
        int hash = 0;
        for (int i = 0; i < palavra.length(); i++) {
            hash = 31 * hash + palavra.charAt(i);
        }
        return (hash & 0x7fffffff) % tabela.length;
    }

    private void validarPalavra(String palavra) {
        if (palavra == null || palavra.isEmpty()) {
            throw new IllegalArgumentException("A palavra nao pode ser nula ou vazia.");
        }
    }
}
