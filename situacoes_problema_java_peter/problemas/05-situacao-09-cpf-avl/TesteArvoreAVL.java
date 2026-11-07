/** Testes executaveis da arvore AVL e dos tratamentos de erro. */
public class TesteArvoreAVL {
    public static void main(String[] args) {
        testarRotacoesDeInsercao();
        testarOperacoesComFuncionarios();
        testarCasosDeErro();
        System.out.println("Todos os testes da arvore AVL foram aprovados.");
    }

    private static void testarRotacoesDeInsercao() {
        verificarRaizAposRotacao(new int[] { 30, 20, 10 }, 20);
        verificarRaizAposRotacao(new int[] { 10, 20, 30 }, 20);
        verificarRaizAposRotacao(new int[] { 30, 10, 20 }, 20);
        verificarRaizAposRotacao(new int[] { 10, 30, 20 }, 20);
    }

    private static void verificarRaizAposRotacao(int[] numeros, int raizEsperada) {
        ArvoreAVL arvore = new ArvoreAVL();
        for (int numero : numeros) {
            arvore.inserir(funcionario(numero));
        }

        verificar(arvore.getCpfRaiz().equals(cpf(raizEsperada)),
                "A rotacao deveria deixar o CPF " + cpf(raizEsperada) + " na raiz.");
        verificar(arvore.estaBalanceada(), "A arvore deveria estar balanceada apos a rotacao.");
    }

    private static void testarOperacoesComFuncionarios() {
        ArvoreAVL arvore = new ArvoreAVL();
        for (int numero = 1; numero <= 25; numero++) {
            arvore.inserir(funcionario(numero));
        }

        verificar(arvore.tamanho() == 25, "A arvore deveria conter 25 funcionarios.");
        verificar(arvore.buscar(cpf(13)) != null, "O CPF cadastrado deveria ser encontrado.");
        verificar(arvore.buscar("99999999999") == null, "CPF inexistente deveria retornar null.");
        verificar(arvore.altura() <= 6, "A altura da AVL de 25 nos deveria ser pequena.");
        verificar(arvore.estaBalanceada(), "A arvore deveria estar balanceada apos insercoes.");

        verificar(arvore.remover(cpf(13)), "A remocao de um CPF existente deveria funcionar.");
        verificar(arvore.buscar(cpf(13)) == null, "O CPF removido nao deveria ser encontrado.");
        verificar(!arvore.remover("99999999999"), "A remocao de CPF inexistente deveria retornar false.");
        verificar(arvore.estaBalanceada(), "A arvore deveria estar balanceada apos remocao.");
    }

    private static void testarCasosDeErro() {
        ArvoreAVL arvore = new ArvoreAVL();

        esperarErro(() -> arvore.inserir(null), "insercao de null");
        esperarErro(() -> arvore.buscar("123"), "busca com CPF invalido");
        esperarErro(() -> arvore.inserir(new Funcionario("123", "Nome", "Cargo")),
                "funcionario com CPF invalido");

        arvore.inserir(funcionario(1));
        esperarErro(() -> arvore.inserir(funcionario(1)), "CPF duplicado");
    }

    private static Funcionario funcionario(int numero) {
        return new Funcionario(cpf(numero), "Funcionario " + numero, "Analista");
    }

    private static String cpf(int numero) {
        return String.format("%011d", 10000000000L + numero);
    }

    private static void esperarErro(Runnable operacao, String descricao) {
        try {
            operacao.run();
            throw new AssertionError("Deveria rejeitar: " + descricao);
        } catch (IllegalArgumentException erro) {
            // Erro esperado para o caso invalido.
        }
    }

    private static void verificar(boolean condicao, String mensagem) {
        if (!condicao) {
            throw new AssertionError(mensagem);
        }
    }
}
