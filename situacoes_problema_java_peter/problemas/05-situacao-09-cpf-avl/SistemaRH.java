/** Executa a demonstracao do indice de funcionarios por CPF. */
public class SistemaRH {
    public static void main(String[] args) {
        ArvoreAVL indice = new ArvoreAVL();

        System.out.println("=== Cadastro de funcionarios ===");
        for (int numero = 1; numero <= 25; numero++) {
            indice.inserir(new Funcionario(
                    cpf(numero),
                    "Funcionario " + numero,
                    cargo(numero)));
        }
        System.out.println("Funcionarios cadastrados: " + indice.tamanho());
        imprimirEstado(indice);

        System.out.println();
        System.out.println("=== Busca por CPF ===");
        imprimirBusca(indice, cpf(13));
        imprimirBusca(indice, "99999999999");

        System.out.println();
        System.out.println("=== Remocao de funcionarios ===");
        removerEImprimir(indice, cpf(10));
        removerEImprimir(indice, cpf(20));
        removerEImprimir(indice, "99999999999");
        imprimirEstado(indice);

        System.out.println();
        System.out.println("=== Fatores de balanceamento em ordem de CPF ===");
        System.out.print(indice.relatorioBalanceamento());

        System.out.println();
        System.out.println("=== Casos de erro ===");
        try {
            indice.inserir(new Funcionario(cpf(13), "Duplicado", "Teste"));
        } catch (IllegalArgumentException erro) {
            System.out.println("Duplicidade rejeitada: " + erro.getMessage());
        }

        try {
            indice.buscar("123");
        } catch (IllegalArgumentException erro) {
            System.out.println("CPF invalido rejeitado: " + erro.getMessage());
        }
    }

    private static void imprimirEstado(ArvoreAVL indice) {
        System.out.println("Altura da arvore: " + indice.altura());
        System.out.println("Fator da raiz: " + indice.fatorBalanceamento());
        System.out.println("Arvore balanceada? " + indice.estaBalanceada());
    }

    private static void imprimirBusca(ArvoreAVL indice, String cpf) {
        Funcionario funcionario = indice.buscar(cpf);
        if (funcionario == null) {
            System.out.println("CPF " + cpf + " nao encontrado.");
        } else {
            System.out.println(funcionario);
        }
    }

    private static void removerEImprimir(ArvoreAVL indice, String cpf) {
        boolean removido = indice.remover(cpf);
        System.out.println(removido
                ? "CPF " + cpf + " removido."
                : "CPF " + cpf + " nao encontrado para remocao.");
        System.out.println("Balanceada apos a operacao? " + indice.estaBalanceada());
    }

    private static String cpf(int numero) {
        return String.format("%011d", 10000000000L + numero);
    }

    private static String cargo(int numero) {
        String[] cargos = { "Analista", "Desenvolvedor", "Assistente", "Gerente", "Tecnico" };
        return cargos[(numero - 1) % cargos.length];
    }
}
