/** Executa a simulacao exigida para o problema 3. */
public class PlaylistApp {
    public static void main(String[] args) {
        Playlist playlist = criarPlaylist();

        System.out.println("=== Playlist criada: " + playlist.getNome() + " ===");
        listar("Playlist inicial", playlist.listar());

        playlist.inserirInicio(new Musica("Aquarela", "Toquinho", 258));
        playlist.inserirFinal(new Musica("O Leaozinho", "Caetano Veloso", 194));
        playlist.inserir(new Musica("Tempo Perdido", "Legiao Urbana", 306), 4);
        System.out.println();
        listar("Apos insercoes no inicio, final e posicao 4", playlist.listar());

        boolean removida = playlist.removerPorTitulo("Pais e Filhos");
        System.out.println();
        System.out.println("Remocao de 'Pais e Filhos': "
                + (removida ? "realizada" : "titulo nao encontrado"));
        listar("Apos remocao", playlist.listar());

        System.out.println();
        listar("Busca por 'Legiao'", playlist.buscar("Legiao"));

        playlist.reordenarPorTitulo();
        System.out.println();
        listar("Apos reordenacao alfabetica", playlist.listar());
    }

    private static Playlist criarPlaylist() {
        Playlist playlist = new Playlist("Favoritas brasileiras");
        playlist.inserirFinal(new Musica("Construção", "Chico Buarque", 385));
        playlist.inserirFinal(new Musica("Pais e Filhos", "Legiao Urbana", 293));
        playlist.inserirFinal(new Musica("Velha Infancia", "Tribalistas", 252));
        playlist.inserirFinal(new Musica("Trem Bala", "Ana Vilela", 189));
        playlist.inserirFinal(new Musica("Epitafio", "Titãs", 248));
        playlist.inserirFinal(new Musica("Lanterna dos Afogados", "Os Paralamas do Sucesso", 233));
        playlist.inserirFinal(new Musica("Malandragem", "Cássia Eller", 247));
        playlist.inserirFinal(new Musica("Segundo Sol", "Cássia Eller", 260));
        playlist.inserirFinal(new Musica("Sampa", "Caetano Veloso", 305));
        playlist.inserirFinal(new Musica("Exagerado", "Cazuza", 231));
        playlist.inserirFinal(new Musica("Tempo Perdido", "Legiao Urbana", 306));
        playlist.inserirFinal(new Musica("Como Nossos Pais", "Elis Regina", 268));
        return playlist;
    }

    private static void listar(String titulo, Musica[] musicas) {
        System.out.println("--- " + titulo + " ---");
        if (musicas.length == 0) {
            System.out.println("Nenhuma musica encontrada.");
            return;
        }
        for (int indice = 0; indice < musicas.length; indice++) {
            System.out.println((indice + 1) + ". " + musicas[indice]);
        }
    }
}
