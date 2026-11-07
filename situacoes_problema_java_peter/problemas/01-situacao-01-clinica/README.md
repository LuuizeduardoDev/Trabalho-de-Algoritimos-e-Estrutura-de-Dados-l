## Problema 1 — Sistema de Atendimento de uma Clínica Médica

O projeto implementa uma fila manual com comportamento FIFO para simular o atendimento de 15 pacientes.

### Estrutura

- `Fila.java`: fila genérica implementada com nós encadeados próprios;
- `Paciente.java`: dados do paciente, horário de chegada e tipo de atendimento;
- `Clinica.java`: simulação, consulta da fila e relatório final;
- `TesteFila.java`: testes executáveis das operações da fila e da fila vazia.

Não são utilizadas `java.util.Queue` nem `java.util.LinkedList`.

### Compilação e execução

Na pasta do projeto:

```bash
javac -d bin *.java
java -cp bin TesteFila
java -cp bin Clinica
```

### Decisões para pontos não especificados

- `front` e `dequeue` lançam `IllegalStateException` quando a fila está vazia;
- o tempo médio é uma estimativa baseada em 15 minutos por atendimento;
- o horário de atendimento é calculado durante a simulação, a partir do horário de chegada e da disponibilidade do atendimento;
- a fila rejeita a inserção de `null` com `IllegalArgumentException`.

### Complexidade

As operações `enqueue`, `dequeue`, `front`, `isEmpty` e `size` possuem complexidade de tempo O(1). A fila utiliza O(n) de espaço para `n` elementos.
