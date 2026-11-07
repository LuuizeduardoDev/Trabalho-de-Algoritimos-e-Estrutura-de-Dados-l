/** Pilha manual de acoes, com comportamento LIFO. */
public class PilhaAcoes {
    private static class No {
        private final Acao acao;
        private No abaixo;

        private No(Acao acao, No abaixo) {
            this.acao = acao;
            this.abaixo = abaixo;
        }
    }

    private No topo;
    private int tamanho;

    /** Coloca uma acao no topo da pilha. */
    public void push(Acao acao) {
        if (acao == null) {
            throw new IllegalArgumentException("A pilha nao aceita acao null.");
        }
        topo = new No(acao, topo);
        tamanho++;
    }

    /** Remove e retorna a acao mais recente. */
    public Acao pop() {
        if (estaVazia()) {
            throw new IllegalStateException("Nao ha acoes para remover da pilha.");
        }
        Acao acao = topo.acao;
        topo = topo.abaixo;
        tamanho--;
        return acao;
    }

    public boolean estaVazia() {
        return topo == null;
    }

    public int tamanho() {
        return tamanho;
    }
}
