import java.util.Locale;

/** Resultado de uma consulta de menor caminho. */
public final class Rota {
    private final String[] caminho;
    private final double custo;
    private final boolean encontrada;

    private Rota(String[] caminho, double custo, boolean encontrada) {
        this.caminho = caminho;
        this.custo = custo;
        this.encontrada = encontrada;
    }

    static Rota encontrada(String[] caminho, double custo) {
        return new Rota(caminho, custo, true);
    }

    static Rota semCaminho() {
        return new Rota(new String[0], -1, false);
    }

    public boolean existeCaminho() {
        return encontrada;
    }

    public double getCusto() {
        if (!encontrada) {
            throw new IllegalStateException("Nao existe caminho entre os vertices.");
        }
        return custo;
    }

    public int quantidadeDePontos() {
        return caminho.length;
    }

    public String getPonto(int indice) {
        if (indice < 0 || indice >= caminho.length) {
            throw new IndexOutOfBoundsException("Indice de ponto invalido: " + indice);
        }
        return caminho[indice];
    }

    public String formatarCaminho() {
        if (!encontrada) {
            return "nenhum caminho";
        }

        StringBuilder resultado = new StringBuilder();
        for (int i = 0; i < caminho.length; i++) {
            if (i > 0) {
                resultado.append(" -> ");
            }
            resultado.append(caminho[i]);
        }
        return resultado.toString();
    }

    @Override
    public String toString() {
        if (!encontrada) {
            return "Nenhum caminho encontrado.";
        }
        return formatarCaminho() + " | custo: "
                + String.format(Locale.ROOT, "%.1f", custo);
    }
}
