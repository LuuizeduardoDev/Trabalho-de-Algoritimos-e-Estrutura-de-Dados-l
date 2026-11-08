public class Problema4 {
    public static void main(String[] args) {
        ArvoreAlunos arvore = new ArvoreAlunos();

        Aluno[] alunos = {
            new Aluno(202310, "Ana Souza", "Sistemas de Informacao"),
            new Aluno(202305, "Bruno Lima", "Engenharia de Software"),
            new Aluno(202315, "Carla Mendes", "Ciencia da Computacao"),
            new Aluno(202302, "Diego Alves", "Sistemas de Informacao"),
            new Aluno(202308, "Elisa Rocha", "Analise e Desenvolvimento de Sistemas"),
            new Aluno(202312, "Fabio Costa", "Engenharia de Software"),
            new Aluno(202318, "Gabriela Santos", "Ciencia da Computacao"),
            new Aluno(202301, "Heitor Martins", "Sistemas de Informacao"),
            new Aluno(202304, "Isabela Dias", "Administracao"),
            new Aluno(202306, "Joao Ferreira", "Engenharia de Software"),
            new Aluno(202307, "Karina Oliveira", "Ciencia da Computacao"),
            new Aluno(202309, "Lucas Ribeiro", "Sistemas de Informacao"),
            new Aluno(202311, "Mariana Gomes", "Engenharia de Software"),
            new Aluno(202313, "Nicolas Martins", "Ciencia da Computacao"),
            new Aluno(202314, "Olivia Cardoso", "Sistemas de Informacao"),
            new Aluno(202316, "Paulo Nunes", "Administracao"),
            new Aluno(202317, "Quezia Barros", "Engenharia de Software"),
            new Aluno(202319, "Rafael Teixeira", "Ciencia da Computacao"),
            new Aluno(202320, "Sofia Castro", "Sistemas de Informacao"),
            new Aluno(202321, "Tiago Araujo", "Engenharia de Software")
        };

        for (Aluno aluno : alunos) {
            arvore.inserir(aluno);
        }

        System.out.println("=== Cadastro concluido ===");
        System.out.println("Total de alunos: " + arvore.tamanho());

        System.out.println("\n=== Buscas ===");
        exibirBusca(arvore, 202315);
        exibirBusca(arvore, 202399);

        System.out.println("\n=== Listagem em ordem antes da remocao ===");
        arvore.listarEmOrdem();

        System.out.println("\n=== Remocoes ===");
        exibirRemocao(arvore, 202305);
        exibirRemocao(arvore, 202399);

        System.out.println("\n=== Listagem em ordem depois da remocao ===");
        arvore.listarEmOrdem();
    }

    private static void exibirBusca(ArvoreAlunos arvore, int matricula) {
        Aluno aluno = arvore.buscar(matricula);
        if (aluno == null) {
            System.out.println("Matricula " + matricula + " nao encontrada.");
        } else {
            System.out.println("Aluno encontrado: " + aluno);
        }
    }

    private static void exibirRemocao(ArvoreAlunos arvore, int matricula) {
        if (arvore.remover(matricula)) {
            System.out.println("Matricula " + matricula + " removida com sucesso.");
        } else {
            System.out.println("Nao foi possivel remover: matricula " + matricula + " inexistente.");
        }
    }
}
