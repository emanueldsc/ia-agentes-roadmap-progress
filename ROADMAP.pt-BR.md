# Roadmap — Dominar IA e Agentes de IA para Criar Aplicações e Negócios
Data de referência: 2026-04-08  
Autor: Serasa Emanuel Costa

---

## Visão geral
Este roadmap organiza, em fases, o que aprender para dominar **IA (Machine Learning + LLMs)** e **Agentes de IA**, com foco em **criar aplicações**, levar para **produção** e começar a **construir negócios**.

Cada fase contém:
- **Objetivo**
- **O que aprender**
- **Projetos** (para consolidar e provar competência)

---

## Fase 0 — Fundamentos de programação (2–6 semanas)
### Objetivo
Conseguir construir e manter um app simples, manipular APIs e dados, e trabalhar com ferramentas de desenvolvimento.

### Aprender
- **Python** (prioridade) e um pouco de **JavaScript/TypeScript** (útil para front/back)
- Git e GitHub (branch, PR, versionamento)
- Ambientes e dependências: `venv`/Poetry, `pip`, requirements, boas práticas de reprodutibilidade
- Docker básico (build, run, volumes) + noções de docker-compose
- HTTP/REST, JSON, autenticação (tokens, JWT, OAuth básico)
- Testes básicos (pytest), logging, tratamento de erros
- Banco de dados (SQL básico) e ORM (SQLAlchemy) — noções

### Projetos
- API simples em **FastAPI** (CRUD + autenticação)
- Bot/serviço que consome uma API externa e armazena dados (SQLite/Postgres)
- Pequeno CLI em Python para automatizar uma tarefa (ex.: organizar arquivos, gerar relatórios)

---

## Fase 1 — Base matemática e estatística “pra IA prática” (2–6 semanas em paralelo)
### Objetivo
Entender por que modelos erram, o que é overfitting, e como avaliar resultados com métricas.

### Aprender (focado no essencial)
- Álgebra linear: vetores, matrizes, produto escalar, norma, multiplicação de matrizes (intuição)
- Cálculo: derivada e intuição de gradiente (otimização)
- Probabilidade/estatística: distribuições, correlação vs causalidade, Bayes (intuição), média/variância
- Métricas:
  - Classificação: acurácia, precisão/recall/F1, ROC-AUC
  - Regressão: MAE/RMSE
- Conceitos-chave: viés vs variância, overfitting vs underfitting, dataset shift (noção)

### Projetos
- Notebook com regressão linear/logística “do zero” (simples, mas completo)
- Experimento guiado: mostrar overfitting alterando complexidade do modelo e tamanho do dataset
- Análise de um dataset público e relatório com métricas e interpretação

---

## Fase 2 — Machine Learning “clássico” (4–8 semanas)
### Objetivo
Saber construir modelos para problemas comuns e entender pipeline de ML do dado ao modelo.

### Aprender
- Pré-processamento: limpeza, encoding, normalização, tratamento de missing values
- Modelos: árvores, random forest, gradient boosting (XGBoost/LightGBM), regressões regulares
- Validação: split, cross-validation, leakage, validação temporal (séries)
- Feature engineering (prática) e interpretação (feature importance, SHAP básico)
- Scikit-learn: pipelines, transformers, `ColumnTransformer`
- Noções de MLOps²:
  - versionamento de dados/modelos (conceito)
  - rastreamento de experimentos (MLflow ou equivalente)

### Projetos
- Classificador de churn/fraude/propensão (pipeline completo, com relatório)
- Modelo com tracking² (MLflow) e comparação de abordagens
- Mini-projeto “do dado ao deploy⁶”: servir um modelo via FastAPI (endpoint `/predict`)

---

## Fase 3 — Deep Learning e LLMs (4–10 semanas)
### Objetivo
Entender redes neurais e como LLMs funcionam e são usados em produtos.

### Aprender
- Fundamentos de deep learning:
  - embeddings
  - MLP
  - noções de CNN/RNN (contexto histórico)
- Atenção e Transformer (conceitos essenciais)
- Treino vs inferência, custo/latência e limitações (context window, alucinações)
- Tokenização e contexto
- Estratégias:
  - prompting³
  - **RAG⁷**
  - fine-tuning⁴ (conceito) e LoRA (noção prática)
