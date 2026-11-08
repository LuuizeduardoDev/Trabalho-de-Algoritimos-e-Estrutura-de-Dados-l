/** Testes executaveis do editor e da pilha de acoes. */
public class TesteEditorTexto {
    public static void main(String[] args) {
        testarLifoDaPilha();
        testarOperacoesEUndo();
        testarErros();
        System.out.println("Todos os testes do Problema 2 foram aprovados.");
    }

    private static void testarLifoDaPilha() {
        PilhaAcoes pilha = new PilhaAcoes();
        EstadoEditor estado = new EstadoEditor("", FormatoTexto.NORMAL);
        Acao primeira = new Acao(TipoAcao.DIGITACAO, "primeira", estado,
                new EstadoEditor("a", FormatoTexto.NORMAL));
        Acao segunda = new Acao(TipoAcao.EXCLUSAO, "segunda", estado,
                new EstadoEditor("b", FormatoTexto.NORMAL));

        pilha.push(primeira);
        pilha.push(segunda);
        verificar(pilha.tamanho() == 2, "push deve aumentar o tamanho");
        verificar(pilha.pop() == segunda, "pop deve remover a acao mais recente");
        verificar(pilha.pop() == primeira, "pop deve seguir a ordem LIFO");
        verificar(pilha.estaVazia(), "a pilha deve ficar vazia");
    }

    private static void testarOperacoesEUndo() {
        EditorTexto editor = new EditorTexto();
        editor.digitar("Ola");
        editor.digitar(" mundo");
        editor.formatar(FormatoTexto.MAIUSCULAS);
        verificar(editor.getTexto().equals("OLA MUNDO"), "formatacao deve alterar o texto");
        verificar(editor.quantidadeAcoes() == 3, "cada operacao deve ser registrada");

        verificar(editor.desfazer(), "deve desfazer a formatacao");
        verificar(editor.getTexto().equals("Ola mundo"), "undo deve restaurar o texto anterior");
        verificar(editor.getFormato() == FormatoTexto.NORMAL,
                "undo deve restaurar o formato anterior");

        editor.excluir(3, 9);
        verificar(editor.getTexto().equals("Ola"), "exclusao deve remover o intervalo");
        verificar(editor.desfazer(), "deve desfazer a exclusao");
        verificar(editor.getTexto().equals("Ola mundo"), "undo da exclusao deve restaurar o texto");

        verificar(editor.desfazer(), "deve desfazer a digitacao mais recente");
        verificar(editor.getTexto().equals("Ola"), "undo deve voltar ao estado anterior");
        verificar(editor.desfazer(), "deve desfazer a primeira digitacao");
        verificar(editor.getTexto().isEmpty(), "o editor deve voltar a ficar vazio");
        verificar(!editor.desfazer(), "undo sem historico deve retornar false");
    }

    private static void testarErros() {
        EditorTexto editor = new EditorTexto();
        verificarExcecao(() -> editor.digitar(null), "digitacao null");
        verificarExcecao(() -> editor.digitar(""), "digitacao vazia");
        verificarExcecao(() -> editor.excluir(0, 1), "exclusao fora do texto");
        verificarExcecao(() -> editor.formatar(null), "formato null");

        PilhaAcoes pilha = new PilhaAcoes();
        verificarExcecao(pilha::pop, "pop de pilha vazia");
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
        } catch (IllegalArgumentException | IndexOutOfBoundsException | IllegalStateException excecao) {
            // Comportamento esperado para dados invalidos.
        }
    }
}
