import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Extrai palavras de um texto e registra suas frequencias na tabela hash. */
public class ContadorPalavras {
    private static final Pattern PADRAO_PALAVRA = Pattern.compile(
            "[\\p{L}\\p{M}0-9]+(?:-[\\p{L}\\p{M}0-9]+)*");

    private final TabelaHash tabela;

    public ContadorPalavras() {
        tabela = new TabelaHash();
    }

    /** Processa o texto; maiusculas e minusculas sao consideradas iguais. */
    public void processar(String texto) {
        if (texto == null) {
            throw new IllegalArgumentException("O texto nao pode ser nulo.");
        }

        Matcher matcher = PADRAO_PALAVRA.matcher(texto.toLowerCase(Locale.ROOT));
        while (matcher.find()) {
            tabela.adicionar(matcher.group());
        }
    }

    public TabelaHash getTabela() {
        return tabela;
    }

    /** Retorna as frequencias em ordem decrescente, com desempate alfabetico. */
    public PalavraFrequencia[] maisFrequentes(int limite) {
        if (limite < 0) {
            throw new IllegalArgumentException("O limite nao pode ser negativo.");
        }

        PalavraFrequencia[] frequencias = tabela.listarFrequencias();
        ordenar(frequencias);

        int quantidade = limite < frequencias.length ? limite : frequencias.length;
        PalavraFrequencia[] resultado = new PalavraFrequencia[quantidade];
        for (int i = 0; i < quantidade; i++) {
            resultado[i] = frequencias[i];
        }
        return resultado;
    }

    private void ordenar(PalavraFrequencia[] frequencias) {
        for (int i = 1; i < frequencias.length; i++) {
            PalavraFrequencia atual = frequencias[i];
            int j = i - 1;
            while (j >= 0 && vemDepois(frequencias[j], atual)) {
                frequencias[j + 1] = frequencias[j];
                j--;
            }
            frequencias[j + 1] = atual;
        }
    }

    private boolean vemDepois(PalavraFrequencia primeira, PalavraFrequencia segunda) {
        if (primeira.getFrequencia() != segunda.getFrequencia()) {
            return primeira.getFrequencia() < segunda.getFrequencia();
        }
        return primeira.getPalavra().compareTo(segunda.getPalavra()) > 0;
    }
}