- Ferramentas: PyTorch (ou TensorFlow), Hugging Face (noções)

### Projetos
- Classificação de texto com fine-tuning⁴ leve (ou LoRA) em dataset pequeno
- Comparar prompting³ vs fine-tuning⁴ vs RAG⁷ para um mesmo problema (documentar trade-offs)
- “Playground⁸” de prompts com registro de resultados e versões (mesmo que simples)

---

## Fase 4 — Engenharia de produtos com LLM (prompting + avaliações) (3–6 semanas)
### Objetivo
Sair do “demo” e chegar em algo confiável (qualidade, testes, segurança e observabilidade).

### Aprender
- Prompting³ para produção:
  - instruções claras, few-shot, cadeia de raciocínio **não exposta** (quando aplicável)
  - saídas estruturadas (JSON), schemas e validação
  - tool calling⁹ (funções), roteamento por intenção
- **Avaliação**:
  - golden set¹⁰ (conjunto de casos)
  - testes automatizados e regressão de prompts
  - métricas: utilidade, consistência, groundedness, taxa de falhas
- Segurança e conformidade:
  - PII¹¹ e dados sensíveis
  - jailbreak¹²/prompt injection¹³ (noções)
  - políticas internas e logs de auditoria
- Observabilidade:
  - logs estruturados
  - tracing¹⁴ (ex.: OpenTelemetry — noção)
  - análise de falhas e feedback do usuário

### Projetos
- “Assistente especialista” com:
  - entradas estruturadas
  - saídas em JSON validado
  - suíte de testes (20–100 casos)
  - dashboard¹⁵ simples de erros (ou relatório periódico)
- Implementar fallback¹⁶ e mensagens de erro “humanas” quando o modelo falhar

---

## Fase 5 — RAG (Retrieval-Augmented Generation) bem feito (4–8 semanas)
### Objetivo
Fazer IA consultar conhecimento da empresa/cliente com alta qualidade e rastreabilidade.

### Aprender
- Preparação de dados:
  - chunking, overlap, deduplicação
  - metadados, filtros, permissões por documento (ACL¹⁷)
- Embeddings e busca vetorial
- Híbrido (vetorial + keyword) — quando fizer sentido
- Reranking e query rewriting
- Avaliar RAG⁷:
  - recall/precision de recuperação
  - groundedness (resposta apoiada nas fontes)
  - citações e trechos usados
- Bancos vetoriais: pgvector, Pinecone, Weaviate, Milvus (escolha 1)

### Projetos
- RAG⁷ para documentos (PDF/Notion/Drive) com:
  - indexação incremental
  - citações e trechos usados
  - fallback¹⁶ quando não encontra
  - avaliação offline + logs de produção
- “RAG⁷ com permissões”: garantir que usuários diferentes vejam respostas diferentes conforme acesso

---

## Fase 6 — Agentes de IA (4–10 semanas)
### Objetivo
Criar agentes que planejam, usam ferramentas, executam tarefas e funcionam com segurança em produção.

### Aprender (em ordem sugerida)
1. **Tool calling⁹ / function calling** (chamar APIs, DB, serviços)
2. **Orquestração**:
   - planner-executor
   - ReAct¹⁸
   - roteamento por intenção
3. **Memória** (do jeito certo)
   - memória de curto prazo (contexto)
   - memória longa (perfil, preferências) com controle e consentimento
4. **Estados e workflows¹⁹**
   - máquinas de estado, filas, retries, idempotência
   - execução assíncrona (Celery/Redis, Temporal etc.)
   - execução “human-in-the-loop²⁰” (aprovação antes de ações críticas)
5. **Multi-agente** (quando realmente precisa)
   - especialista por domínio + agregador
6. **Segurança**
   - permissões por ferramenta
   - validação de output (schemas)
   - limites de custo e tempo
   - prevenção de prompt injection¹³ em RAG⁷
   - sandboxing²¹ de ferramentas (o agente não deve “poder tudo”)

### Projetos
- Agente “operador” que:
  - lê emails/tickets
  - classifica + resume
  - consulta base de conhecimento (RAG⁷)
  - sugere resposta
  - abre/atualiza chamados via API
