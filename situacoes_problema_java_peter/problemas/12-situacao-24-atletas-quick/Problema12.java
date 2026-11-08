/** Executa a demonstracao da classificacao final e do podio da corrida. */
public class Problema12 {

    public static void main(String[] args) {
        Atleta[] atletas = criarAtletasDaDemonstracao();

        QuickSortAtletas.ordenar(atletas);
        imprimirClassificacao(atletas);
        imprimirPodio(atletas);
    }

    public static void imprimirClassificacao(Atleta[] atletas) {
        if (atletas == null) {
            throw new IllegalArgumentException("O vetor de atletas nao pode ser nulo.");
        }

        System.out.println("Classificacao final:");
        for (int indice = 0; indice < atletas.length; indice++) {
            System.out.printf("%2do lugar - %s%n", indice + 1, atletas[indice]);
        }
    }

    public static void imprimirPodio(Atleta[] atletas) {
        if (atletas == null) {
            throw new IllegalArgumentException("O vetor de atletas nao pode ser nulo.");
        }

        int quantidadeNoPodio = Math.min(3, atletas.length);
        System.out.println("\nPodio:");
        for (int indice = 0; indice < quantidadeNoPodio; indice++) {
            System.out.printf("%do lugar - %s%n", indice + 1, atletas[indice]);
        }
        if (quantidadeNoPodio == 0) {
            System.out.println("Nao ha atletas classificados.");
        }
    }

    private static Atleta[] criarAtletasDaDemonstracao() {
        return new Atleta[] {
            new Atleta("Ana", 62.41),
            new Atleta("Bruno", 60.12),
            new Atleta("Carla", 64.70),
            new Atleta("Diego", 59.88),
            new Atleta("Elisa", 61.03),
            new Atleta("Fabio", 63.25),
            new Atleta("Gabriela", 58.92),
            new Atleta("Henrique", 65.10),
            new Atleta("Isabela", 60.12),
            new Atleta("Joao", 66.44),
            new Atleta("Karen", 62.09),
            new Atleta("Lucas", 59.88),
            new Atleta("Marina", 67.31),
            new Atleta("Nicolas", 61.77),
            new Atleta("Olivia", 63.90),
            new Atleta("Paulo", 57.84),
            new Atleta("Quenia", 64.11),
            new Atleta("Rafael", 60.85),
            new Atleta("Sara", 62.88),
            new Atleta("Tiago", 68.02),
            new Atleta("Ursula", 58.41),
            new Atleta("Victor", 61.41),
            new Atleta("Wesley", 63.02),
            new Atleta("Xavier", 66.02),
            new Atleta("Yara", 59.20),
            new Atleta("Zeca", 65.75),
            new Atleta("Alice", 62.41),
            new Atleta("Breno", 60.50),
            new Atleta("Cintia", 64.70),
            new Atleta("Davi", 58.75)
        };
    }
}
