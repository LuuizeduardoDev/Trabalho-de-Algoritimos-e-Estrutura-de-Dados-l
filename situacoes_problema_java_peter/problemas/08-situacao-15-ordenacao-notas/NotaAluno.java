import java.util.Locale;

/** Representa a nota de um aluno da turma. */
public class NotaAluno {
    private final String aluno;
    private final double nota;

    public NotaAluno(String aluno, double nota) {
        if (aluno == null || aluno.trim().isEmpty()) {
            throw new IllegalArgumentException("O nome do aluno nao pode ser nulo ou vazio.");
        }
        if (Double.isNaN(nota) || nota < 0.0 || nota > 10.0) {
            throw new IllegalArgumentException("A nota deve estar entre 0 e 10.");
        }
        this.aluno = aluno.trim();
        this.nota = nota;
    }

    public String getAluno() {
        return aluno;
    }

    public double getNota() {
        return nota;
    }

    @Override
    public String toString() {
        return String.format(Locale.ROOT, "%s: %.2f", aluno, nota);
    }
}
