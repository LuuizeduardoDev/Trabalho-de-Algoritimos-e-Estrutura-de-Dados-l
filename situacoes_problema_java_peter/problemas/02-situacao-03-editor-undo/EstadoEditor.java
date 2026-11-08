/** Estado completo do editor em um determinado momento. */
public final class EstadoEditor {
    private final String texto;
    private final FormatoTexto formato;

    public EstadoEditor(String texto, FormatoTexto formato) {
        if (texto == null) {
            throw new IllegalArgumentException("O texto nao pode ser null.");
        }
        if (formato == null) {
            throw new IllegalArgumentException("O formato nao pode ser null.");
        }
        this.texto = texto;
        this.formato = formato;
    }

    public String getTexto() {
        return texto;
    }

    public FormatoTexto getFormato() {
        return formato;
    }

    @Override
    public String toString() {
        return "texto=\"" + texto + "\", formato=" + formato;
    }
}
