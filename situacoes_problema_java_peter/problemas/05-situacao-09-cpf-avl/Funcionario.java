/** Representa um funcionario indexado pelo CPF. */
public class Funcionario {
    private final String cpf;
    private final String nome;
    private final String cargo;

    public Funcionario(String cpf, String nome, String cargo) {
        this.cpf = validarCpf(cpf);
        this.nome = validarTexto(nome, "O nome do funcionario nao pode ser vazio.");
        this.cargo = validarTexto(cargo, "O cargo do funcionario nao pode ser vazio.");
    }

    public String getCpf() {
        return cpf;
    }

    public String getNome() {
        return nome;
    }

    public String getCargo() {
        return cargo;
    }

    @Override
    public String toString() {
        return "CPF: " + cpf + " | nome: " + nome + " | cargo: " + cargo;
    }

    private static String validarCpf(String cpf) {
        if (cpf == null || !cpf.matches("[0-9]{11}")) {
            throw new IllegalArgumentException(
                    "O CPF deve conter exatamente 11 digitos, sem pontuacao.");
        }
        return cpf;
    }

    private static String validarTexto(String texto, String mensagem) {
        if (texto == null || texto.trim().isEmpty()) {
            throw new IllegalArgumentException(mensagem);
        }
        return texto.trim();
    }
}
