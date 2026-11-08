/** Demonstracao do sistema de desfazer com 12 acoes. */
public class Problema2 {
    public static void main(String[] args) {
        EditorTexto editor = new EditorTexto();

        System.out.println("=== Acoes realizadas ===");
        executar("1. ", editor, () -> editor.digitar("Ola"));
        executar("2. ", editor, () -> editor.digitar(", mundo"));
        executar("3. ", editor, () -> editor.digitar("!"));
        executar("4. ", editor, () -> editor.formatar(FormatoTexto.MAIUSCULAS));
        executar("5. ", editor, () -> editor.digitar(" Bem-vindo"));
        executar("6. ", editor, () -> editor.excluir(10, 11));
        executar("7. ", editor, () -> editor.formatar(FormatoTexto.MINUSCULAS));
        executar("8. ", editor, () -> editor.digitar(" ao editor"));
        executar("9. ", editor, () -> editor.excluir(0, 4));
        executar("10. ", editor, () -> editor.formatar(FormatoTexto.MAIUSCULAS));
        executar("11. ", editor, () -> editor.digitar("!"));
        executar("12. ", editor, () -> editor.formatar(FormatoTexto.MINUSCULAS));

        System.out.println("\n=== Desfazendo passo a passo ===");
        while (editor.podeDesfazer()) {
            editor.desfazer();
            System.out.println("Desfeito -> " + editor.getEstadoAtual());
        }

        System.out.println("Sem mais acoes para desfazer: " + !editor.desfazer());
    }

    private static void executar(String prefixo, EditorTexto editor, Runnable acao) {
        acao.run();
        System.out.println(prefixo + editor.getEstadoAtual());
    }
}
