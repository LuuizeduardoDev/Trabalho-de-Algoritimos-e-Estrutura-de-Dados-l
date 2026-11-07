/** Testes simples e executaveis da estrutura Fila. */
public class TesteFila {
    public static void main(String[] args) {
        Fila<String> fila = new Fila<>();

        verificar(fila.isEmpty(), "uma fila nova deve estar vazia");
        verificar(fila.size() == 0, "o tamanho inicial deve ser zero");

        fila.enqueue("Ana");
        fila.enqueue("Bruno");
        verificar(!fila.isEmpty(), "a fila deve deixar de estar vazia apos enqueue");
        verificar(fila.size() == 2, "o tamanho deve ser atualizado apos dois enqueue");
        verificar(fila.front().equals("Ana"), "front deve retornar o primeiro elemento");
        verificar(fila.size() == 2, "front nao deve remover o elemento");

        verificar(fila.dequeue().equals("Ana"), "dequeue deve respeitar FIFO");
        verificar(fila.dequeue().equals("Bruno"), "dequeue deve retornar o segundo elemento depois do primeiro");
        verificar(fila.isEmpty(), "a fila deve estar vazia apos remover todos os elementos");
        verificar(fila.size() == 0, "o tamanho final deve ser zero");

        verificarExcecao(() -> fila.front(), "front em fila vazia");
        verificarExcecao(() -> fila.dequeue(), "dequeue em fila vazia");

        System.out.println("Todos os testes da Fila foram aprovados.");
    }

    private static void verificar(boolean condicao, String descricao) {
        if (!condicao) {
            throw new AssertionError("Falha: " + descricao);
        }
    }

    private static void verificarExcecao(Runnable acao, String descricao) {
        try {
            acao.run();
            throw new AssertionError("Falha: era esperada uma excecao em " + descricao);
        } catch (IllegalStateException excecao) {
            // Comportamento esperado para front e dequeue em fila vazia.
        }
    }
}
