/** Representa um candidato e sua pontuacao na prova. */
public class Candidato {
    private final String nome;
    private final double pontuacao;

    public Candidato(String nome, double pontuacao) {
        if (nome == null || nome.trim().isEmpty()) {
            throw new IllegalArgumentException("O nome do candidato nao pode ser vazio.");
        }
        if (Double.isNaN(pontuacao) || Double.isInfinite(pontuacao)) {
            throw new IllegalArgumentException("A pontuacao deve ser um numero valido.");
        }

        this.nome = nome;
        this.pontuacao = pontuacao;
    }

    public String getNome() {
        return nome;
    }

    public double getPontuacao() {
        return pontuacao;
    }

    @Override
    public String toString() {
        return nome + " - " + String.format("%.1f", pontuacao) + " pontos";
    }
}
