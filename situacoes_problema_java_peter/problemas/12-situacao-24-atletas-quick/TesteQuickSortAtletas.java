/** Testes manuais do Quick Sort e das regras basicas de entrada do Problema 12. */
public class TesteQuickSortAtletas {

    public static void main(String[] args) {
        testarOrdenacaoCom30Atletas();
        testarDesempatePorNome();
        testarVetorVazio();
        testarVetorNulo();
        testarAtletaNuloNoVetor();
        testarAtletaComDadosInvalidos();
        testarPodioComMenosDeTresAtletas();
        System.out.println("Todos os testes do Problema 12 passaram.");
    }

    private static void testarOrdenacaoCom30Atletas() {
        Atleta[] atletas = criarAtletasDeTeste();
        QuickSortAtletas.ordenar(atletas);

        verificar(atletas.length == 30, "O teste deve possuir 30 atletas.");
        verificar(atletas[0].getNome().equals("Paulo"), "O menor tempo deve ficar em primeiro.");
        verificar(atletas[1].getNome().equals("Ursula"), "A classificacao deve estar ordenada.");
        verificar(atletas[29].getNome().equals("Tiago"), "O maior tempo deve ficar em ultimo.");

        for (int indice = 1; indice < atletas.length; indice++) {
            verificar(atletas[indice - 1].getTempo() <= atletas[indice].getTempo(),
                    "Os tempos devem estar em ordem crescente.");
        }
    }

    private static void testarDesempatePorNome() {
        Atleta[] atletas = {
            new Atleta("Zoe", 50.0),
            new Atleta("Ana", 50.0),
            new Atleta("Bia", 49.0)
        };
        QuickSortAtletas.ordenar(atletas);

        verificar(atletas[1].getNome().equals("Ana"), "O empate deve ser desempate pelo nome.");
        verificar(atletas[2].getNome().equals("Zoe"), "O desempate deve ser deterministico.");
    }

    private static void testarVetorVazio() {
        Atleta[] atletas = new Atleta[0];
        QuickSortAtletas.ordenar(atletas);
        verificar(atletas.length == 0, "Vetor vazio deve ser aceito.");
    }

    private static void testarVetorNulo() {
        esperarErro(() -> QuickSortAtletas.ordenar(null), "Vetor nulo deve gerar erro.");
    }

    private static void testarAtletaNuloNoVetor() {
        esperarErro(() -> QuickSortAtletas.ordenar(new Atleta[] { null }),
                "Atleta nulo deve gerar erro.");
    }

    private static void testarAtletaComDadosInvalidos() {
        esperarErro(() -> new Atleta("", 10.0), "Nome vazio deve gerar erro.");
        esperarErro(() -> new Atleta("Atleta", -1.0), "Tempo negativo deve gerar erro.");
    }

    private static void testarPodioComMenosDeTresAtletas() {
        Atleta[] atletas = { new Atleta("Ana", 10.0) };
        QuickSortAtletas.ordenar(atletas);
        Problema12.imprimirPodio(atletas);
    }

    private static Atleta[] criarAtletasDeTeste() {
        return new Atleta[] {
            new Atleta("Ana", 62.41), new Atleta("Bruno", 60.12), new Atleta("Carla", 64.70),
            new Atleta("Diego", 59.88), new Atleta("Elisa", 61.03), new Atleta("Fabio", 63.25),
            new Atleta("Gabriela", 58.92), new Atleta("Henrique", 65.10), new Atleta("Isabela", 60.12),
            new Atleta("Joao", 66.44), new Atleta("Karen", 62.09), new Atleta("Lucas", 59.88),
            new Atleta("Marina", 67.31), new Atleta("Nicolas", 61.77), new Atleta("Olivia", 63.90),
            new Atleta("Paulo", 57.84), new Atleta("Quenia", 64.11), new Atleta("Rafael", 60.85),
            new Atleta("Sara", 62.88), new Atleta("Tiago", 68.02), new Atleta("Ursula", 58.41),
            new Atleta("Victor", 61.41), new Atleta("Wesley", 63.02), new Atleta("Xavier", 66.02),
            new Atleta("Yara", 59.20), new Atleta("Zeca", 65.75), new Atleta("Alice", 62.41),
            new Atleta("Breno", 60.50), new Atleta("Cintia", 64.70), new Atleta("Davi", 58.75)
        };
    }

    private static void esperarErro(Runnable operacao, String mensagem) {
        try {
            operacao.run();
            throw new AssertionError(mensagem);
        } catch (IllegalArgumentException esperado) {
            // Erro esperado para validar o tratamento de entrada.
        }
    }

    private static void verificar(boolean condicao, String mensagem) {
        if (!condicao) {
            throw new AssertionError(mensagem);
        }
    }
}
