/** Programa demonstrativo do problema 9. */
public class Problema9 {
    public static void main(String[] args) {
        int n = 5;

        try {
            if (args.length > 1) {
                throw new IllegalArgumentException("Informe no maximo um argumento: N.");
            }
            if (args.length == 1) {
                n = Integer.parseInt(args[0]);
            }

            Candidato[] candidatos = criarCandidatosDeExemplo();
            SelectionSort.ordenar(candidatos);
            Candidato[] melhores = SelectionSort.extrairTopN(candidatos, n);

            System.out.println("Candidatos ordenados por pontuacao (decrescente):");
            imprimir(candidatos);
            System.out.println("\nTop-" + n + ":");
            imprimir(melhores);
        } catch (NumberFormatException e) {
            System.out.println("Erro: N deve ser um numero inteiro.");
        } catch (IllegalArgumentException e) {
            System.out.println("Erro: " + e.getMessage());
        }
    }

    private static Candidato[] criarCandidatosDeExemplo() {
        return new Candidato[] {
                new Candidato("Ana Souza", 82.5),
                new Candidato("Bruno Lima", 91.0),
                new Candidato("Carla Mendes", 76.5),
                new Candidato("Diego Alves", 88.0),
                new Candidato("Eduarda Rocha", 95.5),
                new Candidato("Felipe Costa", 84.0),
                new Candidato("Gabriela Martins", 91.0),
                new Candidato("Henrique Silva", 73.5),
                new Candidato("Isabela Nunes", 89.5),
                new Candidato("Joao Pereira", 68.0),
                new Candidato("Karen Oliveira", 87.0),
                new Candidato("Lucas Ferreira", 79.0),
                new Candidato("Mariana Santos", 95.5),
                new Candidato("Nicolas Barros", 81.0),
                new Candidato("Patricia Gomes", 90.0)
        };
    }

    private static void imprimir(Candidato[] candidatos) {
        for (int i = 0; i < candidatos.length; i++) {
            System.out.println((i + 1) + ". " + candidatos[i]);
        }
    }
}