- Agente de negócio:
  - “Gerador de propostas comerciais” + envio + integração com CRM
- Agente “automações internas”:
  - cria tarefas em um board (ex.: Jira/Trello)
  - gera relatórios semanais automáticos
  - pede aprovação humana para ações críticas

---

## Fase 7 — Produção: backend, arquitetura, custo e performance (contínuo)
### Objetivo
Transformar agentes em produtos que vendem e escalam.

### Aprender
- Backend: FastAPI/NestJS, Postgres, Redis
- Filas e jobs: Celery/RQ/Temporal
- Cache e rate limiting
- Multi-tenant²² (vários clientes no mesmo sistema) e isolamento de dados
- Observabilidade:
  - OpenTelemetry (noções)
  - logs estruturados e correlação por request/trace
  - auditoria de ações do agente (quem fez o quê e por quê)
- Custos:
  - controle de tokens
  - modelos por tier²³ (barato vs caro)
  - roteamento por complexidade
  - caching de respostas e de recuperação (RAG⁷)
- Performance e confiabilidade:
  - timeouts, retries, circuit breakers²⁴
  - idempotência em operações externas
- Deploy⁶: Docker, CI/CD, Kubernetes (opcional), serverless (opcional)

### Projetos
- SaaS pequeno multi-tenant²² com billing simples (Stripe) e controle de uso
- Painel admin:
  - uso por cliente
  - custo estimado por cliente
  - auditoria de ações do agente
- “Playbook”¹ de incidentes:
  - o que fazer quando o modelo falha
  - rollback²⁵ de prompt/config
  - limites de segurança e bloqueio de ferramentas

---

## Fase 8 — Negócios com IA: como escolher problema, vender e escalar (paralelo desde a Fase 4)
### Objetivo
Não só “saber IA”, mas **ganhar dinheiro com IA**: escolher um problema que paga, entregar valor mensurável, vender e crescer.

### Aprender / Executar
- **Escolha de nicho** (critério prático):
  - alto custo operacional e tarefas repetitivas
  - backlog grande (tickets, análise, documentação, propostas)
  - dados/documentos disponíveis (para RAG⁷)
  - dor “urgente” e mensurável (tempo, dinheiro, risco)
- **Proposta de valor** (sempre quantificada):
  - “reduz X horas/semana”
  - “aumenta conversão em Y%”
  - “reduz tempo de resposta de A para B”
  - “reduz erros/compliance risk”
- **Posicionamento**:
  - automação (executa tarefas)
  - copiloto (sugere e humano aprova)
  - agente operador (atua com permissões limitadas)
- **GTM²⁶ (go-to-market) para começar rápido**:
  - consultivo B2B primeiro (serviço + produto)
  - produto self-serve depois (quando já souber o que funciona)
- **Pricing²⁷ (precificação)**:
  - por assento (seat)
  - por uso (tokens/ações/documentos)
  - por pacote (S/M/L)
  - por resultado (quando mensurável e controlável)
- **Retenção e expansão**:
  - onboarding²⁸ simples
  - “Aha moment”²⁹ rápido
  - métricas de valor (tempo economizado, tickets resolvidos etc.)
- **Riscos e responsabilidade**:
  - privacidade, retenção e consentimento
  - limites do agente (o que ele pode/não pode fazer)
  - registro/auditoria para clientes (principalmente B2B)

### Projetos (para virar negócio de verdade)
- **1 micro-produto em 30 dias**:
  - resolver UMA dor específica
  - entregar valor em 1 fluxo principal
  - cobrar (mesmo barato) para validar
- **5–15 entrevistas com potenciais clientes**:
  - mapear processo atual, custo e fricções
  - validar disposição de pagamento
- **MVP³⁰ com um cliente piloto**:
  - implementar em 1–2 semanas
  - medir “antes vs depois”
  - transformar em case e referência
- **Pacote comercial**:
  - landing page simples
  - demo gravada
  - proposta padrão (escopo + preço + limites + SLA básico)

---

