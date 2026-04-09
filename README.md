# ia-agentes-roadmap-progress

Repositório para **documentar e rastrear** meu progresso no roadmap **“Dominar IA e Agentes de IA para Criar Aplicações e Negócios”**.

Este repo **não é** onde eu implemento os projetos finais (cada projeto terá seu próprio repositório). Aqui é o **hub de gestão**: planejamento, checklists, links, aprendizados, decisões e status.

## Documento principal (playbook)
- **Roadmap completo (PT-BR):** `ROADMAP.pt-BR.md`  
  Contém: Fases 0–8, trilha de 90 dias, projetos de portfólio (tabela + detalhamento), como publicar no LinkedIn, como manter repositórios multi-language (PT/EN/ES) e glossário com âncoras.

## Como usar este repositório (fluxo recomendado)
1. **Leia o playbook:** comece por `ROADMAP.pt-BR.md`.
2. **Escolha o projeto atual:** selecione 1 dos projetos do portfólio.
3. **Crie um repositório separado** para implementar o projeto (ex.: `01-python-automation-cli`).
4. **Registre aqui o progresso**:
   - atualize o arquivo `docs/project-XX-*.md` correspondente;
   - inclua link do repo do projeto, screenshots, decisões e lições aprendidas.
5. (Opcional) Use **Issues + Milestones** no GitHub para acompanhar tarefas por fase/projeto.

## Estrutura do repositório
- `ROADMAP.pt-BR.md` — o guia principal (playbook)
- `PROJECTS_TRACKING.md` — visão de status (checklist/tabela de acompanhamento)
- `docs/` — páginas de acompanhamento por projeto e templates
  - `docs/PROJECT_TEMPLATE.md` — modelo para documentar qualquer projeto
  - `docs/project-01-cli.md` — Projeto 1: Python Automation CLI
  - `docs/project-02-fastapi.md` — Projeto 2: FastAPI CRUD + Auth
  - `docs/project-03-ml-pipeline.md` — Projeto 3: ML Pipeline (Churn/Fraude)
  - `docs/project-04-llm-evals.md` — Projeto 4: LLM Prompt Playground + Evals
  - `docs/project-05-rag.md` — Projeto 5: RAG Knowledge Base
  - `docs/project-06-agent-operator.md` — Projeto 6: Agent Operator (Tickets/Email)
  - `docs/project-07-saas-multi-tenant.md` — Projeto 7: Multi-tenant AI SaaS Starter
  - `docs/project-08-mini-produto.md` — Projeto 8: Mini Produto de Nicho

## Padrões de registro (para manter consistência)
Em cada `docs/project-XX-*.md`:
- status (planejado / em andamento / concluído)
- o que foi entregue (demo, endpoints, UI, etc.)
- decisões técnicas e trade-offs
- problemas encontrados e como resolvi
- próximos passos
- link do repositório do projeto e (se existir) link do deploy

## Como publicar progresso no LinkedIn
O modelo de postagem está descrito em `ROADMAP.pt-BR.md`.  
Sugestão: poste sempre que fechar um “marco” (MVP, avaliação, deploy, 1ª demo, 1º cliente piloto).

## Multi-language (PT/EN/ES)
O padrão recomendado para manter seus projetos em 3 idiomas está em `ROADMAP.pt-BR.md` (documentação + app + prompts).

---

**Autor:** Emanuel Costa (@emanueldsc)  
**Última atualização:** 2026-04-09
