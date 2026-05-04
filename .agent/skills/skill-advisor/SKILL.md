---
name: skill-advisor
description: Busca, avalia e sugere as melhores skills do skills.sh para um propósito específico. Use esta skill sempre que precisar encontrar ferramentas para novas tarefas, comparar opções existentes ou garantir que está usando skills populares. Ela lista as 5 mais baixadas, fornece uma análise comparativa opinativa e pode baixar automaticamente a skill escolhida para o repositório local usando `git clone`.
---

# Skill Advisor

Esta skill é seu guia para o ecossistema de skills do `skills.sh`. Ela busca e ajuda você a escolher a melhor opção técnica para qualquer necessidade.

## Diretrizes de Uso

### 1. Pesquisa e Descoberta
Quando o usuário solicitar uma skill ou uma funcionalidade, você deve:
- Realizar uma busca semântica na API pública: `GET https://skills.sh/api/search?q={termo}`
- A resposta contém uma lista de `skills`. Você deve ordenar os resultados pelo campo `installs` (decrescente).
- Selecionar as 5 principais skills.

### 2. Análise e Comparação
Apresente uma tabela comparativa com as seguintes colunas:
- **ID**: O `id` completo da skill (necessário para download).
- **Nome**: O nome da skill.
- **Instalações**: Quantidade de downloads.
- **Comparação/Destaque**: Avalie o nome e o id da skill para deduzir seu foco principal em relação às outras.
- **Origem**: Repositório de origem (campo `source`).

*Nota: A auditoria de segurança automatizada está indisponível na API pública atual. Aconselhe o usuário a revisar o código-fonte (SKILL.md) antes de executá-lo.*

### 3. Veredito Opinativo
Como um conselheiro especialista, indique **qual é a melhor escolha** baseando-se na popularidade (installs) e na relevância do nome para o que o usuário pediu.

### 4. Download Automático
Após o veredito, pergunte ao usuário se ele deseja baixar a skill recomendada.
Se ele confirmar, execute o script de download passando o ID completo (ex: `vercel-labs/agent-skills/vercel-react-best-practices`):
`python scripts/downloader.py --id "{skill_id}" --path "C:\SKILLS"`

