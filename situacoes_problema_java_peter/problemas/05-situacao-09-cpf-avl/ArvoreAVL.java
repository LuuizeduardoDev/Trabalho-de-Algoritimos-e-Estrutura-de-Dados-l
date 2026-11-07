/**
 * Arvore AVL para indexar funcionarios pelo CPF.
 * A altura armazenada em cada no comeca em 1; uma arvore vazia tem altura 0.
 */
public class ArvoreAVL {
    private static class No {
        private Funcionario funcionario;
        private No esquerdo;
        private No direito;
        private int altura;

        private No(Funcionario funcionario) {
            this.funcionario = funcionario;
            this.altura = 1;
        }
    }

    private No raiz;
    private int quantidade;

    /** Insere um funcionario e realiza as rotacoes necessarias. */
    public void inserir(Funcionario funcionario) {
        if (funcionario == null) {
            throw new IllegalArgumentException("Nao e permitido inserir funcionario null.");
        }

        raiz = inserir(raiz, funcionario);
        quantidade++;
    }

    /** Busca um funcionario pelo CPF. Retorna null quando a chave nao existe. */
    public Funcionario buscar(String cpf) {
        validarCpf(cpf);
        No no = buscarNo(raiz, cpf);
        return no == null ? null : no.funcionario;
    }

    /** Remove um funcionario. Retorna false quando o CPF nao esta cadastrado. */
    public boolean remover(String cpf) {
        validarCpf(cpf);
        if (buscarNo(raiz, cpf) == null) {
            return false;
        }

        raiz = remover(raiz, cpf);
        quantidade--;
        return true;
    }

    /** Retorna a altura da arvore. */
    public int altura() {
        return altura(raiz);
    }

    /** Retorna o fator de balanceamento da raiz. */
    public int fatorBalanceamento() {
        return fator(raiz);
    }

    /** Retorna o fator de balanceamento do no identificado pelo CPF. */
    public int fatorBalanceamento(String cpf) {
        validarCpf(cpf);
        No no = buscarNo(raiz, cpf);
        if (no == null) {
            throw new IllegalArgumentException("CPF nao encontrado: " + cpf);
        }
        return fator(no);
    }

    /** Verifica se todos os nos respeitam o limite de balanceamento da AVL. */
    public boolean estaBalanceada() {
        return estaBalanceada(raiz);
    }

    /** Retorna a quantidade de funcionarios armazenados. */
    public int tamanho() {
        return quantidade;
    }

    /** Retorna o CPF da raiz, principalmente para testes das rotacoes. */
    public String getCpfRaiz() {
        return raiz == null ? null : raiz.funcionario.getCpf();
    }

    /** Retorna os funcionarios em ordem crescente de CPF. */
    public Funcionario[] listarEmOrdem() {
        Funcionario[] resultado = new Funcionario[quantidade];
        preencherEmOrdem(raiz, resultado, new int[] { 0 });
        return resultado;
    }

    /** Monta um relatorio simples com o fator de cada no em ordem de CPF. */
    public String relatorioBalanceamento() {
        StringBuilder relatorio = new StringBuilder();
        adicionarRelatorio(raiz, relatorio);
        return relatorio.toString();
    }

    private No inserir(No no, Funcionario funcionario) {
        if (no == null) {
            return new No(funcionario);
        }

        int comparacao = funcionario.getCpf().compareTo(no.funcionario.getCpf());
        if (comparacao < 0) {
            no.esquerdo = inserir(no.esquerdo, funcionario);
        } else if (comparacao > 0) {
            no.direito = inserir(no.direito, funcionario);
        } else {
            throw new IllegalArgumentException(
                    "Ja existe funcionario cadastrado com o CPF " + funcionario.getCpf() + ".");
        }

        atualizarAltura(no);
        return balancear(no);
    }

