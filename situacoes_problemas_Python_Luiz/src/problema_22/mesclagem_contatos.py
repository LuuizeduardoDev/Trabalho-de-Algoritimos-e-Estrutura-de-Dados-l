"""SP22 – Mesclagem de Duas Listas de Contatos Ordenadas.

Algoritmo usado: etapa de intercalação (merge) do Merge Sort -> merge_sort.py

O que o enunciado pede e onde está:
  * usar a etapa de merge para combinar duas listas ordenadas .. mesclar_sem_duplicatas()
  * remover duplicatas DURANTE a mesclagem ...................... idem (comparação com o último)
  * demonstração com duas listas de 20 contatos ................. COMERCIAL e FINANCEIRO

Por que a etapa de merge: as duas listas JÁ estão em ordem alfabética, então
não é preciso reordenar nada. Basta caminhar com um índice em cada lista e
copiar sempre o menor dos dois da vez: O(n + m), uma única passada.

Duplicatas: o mesmo contato pode estar nas duas listas. Como a lista
resultante sai em ordem, cópias de um mesmo contato ficam LADO A LADO, então
basta comparar cada contato com o último colocado no resultado. Se for o
mesmo, ele não entra de novo; só os departamentos são juntados. Isso também
elimina repetições dentro de uma mesma lista.

Chave de ordenação = chave de duplicata = (nome sem acentos/maiúsculas, e-mail).
Dois contatos com o mesmo nome e e-mails diferentes são HOMÔNIMOS (pessoas
diferentes) e os dois são mantidos.
"""

from __future__ import annotations

from dataclasses import dataclass

from merge_sort import merge_sort
from metricas import Metricas
from utilidades import cabecalho, configurar_terminal, imprimir_tabela, normalizar_texto, secao


@dataclass
class Contato:
    nome: str
    email: str
    telefone: str
    departamentos: str


def chave_contato(contato: Contato) -> tuple:
    return (normalizar_texto(contato.nome), contato.email.strip().lower())


def esta_ordenada(contatos: list) -> bool:
    return all(chave_contato(contatos[i]) <= chave_contato(contatos[i + 1]) for i in range(len(contatos) - 1))


def mesclar_sem_duplicatas(lista_a: list, lista_b: list):
    """Intercala duas listas ORDENADAS removendo duplicatas. O(n + m).

    É a mesma intercalação do Merge Sort (merge_sort.py,
    função _intercalar), com um passo a mais: antes de colocar um contato no
    resultado, ele é comparado com o último colocado.

    Devolve (lista_mesclada, duplicatas_removidas, metricas).
    """
    metricas = Metricas("Intercalação sem duplicatas", len(lista_a) + len(lista_b))
    resultado = []
    removidas = []

    def colocar(contato: Contato) -> None:
        if resultado:
            metricas.comparacoes += 1
            if chave_contato(resultado[-1]) == chave_contato(contato):   # duplicata
                ultimo = resultado[-1]
                if contato.departamentos not in ultimo.departamentos:
                    ultimo.departamentos += " + " + contato.departamentos
                removidas.append(contato)
                return
        resultado.append(Contato(contato.nome, contato.email, contato.telefone, contato.departamentos))

    i = j = 0
    while i < len(lista_a) and j < len(lista_b):
        metricas.comparacoes += 1
        if chave_contato(lista_b[j]) < chave_contato(lista_a[i]):   # o menor dos dois sai primeiro
            colocar(lista_b[j])
            j += 1
        else:                                                         # empate: sai o da lista A
            colocar(lista_a[i])
            i += 1
    while i < len(lista_a):          # uma lista acabou: o resto da outra já está em ordem
        colocar(lista_a[i])
        i += 1
    while j < len(lista_b):
        colocar(lista_b[j])
        j += 1
    return resultado, removidas, metricas


def _lista(departamento: str, dados: list) -> list:
    return [Contato(nome, email, telefone, departamento) for nome, email, telefone in dados]


COMERCIAL = _lista("Comercial", [
    ("Adriana Mello", "adriana.mello@fornecedoraalfa.com.br", "(86) 99811-2034"),
    ("Ana Paula Souza", "ana.souza@graficarapida.com.br", "(86) 99902-1120"),
    ("Bernardo Lima", "bernardo.lima@transportesbl.com.br", "(86) 98123-4410"),
    ("Carlos Eduardo Nunes", "carlos.nunes@grupoalfa.com.br", "(86) 99455-0091"),
    ("Cecília Andrade", "cecilia.andrade@clienteplus.com.br", "(86) 99730-5521"),
    ("Daniela Freitas", "daniela.freitas@grupoalfa.com.br", "(86) 99214-7788"),
    ("Eduardo Pires", "eduardo.pires@atacadopiaui.com.br", "(86) 98840-3302"),
    ("Fernanda Lopes", "fernanda.lopes@grupoalfa.com.br", "(86) 99377-6610"),
    ("Gustavo Ramos", "gustavo.ramos@logmax.com.br", "(86) 98102-9945"),
    ("Helena Castro", "helena.castro@clienteplus.com.br", "(86) 99561-2207"),
    ("Igor Matos", "igor.matos@grupoalfa.com.br", "(86) 99688-4013"),
    ("Juliana Teixeira", "juliana.teixeira@feiradomovel.com.br", "(86) 98955-1176"),
    ("Leonardo Batista", "leonardo.batista@grupoalfa.com.br", "(86) 99140-8832"),
    ("Marcos Vieira", "marcos.vieira@papelariacentral.com.br", "(86) 98777-0458"),
    ("Natália Gomes", "natalia.gomes@clienteplus.com.br", "(86) 99823-6694"),
    ("Otávio Rezende", "otavio.rezende@agenciaora.com.br", "(86) 99016-3327"),
    ("Patrícia Moura", "patricia.moura@grupoalfa.com.br", "(86) 99234-5580"),
    ("Renato Cardoso", "renato.cardoso@techsul.com.br", "(86) 98611-7092"),
    ("Simone Barros", "simone.barros@atacadopiaui.com.br", "(86) 99470-1863"),
    ("Thiago Moreira", "thiago.moreira@logmax.com.br", "(86) 98390-2215"),
])

