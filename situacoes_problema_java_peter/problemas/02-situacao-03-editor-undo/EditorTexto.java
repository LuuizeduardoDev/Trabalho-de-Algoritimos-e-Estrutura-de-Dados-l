import java.util.Locale;

/** Editor simples que registra cada alteracao em uma pilha manual. */
public class EditorTexto {
    private EstadoEditor estadoAtual;
    private final PilhaAcoes historico;

    public EditorTexto() {
        estadoAtual = new EstadoEditor("", FormatoTexto.NORMAL);
        historico = new PilhaAcoes();
    }

    public String getTexto() {
        return estadoAtual.getTexto();
    }

    public FormatoTexto getFormato() {
        return estadoAtual.getFormato();
    }

    public EstadoEditor getEstadoAtual() {
        return estadoAtual;
    }

    public int quantidadeAcoes() {
        return historico.tamanho();
    }

    public boolean podeDesfazer() {
        return !historico.estaVazia();
    }

    /** Insere texto no final do documento e registra a digitacao. */
    public void digitar(String texto) {
        validarTextoNaoVazio(texto, "O texto digitado nao pode ser vazio.");
        EstadoEditor anterior = estadoAtual;
        EstadoEditor posterior = new EstadoEditor(
                anterior.getTexto() + texto, anterior.getFormato());
        registrar(TipoAcao.DIGITACAO, "digitar \"" + texto + "\"", anterior, posterior);
    }

    /** Exclui o intervalo [inicio, fim) e registra a exclusao. */
    public void excluir(int inicio, int fim) {
        String texto = estadoAtual.getTexto();
        if (inicio < 0 || fim > texto.length() || inicio >= fim) {
            throw new IndexOutOfBoundsException("Intervalo de exclusao invalido: ["
                    + inicio + ", " + fim + ")");
        }

        EstadoEditor anterior = estadoAtual;
        String novoTexto = texto.substring(0, inicio) + texto.substring(fim);
        EstadoEditor posterior = new EstadoEditor(novoTexto, anterior.getFormato());
        registrar(TipoAcao.EXCLUSAO,
                "excluir \"" + texto.substring(inicio, fim) + "\"", anterior, posterior);
    }

    /** Aplica uma formatacao simples ao texto atual e registra a mudanca. */
    public void formatar(FormatoTexto novoFormato) {
        if (novoFormato == null) {
            throw new IllegalArgumentException("O formato nao pode ser null.");
        }

        EstadoEditor anterior = estadoAtual;
        String textoFormatado = aplicarFormato(anterior.getTexto(), novoFormato);
        EstadoEditor posterior = new EstadoEditor(textoFormatado, novoFormato);
        registrar(TipoAcao.FORMATACAO,
                "formatar como " + novoFormato, anterior, posterior);
    }

    /** Desfaz a acao mais recente. Retorna false quando nao existe historico. */
    public boolean desfazer() {
        if (historico.estaVazia()) {
            return false;
        }
        Acao acao = historico.pop();
        estadoAtual = acao.getEstadoAnterior();
        return true;
    }

    private void registrar(TipoAcao tipo, String descricao, EstadoEditor anterior,
            EstadoEditor posterior) {
        estadoAtual = posterior;
        historico.push(new Acao(tipo, descricao, anterior, posterior));
    }

    private String aplicarFormato(String texto, FormatoTexto formato) {
        switch (formato) {
            case MAIUSCULAS:
                return texto.toUpperCase(Locale.ROOT);
            case MINUSCULAS:
                return texto.toLowerCase(Locale.ROOT);
            case NORMAL:
                return texto;
            default:
                throw new IllegalArgumentException("Formato nao suportado: " + formato);
        }
    }

    private void validarTextoNaoVazio(String texto, String mensagem) {
        if (texto == null || texto.isEmpty()) {
            throw new IllegalArgumentException(mensagem);
        }
    }
}
