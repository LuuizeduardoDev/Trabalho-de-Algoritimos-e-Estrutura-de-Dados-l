public class TesteArvoreAlunos {
    public static void main(String[] args) {
        ArvoreAlunos arvore = new ArvoreAlunos();

        verificar(arvore.estaVazia(), "A arvore deve iniciar vazia.");
        verificar(arvore.inserir(new Aluno(30, "Aluno 30", "Computacao")), "A primeira insercao deve funcionar.");
        verificar(arvore.inserir(new Aluno(20, "Aluno 20", "Computacao")), "A insercao a esquerda deve funcionar.");
        verificar(arvore.inserir(new Aluno(40, "Aluno 40", "Computacao")), "A insercao a direita deve funcionar.");
        verificar(arvore.inserir(new Aluno(10, "Aluno 10", "Computacao")), "A insercao de folha deve funcionar.");
        verificar(!arvore.inserir(new Aluno(30, "Outro aluno", "Administracao")),
                "Matricula duplicada nao deve ser inserida.");
        verificar(arvore.buscar(20) != null, "A busca de matricula existente deve funcionar.");
        verificar(arvore.buscar(99) == null, "A busca de matricula inexistente deve retornar null.");
        verificar(arvore.remover(30), "A remocao de no com dois filhos deve funcionar.");
        verificar(arvore.buscar(30) == null, "O aluno removido nao deve ser encontrado.");
        verificar(!arvore.remover(99), "A remocao de matricula inexistente deve retornar false.");
        verificar(arvore.tamanho() == 3, "A quantidade deve ser atualizada apos a remocao.");

        try {
            arvore.inserir(null);
            throw new AssertionError("Inserir null deveria produzir erro.");
        } catch (IllegalArgumentException esperado) {
            System.out.println("Caso de erro de aluno nulo tratado.");
        }

        try {
            new Aluno(0, "Aluno invalido", "Computacao");
            throw new AssertionError("Matricula invalida deveria produzir erro.");
        } catch (IllegalArgumentException esperado) {
            System.out.println("Caso de erro de matricula invalida tratado.");
        }

        System.out.println("Todos os testes da arvore de alunos passaram.");
    }

    private static void verificar(boolean condicao, String mensagem) {
        if (!condicao) {
            throw new AssertionError(mensagem);
        }
    }
}
