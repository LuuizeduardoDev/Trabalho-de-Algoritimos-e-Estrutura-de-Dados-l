"""SP18 – Organização de Tarefas por Prioridade (Valor Numérico).

Algoritmo usado: Selection Sort -> ordenacao/selection_sort.py

O que o enunciado pede e onde está:
  * lista de tarefas com prioridade e descrição ...... Tarefa
  * Selection Sort por prioridade ..................... organizar_por_prioridade()
  * simulação de um dia de trabalho com 12-15 tarefas . executar_demonstracao() (13 + 2 que chegam)

Convenção: prioridade 5 = urgente ... 1 = muito baixa. A lista é organizada da
mais urgente para a menos urgente.

Por que Selection Sort: a cada passada ele SELECIONA a tarefa mais urgente que
ainda falta e faz no máximo UMA troca, que é como uma pessoa organiza a agenda
("qual é a próxima mais importante?"). Com 12 a 15 tarefas, as n(n-1)/2
comparações são irrelevantes e o número de trocas fica no mínimo (no máximo n-1).

Cuidado: o Selection Sort NÃO é estável. Tarefas com a mesma prioridade podem
trocar de ordem entre si. Por isso a chave usada é (prioridade, ordem de
cadastro): no empate, quem foi anotado primeiro vem primeiro.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):  # permite rodar este arquivo diretamente
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ordenacao.selection_sort import selection_sort
from situacoes.utilidades import cabecalho, imprimir_tabela, secao

NIVEIS = ["", "muito baixa", "baixa", "média", "alta", "urgente"]


@dataclass
class Tarefa:
    codigo: int          # ordem em que a tarefa foi anotada
    descricao: str
    prioridade: int      # 1 (muito baixa) a 5 (urgente)
    duracao_min: int

    def __post_init__(self):
        if not 1 <= self.prioridade <= 5:
            raise ValueError("a prioridade deve estar entre 1 e 5")


def organizar_por_prioridade(tarefas: list):
    """Devolve (nova lista da mais urgente para a menos urgente, métricas).

    Chave (-prioridade, codigo): prioridade maior primeiro e, no empate, a
    tarefa anotada antes. Assim o resultado não depende da instabilidade do
    Selection Sort.
    """
    copia = list(tarefas)
    metricas = selection_sort(copia, chave=lambda t: (-t.prioridade, t.codigo))
    return copia, metricas


def _hora(minutos: int) -> str:
    return f"{minutos // 60:02d}:{minutos % 60:02d}"


TAREFAS_DA_MANHA = [
    Tarefa(1, "Responder e-mails de clientes", 3, 30),
    Tarefa(2, "Preparar apresentação da reunião de equipe", 4, 60),
    Tarefa(3, "Corrigir erro no relatório financeiro", 5, 45),
    Tarefa(4, "Organizar a pasta compartilhada", 1, 20),
    Tarefa(5, "Ligar para o fornecedor de papel", 2, 15),
    Tarefa(6, "Revisar contrato de manutenção", 4, 40),
    Tarefa(7, "Atualizar planilha de despesas", 3, 35),
    Tarefa(8, "Reunião de alinhamento com o gerente", 5, 30),
    Tarefa(9, "Treinamento online obrigatório", 3, 60),
    Tarefa(10, "Agendar consulta médica", 2, 10),
    Tarefa(11, "Enviar proposta comercial", 5, 50),
    Tarefa(12, "Ler a newsletter do setor", 1, 15),
    Tarefa(13, "Planejar as tarefas da próxima semana", 2, 25),
]

TAREFAS_DA_TARDE = [   # chegam no almoço
    Tarefa(14, "Atender chamado: sistema de pagamentos fora do ar", 5, 45),
    Tarefa(15, "Responder pesquisa de clima do RH", 2, 20),
]

INICIO, ALMOCO, VOLTA, FIM = 8 * 60, 12 * 60, 13 * 60, 17 * 60


def _executar_periodo(agenda: list, inicio: int, fim: int, feitas: list) -> list:
    """Executa as tarefas na ordem da agenda até `fim`. Devolve as que sobraram.

    Se a próxima tarefa não cabe antes do fim do período, ela fica para depois
    (continua no topo das pendentes) e a agenda ENCAIXA a próxima que couber,
    para não desperdiçar o tempo livre. Cada item de `feitas` é
    (início, fim, tarefa, foi_encaixe).
    """
    agora = inicio
    sobraram = []
    for tarefa in agenda:
        if agora + tarefa.duracao_min <= fim:
            encaixe = len(sobraram) > 0   # passou na frente de alguma que não coube
            feitas.append((agora, agora + tarefa.duracao_min, tarefa, encaixe))
            agora += tarefa.duracao_min
        else:
            sobraram.append(tarefa)       # não cabe antes do intervalo: fica para depois
    return sobraram


def executar_demonstracao() -> None:
    cabecalho("SP18 - Tarefas do dia organizadas por prioridade (Selection Sort)")

    secao(f"Tarefas anotadas às 08:00, na ordem em que surgiram ({len(TAREFAS_DA_MANHA)})")
    imprimir_tabela(["Nº", "Tarefa", "Prioridade", "Duração"],
                    [[t.codigo, t.descricao, f"{t.prioridade} ({NIVEIS[t.prioridade]})", f"{t.duracao_min} min"]
                     for t in TAREFAS_DA_MANHA], "><<>")

    agenda, metricas = organizar_por_prioridade(TAREFAS_DA_MANHA)
    secao("Agenda organizada com Selection Sort (mais urgente primeiro)")
    imprimir_tabela(["Ordem", "Nº", "Tarefa", "Prioridade"],
                    [[f"{i}º", t.codigo, t.descricao, t.prioridade] for i, t in enumerate(agenda, start=1)],
                    ">><>")
    print(metricas.resumo())
    print(f"Comparações = n(n-1)/2 = {len(agenda) * (len(agenda) - 1) // 2}; trocas: no máximo n-1 = {len(agenda) - 1}.")

    secao("Por que a chave tem desempate (o Selection Sort não é estável)")
    so_prioridade = list(TAREFAS_DA_MANHA)
    selection_sort(so_prioridade, chave=lambda t: t.prioridade, decrescente=True)
    invertidas = []
    for i, primeira in enumerate(so_prioridade):
        for segunda in so_prioridade[i + 1:]:
            if primeira.prioridade == segunda.prioridade and primeira.codigo > segunda.codigo:
                invertidas.append((primeira, segunda))
    print("  Ordenando SÓ pela prioridade, tarefas empatadas trocaram de lugar:")
    for primeira, segunda in invertidas:
        print(f"    nº {primeira.codigo} ficou antes do nº {segunda.codigo} (ambas prioridade {primeira.prioridade})")
    print("  Com a chave (prioridade, nº da tarefa) isso não acontece: veja a agenda acima.")

    secao("Simulação do dia (08:00-12:00 e 13:00-17:00)")
    feitas = []
    pendentes = _executar_periodo(agenda, INICIO, ALMOCO, feitas)
    print(f"  Manhã: {len(feitas)} tarefas concluídas; {len(pendentes)} ficaram para a tarde.")
    print(f"  No almoço chegaram {len(TAREFAS_DA_TARDE)} tarefas novas: "
          + "; ".join(f"nº {t.codigo} {t.descricao} (prioridade {t.prioridade})" for t in TAREFAS_DA_TARDE))
    agenda_tarde, metricas_tarde = organizar_por_prioridade(pendentes + TAREFAS_DA_TARDE)
    print(f"  Lista reorganizada com Selection Sort: {metricas_tarde.comparacoes} comparações, "
          f"{metricas_tarde.trocas} trocas.")
    ficaram = _executar_periodo(agenda_tarde, VOLTA, FIM, feitas)

    imprimir_tabela(["Início", "Fim", "Nº", "Tarefa", "Prior.", "Obs."],
                    [[_hora(ini), _hora(fim), t.codigo, t.descricao, t.prioridade, "encaixe" if encaixe else ""]
                     for ini, fim, t, encaixe in feitas],
                    "<<><><")
    print("encaixe = a tarefa seguinte da agenda não cabia antes do intervalo; esta, mais curta, coube.")
    print(f"\nConcluídas: {len(feitas)} de {len(TAREFAS_DA_MANHA) + len(TAREFAS_DA_TARDE)} tarefas.")
    adiadas = ", ".join(f"nº {t.codigo} {t.descricao} (prioridade {t.prioridade})" for t in ficaram)
    print("Ficam para amanhã: " + (adiadas or "nenhuma"))


if __name__ == "__main__":
    executar_demonstracao()
