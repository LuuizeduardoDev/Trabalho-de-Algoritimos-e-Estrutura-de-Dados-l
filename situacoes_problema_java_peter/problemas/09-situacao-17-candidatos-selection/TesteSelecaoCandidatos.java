/** Testes simples do Selection Sort e da extracao Top-N. */
public class TesteSelecaoCandidatos {
    public static void main(String[] args) {
        testarOrdenacaoEExtracao();
        testarEmpate();
        testarErros();
        System.out.println("Todos os testes do problema 9 passaram.");
    }

    private static void testarOrdenacaoEExtracao() {
        Candidato[] candidatos = {
                new Candidato("Ana", 70),
                new Candidato("Bruno", 95),
                new Candidato("Carla", 82),
                new Candidato("Diego", 60)
        };

        SelectionSort.ordenar(candidatos);
        exigir(candidatos[0].getNome().equals("Bruno"), "Maior pontuacao deve ficar primeiro.");
        exigir(candidatos[3].getNome().equals("Diego"), "Menor pontuacao deve ficar por ultimo.");

        Candidato[] top2 = SelectionSort.extrairTopN(candidatos, 2);
        exigir(top2.length == 2, "Top-N deve ter N elementos.");
        exigir(top2[1].getNome().equals("Carla"), "Top-2 incorreto.");
    }

    private static void testarEmpate() {
        Candidato[] candidatos = {
                new Candidato("Zeca", 90),
                new Candidato("Alice", 90)
        };
        SelectionSort.ordenar(candidatos);
        exigir(candidatos[0].getNome().equals("Alice"), "Desempate alfabetico incorreto.");
    }

    private static void testarErros() {
        esperarErro(() -> SelectionSort.ordenar(new Candidato[0]));
        esperarErro(() -> SelectionSort.extrairTopN(
                new Candidato[] { new Candidato("Ana", 80) }, 0));
        esperarErro(() -> SelectionSort.extrairTopN(
                new Candidato[] { new Candidato("Ana", 80), new Candidato("Bia", 90) }, 1));
    }

    private static void esperarErro(Runnable operacao) {
        try {
            operacao.run();
            throw new AssertionError("Era esperada uma entrada invalida.");
        } catch (IllegalArgumentException esperado) {
            // Comportamento esperado para o caso de erro.
        }
    }

    private static void exigir(boolean condicao, String mensagem) {
        if (!condicao) {
            throw new AssertionError(mensagem);
        }
    }
}
