import java.time.LocalTime;

/** Representa um paciente da simulacao da clinica. */
public class Paciente {
    private final String nome;
    private final LocalTime horarioChegada;
    private final String tipoAtendimento;

    public Paciente(String nome, LocalTime horarioChegada, String tipoAtendimento) {
        this.nome = nome;
        this.horarioChegada = horarioChegada;
        this.tipoAtendimento = tipoAtendimento;
    }

    public String getNome() {
        return nome;
    }

    public LocalTime getHorarioChegada() {
        return horarioChegada;
    }

    public String getTipoAtendimento() {
        return tipoAtendimento;
    }
}
