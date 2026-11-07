/** Representa um atleta inscrito na corrida, com seu tempo final em segundos. */
public class Atleta {
    private final String nome;
    private final double tempo;

    public Atleta(String nome, double tempo) {
        if (nome == null || nome.trim().isEmpty()) {
            throw new IllegalArgumentException("O nome do atleta nao pode ser vazio.");
        }
        if (Double.isNaN(tempo) || Double.isInfinite(tempo) || tempo < 0) {
            throw new IllegalArgumentException("O tempo deve ser um numero finito e nao negativo.");
        }

        this.nome = nome.trim();
        this.tempo = tempo;
    }

    public String getNome() {
        return nome;
    }

    public double getTempo() {
        return tempo;
    }

    @Override
    public String toString() {
        return nome + " - " + String.format("%.2f s", tempo);
    }
}
