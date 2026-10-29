
package problema_03;

import java.util.Stack;

public class editor_text {

    // Armazena as informações de cada ação realizada.
    static class Acao {
        String tipo;
        String conteudo;

        String textoAnterior;
        boolean textoAnteriorNegrito;

        String textoNovo;
        boolean textoNovoNegrito;

        Acao(String tipo, String conteudo, String textoAnterior,
             boolean textoAnteriorNegrito) {

            this.tipo = tipo;
            this.conteudo = conteudo;
            this.textoAnterior = textoAnterior;
            this.textoAnteriorNegrito = textoAnteriorNegrito;
        }
    }

    static class TextoEditor {
        String texto = "";
        boolean negrito = false;

        Stack<Acao> undoStack = new Stack<>();
        Stack<Acao> redoStack = new Stack<>();

        // Executa uma ação e salva seu estado para permitir undo.
        void executarAcao(String tipo, String conteudo) {

            Acao acao = new Acao(tipo, conteudo, texto, negrito);

            switch (tipo) {
                case "TIPO":
                    texto += conteudo;
                    break;

                case "APAGAR":
                    if (texto.endsWith(conteudo)) {
                        texto = texto.substring(
                            0, texto.length() - conteudo.length()
                        );
                    } else {
                        System.out.println(
                            "Não foi possível apagar: sufixo não encontrado."
                        );
                        return;
                    }
                    break;

                case "FORMATAR":
                    if (conteudo.equals("Negrito")) {
                        negrito = !negrito;
                    } else {
                        System.out.println("Formatação desconhecida.");
                        return;
                    }
                    break;

                default:
                    System.out.println("Ação desconhecida: " + tipo);
                    return;
            }

            // Salva o estado resultante da ação.
            acao.textoNovo = texto;
            acao.textoNovoNegrito = negrito;

            undoStack.push(acao);

            // Uma nova ação invalida o histórico de redo.
            redoStack.clear();

            System.out.println("Ação: " + tipo + " (" + conteudo + ")");
            display();
        }

        // Desfaz a ação mais recente.
        void undo() {
            if (undoStack.empty()) {
                System.out.println("Nada a desfazer.");
                return;
            }

            Acao acao = undoStack.pop();

            texto = acao.textoAnterior;
            negrito = acao.textoAnteriorNegrito;

            redoStack.push(acao);

            System.out.println(
                "Desfazer: " + acao.tipo + " (" + acao.conteudo + ")"
            );
            display();
        }

        // Refaz a ação desfeita mais recentemente.
        void redo() {
            if (redoStack.empty()) {
                System.out.println("Nada a refazer.");
                return;
            }

            Acao acao = redoStack.pop();

            texto = acao.textoNovo;
            negrito = acao.textoNovoNegrito;

            undoStack.push(acao);

            System.out.println(
                "Refazer: " + acao.tipo + " (" + acao.conteudo + ")"
            );
            display();
        }

        // Exibe o estado atual do editor.
        void display() {
            System.out.println("Texto: \"" + texto + "\"");
            System.out.println("Negrito: " + negrito);
            System.out.println("---------------------");
        }
    }

    public static void main(String[] args) {

        TextoEditor editor = new TextoEditor();

        System.out.println("=== Realizando 12 ações ===");

        editor.executarAcao("TIPO", "Sou");
        editor.executarAcao("TIPO", " estudante");
        editor.executarAcao("TIPO", " iCEV");
        editor.executarAcao("TIPO", " de Engenharia de Software");
        editor.executarAcao("FORMATAR", "Negrito");
        editor.executarAcao("TIPO", " e estou aprendendo Java");
        editor.executarAcao("APAGAR", " Java");
        editor.executarAcao("TIPO", " estruturas de dados");
        editor.executarAcao("FORMATAR", "Negrito");
        editor.executarAcao("APAGAR", " estruturas de dados");
        editor.executarAcao("TIPO", " programação");
        editor.executarAcao("APAGAR", " programação");

        System.out.println("\n=== Desfazendo uma ação ===");
        editor.undo();

        System.out.println("\n=== Refazendo uma ação ===");
        editor.redo();
    }
}
