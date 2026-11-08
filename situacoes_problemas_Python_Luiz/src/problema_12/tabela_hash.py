"""Tabela hash com tratamento de colisões por ENCADEAMENTO SEPARADO.

Como funciona:
  1. A função de espalhamento (hash) transforma a chave em um número inteiro.
  2. O resto da divisão desse número pela capacidade escolhe o BALDE (posição
     do vetor) onde o par (chave, valor) será guardado.
  3. Duas chaves diferentes podem cair no mesmo balde: é a COLISÃO. Aqui cada
     balde é uma lista encadeada de nós, então os pares que colidem ficam
     encadeados no mesmo balde.
  4. Quando a tabela fica cheia demais (fator de carga = itens / baldes acima
     do limite), ela dobra de tamanho (próximo número primo) e redistribui
     todos os itens: o REDIMENSIONAMENTO (rehash). Assim as cadeias continuam
     curtas e as operações continuam O(1) em média.

Custos (n = itens, m = baldes, fator de carga a = n/m):
    inserir / buscar / remover ... O(1) em média (O(1 + a)), O(n) no pior caso
    redimensionar ................ O(n), raro (custo amortizado O(1) por inserção)
    espaço ....................... O(n + m)

Por que uma função de hash própria e não o hash() do Python?
    O hash() de textos muda a cada execução do Python (proteção de segurança),
    então os baldes e as colisões mudariam a cada vez que o programa roda.
    A função polinomial abaixo é determinística: os testes de colisão sempre
    dão o mesmo resultado.
"""

from __future__ import annotations


class _NoHash:
    """Nó da cadeia de um balde."""

    __slots__ = ("chave", "valor", "proximo")

    def __init__(self, chave, valor, proximo=None):
        self.chave = chave
        self.valor = valor
        self.proximo = proximo


def _eh_primo(numero: int) -> bool:
    if numero < 2:
        return False
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 1
    return True


def proximo_primo(numero: int) -> int:
    """Menor número primo maior ou igual a `numero`."""
    while not _eh_primo(numero):
        numero += 1
    return numero


