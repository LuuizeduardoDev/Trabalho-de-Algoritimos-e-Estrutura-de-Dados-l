/** Executa a demonstracao da contagem de frequencia de palavras. */
public class Problema7 {
    // Trecho real: preambulo da Constituicao da Republica Federativa do Brasil.
    private static final String TEXTO_REAL =
            "Nós, representantes do povo brasileiro, reunidos em Assembleia Nacional "
                    + "Constituinte para instituir um Estado Democrático, destinado a assegurar "
                    + "o exercício dos direitos sociais e individuais, a liberdade, a segurança, "
                    + "o bem-estar, o desenvolvimento, a igualdade e a justiça como valores "
                    + "supremos de uma sociedade fraterna, pluralista e sem preconceitos, "
                    + "fundada na harmonia social e comprometida, na ordem interna e internacional, "
                    + "com a solução pacífica das controvérsias, promulgamos, sob a proteção de Deus, "
                    + "a seguinte Constituição da República Federativa do Brasil.";

    public static void main(String[] args) {
        ContadorPalavras contador = new ContadorPalavras();
        contador.processar(TEXTO_REAL);

        System.out.println("=== Contagem de frequencia de palavras ===");
        System.out.println("Texto processado: preambulo da Constituicao Federal do Brasil.");
        System.out.println();
        System.out.println("Palavras mais frequentes:");
        for (PalavraFrequencia item : contador.maisFrequentes(10)) {
            System.out.println("- " + item.getPalavra() + ": " + item.getFrequencia());
        }
        System.out.println();
        System.out.println("Total de palavras distintas: "
                + contador.getTabela().palavrasDistintas());
        System.out.println("Total de ocorrencias: "
                + contador.getTabela().totalOcorrencias());
    }
}