    private No remover(No no, String cpf) {
        if (no == null) {
            return null;
        }

        int comparacao = cpf.compareTo(no.funcionario.getCpf());
        if (comparacao < 0) {
            no.esquerdo = remover(no.esquerdo, cpf);
        } else if (comparacao > 0) {
            no.direito = remover(no.direito, cpf);
        } else {
            if (no.esquerdo == null) {
                return no.direito;
            }
            if (no.direito == null) {
                return no.esquerdo;
            }

            No sucessor = menorNo(no.direito);
            no.funcionario = sucessor.funcionario;
            no.direito = remover(no.direito, sucessor.funcionario.getCpf());
        }

        atualizarAltura(no);
        return balancear(no);
    }

    private No balancear(No no) {
        int fator = fator(no);

        if (fator > 1) {
            if (fator(no.esquerdo) < 0) {
                no.esquerdo = rotacaoEsquerda(no.esquerdo);
            }
            return rotacaoDireita(no);
        }

        if (fator < -1) {
            if (fator(no.direito) > 0) {
                no.direito = rotacaoDireita(no.direito);
            }
            return rotacaoEsquerda(no);
        }

        return no;
    }

    private No rotacaoDireita(No no) {
        No novaRaiz = no.esquerdo;
        No subarvoreMovida = novaRaiz.direito;

        novaRaiz.direito = no;
        no.esquerdo = subarvoreMovida;

        atualizarAltura(no);
        atualizarAltura(novaRaiz);
        return novaRaiz;
    }

    private No rotacaoEsquerda(No no) {
        No novaRaiz = no.direito;
        No subarvoreMovida = novaRaiz.esquerdo;

        novaRaiz.esquerdo = no;
        no.direito = subarvoreMovida;

        atualizarAltura(no);
        atualizarAltura(novaRaiz);
        return novaRaiz;
    }

    private No buscarNo(No no, String cpf) {
        if (no == null) {
            return null;
        }

        int comparacao = cpf.compareTo(no.funcionario.getCpf());
        if (comparacao == 0) {
            return no;
        }
        return comparacao < 0
                ? buscarNo(no.esquerdo, cpf)
                : buscarNo(no.direito, cpf);
    }

    private No menorNo(No no) {
        No atual = no;
        while (atual.esquerdo != null) {
            atual = atual.esquerdo;
        }
        return atual;
    }

    private boolean estaBalanceada(No no) {
        if (no == null) {
            return true;
        }

        return Math.abs(fator(no)) <= 1
                && altura(no) == 1 + maior(altura(no.esquerdo), altura(no.direito))
                && estaBalanceada(no.esquerdo)
                && estaBalanceada(no.direito);
    }

    private void preencherEmOrdem(No no, Funcionario[] resultado, int[] indice) {
        if (no == null) {
            return;
        }

        preencherEmOrdem(no.esquerdo, resultado, indice);
        resultado[indice[0]++] = no.funcionario;
        preencherEmOrdem(no.direito, resultado, indice);
    }

    private void adicionarRelatorio(No no, StringBuilder relatorio) {
        if (no == null) {
            return;
        }

        adicionarRelatorio(no.esquerdo, relatorio);
        relatorio.append(no.funcionario.getCpf())
                .append(" -> fator ")
                .append(fator(no))
                .append(System.lineSeparator());
        adicionarRelatorio(no.direito, relatorio);
    }

    private void atualizarAltura(No no) {
        no.altura = 1 + maior(altura(no.esquerdo), altura(no.direito));
    }

    private int fator(No no) {
        return no == null ? 0 : altura(no.esquerdo) - altura(no.direito);
    }

    private int altura(No no) {
        return no == null ? 0 : no.altura;
    }

    private int maior(int primeiro, int segundo) {
        return primeiro > segundo ? primeiro : segundo;
    }

    private void validarCpf(String cpf) {
        if (cpf == null || !cpf.matches("[0-9]{11}")) {
            throw new IllegalArgumentException(
                    "O CPF deve conter exatamente 11 digitos, sem pontuacao.");
        }
    }
}