## Trilha sugerida “em 90 dias” (velocidade)
- **Dias 1–15:** Python + APIs + Git + FastAPI  
- **Dias 16–35:** LLM apps (prompting³, tool calling⁹, structured outputs) + testes  
- **Dias 36–60:** RAG⁷ completo (indexação + avaliação + observabilidade)  
- **Dias 61–90:** Agente com workflow¹⁹ (fila, retries, permissões) + deploy⁶ + primeiros clientes pagantes  

---

## Perguntas para personalizar o roadmap
1. Você quer focar em **B2B** (empresas) ou **B2C** (consumidor final)?
2. Qual seu nível hoje: **iniciante / intermediário / avançado** em programação?
3. Você tem um nicho em mente (ex.: jurídico, saúde, imobiliário, financeiro, suporte ao cliente, marketing, RH)?

---

# Projetos para publicar no GitHub (portfólio de progresso)

A seção abaixo sugere uma sequência de projetos “de portfólio” que mostram evolução real: fundamentos → ML → LLM → RAG → agentes → produção → negócio.  
A ideia é você ir publicando cada projeto como um repositório separado, com README caprichado, releases e posts no LinkedIn.

---

## Sumário (tabela dos projetos)

| # | Projeto | O que demonstra | Tecnologias principais | Entregável / Demo |
|---|---------|------------------|------------------------|-------------------|
| 1 | **Python Automation CLI** | Fundamentos + boas práticas + testes | Python, Typer/Click, Pytest, Ruff/Black | CLI + README + testes |
| 2 | **FastAPI CRUD + Auth** | Backend pronto para produção | FastAPI, Pydantic, SQLAlchemy, Postgres, Docker | API documentada (OpenAPI) |
| 3 | **ML Pipeline (Churn/Fraude)** | ML clássico com validação e métricas | pandas, scikit-learn, MLflow, Jupyter | Relatório + modelo salvo |
| 4 | **LLM Prompt Playground + Evals** | Prompting³, JSON output, avaliação | Python, LLM SDK, JSON Schema, pytest | Suite de evals + relatório |
| 5 | **RAG Knowledge Base (com citações)** | RAG⁷ completo + observabilidade | FastAPI, embeddings, pgvector, reranker (opcional) | API + UI simples + logs |
| 6 | **Agent Operator (Tickets/Email)** | Agente com ferramentas + workflow¹⁹ | Orquestração, filas (Redis/Celery), RBAC | Demo end-to-end |
| 7 | **Multi-tenant AI SaaS Starter** | Produção, billing e métricas de custo | FastAPI/NestJS, Postgres, Redis, Stripe | SaaS básico com painel |
| 8 | **Mini Produto “de nicho”** | Produto + venda + iteração | Stack do seu preferido + analytics | Landing + demo + case |

> Dica: mantenha os projetos numerados no GitHub (prefixo no nome do repo) para ficar claro seu caminho de aprendizado.

---

## Como deixar cada projeto **Multi-language** (PT/EN/ES)

Você tem duas partes para internacionalizar:
1) **Documentação do repositório** (README, docs)  
2) **Aplicação** (UI, mensagens, mensagens de erro, e/ou conteúdo do agente)

### Padrão recomendado (documentação)
- Use um README principal em inglês (mais universal) e links para versões em PT/ES.

Estrutura sugerida:
- `README.md` (EN)
- `README.pt-BR.md`
- `README.es.md`
- `docs/en/...`
- `docs/pt-BR/...`
- `docs/es/...`

No topo de cada README:
- Links entre idiomas (language switch)

Exemplo (no topo do README):
- English | Português | Español

### Padrão recomendado (aplicação)
- Para **front-end (Next.js/React)**: `next-intl` ou `react-i18next`
- Para **back-end (FastAPI)**:
  - mensagens em um dicionário por idioma (simples)
  - ou `gettext` / `babel` se quiser algo mais “enterprise”
- Para **agentes**:
  - mantenha prompts em arquivos por idioma:
    - `prompts/en/system.md`
    - `prompts/pt-BR/system.md`
    - `prompts/es/system.md`
  - e selecione pelo `locale` do usuário (header, perfil ou parâmetro)

