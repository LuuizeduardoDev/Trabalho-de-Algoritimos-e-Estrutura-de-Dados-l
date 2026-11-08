/**
 * Fila generica implementada manualmente com nos encadeados.
 * A fila segue o comportamento FIFO: o primeiro elemento inserido
 * e o primeiro elemento removido.
 */
public class Fila<T> {
    private static class No<T> {
        private final T elemento;
        private No<T> proximo;

        private No(T elemento) {
            this.elemento = elemento;
        }
    }

    private No<T> inicio;
    private No<T> fim;
    private int quantidade;

    /** Insere um elemento no final da fila. */
    public void enqueue(T elemento) {
        if (elemento == null) {
            throw new IllegalArgumentException("Nao e permitido inserir null na fila.");
        }

        No<T> novoNo = new No<>(elemento);

        if (isEmpty()) {
            inicio = novoNo;
            fim = novoNo;
        } else {
            fim.proximo = novoNo;
            fim = novoNo;
        }

        quantidade++;
    }

    /** Remove e retorna o elemento que esta no inicio da fila. */
    public T dequeue() {
        verificarFilaNaoVazia();

        T elemento = inicio.elemento;
        inicio = inicio.proximo;
        quantidade--;

        if (quantidade == 0) {
            fim = null;
        }

        return elemento;
    }

    /** Retorna o primeiro elemento sem remove-lo. */
    public T front() {
        verificarFilaNaoVazia();
        return inicio.elemento;
    }

    /** Indica se a fila nao possui elementos. */
    public boolean isEmpty() {
        return quantidade == 0;
    }

    /** Retorna a quantidade atual de elementos. */
    public int size() {
        return quantidade;
    }

    private void verificarFilaNaoVazia() {
        if (isEmpty()) {
            throw new IllegalStateException("A fila esta vazia.");
        }
    }
}
