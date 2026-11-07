/** Testes executaveis do Problema 8. */
public class TesteOrdenacaoNotas {
    public static void main(String[] args) {
        testarOrdenacaoEContagem();
        testarParadaAntecipada();
        testarComparacaoComOutrosAlgoritmos();
        testarLimiteValido();
        testarCasosDeErro();
        System.out.println("Todos os testes do problema 8 foram aprovados.");
    }

    private static void testarOrdenacaoEContagem() {
        NotaAluno[] notas = {
                new NotaAluno("Carlos", 8.5),
                new NotaAluno("Bruno", 6.0),
                new NotaAluno("Ana", 6.0),
                new NotaAluno("Diana", 9.0)
        };

        EstatisticasOrdenacao estatisticas = BubbleSortNotas.ordenar(notas);

        verificar(notas[0].getAluno().equals("Ana"), "Ana deveria ser a primeira nota.");
        verificar(notas[1].getAluno().equals("Bruno"), "Bruno deveria ser o segundo em caso de empate.");
        verificar(notas[2].getAluno().equals("Carlos"), "Carlos deveria ser o terceiro.");
        verificar(notas[3].getAluno().equals("Diana"), "Diana deveria ser a ultima nota.");
        verificar(estatisticas.getComparacoes() > 0, "As comparacoes deveriam ser contabilizadas.");
        verificar(estatisticas.getTrocas() > 0, "As trocas deveriam ser contabilizadas.");
    }

    private static void testarParadaAntecipada() {
        NotaAluno[] notas = {
                new NotaAluno("Ana", 5.0),
                new NotaAluno("Bruno", 6.0),
                new NotaAluno("Carla", 7.0)
        };

        EstatisticasOrdenacao estatisticas = BubbleSortNotas.ordenar(notas);

        verificar(estatisticas.getComparacoes() == 2,
                "Um vetor ja ordenado deveria parar apos a primeira passagem.");
        verificar(estatisticas.getTrocas() == 0,
                "Um vetor ja ordenado nao deveria ter trocas.");
    }

    private static void testarComparacaoComOutrosAlgoritmos() {
        NotaAluno[] original = {
                new NotaAluno("A", 8.0),
                new NotaAluno("B", 3.0),
                new NotaAluno("C", 6.0),
                new NotaAluno("D", 3.0)
        };
        NotaAluno[] bubble = original.clone();
        NotaAluno[] selection = original.clone();
        NotaAluno[] insertion = original.clone();

        BubbleSortNotas.ordenar(bubble);
        SelectionSortNotas.ordenar(selection);
        InsertionSortNotas.ordenar(insertion);

        for (int i = 0; i < original.length; i++) {
            verificar(bubble[i].getAluno().equals(selection[i].getAluno()),
                    "Bubble e Selection deveriam produzir a mesma ordem.");
            verificar(bubble[i].getAluno().equals(insertion[i].getAluno()),
                    "Bubble e Insertion deveriam produzir a mesma ordem.");
        }
    }

    private static void testarCasosDeErro() {
        esperarErro(() -> BubbleSortNotas.ordenar(null), "vetor nulo");
        esperarErro(() -> BubbleSortNotas.ordenar(new NotaAluno[] { null }), "aluno nulo");
        esperarErro(() -> new NotaAluno("", 7.0), "nome vazio");
        esperarErro(() -> new NotaAluno("Ana", 10.1), "nota acima de 10");
        esperarErro(() -> ordenarTurmaCom31Alunos(), "turma acima do limite");

        EstatisticasOrdenacao vazio = BubbleSortNotas.ordenar(new NotaAluno[0]);
        verificar(vazio.getComparacoes() == 0 && vazio.getTrocas() == 0,
                "Vetor vazio deveria ter zero comparacoes e trocas.");
    }

    private static void testarLimiteValido() {
        NotaAluno[] turma = new NotaAluno[BubbleSortNotas.MAX_ALUNOS];
        for (int i = 0; i < turma.length; i++) {
            turma[i] = new NotaAluno("Aluno " + i, i % 11);
        }

        BubbleSortNotas.ordenar(turma);
        verificar(turma.length == 30, "Uma turma com exatamente 30 alunos deveria ser aceita.");
    }

    private static void ordenarTurmaCom31Alunos() {
        NotaAluno[] turma = new NotaAluno[31];
        for (int i = 0; i < turma.length; i++) {
            turma[i] = new NotaAluno("Aluno " + i, 5.0);
        }
        BubbleSortNotas.ordenar(turma);
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
