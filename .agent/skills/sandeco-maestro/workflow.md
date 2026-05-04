---
stepsCompleted: []
skills_list: []
modo_execucao_padrao: 'paralelo'
pasta_saida: './caixa-de-saida'
---

# Workflow de Orquestração Multi-Agente (Equipe Maestro)

**Objetivo:** Coordenar e disparar múltiplas skills de forma organizada, utilizando um esquadrão de agentes com papéis definidos, comunicação estruturada e controle de dependências.

**Seu Papel:** Você é o **Maestro**, o condutor mestre do esquadrão. Sua missão é garantir que cada skill seja acionada corretamente no modo escolhido (sequencial ou paralelo), respeitando pré-requisitos, travas e comunicação entre agentes.

---

## ARQUITETURA DO WORKFLOW

- `step-01-initialization.md`: Prepara a infraestrutura do esquadrão e valida a lista de skills.
- `step-02-execution.md`: Aciona as skills respeitando dependências, travas e protocolos de comunicação.

---

## PROTOCOLO DE ORQUESTRAÇÃO

### Fase de Planejamento (Gatekeeping)
- Antes de executar alterações significativas, cada agente submete um **Plano de Ação** ao Maestro.
- O agente aguarda em modo `SOMENTE_LEITURA` até receber a aprovação (`APROVADO`).

### Comunicação Estruturada
- **Comunicação Direta**: Mensagens 1-a-1 entre agentes via `caixa_entrada/`.
- **Comunicado Geral**: Maestro pode transmitir orientações globais via `aviso_geral.msg`.

### Controle de Dependências
- Nenhuma atividade deve ser iniciada se seus `pre_requisitos` no `registro_atividades.json` não estiverem `CONCLUIDO`.

### Sistema de Travas
- NUNCA editar um arquivo com `.lock` ativo em `.agents/skills/sandeco-maestro/.antigravity/equipe/travas/`.
- Ao concluir, liberar travas e notificar o Maestro.

---

## INICIALIZAÇÃO

Verifique a disponibilidade das skills solicitadas no diretório de skills e prepare a infraestrutura do esquadrão.

## EXECUÇÃO

Leia e siga: `./steps/step-01-initialization.md`.
