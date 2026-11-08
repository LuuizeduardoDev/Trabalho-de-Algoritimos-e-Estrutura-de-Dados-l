/** Executa a demonstracao da ordenacao de notas de uma turma pequena. */
public class Problema8 {
    public static void main(String[] args) {
        NotaAluno[] turma = {
                new NotaAluno("Ana", 7.5),
                new NotaAluno("Bruno", 5.0),
                new NotaAluno("Carla", 9.0),
                new NotaAluno("Diego", 6.5),
                new NotaAluno("Elisa", 8.0),
                new NotaAluno("Fabio", 5.0),
                new NotaAluno("Gabriela", 10.0),
                new NotaAluno("Henrique", 4.5)
        };

        System.out.println("=== Ordenacao de notas da turma ===");
        System.out.println("Notas originais:");
        imprimir(turma);

        NotaAluno[] notasBubble = turma.clone();
        EstatisticasOrdenacao bubble = BubbleSortNotas.ordenar(notasBubble);
        System.out.println("\nNotas ordenadas pelo Bubble Sort otimizado:");
        imprimir(notasBubble);
        System.out.println("Estatisticas: " + bubble);

        EstatisticasOrdenacao selection = SelectionSortNotas.ordenar(turma.clone());
        EstatisticasOrdenacao insertion = InsertionSortNotas.ordenar(turma.clone());
        System.out.println("\nComparacao com outros algoritmos:");
        System.out.println("- Bubble Sort otimizado: " + bubble);
        System.out.println("- Selection Sort:       " + selection);
        System.out.println("- Insertion Sort:       " + insertion);
    }

    private static void imprimir(NotaAluno[] notas) {
        for (NotaAluno nota : notas) {
            System.out.println("- " + nota);
        }
    }
}
