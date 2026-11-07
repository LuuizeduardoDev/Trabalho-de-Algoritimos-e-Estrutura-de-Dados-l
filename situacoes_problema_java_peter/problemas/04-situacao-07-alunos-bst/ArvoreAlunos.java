public class ArvoreAlunos {
    private No raiz;
    private int quantidade;

    private static class No {
        private Aluno aluno;
        private No esquerda;
        private No direita;

        private No(Aluno aluno) {
            this.aluno = aluno;
        }
    }

    /**
     * Insere o aluno mantendo a regra da BST: menores a esquerda e maiores a direita.
     * Uma matricula repetida nao e inserida.
     */
    public boolean inserir(Aluno aluno) {
        if (aluno == null) {
            throw new IllegalArgumentException("O aluno nao pode ser nulo.");
        }

        if (raiz == null) {
            raiz = new No(aluno);
            quantidade++;
            return true;
        }

        No atual = raiz;
        while (true) {
            if (aluno.getMatricula() == atual.aluno.getMatricula()) {
                return false;
            }

            if (aluno.getMatricula() < atual.aluno.getMatricula()) {
                if (atual.esquerda == null) {
                    atual.esquerda = new No(aluno);
                    quantidade++;
                    return true;
                }
                atual = atual.esquerda;
            } else {
                if (atual.direita == null) {
                    atual.direita = new No(aluno);
                    quantidade++;
                    return true;
                }
                atual = atual.direita;
            }
        }
    }

    /** Retorna o aluno da matricula informada ou null quando ela nao existe. */
    public Aluno buscar(int matricula) {
        No atual = raiz;
        while (atual != null) {
            if (matricula == atual.aluno.getMatricula()) {
                return atual.aluno;
            }
            atual = matricula < atual.aluno.getMatricula()
                    ? atual.esquerda
                    : atual.direita;
        }
        return null;
    }

    /** Remove a matricula informada e retorna false quando ela nao existe. */
    public boolean remover(int matricula) {
        int quantidadeAntes = quantidade;
        raiz = remover(raiz, matricula);
        return quantidade < quantidadeAntes;
    }

    private No remover(No no, int matricula) {
        if (no == null) {
            return null;
        }

        if (matricula < no.aluno.getMatricula()) {
            no.esquerda = remover(no.esquerda, matricula);
        } else if (matricula > no.aluno.getMatricula()) {
            no.direita = remover(no.direita, matricula);
        } else {
            if (no.esquerda == null) {
                quantidade--;
                return no.direita;
            }
            if (no.direita == null) {
                quantidade--;
                return no.esquerda;
            }

            // Com dois filhos, o sucessor e o menor elemento da subarvore direita.
            No sucessor = menorNo(no.direita);
            no.aluno = sucessor.aluno;
            no.direita = removerSucessor(no.direita);
        }
        return no;
    }

    private No menorNo(No no) {
        while (no.esquerda != null) {
            no = no.esquerda;
        }
        return no;
    }

    private No removerSucessor(No no) {
        if (no.esquerda == null) {
            quantidade--;
            return no.direita;
        }
        no.esquerda = removerSucessor(no.esquerda);
        return no;
    }

    public boolean estaVazia() {
        return raiz == null;
    }

    public int tamanho() {
        return quantidade;
    }

    /** Imprime os alunos em ordem crescente de matricula. */
    public void listarEmOrdem() {
        listarEmOrdem(raiz);
    }

    private void listarEmOrdem(No no) {
        if (no == null) {
            return;
        }
        listarEmOrdem(no.esquerda);
        System.out.println(no.aluno);
        listarEmOrdem(no.direita);
    }
}
