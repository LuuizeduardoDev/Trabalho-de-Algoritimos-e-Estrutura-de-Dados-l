/** Testes executaveis da lista encadeada usada pela playlist. */
public class TestePlaylist {
    public static void main(String[] args) {
        Playlist playlist = new Playlist("Teste");
        Musica primeira = new Musica("B", "Artista B", 120);
        Musica segunda = new Musica("A", "Artista A", 180);
        Musica terceira = new Musica("C", "Artista C", 200);

        verificar(playlist.estaVazia(), "uma playlist nova deve estar vazia");
        playlist.inserirFinal(primeira);
        playlist.inserirInicio(segunda);
        playlist.inserir(terceira, 2);
        verificar(playlist.tamanho() == 3, "as tres insercoes devem atualizar o tamanho");
        verificar(playlist.listar()[0] == segunda, "inserirInicio deve colocar a musica no inicio");
        verificar(playlist.listar()[2] == terceira, "inserir na ultima posicao deve funcionar");

        verificar(playlist.buscar("artista").length == 3,
                "a busca deve considerar o artista");
        verificar(playlist.buscar("nao existe").length == 0,
                "uma busca sem resultado deve retornar array vazio");

        verificar(playlist.removerPorTitulo("B"), "a musica existente deve ser removida");
        verificar(!playlist.removerPorTitulo("inexistente"),
                "remover titulo inexistente deve retornar false");
        verificar(playlist.tamanho() == 2, "a remocao deve reduzir o tamanho");

        playlist.reordenarPorTitulo();
        Musica[] ordenadas = playlist.listar();
        verificar(ordenadas[0].getTitulo().equals("A"), "a primeira musica deve ser A apos ordenar");
        verificar(ordenadas[1].getTitulo().equals("C"), "a segunda musica deve ser C apos ordenar");

        verificarExcecao(() -> playlist.inserir(null, 0), "insercao de musica null");
        verificarExcecao(() -> playlist.inserir(new Musica("D", "Artista D", 100), 4),
                "insercao em posicao invalida");
        verificarExcecao(() -> playlist.buscar("  "), "busca com criterio vazio");
        verificarExcecao(() -> new Musica("X", "Artista X", -1), "duracao negativa");

        System.out.println("Todos os testes da Playlist foram aprovados.");
    }

    private static void verificar(boolean condicao, String descricao) {
        if (!condicao) {
            throw new AssertionError("Falha: " + descricao);
        }
    }

    private static void verificarExcecao(Runnable acao, String descricao) {
        try {
            acao.run();
            throw new AssertionError("Falha: era esperada uma excecao em " + descricao);
        } catch (IllegalArgumentException | IndexOutOfBoundsException excecao) {
            // Comportamento esperado para dados invalidos.
        }
    }
}