### Recomendações práticas
- Não traduza “na mão” tudo desde o dia 1: comece com PT e EN, depois inclua ES.
- Garanta consistência com:
  - chave de tradução (ex.: `errors.invalid_input`)
  - revisão manual nos textos críticos (principalmente marketing e termos legais)
- Adicione no GitHub:
  - label `i18n`
  - issues do tipo checklist¹ (“Translate README to ES/EN” etc.)

---

## Como publicar progresso no LinkedIn (modelo repetível)

Para cada projeto, faça um post com estrutura:
1. **Problema** (1 frase): “Eu queria aprender X e resolver Y”
2. **O que eu construí** (2–3 itens em lista (bullets¹))
3. **Stack** (linha curta)
4. **O que eu aprendi** (3 itens em lista (bullets¹))
5. **Link do GitHub** (repo)
6. **Próximo passo** (1 frase) — mostra continuidade

Formato de “série”:
- “Dia 1/90”, “Semana 2/12”, etc.
- Use sempre o mesmo padrão para criar consistência.

Checklist¹ antes de postar:
- README com screenshot/gif
- `How to run` (passo a passo)
- `Architecture` (diagrama simples)
- `Roadmap` (checklist¹ no README)
- `Changelog` (releases ou seção no README)

---

# Detalhamento dos projetos (um por um)

## 1) Python Automation CLI
### Objetivo
Mostrar fundamentos fortes: CLI, organização de projeto, testes, lint e distribuição.

### O que construir (exemplos)
- CLI que:
  - lê uma pasta de arquivos
  - renomeia/padroniza nomes
  - gera um CSV de inventário
  - cria um relatório em Markdown

### Tecnologias
- Python 3.11+
- Typer (ou Click) para CLI
- Pytest
- Ruff (lint) + Black (format)
- pre-commit (opcional)
- GitHub Actions (CI)

### Estrutura recomendada
- `src/<projeto>/...`
- `tests/...`
- `README.md` + `README.pt-BR.md` + `README.es.md`

### Como mostrar evolução no GitHub
- Issues do tipo checklist¹: “v1: MVP”, “v2: adicionar logs”, “v3: cobertura de testes”
- Releases: `v0.1`, `v0.2`, `v1.0`

### Post no LinkedIn (exemplo de tópicos)
- “Construí um CLI em Python com testes e CI”
- “Aprendi packaging + pre-commit + GitHub Actions”
- Link do repo + GIF curto rodando a CLI

---

## 2) FastAPI CRUD + Auth
### Objetivo
Demonstrar backend e arquitetura mínima de produção.

### O que construir
- API com:
  - cadastro/login (JWT)
  - CRUD de uma entidade (ex.: “clientes”, “tarefas”)
  - paginação e filtros
  - documentação Swagger/OpenAPI
  - migrations (Alembic)

### Tecnologias
- FastAPI + Pydantic
- SQLAlchemy + Alembic
- Postgres
- Docker + docker-compose
- Pytest

### Extras que contam pontos
- Rate limit básico
- Logs estruturados
- `.env.example` (nunca commitar secrets)

### Post no LinkedIn
- “Meu template de API pronta para produção”
- “Inclui auth, migrations, Docker e testes”

---

## 3) ML Pipeline (Churn/Fraude)
### Objetivo
Mostrar ML clássico com seriedade: validação, métricas e reprodutibilidade.

### O que construir
- Pipeline:
  - EDA
  - treino
  - validação
  - export do modelo
  - relatório final (Markdown)

### Tecnologias
- pandas, numpy
- scikit-learn
- MLflow (tracking²)
- matplotlib/seaborn
- Jupyter + scripts Python (evite ficar 100% no notebook)

### Entregáveis fortes
- `REPORT.md` com:
  - dataset, features
  - métricas
  - erros comuns
  - próximos passos

### Post no LinkedIn
- “Treinei um modelo de churn com pipeline e rastreamento”
- “Mostrei risco de leakage e como evitar”

---

## 4) LLM Prompt Playground + Evals
### Objetivo
Mostrar que você sabe ir além do “prompt bonito”: versão, testes e avaliação.

