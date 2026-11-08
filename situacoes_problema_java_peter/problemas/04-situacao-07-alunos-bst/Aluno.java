public class Aluno {
    private final int matricula;
    private final String nome;
    private final String curso;

    public Aluno(int matricula, String nome, String curso) {
        if (matricula <= 0) {
            throw new IllegalArgumentException("A matricula deve ser positiva.");
        }
        if (nome == null || nome.trim().isEmpty()) {
            throw new IllegalArgumentException("O nome do aluno nao pode ser vazio.");
        }
        if (curso == null || curso.trim().isEmpty()) {
            throw new IllegalArgumentException("O curso do aluno nao pode ser vazio.");
        }

        this.matricula = matricula;
        this.nome = nome;
        this.curso = curso;
    }

    public int getMatricula() {
        return matricula;
    }

    public String getNome() {
        return nome;
    }

    public String getCurso() {
        return curso;
    }

    @Override
    public String toString() {
        return "Matricula: " + matricula + " | Nome: " + nome + " | Curso: " + curso;
    }
}
