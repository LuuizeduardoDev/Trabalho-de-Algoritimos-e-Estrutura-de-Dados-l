
package problema_01;

import java.util.Queue;
import java.util.LinkedList;

public class hospital_fila {

    // Classe que representa um paciente
    static class Paciente {
        String nome;
        int horarioChegada;

        Paciente(String nome, int horarioChegada) {
            this.nome = nome;
            this.horarioChegada = horarioChegada;
        }
    }

    public static void main(String[] args) {

        // Cria a fila de pacientes usando FIFO
        Queue<Paciente> pacientes = new LinkedList<>();

        // Cadastra os 15 pacientes e seus horários de chegada
        pacientes.offer(new Paciente("Ana", 0));
        pacientes.offer(new Paciente("Paulo", 0));
        pacientes.offer(new Paciente("Renata", 0));
        pacientes.offer(new Paciente("Arthur", 0));
        pacientes.offer(new Paciente("Luiz", 0));
        pacientes.offer(new Paciente("Amanda", 0));
        pacientes.offer(new Paciente("José", 0));
        pacientes.offer(new Paciente("Maria", 0));
        pacientes.offer(new Paciente("Adão", 0));
        pacientes.offer(new Paciente("Rebeca", 0));
        pacientes.offer(new Paciente("Gustavo", 0));
        pacientes.offer(new Paciente("Alice", 0));
        pacientes.offer(new Paciente("Sérgio", 0));
        pacientes.offer(new Paciente("Pedro", 0));
        pacientes.offer(new Paciente("Júlia", 0));

        // Define a duração da consulta e inicializa os contadores
        int tempoConsulta = 10;
        int horarioDisponivelDoutor = 0;
        int tempoTotalEspera = 0;
        int pacientesAtendidos = 0;

        // Exibe o cabeçalho da tabela
        System.out.println("Fila de espera | Clínica");
        System.out.println("--------------------------------------------------");

        System.out.printf(
            "%-12s %-12s %-12s %-12s%n",
            "Paciente", "Chegada", "Serviço", "Espera"
        );

        // Atende os pacientes na ordem em que entraram na fila
        while (!pacientes.isEmpty()) {

            // Remove o primeiro paciente da fila
            Paciente atual = pacientes.poll();

            // Define o início do atendimento
            int inicioServico = Math.max(
                atual.horarioChegada,
                horarioDisponivelDoutor
            );

            // Calcula o tempo que o paciente esperou
            int tempoEspera = inicioServico - atual.horarioChegada;

            // Atualiza o horário em que o médico estará disponível
            horarioDisponivelDoutor = inicioServico + tempoConsulta;

            // Acumula o tempo de espera e conta o atendimento
            tempoTotalEspera += tempoEspera;
            pacientesAtendidos++;

            // Exibe os dados do paciente atendido
            System.out.printf(
                "%-12s %-12s %-12s %-12d min%n",
                atual.nome,
                formatarHora(atual.horarioChegada),
                formatarHora(inicioServico),
                tempoEspera
            );
        }

        // Calcula o tempo médio de espera dos pacientes
        double tempoMedioEspera =
            (double) tempoTotalEspera / pacientesAtendidos;

        // Exibe os resultados finais
        System.out.println("--------------------------------------------------");
        System.out.println("Pacientes atendidos: " + pacientesAtendidos);
        System.out.println("Tempo total de espera: " + tempoTotalEspera + " minutos");

        System.out.printf(
            "Tempo médio de espera: %.2f minutos%n",
            tempoMedioEspera
        );
    }

    // Converte os minutos após as 08:00 para o formato HH:mm
    public static String formatarHora(int minutos) {
        int totalMinutos = 8 * 60 + minutos;
        int horas = totalMinutos / 60;
        int minutosRestantes = totalMinutos % 60;

        return String.format("%02d:%02d", horas, minutosRestantes);
    }
}