### O que construir
- Uma pequena aplicação (CLI ou web) que:
  - roda prompts versionados
  - exige saída JSON (schema)
  - roda um conjunto de testes (golden set¹⁰)
  - gera um relatório de métricas (ex.: taxa de parse, utilidade)

### Tecnologias
- Python
- SDK do provedor de LLM
- JSON Schema / Pydantic para validação
- pytest
- (Opcional) um dashboard¹⁵ simples com Streamlit

### Post no LinkedIn
- “Criei um framework simples de evals para prompts”
- “Agora consigo detectar regressões quando altero prompts”

---

## 5) RAG Knowledge Base (com citações)
### Objetivo
Mostrar RAG⁷ completo, com qualidade e rastreabilidade.

### O que construir
- Serviço que:
  - faz ingestão (PDF/Markdown)
  - cria embeddings
  - armazena em banco vetorial
  - responde com citações (trechos + fonte)
  - tem endpoint de avaliação offline

### Tecnologias
- FastAPI
- Vector store:
  - pgvector + Postgres
- (Opcional) reranker
- Observabilidade (mínimo):
  - logs + IDs de request
  - salvar queries e docs recuperados

### Post no LinkedIn
- “Construí uma base de conhecimento com RAG⁷ e citações”
- “Foquei em chunking, metadados e avaliação”

---

## 6) Agent Operator (Tickets/Email)
### Objetivo
Demonstrar agente real: ferramentas, workflow¹⁹ e segurança.

### O que construir
- Agente que:
  - recebe ticket/email (simulado)
  - classifica
  - consulta base de conhecimento (RAG⁷)
  - sugere resposta
  - (opcional) abre/atualiza ticket via API mock
  - pede aprovação humana (human-in-the-loop²⁰) para ações críticas

### Tecnologias
- Orquestração de agente (framework de sua escolha)
- FastAPI
- Redis + Celery (jobs assíncronos)
- Postgres (auditoria)
- RBAC simples (permissões por ferramenta)

### Post no LinkedIn
- “Criei um agente operador com ferramentas e aprovação humana”
- “Implementei auditoria e limites para evitar ações indevidas”

---

## 7) Multi-tenant AI SaaS Starter
### Objetivo
Mostrar capacidade de produto: multi-tenant²², billing, métricas e painel.

### O que construir
- SaaS com:
  - login
  - organizações/tenants
  - limites de uso
  - cobrança (Stripe)
  - painel de consumo (tokens/ações)

### Tecnologias
- Backend: FastAPI ou NestJS
- Postgres + Redis
- Stripe
- Docker + CI/CD
- Observabilidade básica

### Post no LinkedIn
- “Meu starter de SaaS multi-tenant²² com billing e tracking² de custos”
- “Arquitetura pronta para escalar com segurança”

---

## 8) Mini Produto “de nicho” (projeto final)
### Objetivo
Transformar conhecimento em negócio: resolver uma dor específica e vender.

### Exemplos de nicho (ideias)
- “Gerador de propostas” para prestadores de serviço
- “Classificador e respondedor de tickets” para e-commerce pequeno
- “Leitor de contratos” para time comercial (com extração de cláusulas)

### Tecnologias
- A stack que você já dominou nos projetos anteriores (consistência conta)
- Analytics (mesmo simples): evento de uso, funil básico
- Landing page (Next.js ou similar)

### Entregáveis
- Landing + demo
- “Case study” no README
- Roadmap público (issues/milestones)

### Post no LinkedIn
- “Lancei um micro-produto com IA e consegui X pilotos”
- “Medi impacto: antes vs depois”
- Link + CTA para testes/pilotos

---

## Checklist “padrão ouro” para cada repositório
- README (EN) + README.pt-BR.md + README.es.md
- `docs/` com guia de instalação e arquitetura
- `.env.example`
- CI com testes
- `CONTRIBUTING.md` (mesmo simples)
- `LICENSE`
- `CHANGELOG.md` ou Releases
- 1 screenshot/GIF de demo

---

# Legenda de termos em inglês (Glossário)

> Clique no número para ir para a explicação do termo.  
> Dica: no texto, os termos aparecem como `termo¹`, `termo²`, etc.

