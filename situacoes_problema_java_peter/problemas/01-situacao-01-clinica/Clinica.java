import java.time.Duration;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

/** Executa a simulacao de atendimento da clinica. */
public class Clinica {
    private static final DateTimeFormatter FORMATO_HORARIO = DateTimeFormatter.ofPattern("HH:mm");
    private static final int DURACAO_ESTIMADA_ATENDIMENTO_MINUTOS = 15;

    public static void main(String[] args) {
        Fila<Paciente> fila = new Fila<>();
        Paciente[] pacientes = criarPacientes();

        System.out.println("=== Chegada dos pacientes ===");
        for (Paciente paciente : pacientes) {
            fila.enqueue(paciente);
            imprimirPaciente(paciente);
        }

        System.out.println();
        System.out.println("Fila vazia? " + fila.isEmpty());
        System.out.println("Tamanho da fila: " + fila.size());
        System.out.println("Proximo paciente: " + fila.front().getNome());

        System.out.println();
        System.out.println("=== Relatorio final de atendimento ===");
        LocalTime horarioDisponivel = fila.front().getHorarioChegada();
        long somaEsperaMinutos = 0;
        int totalAtendidos = 0;

        while (!fila.isEmpty()) {
            Paciente paciente = fila.dequeue();
            LocalTime horarioAtendimento = horarioDisponivel;

            if (horarioAtendimento.isBefore(paciente.getHorarioChegada())) {
                horarioAtendimento = paciente.getHorarioChegada();
            }

            long esperaMinutos = Duration.between(
                    paciente.getHorarioChegada(), horarioAtendimento).toMinutes();
            somaEsperaMinutos += esperaMinutos;
            totalAtendidos++;

            System.out.printf(
                    "%d. %s | chegada: %s | atendimento: %s | espera estimada: %d min%n",
                    totalAtendidos,
                    paciente.getNome(),
                    formatarHorario(paciente.getHorarioChegada()),
                    formatarHorario(horarioAtendimento),
                    esperaMinutos);

            horarioDisponivel = horarioAtendimento.plusMinutes(
                    DURACAO_ESTIMADA_ATENDIMENTO_MINUTOS);
        }

        double mediaEspera = (double) somaEsperaMinutos / totalAtendidos;
        System.out.printf("Tempo medio estimado de espera: %.2f min%n", mediaEspera);
        System.out.println("Fila vazia apos os atendimentos? " + fila.isEmpty());
        System.out.println("Tamanho final da fila: " + fila.size());
    }

    private static void imprimirPaciente(Paciente paciente) {
        System.out.printf(
                "%s | chegada: %s | tipo: %s%n",
                paciente.getNome(),
                formatarHorario(paciente.getHorarioChegada()),
                paciente.getTipoAtendimento());
    }

    private static String formatarHorario(LocalTime horario) {
        return horario.format(FORMATO_HORARIO);
    }

    private static Paciente[] criarPacientes() {
        return new Paciente[] {
                new Paciente("Ana", LocalTime.of(8, 5), "Consulta"),
                new Paciente("Bruno", LocalTime.of(8, 12), "Exame"),
                new Paciente("Carla", LocalTime.of(8, 15), "Cirurgia"),
                new Paciente("Diego", LocalTime.of(8, 22), "Retorno"),
                new Paciente("Elisa", LocalTime.of(8, 28), "Consulta"),
                new Paciente("Fabio", LocalTime.of(8, 35), "Exame"),
                new Paciente("Gabriela", LocalTime.of(8, 41), "Consulta"),
                new Paciente("Henrique", LocalTime.of(8, 49), "Curativo"),
                new Paciente("Isabela", LocalTime.of(8, 56), "Consulta"),
                new Paciente("Joao", LocalTime.of(9, 4), "Exame"),
                new Paciente("Karina", LocalTime.of(9, 12), "Retorno"),
                new Paciente("Lucas", LocalTime.of(9, 20), "Consulta"),
                new Paciente("Marina", LocalTime.of(9, 27), "Vacinacao"),
                new Paciente("Nicolas", LocalTime.of(9, 35), "Consulta"),
                new Paciente("Olivia", LocalTime.of(9, 43), "Exame")
        };
    }
}