FINANCEIRO = _lista("Financeiro", [
    ("Alessandra Rocha", "alessandra.rocha@contabilfacil.com.br", "(86) 99105-6620"),
    ("Ana Paula Souza", "ana.p.souza@bancoregional.com.br", "(86) 98204-3391"),   # homônima
    ("Beatriz Campos", "beatriz.campos@bancoregional.com.br", "(86) 99652-0147"),
    ("Carlos Eduardo Nunes", "carlos.nunes@grupoalfa.com.br", "(86) 99455-0091"),
    ("Daniela Freitas", "daniela.freitas@grupoalfa.com.br", "(86) 99214-7788"),
    ("Diego Albuquerque", "diego.albuquerque@auditoriaxp.com.br", "(86) 98533-8204"),
    ("Fábio Nascimento", "fabio.nascimento@seguradoraboa.com.br", "(86) 99318-4479"),
    ("Fernanda Lopes", "fernanda.lopes@grupoalfa.com.br", "(86) 99377-6610"),
    ("Igor Matos", "igor.matos@grupoalfa.com.br", "(86) 99688-4013"),
    ("Joana Ribeiro", "joana.ribeiro@contabilfacil.com.br", "(86) 98476-5530"),
    ("Leonardo Batista", "leonardo.batista@grupoalfa.com.br", "(86) 99140-8832"),
    ("Luciana Prado", "luciana.prado@receitaconsult.com.br", "(86) 99087-2216"),
    ("Márcio Tavares", "marcio.tavares@bancoregional.com.br", "(86) 98265-9013"),
    ("Patrícia Moura", "patricia.moura@grupoalfa.com.br", "(86) 99234-5580"),
    ("Priscila Antunes", "priscila.antunes@auditoriaxp.com.br", "(86) 99741-3368"),
    ("Rodrigo Farias", "rodrigo.farias@seguradoraboa.com.br", "(86) 98150-6687"),
    ("Sérgio Mendes", "sergio.mendes@bancoregional.com.br", "(86) 99399-7105"),
    ("Tatiane Duarte", "tatiane.duarte@contabilfacil.com.br", "(86) 98824-1149"),
    ("Vanessa Queiroz", "vanessa.queiroz@receitaconsult.com.br", "(86) 99563-0782"),
    ("Wagner Lacerda", "wagner.lacerda@auditoriaxp.com.br", "(86) 98917-4456"),
])


def executar_demonstracao() -> None:
    cabecalho("SP22 - Mesclagem de duas listas de contatos ordenadas (etapa de merge)")
    listas = [("Comercial", COMERCIAL), ("Financeiro", FINANCEIRO)]
    for nome, lista in listas:
        if esta_ordenada(lista):
            print(f"Lista do {nome}: {len(lista)} contatos, já em ordem alfabética.")
        else:   # proteção: se alguém entregar a lista fora de ordem, o Merge Sort completo arruma
            merge_sort(lista, chave=chave_contato)
            print(f"Lista do {nome}: {len(lista)} contatos, estava fora de ordem e foi ordenada com Merge Sort.")

    secao("Primeiros passos da intercalação (um índice em cada lista)")
    i = j = 0
    for passo in range(1, 7):
        a, b = COMERCIAL[i], FINANCEIRO[j]
        if chave_contato(b) < chave_contato(a):
            escolhido, j = b, j + 1
        else:
            escolhido, i = a, i + 1
        print(f"  passo {passo}: Comercial '{a.nome}' x Financeiro '{b.nome}' -> sai '{escolhido.nome}' "
              f"({escolhido.departamentos})")

    unica, removidas, metricas = mesclar_sem_duplicatas(COMERCIAL, FINANCEIRO)

    secao(f"Lista única ({len(unica)} contatos)")
    imprimir_tabela(["#", "Nome", "E-mail", "Telefone", "Departamento(s)"],
                    [[i, c.nome, c.email, c.telefone, c.departamentos] for i, c in enumerate(unica, start=1)],
                    "><<<<")

    secao("Resumo")
    print(f"  Entrada: {len(COMERCIAL)} + {len(FINANCEIRO)} = {len(COMERCIAL) + len(FINANCEIRO)} contatos")
    print(f"  Duplicatas removidas durante a mesclagem: {len(removidas)} -> "
          + ", ".join(c.nome for c in removidas))
    homonimos = [c for c in unica if c.nome == "Ana Paula Souza"]
    print("  Homônimos mantidos (mesmo nome, e-mails diferentes): "
          + " e ".join(f"{c.nome} <{c.email}> ({c.departamentos})" for c in homonimos))
    print(f"  Comparações: {metricas.comparacoes} (no máximo 2 por contato de entrada: "
          f"O(n + m), uma única passada)")
    print(f"  Resultado em ordem alfabética: {'sim' if esta_ordenada(unica) else 'NÃO'}")


if __name__ == "__main__":
    configurar_terminal()
    executar_demonstracao()