- [¹](#glossario-1-bullets-checklist-playbook) Bullets / Checklist / Playbook
- [²](#glossario-2-mlops-tracking) MLOps / Tracking
- [³](#glossario-3-prompting) Prompting
- [⁴](#glossario-4-fine-tuning) Fine-tuning
- [⁶](#glossario-6-deploy) Deploy
- [⁷](#glossario-7-rag) RAG (Retrieval-Augmented Generation)
- [⁸](#glossario-8-playground) Playground
- [⁹](#glossario-9-tool-calling-function-calling) Tool calling / Function calling
- [¹⁰](#glossario-10-golden-set) Golden set
- [¹¹](#glossario-11-pii) PII
- [¹²](#glossario-12-jailbreak) Jailbreak
- [¹³](#glossario-13-prompt-injection) Prompt injection
- [¹⁴](#glossario-14-tracing) Tracing
- [¹⁵](#glossario-15-dashboard) Dashboard
- [¹⁶](#glossario-16-fallback) Fallback
- [¹⁷](#glossario-17-acl) ACL
- [¹⁸](#glossario-18-react) ReAct
- [¹⁹](#glossario-19-workflow) Workflow
- [²⁰](#glossario-20-human-in-the-loop) Human-in-the-loop
- [²¹](#glossario-21-sandboxing) Sandboxing
- [²²](#glossario-22-multi-tenant) Multi-tenant
- [²³](#glossario-23-tier) Tier
- [²⁴](#glossario-24-circuit-breaker) Circuit breaker
- [²⁵](#glossario-25-rollback) Rollback
- [²⁶](#glossario-26-gtm) GTM (Go-to-market)
- [²⁷](#glossario-27-pricing) Pricing
- [²⁸](#glossario-28-onboarding) Onboarding
- [²⁹](#glossario-29-aha-moment) Aha moment
- [³⁰](#glossario-30-mvp) MVP

---

## Glossário 1: Bullets / Checklist / Playbook
<a id="glossario-1-bullets-checklist-playbook"></a>

- **Bullets / bullet points**: itens em lista com marcadores (ex.: `- item 1`, `- item 2`).
- **Checklist**: lista de tarefas para marcar como feito (ex.: `- [ ]` e `- [x]`).
- **Playbook**: guia operacional do que fazer em um cenário (ex.: “o que fazer quando a IA falhar”).

---

## Glossário 2: MLOps / Tracking
<a id="glossario-2-mlops-tracking"></a>

- **MLOps**: práticas e ferramentas para “operar ML em produção” (treino, deploy⁶, monitoramento, versionamento).
- **Tracking**: rastrear experimentos (hiperparâmetros, métricas, versões de dados/modelos), geralmente com MLflow.

---

## Glossário 3: Prompting
<a id="glossario-3-prompting"></a>

- **Prompting**: escrever instruções e exemplos para o LLM responder/agir bem (muito usado para apps e agentes).

---

## Glossário 4: Fine-tuning
<a id="glossario-4-fine-tuning"></a>

- **Fine-tuning**: ajustar um modelo previamente treinado com seus dados para melhorar desempenho em uma tarefa específica.

---

## Glossário 6: Deploy
<a id="glossario-6-deploy"></a>

- **Deploy**: publicar a aplicação/modelo para rodar em um servidor/serviço (deixar acessível para usuários).

---

## Glossário 7: RAG
<a id="glossario-7-rag"></a>

- **RAG (Retrieval-Augmented Generation)**: técnica em que o LLM busca informações em documentos/bases e responde usando essas fontes (ideal para “base de conhecimento”).

---

## Glossário 8: Playground
<a id="glossario-8-playground"></a>

- **Playground**: ambiente de testes/experimentos rápidos (para explorar prompts, modelos e configurações sem “quebrar produção”).

---

## Glossário 9: Tool calling / Function calling
<a id="glossario-9-tool-calling-function-calling"></a>

- **Tool calling / function calling**: o LLM chama “funções” (APIs) para executar ações (consultar banco, buscar dados, enviar mensagem), em vez de só gerar texto.

---

## Glossário 10: Golden set
<a id="glossario-10-golden-set"></a>

- **Golden set**: conjunto fixo de casos de teste representativos para medir qualidade e detectar regressões quando você muda prompt/modelo.

---

## Glossário 11: PII
<a id="glossario-11-pii"></a>

- **PII (Personally Identifiable Information)**: dados que identificam uma pessoa (ex.: CPF, e-mail, telefone, endereço).

---

## Glossário 12: Jailbreak
<a id="glossario-12-jailbreak"></a>

- **Jailbreak**: tentativa de “burlar” regras do modelo/sistema para obter respostas proibidas ou comportamento indevido.

---

## Glossário 13: Prompt injection
<a id="glossario-13-prompt-injection"></a>

- **Prompt injection**: quando um texto externo (ex.: documento no RAG ou mensagem do usuário) tenta “enganar” o agente para ignorar regras e executar ações erradas.

---

## Glossário 14: Tracing
<a id="glossario-14-tracing"></a>

- **Tracing**: rastrear o caminho de uma requisição (passo a passo) para debugar e medir latência/erros.

---

## Glossário 15: Dashboard
<a id="glossario-15-dashboard"></a>

- **Dashboard**: painel visual com métricas e indicadores (erros, custo, uso, latência etc.).

---

## Glossário 16: Fallback
<a id="glossario-16-fallback"></a>

- **Fallback**: plano alternativo quando algo falha (ex.: “não encontrei a informação” + pedir mais contexto ou escalar para humano).

---

## Glossário 17: ACL
<a id="glossario-17-acl"></a>

- **ACL (Access Control List)**: regra/lista de permissões para determinar quem pode acessar quais documentos/dados.

---

## Glossário 18: ReAct
<a id="glossario-18-react"></a>

- **ReAct**: padrão de agente que intercala raciocínio e ações (o agente “pensa” e usa ferramentas em ciclos).

---

## Glossário 19: Workflow
<a id="glossario-19-workflow"></a>

- **Workflow**: fluxo de etapas e regras para executar uma tarefa (com estados, filas, retries, aprovações, etc.).

---

## Glossário 20: Human-in-the-loop
<a id="glossario-20-human-in-the-loop"></a>

- **Human-in-the-loop**: quando uma pessoa aprova/revisa ações do agente antes de ele executar algo crítico.

---

## Glossário 21: Sandboxing
<a id="glossario-21-sandboxing"></a>

- **Sandboxing**: isolar e limitar o ambiente/permissões do agente para reduzir risco (não deixar o agente com acesso irrestrito).

---

## Glossário 22: Multi-tenant
<a id="glossario-22-multi-tenant"></a>

- **Multi-tenant**: um sistema que atende múltiplos clientes/organizações, mantendo dados isolados entre eles.

---

## Glossário 23: Tier
<a id="glossario-23-tier"></a>

- **Tier**: “camada” ou “nível” de serviço/preço (ex.: Básico, Pro, Enterprise) ou de modelos (barato vs caro).

---

## Glossário 24: Circuit breaker
<a id="glossario-24-circuit-breaker"></a>

- **Circuit breaker**: padrão para parar chamadas a um serviço que está falhando (evita cascata de falhas e melhora estabilidade).

---

## Glossário 25: Rollback
<a id="glossario-25-rollback"></a>

- **Rollback**: voltar para uma versão anterior (prompt, configuração, release) quando a nova versão deu problema.

---

## Glossário 26: GTM (Go-to-market)
<a id="glossario-26-gtm"></a>

- **GTM**: plano para levar produto ao mercado (público-alvo, canais, posicionamento, vendas).

---

## Glossário 27: Pricing
<a id="glossario-27-pricing"></a>

- **Pricing**: estratégia de precificação (como cobrar e como empacotar o produto).

---

## Glossário 28: Onboarding
<a id="glossario-28-onboarding"></a>

- **Onboarding**: primeiros passos do usuário para “pegar valor” no produto (ativação).

---

## Glossário 29: Aha moment
<a id="glossario-29-aha-moment"></a>

- **Aha moment**: momento em que o usuário percebe claramente o valor do produto (“agora entendi por que isso é útil”).

---

## Glossário 30: MVP
<a id="glossario-30-mvp"></a>

- **MVP (Minimum Viable Product)**: versão mínima do produto que já entrega valor e permite validar com clientes.
