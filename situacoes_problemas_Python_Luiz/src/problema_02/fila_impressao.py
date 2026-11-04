"""SP02 – Fila de Impressão em Laboratório de Informática.

Estrutura usada: Fila (FIFO) com nós encadeados -> fila.py

O que o enunciado pede e onde está:
  * trabalhos com aluno, arquivo e número de páginas ....... TrabalhoImpressao
  * enviar, imprimir próximo, listar e cancelar o último ... FilaDeImpressao
  * simulação com 10 a 20 trabalhos e relatório da
    sequência de impressão ................................. executar_demonstracao()

Por que fila: a impressora atende ESTRITAMENTE pela ordem de chegada, sem
prioridade, que é exatamente a disciplina FIFO. Enviar (enqueue) e imprimir
(dequeue) custam O(1).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fila import Fila
from utilidades import cabecalho, configurar_terminal, imprimir_tabela, secao

SEGUNDOS_POR_PAGINA = 5  # impressora do laboratório: 12 páginas por minuto


# ---------------------------------------------------------------------- horários
def para_segundos(horario: str) -> int:
    """"08:01:30" -> segundos desde a meia-noite."""
    horas, minutos, segundos = (int(parte) for parte in horario.split(":"))
    return horas * 3600 + minutos * 60 + segundos


def formatar_horario(segundos: int) -> str:
    horas, resto = divmod(int(segundos), 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def formatar_duracao(segundos: float) -> str:
    minutos, segundos = divmod(int(round(segundos)), 60)
    return f"{minutos}min{segundos:02d}s"


# ---------------------------------------------------------------------- domínio
@dataclass
class TrabalhoImpressao:
    numero: int
    aluno: str
    arquivo: str
    paginas: int
    enviado_em: int                 # segundos desde 00:00
    inicio: Optional[int] = None    # preenchido quando a impressora pega o trabalho
    fim: Optional[int] = None

    @property
    def espera(self) -> int:
        """Tempo entre o envio e o início da impressão, em segundos."""
        return self.inicio - self.enviado_em

    def descricao(self) -> str:
        return f"#{self.numero:02d} {self.aluno} - {self.arquivo} ({self.paginas} p.)"


class FilaDeImpressao:
    """Fila de trabalhos da impressora: atende pela ordem de chegada."""

    def __init__(self):
        self._fila = Fila()
        self._proximo_numero = 1

    def enviar(self, aluno: str, arquivo: str, paginas: int, enviado_em: int = 0) -> TrabalhoImpressao:
        """Enfileira um trabalho novo (enqueue). O(1)."""
        if paginas <= 0:
            raise ValueError("o trabalho precisa ter pelo menos 1 página")
        trabalho = TrabalhoImpressao(self._proximo_numero, aluno, arquivo, paginas, enviado_em)
        self._proximo_numero += 1
        self._fila.enqueue(trabalho)
        return trabalho

    def imprimir_proximo(self) -> TrabalhoImpressao:
        """Retira o trabalho mais antigo (dequeue). O(1). IndexError se vazia."""
        return self._fila.dequeue()

    def proximo(self) -> TrabalhoImpressao:
        """Consulta quem será impresso a seguir (front). O(1)."""
        return self._fila.front()

    def cancelar_ultimo(self) -> Optional[TrabalhoImpressao]:
        """Cancela o ÚLTIMO trabalho enviado que ainda está aguardando. O(n).

        Uma fila só remove pelo início, então usamos uma FILA AUXILIAR (o
        "conceito auxiliar" do enunciado): passamos para ela todos os
        trabalhos menos o último, descartamos o último e a auxiliar passa a
        ser a fila principal. A ordem dos demais é preservada e só são usadas
        operações de fila (enqueue/dequeue). Devolve None se não houver
        trabalho aguardando.
        """
        if self._fila.is_empty():
            return None
        auxiliar = Fila()
        while self._fila.size() > 1:
            auxiliar.enqueue(self._fila.dequeue())
        cancelado = self._fila.dequeue()   # sobrou exatamente o último enviado
        self._fila = auxiliar
        return cancelado

    def listar(self) -> list:
        """Trabalhos aguardando, do próximo a imprimir até o último. O(n)."""
        return list(self._fila)

    def esta_vazia(self) -> bool:
        return self._fila.is_empty()

    def __len__(self) -> int:
        return self._fila.size()


# ---------------------------------------------------------------------- simulação
@dataclass
class Evento:
    horario: str
    acao: str           # "enviar", "cancelar" ou "listar"
    aluno: str = ""
    arquivo: str = ""
    paginas: int = 0


EVENTOS_DO_LABORATORIO = [
    Evento("08:00:05", "enviar", "Ana Beatriz", "relatorio_fisica.pdf", 12),
    Evento("08:00:40", "enviar", "Bruno Henrique", "lista_calculo2.pdf", 4),
    Evento("08:01:10", "enviar", "Camila Rocha", "tcc_capitulo3.docx", 38),
    Evento("08:01:30", "enviar", "Diego Martins", "slides_banco_dados.pptx", 20),
    Evento("08:02:00", "enviar", "Eduarda Lima", "artigo_ia.pdf", 9),
    Evento("08:02:20", "cancelar"),  # Eduarda percebeu que mandou a versão antiga
    Evento("08:02:50", "enviar", "Eduarda Lima", "artigo_ia_v2.pdf", 9),
    Evento("08:03:15", "enviar", "Felipe Araújo", "mapa_mental.png", 1),
    Evento("08:04:00", "enviar", "Gabriela Nunes", "resumo_anatomia.pdf", 15),
    Evento("08:04:20", "enviar", "Henrique Souza", "trabalho_python.py", 6),
    Evento("08:05:30", "enviar", "Isabela Freitas", "fichamento_sociologia.docx", 5),
    Evento("08:06:10", "enviar", "João Pedro", "prova_2025.pdf", 8),
    Evento("08:07:00", "enviar", "Karina Alves", "poster_semana_academica.pdf", 2),
    Evento("08:07:30", "enviar", "Lucas Ferreira", "apostila_redes.pdf", 64),
    Evento("08:07:45", "cancelar"),  # Lucas mandou a apostila inteira sem querer
    Evento("08:08:00", "listar"),
    Evento("08:08:30", "enviar", "Marina Costa", "lista_exercicios_fisica.pdf", 3),
    Evento("08:09:00", "enviar", "Nicolas Barros", "relatorio_quimica.pdf", 11),
    Evento("08:10:15", "enviar", "Olívia Mendes", "curriculo.pdf", 2),
    Evento("08:11:00", "enviar", "Rafael Teixeira", "projeto_final_es.pdf", 25),
    Evento("08:12:00", "cancelar"),  # tarde demais: o trabalho do Rafael já está imprimindo
]


class SimuladorLaboratorio:
    """Simula a impressora ao longo da manhã, processando os eventos em ordem cronológica."""

    def __init__(self, segundos_por_pagina: int = SEGUNDOS_POR_PAGINA, mostrar: bool = True):
        self.fila = FilaDeImpressao()
        self.segundos_por_pagina = segundos_por_pagina
        self.mostrar = mostrar
        self.em_impressao = None   # trabalho que está saindo da impressora agora
        self.livre_desde = 0       # instante em que a impressora ficou livre
        self.impressos = []        # sequência real de impressão (para o relatório)
        self.cancelados = []
        self.enviados = 0

    def _registrar(self, instante: int, evento: str, texto: str) -> None:
        if self.mostrar:
            print(f"{formatar_horario(instante)}  {evento:<10}  {texto}")

    def avancar_ate(self, instante: float) -> None:
        """A impressora trabalha até `instante`: termina trabalhos e começa os próximos."""
        while True:
            if self.em_impressao is not None and self.em_impressao.fim <= instante:
                self.impressos.append(self.em_impressao)          # terminou de imprimir
                self.livre_desde = self.em_impressao.fim
                self.em_impressao = None
            elif self.em_impressao is None and not self.fila.esta_vazia():
                trabalho = self.fila.imprimir_proximo()            # dequeue: O(1)
                trabalho.inicio = max(self.livre_desde, trabalho.enviado_em)
                trabalho.fim = trabalho.inicio + trabalho.paginas * self.segundos_por_pagina
                self.em_impressao = trabalho
                self._registrar(trabalho.inicio, "IMPRIMINDO",
                                f"{trabalho.descricao()}  [aguardando: {len(self.fila)}]")
            else:
                break

    def processar(self, evento: Evento) -> None:
        instante = para_segundos(evento.horario)
        self.avancar_ate(instante)
        if evento.acao == "enviar":
            trabalho = self.fila.enviar(evento.aluno, evento.arquivo, evento.paginas, instante)
            self.enviados += 1
            self._registrar(instante, "ENVIADO", f"{trabalho.descricao()}  [aguardando: {len(self.fila)}]")
        elif evento.acao == "cancelar":
            cancelado = self.fila.cancelar_ultimo()
            if cancelado is None:
                self._registrar(instante, "CANCELAR", "nada a cancelar: o último trabalho já está na impressora")
            else:
                self.cancelados.append(cancelado)
                self._registrar(instante, "CANCELADO", f"{cancelado.descricao()}  [aguardando: {len(self.fila)}]")
        elif evento.acao == "listar":
            self._registrar(instante, "LISTAR", f"{len(self.fila)} trabalho(s) aguardando, na ordem de impressão:")
            if self.mostrar:
                for posicao, trabalho in enumerate(self.fila.listar(), start=1):
                    print(f"{'':22}{posicao}º  {trabalho.descricao()}")
        else:
            raise ValueError(f"ação desconhecida: {evento.acao}")

    def executar(self, eventos) -> None:
        for evento in eventos:
            self.processar(evento)
        self.avancar_ate(float("inf"))   # imprime tudo o que sobrou na fila


# ---------------------------------------------------------------------- demonstração
def executar_demonstracao() -> None:
    cabecalho("SP02 - Fila de impressão do Laboratório de Informática (Fila FIFO)")
    print(f"Impressora: 12 páginas/min ({SEGUNDOS_POR_PAGINA} s por página). "
          "Os trabalhos são atendidos só pela ordem de chegada.")

    secao("Linha do tempo da manhã")
    simulador = SimuladorLaboratorio()
    simulador.executar(EVENTOS_DO_LABORATORIO)

    secao("Relatório da sequência de impressão")
    linhas = []
    for ordem, t in enumerate(simulador.impressos, start=1):
        linhas.append([f"{ordem}º", f"#{t.numero:02d}", t.aluno, t.arquivo, t.paginas,
                       formatar_horario(t.enviado_em), formatar_horario(t.inicio),
                       formatar_horario(t.fim), formatar_duracao(t.espera)])
    imprimir_tabela(["Ordem", "Nº", "Aluno", "Arquivo", "Págs", "Envio", "Início", "Fim", "Espera"],
                    linhas, "<<<<>>>>>")

    impressos = simulador.impressos
    paginas = sum(t.paginas for t in impressos)
    espera_media = sum(t.espera for t in impressos) / len(impressos)
    maior = max(impressos, key=lambda t: t.espera)
    ordem_fifo = all(impressos[i].numero < impressos[i + 1].numero for i in range(len(impressos) - 1))

    secao("Resumo")
    print(f"Trabalhos enviados .......... {simulador.enviados}")
    print(f"Cancelados .................. {len(simulador.cancelados)} "
          f"({', '.join(c.descricao() for c in simulador.cancelados)})")
    print(f"Impressos ................... {len(impressos)} ({paginas} páginas)")
    print(f"Espera média ................ {formatar_duracao(espera_media)}")
    print(f"Maior espera ................ {formatar_duracao(maior.espera)} ({maior.aluno})")
    print(f"Fim da última impressão ..... {formatar_horario(impressos[-1].fim)}")
    print(f"Ordem de chegada respeitada . {'sim' if ordem_fifo else 'NÃO'} "
          "(números dos trabalhos sempre crescentes)")


if __name__ == "__main__":
    configurar_terminal()
    executar_demonstracao()