class TabelaHash:
    """Tabela hash (dicionário) com encadeamento separado e redimensionamento."""

    def __init__(self, capacidade: int = 11, fator_carga_max=0.75):
        """
        capacidade ....... quantidade inicial de baldes (de preferência um primo);
        fator_carga_max .. acima desse fator a tabela redimensiona; use None
                           para nunca redimensionar (útil para estudar colisões).
        """
        if capacidade < 1:
            raise ValueError("a capacidade deve ser pelo menos 1")
        self._baldes = [None] * capacidade
        self._tamanho = 0
        self._fator_carga_max = fator_carga_max
        self.redimensionamentos = 0
        # Função opcional chamada como ao_redimensionar(capacidade_antiga, capacidade_nova);
        # as demonstrações usam para mostrar o momento do rehash.
        self.ao_redimensionar = None

    # ------------------------------------------------------------------ espalhamento
    @staticmethod
    def funcao_hash(chave) -> int:
        """Hash polinomial de 32 bits: h = h * 31 + código de cada caractere.

        É a mesma ideia do String.hashCode() do Java. Também aceita inteiros
        e tuplas (combinando o hash de cada parte).
        """
        if isinstance(chave, str):
            h = 0
            for caractere in chave:
                h = (h * 31 + ord(caractere)) & 0xFFFFFFFF  # mantém em 32 bits
            return h
        if isinstance(chave, int):
            return chave & 0xFFFFFFFF
        if isinstance(chave, tuple):
            h = 17
            for parte in chave:
                h = (h * 31 + TabelaHash.funcao_hash(parte)) & 0xFFFFFFFF
            return h
        raise TypeError(f"tipo de chave não suportado: {type(chave).__name__}")

    def indice_do_balde(self, chave) -> int:
        """Balde onde a chave fica: hash(chave) mod capacidade. O(tamanho da chave)."""
        return self.funcao_hash(chave) % len(self._baldes)

    # ------------------------------------------------------------------ operações principais
    def inserir(self, chave, valor=None) -> bool:
        """Insere ou atualiza. Devolve True se a chave era nova. O(1) em média."""
        indice = self.indice_do_balde(chave)
        no = self._baldes[indice]
        while no is not None:                 # a chave já existe? só atualiza
            if no.chave == chave:
                no.valor = valor
                return False
            no = no.proximo
        # chave nova: entra no INÍCIO da cadeia do balde (O(1))
        self._baldes[indice] = _NoHash(chave, valor, self._baldes[indice])
        self._tamanho += 1
        if self._fator_carga_max is not None and self.fator_carga() > self._fator_carga_max:
            self._redimensionar(proximo_primo(2 * len(self._baldes)))
        return True

    def buscar(self, chave, padrao=None):
        """Devolve o valor da chave, ou `padrao` se ela não existir. O(1) em média."""
        no = self._baldes[self.indice_do_balde(chave)]
        while no is not None:
            if no.chave == chave:
                return no.valor
            no = no.proximo
        return padrao

    def remover(self, chave) -> bool:
        """Remove a chave. Devolve True se ela existia. O(1) em média."""
        indice = self.indice_do_balde(chave)
        anterior = None
        no = self._baldes[indice]
        while no is not None:
            if no.chave == chave:
                if anterior is None:
                    self._baldes[indice] = no.proximo
                else:
                    anterior.proximo = no.proximo
                self._tamanho -= 1
                return True
            anterior = no
            no = no.proximo
        return False

    def contem(self, chave) -> bool:
        marcador = object()
        return self.buscar(chave, marcador) is not marcador

    # ------------------------------------------------------------------ redimensionamento
    def _redimensionar(self, nova_capacidade: int) -> None:
        """Cria um vetor maior e reposiciona cada nó no balde novo. O(n)."""
        antiga_capacidade = len(self._baldes)
        baldes_antigos = self._baldes
        self._baldes = [None] * nova_capacidade
        for no in baldes_antigos:
            while no is not None:
                seguinte = no.proximo
                indice = self.indice_do_balde(no.chave)  # o balde muda com a capacidade
                no.proximo = self._baldes[indice]
                self._baldes[indice] = no
                no = seguinte
        self.redimensionamentos += 1
        if self.ao_redimensionar is not None:
            self.ao_redimensionar(antiga_capacidade, nova_capacidade)

    # ------------------------------------------------------------------ estatísticas
    @property
    def capacidade(self) -> int:
        return len(self._baldes)

    def fator_carga(self) -> float:
        return self._tamanho / len(self._baldes)

    def tamanhos_das_cadeias(self) -> list:
        """Quantos itens há em cada balde (lista com `capacidade` posições)."""
        tamanhos = []
        for no in self._baldes:
            quantidade = 0
            while no is not None:
                quantidade += 1
                no = no.proximo
            tamanhos.append(quantidade)
        return tamanhos

    def cadeia(self, indice: int) -> list:
        """Chaves guardadas no balde `indice`, na ordem da cadeia."""
        chaves = []
        no = self._baldes[indice]
        while no is not None:
            chaves.append(no.chave)
            no = no.proximo
        return chaves

    def baldes_ocupados(self) -> int:
        return sum(1 for no in self._baldes if no is not None)

    def colisoes(self) -> int:
        """Itens que dividem o balde com outro item (itens - baldes ocupados)."""
        return self._tamanho - self.baldes_ocupados()

    def maior_cadeia(self) -> int:
        return max(self.tamanhos_das_cadeias(), default=0)

    # ------------------------------------------------------------------ percursos
    def itens(self):
        """Gera os pares (chave, valor). A ordem é a dos baldes, não a de inserção."""
        for no in self._baldes:
            while no is not None:
                yield (no.chave, no.valor)
                no = no.proximo

    def chaves(self):
        for chave, _ in self.itens():
            yield chave

    def valores(self):
        for _, valor in self.itens():
            yield valor

    # ------------------------------------------------------------------ atalhos no estilo dicionário
    def __len__(self) -> int:
        return self._tamanho

    def __contains__(self, chave) -> bool:
        return self.contem(chave)

    def __getitem__(self, chave):
        marcador = object()
        valor = self.buscar(chave, marcador)
        if valor is marcador:
            raise KeyError(chave)
        return valor

    def __setitem__(self, chave, valor) -> None:
        self.inserir(chave, valor)

    def __delitem__(self, chave) -> None:
        if not self.remover(chave):
            raise KeyError(chave)

    def __iter__(self):
        return self.chaves()

    def __repr__(self) -> str:
        return f"TabelaHash({self._tamanho} itens, {len(self._baldes)} baldes)"
