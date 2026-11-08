import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Scanner;

/**
 * Ponto de entrada central para as demonstracoes e testes dos 12 problemas.
 *
 * Esta classe apenas chama os programas que ja existem em cada problema.
 * A logica das estruturas e algoritmos permanece nas classes originais.
 */
public class Main {
    private static final Programa[] PROGRAMAS = {
            new Programa(1, "Atendimento de uma clinica", "Clinica", "TesteFila"),
            new Programa(2, "Editor de texto com undo", "Problema2", "TesteEditorTexto"),
            new Programa(3, "Gerenciamento de playlist", "PlaylistApp", "TestePlaylist"),
            new Programa(4, "Cadastro de alunos em BST", "Problema4", "TesteArvoreAlunos"),
            new Programa(5, "Indice de CPF com arvore AVL", "SistemaRH", "TesteArvoreAVL"),
            new Programa(6, "Roteamento com Dijkstra", "Problema6", "TesteDijkstra"),
            new Programa(7, "Frequencia de palavras com tabela hash", "Problema7", "TesteTabelaHash"),
            new Programa(8, "Ordenacao de notas com Bubble Sort", "Problema8", "TesteOrdenacaoNotas"),
            new Programa(9, "Selecao de candidatos", "Problema9", "TesteSelecaoCandidatos"),
            new Programa(10, "Insercao ordenada de cartas", "Problema10", "TesteMaoCartas"),
            new Programa(11, "Ordenacao de transacoes com Merge Sort", "Problema11", "TesteMergeSortTransacoes"),
            new Programa(12, "Classificacao de atletas com Quick Sort", "Problema12", "TesteQuickSortAtletas")
    };

    public static void main(String[] args) {
        if (args.length > 0) {
            executarArgumento(args[0]);
            return;
        }

        try (Scanner scanner = new Scanner(System.in)) {
            executarMenu(scanner);
        }
    }

    private static void executarMenu(Scanner scanner) {
        while (true) {
            exibirMenu();
            int opcao = lerInteiro(scanner);

            if (opcao == 0) {
                System.out.println("Programa encerrado.");
                return;
            }

            if (opcao >= 1 && opcao <= PROGRAMAS.length) {
                executarDemonstracao(PROGRAMAS[opcao - 1]);
            } else if (opcao == 13) {
                executarTodosOsTestes();
            } else if (opcao == 14) {
                executarTodasAsDemonstracoes();
            } else {
                System.out.println("Opcao invalida. Escolha uma opcao do menu.");
            }

            System.out.println("\nPressione ENTER para voltar ao menu...");
            scanner.nextLine();
        }
    }

    private static void exibirMenu() {
        System.out.println("\n===============================================");
        System.out.println("  TRABALHO DE ALGORITMOS E ESTRUTURAS DE DADOS");
        System.out.println("===============================================");
        System.out.println("Escolha uma demonstracao:");
        for (Programa programa : PROGRAMAS) {
            System.out.printf("%2d - %s%n", programa.numero, programa.descricao);
        }
        System.out.println("13 - Executar testes automatizados de todos os problemas");
        System.out.println("14 - Executar todas as demonstracoes");
        System.out.println(" 0 - Sair");
        System.out.print("Opcao: ");
    }

    private static int lerInteiro(Scanner scanner) {
        while (true) {
            String linha = scanner.nextLine().trim();
            try {
                return Integer.parseInt(linha);
            } catch (NumberFormatException excecao) {
                System.out.print("Digite um numero valido: ");
            }
        }
    }

    private static void executarArgumento(String argumento) {
        if (argumento.equalsIgnoreCase("testes")) {
            executarTodosOsTestes();
            return;
        }
        if (argumento.equalsIgnoreCase("demonstracoes")) {
            executarTodasAsDemonstracoes();
            return;
        }

        try {
            int numero = Integer.parseInt(argumento);
            if (numero >= 1 && numero <= PROGRAMAS.length) {
                executarDemonstracao(PROGRAMAS[numero - 1]);
            } else {
                exibirAjudaArgumentos();
            }
        } catch (NumberFormatException excecao) {
            exibirAjudaArgumentos();
        }
    }

    private static void executarTodosOsTestes() {
        int aprovados = 0;
        System.out.println("\n=== TESTES AUTOMATIZADOS ===");
        for (Programa programa : PROGRAMAS) {
            System.out.println("\n--- Problema " + programa.numero + " ---");
            if (executarClasse(programa.classeTeste)) {
                aprovados++;
            }
        }
        System.out.printf("\nResumo: %d de %d conjuntos de testes executados sem falha.%n",
                aprovados, PROGRAMAS.length);
    }

    private static void executarTodasAsDemonstracoes() {
        System.out.println("\n=== TODAS AS DEMONSTRACOES ===");
        for (Programa programa : PROGRAMAS) {
            executarDemonstracao(programa);
        }
    }

    private static void executarDemonstracao(Programa programa) {
        System.out.println("\n=== Problema " + programa.numero + ": " + programa.descricao + " ===");
        executarClasse(programa.classeDemonstracao);
    }

    /** Executa uma classe que possui um metodo main(String[]). */
    private static boolean executarClasse(String nomeClasse) {
        try {
            Class<?> classe = Class.forName(nomeClasse);
            Method metodoMain = classe.getMethod("main", String[].class);
            metodoMain.invoke(null, (Object) new String[0]);
            return true;
        } catch (ClassNotFoundException excecao) {
            System.out.println("Classe nao encontrada: " + nomeClasse);
        } catch (NoSuchMethodException excecao) {
            System.out.println("A classe nao possui main(String[]): " + nomeClasse);
        } catch (IllegalAccessException excecao) {
            System.out.println("Nao foi possivel acessar a classe: " + nomeClasse);
        } catch (InvocationTargetException excecao) {
            Throwable causa = excecao.getCause();
            System.out.println("FALHA durante " + nomeClasse + ": "
                    + causa.getClass().getSimpleName() + " - " + causa.getMessage());
            return false;
        }
        return false;
    }

    private static void exibirAjudaArgumentos() {
        System.out.println("Uso: java -cp out Main");
        System.out.println("Ou:  java -cp out Main <numero do problema>");
        System.out.println("     java -cp out Main testes");
        System.out.println("     java -cp out Main demonstracoes");
    }

    private static final class Programa {
        private final int numero;
        private final String descricao;
        private final String classeDemonstracao;
        private final String classeTeste;

        private Programa(int numero, String descricao, String classeDemonstracao,
                         String classeTeste) {
            this.numero = numero;
            this.descricao = descricao;
            this.classeDemonstracao = classeDemonstracao;
            this.classeTeste = classeTeste;
        }
    }
}
