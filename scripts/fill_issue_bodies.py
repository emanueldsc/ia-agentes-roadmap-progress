"""
Script to fill GitHub issue bodies with content for each task.

For each issue in projects P01–P08, this script adds a body describing
what needs to be done and the Definition of Done (DoF).

Usage:
  GITHUB_TOKEN=<token> GITHUB_REPOSITORY=owner/repo python scripts/fill_issue_bodies.py

Options:
  --dry-run   Print what would be updated without making API calls.
  --issue N   Update only issue number N (for testing).
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error


# ---------------------------------------------------------------------------
# Issue bodies: issue_number -> markdown body
# ---------------------------------------------------------------------------

ISSUE_BODIES: dict[int, str] = {

    # -------------------------------------------------------------------------
    # P01 — Python Automation CLI
    # -------------------------------------------------------------------------

    3: """\
# O que fazer

Configurar o ambiente de desenvolvimento do projeto com gerenciamento de
dependências, linting, formatação e testes.

## Tarefas

- [ ] Inicializar o projeto com Poetry (ou venv + pip)
- [ ] Criar `pyproject.toml` com dependências: Typer/Click, Ruff, Black, Pytest
- [ ] Configurar Ruff para lint e Black para formatação automática
- [ ] Configurar Pytest com diretório de testes
- [ ] (Opcional) Configurar pre-commit hooks (Ruff + Black)
- [ ] Criar `.env.example` e `.gitignore` adequados

# (DoF)

- `ruff check .` passa sem erros
- `black --check .` passa sem erros
- `pytest` executa sem erros (mesmo que não haja testes ainda)
- Repositório criado no GitHub com a estrutura inicial commitada
""",

    4: """\
# O que fazer

Criar a estrutura de pastas padrão do projeto para separar código-fonte
de testes e facilitar a escalabilidade.

## Tarefas

- [ ] Criar pasta `src/<nome_do_projeto>/` com `__init__.py`
- [ ] Criar pasta `tests/` com `__init__.py` e `conftest.py`
- [ ] Criar arquivo de ponto de entrada da CLI (ex.: `cli.py` ou `main.py`)
- [ ] Criar arquivo de constantes/configurações (`config.py` ou `settings.py`)
- [ ] Garantir que o módulo é importável: `from <projeto> import ...`
- [ ] Criar um teste vazio como sanidade

# (DoF)

- Estrutura `src/` e `tests/` criada e funcional
- Módulo importável sem erros
- `pytest` executa o teste vazio sem erros
""",

    5: """\
# O que fazer

Implementar o comando de inventário que lista todos os arquivos de uma pasta
e exporta os metadados para CSV.

## Tarefas

- [ ] Criar o comando `inventory` (ou `inventario`) usando Typer/Click
- [ ] Receber um caminho de pasta como argumento obrigatório
- [ ] Listar arquivos recursivamente com os metadados:
  - Nome do arquivo
  - Extensão
  - Tamanho em bytes
  - Data de última modificação
  - Caminho relativo
- [ ] Exportar resultado para CSV (padrão: `inventario.csv`)
- [ ] Adicionar opção `--output` para nome customizado do arquivo
- [ ] Adicionar opção `--no-recursive` para desabilitar recursividade
- [ ] Escrever testes unitários para o comando

# (DoF)

- `cli inventory <pasta>` gera `inventario.csv` com as colunas:
  `nome`, `extensao`, `tamanho_bytes`, `data_modificacao`, `caminho_relativo`
- `--output relatorio.csv` salva no arquivo correto
- Testes passando para pasta válida e pasta inexistente
""",

    6: """\
# O que fazer

Implementar o comando de padronização de nomes de arquivos, aplicando
regras consistentes (lowercase, sem espaços, sem caracteres especiais).

## Tarefas

- [ ] Criar o comando `rename` (ou `padronizar`)
- [ ] Definir as regras de padronização:
  - Converter para lowercase
  - Substituir espaços por hífens (`-`)
  - Remover caracteres especiais (acentos, `@`, `#`, etc.)
  - Preservar extensão original
- [ ] Implementar modo **dry-run** (exibir o que seria renomeado sem executar)
- [ ] Pedir confirmação interativa antes de renomear (com flag `--yes` para pular)
- [ ] Salvar log das alterações realizadas (arquivo ou stdout)
- [ ] Escrever testes unitários para a função de padronização

# (DoF)

- `cli rename <pasta> --dry-run` exibe o mapeamento sem alterar arquivos
- `cli rename <pasta> --yes` renomeia todos os arquivos sem pedir confirmação
- Testes cobrindo: nome simples, nome com espaços, nome com acentos, nome sem mudança
""",

    7: """\
# O que fazer

Implementar o comando que gera um relatório em Markdown com estatísticas
sobre os arquivos de uma pasta.

## Tarefas

- [ ] Criar o comando `report` (ou `relatorio`)
- [ ] Analisar a pasta e calcular:
  - Total de arquivos e tamanho total
  - Distribuição por extensão (tabela com contagem e % do total)
  - Top 10 arquivos maiores
  - Arquivos mais recentes (últimas modificações)
- [ ] Gerar saída em Markdown estruturado com seções e tabelas
- [ ] Salvar o relatório em arquivo (padrão: `REPORT.md`)
- [ ] Adicionar opção `--output` para nome customizado
- [ ] Escrever testes unitários

# (DoF)

- `cli report <pasta>` gera `REPORT.md` com seções: Resumo, Distribuição,
  Top Maiores, Arquivos Recentes
- Relatório formatado em Markdown válido com tabelas
- Testes passando para pasta com arquivos e pasta vazia
""",

    8: """\
# O que fazer

Adicionar logging estruturado e tratamento de erros robusto à CLI para
garantir que falhas sejam comunicadas de forma clara e rastreável.

## Tarefas

- [ ] Configurar o módulo `logging` do Python com nível configurável (via `--verbose`)
- [ ] Definir formato de log: timestamp, nível, mensagem
- [ ] Tratar os erros mais comuns de forma graciosa:
  - Pasta não encontrada → mensagem clara + exit code 1
  - Permissão negada → aviso + pular arquivo
  - Arquivo em uso → aviso + continuar
- [ ] Nunca exibir traceback cru ao usuário (apenas no modo `--verbose`)
- [ ] (Opcional) Salvar log em arquivo com `--log-file`

# (DoF)

- Erros exibem mensagens amigáveis sem traceback exposto
- `--verbose` habilita log detalhado (DEBUG)
- CLI retorna exit code 0 em sucesso e 1 em erro
- Testes cobrindo cenários de erro (pasta inexistente, permissão negada)
""",

    9: """\
# O que fazer

Escrever testes unitários e de integração para os comandos da CLI,
atingindo cobertura mínima de 80%.

## Tarefas

- [ ] Criar fixtures no `conftest.py` (pasta temporária com arquivos de teste)
- [ ] Escrever testes para cada comando:
  - `inventory`: CSV gerado corretamente, pasta vazia, pasta inexistente
  - `rename`: dry-run, renomeação efetiva, conflito de nomes
  - `report`: relatório gerado, pasta vazia
- [ ] Testar casos de erro (permissão negada, arquivo em uso)
- [ ] Configurar `pytest-cov` e executar com `pytest --cov=src`
- [ ] Garantir cobertura ≥ 80% nos módulos principais

# (DoF)

- Todos os testes passando com `pytest`
- Cobertura ≥ 80% nos módulos de `src/`
- Relatório de cobertura gerado e documentado no README
""",

    10: """\
# O que fazer

Configurar integração contínua (CI) no GitHub Actions para rodar lint,
formatação e testes automaticamente em cada push e pull request.

## Tarefas

- [ ] Criar `.github/workflows/ci.yml`
- [ ] Configurar steps:
  - Checkout do código
  - Setup Python 3.11+
  - Instalação de dependências
  - `ruff check .` (lint)
  - `black --check .` (formatação)
  - `pytest --cov` (testes)
- [ ] Configurar trigger em `push` e `pull_request` na branch `main`
- [ ] Adicionar badge de status do CI no `README.md`

# (DoF)

- Workflow do GitHub Actions passando (verde) em todos os pushes
- Badge de CI verde no README
- CI falha se lint, formatação ou testes quebrarem
""",

    11: """\
# O que fazer

Criar o README em três idiomas (EN, PT-BR, ES) com language switch no
topo e incluir um screenshot ou GIF da CLI em funcionamento.

## Tarefas

- [ ] Criar `README.md` (Inglês) com:
  - Visão geral e proposta de valor
  - Pré-requisitos e instalação
  - How to run (exemplos de cada comando)
  - Arquitetura / estrutura do projeto
  - Roadmap / checklist de funcionalidades
  - Badge de CI
- [ ] Criar `README.pt-BR.md` (Português)
- [ ] Criar `README.es.md` (Espanhol)
- [ ] Adicionar language switch no topo de cada arquivo:
  `English | Português | Español`
- [ ] Incluir screenshot ou GIF da CLI rodando no README principal

# (DoF)

- Três READMEs criados com language switch
- README em inglês completo com todos os exemplos de comandos
- Screenshot/GIF mostrando pelo menos 2 comandos em funcionamento
""",

    12: """\
# O que fazer

Gravar e incluir no repositório um GIF ou screenshot demonstrando a CLI
em funcionamento para facilitar a compreensão visual do projeto.

## Tarefas

- [ ] Gravar um GIF curto (30–60s) mostrando:
  - `inventory` gerando CSV
  - `rename` em modo dry-run e depois com `--yes`
  - `report` gerando relatório Markdown
- [ ] Usar ferramenta como `asciinema`, `terminalizer` ou `ttyrec`
- [ ] Converter para GIF e otimizar tamanho (< 5 MB)
- [ ] Adicionar ao `README.md` e ao `README.pt-BR.md`
- [ ] Adicionar na seção de releases como asset (opcional)

# (DoF)

- GIF/screenshot claro e legível incluído no README
- Demonstra pelo menos 2 dos 3 comandos principais
- Arquivo de imagem commitado ou hospedado (GitHub Issues como CDN)
""",

    13: """\
# O que fazer

Criar a release v0.1 no GitHub e publicar um post no LinkedIn
documentando o projeto e os aprendizados.

## Tarefas

- [ ] Criar tag `v0.1` no GitHub (`git tag v0.1 && git push --tags`)
- [ ] Criar Release no GitHub com:
  - Título: "v0.1 — Python Automation CLI"
  - Changelog: o que foi implementado
  - Link para o README
- [ ] Escrever post no LinkedIn com o template do roadmap:
  1. Problema que resolvi
  2. O que construí (3 bullets)
  3. Stack utilizada
  4. O que aprendi (3 bullets)
  5. Link do GitHub
  6. Próximo passo
- [ ] Atualizar `PROJECTS_TRACKING.md` com status, link do repo e link do post

# (DoF)

- Release v0.1 publicada no GitHub
- Post publicado no LinkedIn
- `PROJECTS_TRACKING.md` atualizado com todos os links
""",

    # -------------------------------------------------------------------------
    # P02 — FastAPI CRUD + Auth
    # -------------------------------------------------------------------------

    14: """\
# O que fazer

Definir qual entidade será gerenciada pelo CRUD e documentar a modelagem
inicial do banco de dados antes de começar a implementação.

## Tarefas

- [ ] Escolher a entidade principal (ex.: Tarefas, Clientes, Produtos, Artigos)
- [ ] Definir os campos com tipos de dados (nome, tipo, obrigatório/opcional)
- [ ] Criar diagrama ER simplificado (pode ser em texto/Mermaid)
- [ ] Documentar a modelagem no README inicial do repositório
- [ ] Criar o repositório no GitHub com a estrutura básica

# (DoF)

- Entidade escolhida e documentada com todos os campos e tipos
- Diagrama ER (mesmo que simples) presente no README ou em `docs/`
- Repositório criado no GitHub com README inicial
""",

    15: """\
# O que fazer

Criar a estrutura inicial do projeto FastAPI com configurações,
variáveis de ambiente e endpoint de health check.

## Tarefas

- [ ] Criar repositório e instalar dependências:
  FastAPI, Uvicorn, Pydantic, python-dotenv (ou Pydantic Settings)
- [ ] Criar estrutura de pastas:
  - `app/` — pacote principal
  - `app/api/` — rotas
  - `app/models/` — modelos SQLAlchemy
  - `app/schemas/` — schemas Pydantic
  - `app/core/` — config, segurança, dependências
- [ ] Configurar variáveis de ambiente com Pydantic Settings
- [ ] Criar endpoint `GET /health` que retorna `{"status": "ok"}`
- [ ] Criar `.env.example` com todas as variáveis necessárias
- [ ] Garantir que `uvicorn app.main:app --reload` roda sem erros

# (DoF)

- `uvicorn app.main:app` sobe sem erros
- `GET /health` retorna 200 com `{"status": "ok"}`
- `.env.example` criado com todas as variáveis documentadas
""",

    16: """\
# O que fazer

Configurar o banco de dados PostgreSQL com SQLAlchemy e Alembic para
migrations versionadas.

## Tarefas

- [ ] Instalar SQLAlchemy e Alembic (+ psycopg2 ou asyncpg)
- [ ] Criar `app/db/session.py` com engine e SessionLocal
- [ ] Criar modelo SQLAlchemy para a entidade escolhida (`app/models/`)
- [ ] Inicializar Alembic: `alembic init alembic`
- [ ] Configurar `alembic/env.py` para usar o `DATABASE_URL` do ambiente
- [ ] Criar e aplicar a primeira migration: `alembic revision --autogenerate -m "create entity table"`
- [ ] Adicionar Postgres ao `docker-compose.yml`

# (DoF)

- `alembic upgrade head` aplica a migration sem erros
- Tabela da entidade criada no banco
- `docker-compose up postgres` sobe o banco corretamente
""",

    17: """\
# O que fazer

Implementar autenticação com JWT: cadastro de usuário, login e proteção
de rotas com o token.

## Tarefas

- [ ] Criar modelo `User` com campos: `id`, `email`, `hashed_password`, `created_at`
- [ ] Instalar `passlib[bcrypt]` e `python-jose[cryptography]` (ou `PyJWT`)
- [ ] Implementar `POST /auth/register` — criar usuário com senha hasheada
- [ ] Implementar `POST /auth/login` — validar credenciais e retornar JWT
- [ ] Criar função `get_current_user` como dependência FastAPI
- [ ] Configurar expiração do token (ex.: 30 minutos)
- [ ] Proteger ao menos uma rota com a dependência

# (DoF)

- `POST /auth/register` cria usuário e retorna `201`
- `POST /auth/login` com credenciais válidas retorna JWT
- Rota protegida retorna `401` sem token e `200` com token válido
""",

    18: """\
# O que fazer

Implementar os endpoints CRUD completos para a entidade escolhida,
com paginação e filtros.

## Tarefas

- [ ] Implementar os 5 endpoints:
  - `GET /items` — listar (com paginação)
  - `GET /items/{id}` — buscar por ID
  - `POST /items` — criar
  - `PUT /items/{id}` — atualizar
  - `DELETE /items/{id}` — deletar
- [ ] Adicionar paginação via `skip` e `limit` (ou cursor-based)
- [ ] Adicionar filtros nos parâmetros de query (ex.: busca por nome, status)
- [ ] Garantir que apenas o dono pode editar/deletar seu próprio item
- [ ] Documentar todos os endpoints no Swagger (via docstrings/schemas)

# (DoF)

- Todos os 5 endpoints funcionando e documentados no Swagger
- Paginação funcionando corretamente
- Filtros retornando resultados esperados
- Autorização: tentativa de editar item de outro usuário retorna `403`
""",

    19: """\
# O que fazer

Implementar schemas Pydantic para validação de entrada/saída e definir
um formato padronizado de erros da API.

## Tarefas

- [ ] Criar schemas Pydantic separados para: create, update, response
- [ ] Definir validações nos campos (ex.: email válido, string não-vazia, range de inteiro)
- [ ] Implementar handler de exceções global (`exception_handler`)
- [ ] Padronizar formato de erro: `{"error": "tipo", "detail": "mensagem"}`
- [ ] Mapear erros comuns:
  - `422` — dados inválidos (Pydantic)
  - `404` — recurso não encontrado
  - `401` — não autenticado
  - `403` — sem permissão
  - `500` — erro interno

# (DoF)

- Erros retornam formato padronizado em todos os casos
- Swagger/OpenAPI exibe os schemas de request e response corretamente
- Enviar dados inválidos retorna `422` com detalhe claro
""",

    20: """\
# O que fazer

Escrever testes com Pytest para cobrir as rotas críticas da API,
incluindo autenticação e CRUD.

## Tarefas

- [ ] Configurar cliente de teste com `TestClient` (ou `httpx.AsyncClient`)
- [ ] Configurar banco de dados de teste (SQLite in-memory ou Postgres de teste)
- [ ] Criar fixtures para: usuário autenticado, item criado
- [ ] Escrever testes para:
  - `register` e `login` (sucesso e falha)
  - CRUD completo (criar, listar, buscar, atualizar, deletar)
  - Autorização (acessar item de outro usuário)
  - Paginação e filtros
- [ ] Configurar `pytest-cov` e atingir ≥ 80% de cobertura nas rotas

# (DoF)

- Todos os testes passando com `pytest`
- Cobertura ≥ 80% nas rotas
- Testes de autorização cobrindo cenários de `401` e `403`
""",

    21: """\
# O que fazer

Containerizar a aplicação com Docker e criar um docker-compose que
sobe a API junto com o PostgreSQL.

## Tarefas

- [ ] Criar `Dockerfile` para a API (multi-stage opcional)
- [ ] Criar `docker-compose.yml` com serviços:
  - `api` — FastAPI rodando na porta 8000
  - `postgres` — banco de dados com volume persistente
- [ ] Configurar variáveis de ambiente no docker-compose
- [ ] Garantir que migrations rodam automaticamente no startup (entrypoint)
- [ ] Criar `docker-compose.override.yml` para desenvolvimento (hot-reload)
- [ ] Documentar o processo no README

# (DoF)

- `docker-compose up` sobe API e banco sem erros
- API acessível em `http://localhost:8000`
- Migrations aplicadas automaticamente no startup
- Volume do Postgres persistindo dados entre restarts
""",

    22: """\
# O que fazer

Configurar logs estruturados (JSON) na API para facilitar o rastreamento
de requisições e erros em produção.

## Tarefas

- [ ] Instalar `structlog` ou configurar o módulo `logging` em JSON
- [ ] Criar middleware para logar cada requisição:
  - Método HTTP, path, status code, duração
- [ ] Adicionar `request_id` único em cada requisição (header + log)
- [ ] Logar erros com stack trace (sem expor ao cliente)
- [ ] Garantir que o `user_id` aparece no log quando autenticado
- [ ] Documentar o formato de log no README

# (DoF)

- Cada requisição gera uma linha de log JSON com: `request_id`, `method`,
  `path`, `status_code`, `duration_ms`
- Erros internos logados com stack trace (apenas no servidor)
- `request_id` presente nos headers de resposta para rastreamento
""",

    23: """\
# O que fazer

Criar o README em três idiomas com instruções claras de como rodar a API
e incluir screenshot do Swagger.

## Tarefas

- [ ] Criar `README.md` (Inglês) com:
  - Visão geral e proposta de valor
  - Pré-requisitos (Docker, Python)
  - How to run (local e com Docker)
  - Tabela de endpoints
  - Variáveis de ambiente
  - Arquitetura (diagrama simples)
- [ ] Criar `README.pt-BR.md` (Português)
- [ ] Criar `README.es.md` (Espanhol)
- [ ] Adicionar language switch no topo
- [ ] Incluir screenshot do Swagger/OpenAPI em funcionamento

# (DoF)

- Três READMEs completos com language switch
- Screenshot do Swagger mostrando os endpoints documentados
- Instruções de "How to run" testadas e funcionando
""",

    24: """\
# O que fazer

Criar a release v1.0 no GitHub e publicar um post no LinkedIn
documentando o projeto de API.

## Tarefas

- [ ] Criar tag `v1.0` e Release no GitHub com changelog
- [ ] Escrever post no LinkedIn seguindo o template do roadmap:
  1. Problema resolvido
  2. O que construí (endpoints, auth, Docker)
  3. Stack utilizada
  4. Aprendizados (3 bullets)
  5. Link do GitHub
  6. Próximo passo
- [ ] Atualizar `PROJECTS_TRACKING.md` com status, link do repo e post

# (DoF)

- Release v1.0 publicada no GitHub com changelog
- Post publicado no LinkedIn
- `PROJECTS_TRACKING.md` atualizado
""",

    # -------------------------------------------------------------------------
    # P03 — ML Pipeline (Churn/Fraude)
    # -------------------------------------------------------------------------

    25: """\
# O que fazer

Escolher um dataset público e definir claramente o problema de Machine
Learning que será resolvido no projeto.

## Tarefas

- [ ] Pesquisar e escolher um dataset público relevante:
  - Kaggle: churn de telecomunicações, detecção de fraude, credit risk
  - UCI Machine Learning Repository
  - Hugging Face Datasets
- [ ] Definir o tipo de problema: classificação binária, multiclasse ou regressão
- [ ] Documentar:
  - Fonte e licença do dataset
  - Tamanho (linhas, colunas)
  - Colunas mais importantes e a variável target
  - Hipótese inicial sobre o que influencia o target
- [ ] Criar repositório com estrutura: `notebooks/`, `src/`, `data/`, `models/`

# (DoF)

- Dataset baixado e salvo em `data/raw/` (ou documentado como baixar)
- Problema definido e documentado em `README.md` com hipótese inicial
- Repositório criado no GitHub
""",

    26: """\
# O que fazer

Realizar a Análise Exploratória de Dados (EDA) e criar um modelo baseline
para ter um ponto de referência de performance.

## Tarefas

- [ ] Criar notebook `notebooks/01_eda.ipynb`
- [ ] Analisar:
  - Distribuições de variáveis numéricas e categóricas
  - Missing values (quantidade e padrão)
  - Outliers e valores inconsistentes
  - Correlação entre features e com o target
  - Desbalanceamento de classes (se classificação)
- [ ] Visualizações: histogramas, boxplots, heatmap de correlação, gráfico da target
- [ ] Criar modelo baseline simples (DummyClassifier ou regressão logística sem tuning)
- [ ] Documentar achados principais e hipóteses de features importantes

# (DoF)

- Notebook de EDA completo com visualizações
- Modelo baseline com métricas documentadas (F1, ROC-AUC ou RMSE)
- Principais achados resumidos no notebook e no README
""",

    27: """\
# O que fazer

Definir e implementar a estratégia de split de dados para evitar data
leakage e garantir avaliação justa do modelo.

## Tarefas

- [ ] Escolher e justificar a estratégia de split:
  - Random split com estratificação (problemas de classificação)
  - Split temporal (dados com componente de tempo)
- [ ] Implementar splits: treino (70%), validação (15%), teste (15%) — ou variação justificada
- [ ] Verificar ausência de data leakage:
  - Nenhuma informação do futuro no treino
  - Scaler/encoder fitado APENAS no treino
- [ ] Criar funções reutilizáveis em `src/data/split.py`
- [ ] Documentar a estratégia escolhida e os riscos de leakage identificados

# (DoF)

- Splits criados com proporções corretas e estratificação quando aplicável
- Nenhum leakage identificado na revisão
- Funções de split em `src/` importáveis e testadas
""",

    28: """\
# O que fazer

Construir um Pipeline scikit-learn completo de pré-processamento que
possa ser serializado e aplicado em produção.

## Tarefas

- [ ] Identificar colunas numéricas e categóricas
- [ ] Criar transformadores:
  - `SimpleImputer` para missing values (numérico: mediana, categórico: moda)
  - `StandardScaler` ou `MinMaxScaler` para numéricas
  - `OneHotEncoder` ou `OrdinalEncoder` para categóricas
- [ ] Unir com `ColumnTransformer`
- [ ] Encapsular em `Pipeline` scikit-learn (preprocessor → model placeholder)
- [ ] Serializar o pipeline com `joblib.dump` e testar o carregamento
- [ ] Criar testes unitários em `tests/`

# (DoF)

- Pipeline scikit-learn criado e sem erros ao fittar no treino
- Pipeline aplicado no validação/teste sem leakage
- Serializado e carregado com `joblib` sem erros
""",

    29: """\
# O que fazer

Treinar e comparar múltiplos modelos de árvore (Decision Tree, Random
Forest, GBM) registrando os experimentos no MLflow.

## Tarefas

- [ ] Treinar e comparar:
  - `DecisionTreeClassifier`
  - `RandomForestClassifier`
  - `XGBClassifier` (XGBoost) ou `LGBMClassifier` (LightGBM)
- [ ] Realizar tuning básico de hiperparâmetros com `GridSearchCV` ou `RandomizedSearchCV`
- [ ] Registrar cada experimento no MLflow:
  - Parâmetros do modelo e do pipeline
  - Métricas (F1, ROC-AUC)
  - Artefato: modelo serializado
- [ ] Selecionar o melhor modelo com base nas métricas de validação

# (DoF)

- ≥ 3 modelos treinados e comparados
- MLflow registrando todos os experimentos (acessível via `mlflow ui`)
- Melhor modelo identificado e justificado com métricas
""",

    30: """\
# O que fazer

Calcular métricas de avaliação completas no conjunto de teste e realizar
análise detalhada dos erros do modelo.

## Tarefas

- [ ] Calcular no conjunto de teste:
  - Classificação: F1, ROC-AUC, Precision, Recall, Accuracy
  - Matriz de confusão
- [ ] Analisar os erros:
  - Quais casos o modelo erra mais? (falsos positivos vs falsos negativos)
  - Existem padrões nos erros? (por faixa de valor, segmento, etc.)
- [ ] Gerar visualizações: curva ROC, matriz de confusão, histograma de scores
- [ ] Documentar insights no notebook e no `REPORT.md`

# (DoF)

- Métricas calculadas no conjunto de **teste** (não validação)
- Matriz de confusão gerada
- Análise de erros documentada com pelo menos 2 hipóteses explicativas
""",

    31: """\
# O que fazer

Aplicar técnicas de interpretabilidade para entender quais features mais
influenciam as predições do modelo.

## Tarefas

- [ ] Calcular e visualizar feature importance nativa do modelo (Random Forest/XGBoost)
- [ ] Aplicar SHAP para explicar predições individuais:
  - `shap.summary_plot` para visão global
  - `shap.waterfall_plot` para uma predição individual
- [ ] Identificar as top 5–10 features mais relevantes
- [ ] Documentar insights de negócio:
  - Quais features fazem sentido?
  - Existe alguma feature suspeita (possível leakage)?

# (DoF)

- Gráfico de feature importance gerado e salvo em `reports/figures/`
- Explicação SHAP para pelo menos 1 predição individual documentada
- Insights de negócio documentados no notebook ou `REPORT.md`
""",

    32: """\
# O que fazer

Garantir que todos os experimentos estão registrados corretamente no MLflow
e que a UI está funcionando localmente.

## Tarefas

- [ ] Verificar que todos os runs do MLflow têm:
  - Parâmetros (hiperparâmetros do modelo)
  - Métricas (F1, ROC-AUC, etc.)
  - Artefatos (modelo serializado, gráficos)
- [ ] Nomear experimentos e runs de forma descritiva
- [ ] Registrar o melhor modelo no Model Registry do MLflow
- [ ] Documentar como rodar o MLflow localmente: `mlflow ui`
- [ ] Criar script `src/train.py` reproduzível que treina e loga no MLflow

# (DoF)

- `mlflow ui` mostrando todos os experimentos com métricas e artefatos
- Melhor modelo registrado no Model Registry
- `python src/train.py` reproduz o treino do melhor modelo
""",

    33: """\
# O que fazer

Exportar o modelo final treinado e criar um endpoint ou script de
inferência para demonstrar uso em produção.

## Tarefas

- [ ] Exportar o modelo com `joblib.dump` em `models/final_model.joblib`
- [ ] Criar script de inferência `src/predict.py`:
  - Carrega o pipeline e o modelo
  - Recebe dados novos e retorna predições
- [ ] (Opcional) Criar endpoint FastAPI `POST /predict` que recebe dados JSON
- [ ] Documentar como usar o modelo com exemplo de input/output
- [ ] Salvar artefatos relevantes: scaler, encoder, modelo

# (DoF)

- Modelo exportado em `models/`
- `python src/predict.py` gera predições sem erros
- Exemplo de uso documentado no README com input e output esperados
""",

    34: """\
# O que fazer

Criar o relatório final do projeto em Markdown e os READMEs multilíngues
para o repositório.

## Tarefas

- [ ] Criar `REPORT.md` com seções:
  - Dataset: fonte, tamanho, features
  - Metodologia: pipeline, modelos testados, estratégia de validação
  - Métricas: tabela comparativa de modelos
  - Análise de erros: principais falhas e hipóteses
  - Interpretabilidade: top features
  - Próximos passos: o que poderia melhorar
- [ ] Criar `README.md` (Inglês) com visão geral e link para `REPORT.md`
- [ ] Criar `README.pt-BR.md` (Português)
- [ ] Incluir gráficos e tabelas de métricas no README

# (DoF)

- `REPORT.md` completo com todas as seções
- `README.md` (EN) e `README.pt-BR.md` criados com language switch
- Gráficos das métricas incluídos
""",

    35: """\
# O que fazer

Criar a release do projeto no GitHub e publicar um post no LinkedIn
documentando o pipeline de ML e os aprendizados.

## Tarefas

- [ ] Criar Release no GitHub com changelog e assets (modelo exportado, opcional)
- [ ] Escrever post no LinkedIn:
  1. Problema (classificação de churn/fraude)
  2. O que construí (EDA → pipeline → comparação de modelos → SHAP)
  3. Stack (scikit-learn, MLflow, pandas)
  4. Métricas alcançadas e aprendizados
  5. Link do GitHub
  6. Próximo passo
- [ ] Atualizar `PROJECTS_TRACKING.md`

# (DoF)

- Release publicada no GitHub
- Post publicado no LinkedIn
- `PROJECTS_TRACKING.md` atualizado com todos os links
""",

    # -------------------------------------------------------------------------
    # P04 — LLM Prompt Playground + Evals
    # -------------------------------------------------------------------------

    36: """\
# O que fazer

Definir o objetivo do playground de prompts e os casos de uso que serão
avaliados no projeto.

## Tarefas

- [ ] Escolher o domínio do playground (ex.: resumo de textos, extração de dados,
  classificação de sentimento, geração de respostas de suporte)
- [ ] Definir os casos de uso com:
  - Descrição do input
  - Output esperado (formato e conteúdo)
  - Critérios de qualidade (o que é uma boa resposta)
- [ ] Documentar tudo em `docs/spec.md`
- [ ] Criar repositório com estrutura básica

# (DoF)

- Documento `docs/spec.md` com objetivo, ≥ 3 casos de uso e critérios de qualidade
- Repositório criado no GitHub
""",

    37: """\
# O que fazer

Configurar o projeto Python e integrar o SDK do LLM escolhido, validando
que a primeira chamada funciona corretamente.

## Tarefas

- [ ] Criar repositório e instalar dependências (SDK do provedor: openai, anthropic, etc.)
- [ ] Configurar variável de ambiente para a API key (`.env` + `.env.example`)
- [ ] Criar módulo `src/llm_client.py` com função de chamada ao LLM
- [ ] Testar uma chamada simples (ex.: "Diga olá") e logar o resultado
- [ ] Criar estrutura de pastas:
  - `prompts/` — templates de prompts versionados
  - `evals/` — casos de avaliação
  - `src/` — código-fonte
  - `reports/` — relatórios gerados

# (DoF)

- `python src/llm_client.py` faz uma chamada e imprime a resposta
- `.env.example` com todas as variáveis documentadas
- Estrutura de pastas criada
""",

    38: """\
# O que fazer

Criar um sistema de versionamento de prompts usando uma estrutura de
pastas organizada e um loader em Python.

## Tarefas

- [ ] Definir estrutura de versionamento:
  ```
  prompts/
    v1/
      system.md
      user_template.md
      metadata.yaml  (descrição, data, autor)
    v2/
      ...
  ```
- [ ] Criar o loader `src/prompt_loader.py`:
  - Listar versões disponíveis
  - Carregar system prompt e user template de uma versão
  - Renderizar o template com variáveis (Jinja2 ou f-string)
- [ ] Criar prompts v1 para o caso de uso definido
- [ ] Documentar como criar uma nova versão de prompt

# (DoF)

- Estrutura de pastas criada com prompts v1
- Loader funcionando: `load_prompt("v1", input_data)` retorna o prompt renderizado
- Documentação de como versionar prompts no README
""",

    39: """\
# O que fazer

Implementar validação de saída JSON do LLM usando Pydantic ou JSON
Schema, com retry automático quando a validação falhar.

## Tarefas

- [ ] Definir o schema JSON esperado na saída do LLM (Pydantic model)
- [ ] Implementar parsing e validação da resposta do LLM
- [ ] Adicionar lógica de retry (máx. 2–3 tentativas) quando:
  - O LLM não retorna JSON válido
  - O JSON não passa na validação do schema
- [ ] Logar: tentativa número, erro de parsing, resposta recebida
- [ ] Calcular e logar a taxa de falha de parse

# (DoF)

- Resposta do LLM validada contra schema Pydantic
- Retry funcionando automaticamente em caso de JSON inválido
- Taxa de falha de parse sendo logada
""",

    40: """\
# O que fazer

Criar um golden set com casos de teste que servirá como base para
avaliação e regressão de prompts.

## Tarefas

- [ ] Criar arquivo `evals/golden_set.json` (ou `.yaml`) com estrutura:
  ```json
  [
    {
      "id": "001",
      "input": "...",
      "expected_output": {...},
      "acceptance_criteria": "..."
    }
  ]
  ```
- [ ] Criar ≥ 20 casos de teste cobrindo:
  - Casos comuns (happy path)
  - Casos edge (input vazio, input ambíguo, input muito longo)
  - Casos de falha esperada
- [ ] Documentar o critério de aceitação para cada caso

# (DoF)

- `evals/golden_set.json` com ≥ 20 casos de teste
- Cada caso tem: `id`, `input`, `expected_output`, `acceptance_criteria`
- Casos edge incluídos e documentados
""",

    41: """\
# O que fazer

Criar um runner que executa o LLM em todos os casos do golden set e
gera um relatório de métricas.

## Tarefas

- [ ] Criar `src/eval_runner.py`:
  - Iterar sobre todos os casos do golden set
  - Chamar o LLM com o prompt da versão atual
  - Comparar resultado com expected_output
  - Registrar: caso, resultado, passou/falhou, latência
- [ ] Calcular métricas agregadas:
  - Taxa de parse correto (JSON válido)
  - Taxa de aceitação (output dentro do critério)
  - Latência média e p95
- [ ] Gerar relatório em `reports/eval_YYYYMMDD.md`

# (DoF)

- `python src/eval_runner.py` executa todos os casos e gera relatório
- Relatório inclui métricas agregadas e lista de casos que falharam
""",

    42: """\
# O que fazer

Criar testes Pytest de regressão que detectam automaticamente quando
uma mudança de prompt degrada a qualidade das respostas.

## Tarefas

- [ ] Criar `tests/test_prompt_regression.py`
- [ ] Implementar testes que:
  - Rodam o runner no golden set (ou subconjunto)
  - Falham se a taxa de aceitação cair abaixo de um threshold (ex.: 80%)
  - Usam mock do LLM para evitar chamadas reais no CI (opcional)
- [ ] Integrar ao CI do GitHub Actions
- [ ] Documentar como rodar os testes de regressão

# (DoF)

- `pytest tests/test_prompt_regression.py` passa quando qualidade está ok
- CI falha automaticamente quando prompt regride
- Threshold de qualidade configurável por variável de ambiente ou config
""",

    43: """\
# O que fazer

(Opcional) Criar um dashboard simples com Streamlit para explorar prompts
interativamente e visualizar métricas.

## Tarefas

- [ ] Instalar Streamlit
- [ ] Criar `app.py` com funcionalidades:
  - Selector de versão de prompt
  - Campo de input customizado
  - Botão de executar e exibir resposta
  - Métricas da última execução (latência, passou/falhou)
- [ ] (Opcional) Adicionar comparação side-by-side entre versões de prompts
- [ ] Documentar como rodar: `streamlit run app.py`

# (DoF)

- `streamlit run app.py` abre o dashboard no navegador
- É possível selecionar versão de prompt, inserir input e ver resposta
- Documentação de como rodar no README
""",

    44: """\
# O que fazer

Criar README multilíngue com exemplos de input/output e incluir
uma demonstração visual do playground.

## Tarefas

- [ ] Criar `README.md` (Inglês) com:
  - Visão geral do projeto
  - How to run (local)
  - Como versionar prompts
  - Exemplo de input/output
  - Resultados do eval (taxa de aceitação, latência)
- [ ] Criar `README.pt-BR.md` (Português)
- [ ] Adicionar language switch no topo
- [ ] Incluir GIF ou screenshot do playground/dashboard
- [ ] Incluir exemplo de relatório de eval

# (DoF)

- `README.md` (EN) e `README.pt-BR.md` criados com language switch
- Exemplo de input/output documentado
- Demo visual (GIF/screenshot) incluída
""",

    45: """\
# O que fazer

Criar a release do projeto e publicar um post no LinkedIn demonstrando
o framework de avaliação de prompts.

## Tarefas

- [ ] Criar Release no GitHub com changelog
- [ ] Escrever post no LinkedIn:
  1. O problema: prompts quebram silenciosamente
  2. O que construí: playground + versionamento + evals + regressão
  3. Stack: Python, LLM SDK, pytest
  4. Métricas: taxa de aceitação, latência
  5. Link do GitHub
  6. Próximo passo
- [ ] Atualizar `PROJECTS_TRACKING.md`

# (DoF)

- Release publicada no GitHub
- Post publicado no LinkedIn
- `PROJECTS_TRACKING.md` atualizado
""",

    # -------------------------------------------------------------------------
    # P05 — RAG Knowledge Base (com citações)
    # -------------------------------------------------------------------------

    46: """\
# O que fazer

Definir quais fontes de documentos serão indexadas e especificar o
formato de dados para cada uma.

## Tarefas

- [ ] Escolher as fontes de documentos:
  - PDFs (relatórios, manuais, contratos)
  - Markdown (documentação, wikis)
  - (Opcional) Notion, Google Drive, Confluence
- [ ] Documentar para cada fonte:
  - Como os arquivos serão obtidos/baixados
  - Estrutura esperada dos documentos
  - Metadados disponíveis (título, autor, data, seção)
- [ ] Coletar exemplos de documentos para testes (5–10 arquivos)
- [ ] Criar repositório com estrutura: `src/`, `data/`, `docs/`

# (DoF)

- Fontes documentadas em `docs/sources.md`
- ≥ 5 documentos de exemplo disponíveis para teste
- Repositório criado no GitHub
""",

    47: """\
# O que fazer

Construir o pipeline de ingestão de documentos com chunking e extração
de metadados por chunk.

## Tarefas

- [ ] Criar leitores para cada fonte:
  - PDF: `PyPDF2` ou `pdfplumber`
  - Markdown: parser simples
- [ ] Implementar estratégia de chunking:
  - Tamanho de chunk (ex.: 500 tokens)
  - Overlap entre chunks (ex.: 50 tokens)
  - Preservar estrutura semântica (parágrafos, seções)
- [ ] Extrair e armazenar metadados por chunk:
  `source`, `page`, `chunk_index`, `doc_id`, `created_at`
- [ ] Criar script de ingestão `src/ingest.py`
- [ ] Testar com documentos de exemplo

# (DoF)

- `python src/ingest.py <caminho>` processa documentos e gera chunks com metadados
- Chunks de tamanho correto com overlap adequado
- Metadados presentes em cada chunk
""",

    48: """\
# O que fazer

Configurar o modelo de embeddings, o banco vetorial com pgvector e
implementar a indexação dos documentos.

## Tarefas

- [ ] Escolher modelo de embeddings:
  - OpenAI `text-embedding-3-small` (cloud)
  - `sentence-transformers` (local, ex.: `all-MiniLM-L6-v2`)
- [ ] Configurar Postgres com extensão pgvector:
  - `CREATE EXTENSION vector`
  - Tabela `document_chunks` com coluna `embedding vector(N)`
- [ ] Implementar `src/indexer.py`:
  - Calcular embeddings para cada chunk
  - Salvar chunk + embedding no banco
  - Criar índice HNSW ou IVFFlat no pgvector
- [ ] Rodar indexação completa nos documentos de exemplo

# (DoF)

- Postgres rodando com extensão pgvector
- Embeddings calculados e salvos para todos os chunks
- Índice vetorial criado (busca retorna resultados em < 100ms)
""",

    50: """\
# O que fazer

Implementar o endpoint de recuperação de documentos com busca vetorial
e, opcionalmente, busca híbrida (vetorial + keyword).

## Tarefas

- [ ] Implementar busca vetorial:
  - Calcular embedding da query
  - Buscar top-K chunks mais similares no pgvector
  - Retornar chunks com score de similaridade e metadados
- [ ] Criar endpoint FastAPI `POST /search`:
  - Input: `{"query": "...", "top_k": 5}`
  - Output: lista de chunks com `content`, `source`, `page`, `score`
- [ ] (Opcional) Implementar busca por keyword (full-text search do Postgres)
- [ ] (Opcional) Busca híbrida com re-ranking simples por score combinado

# (DoF)

- `POST /search` retornando top-K chunks relevantes em < 500ms
- Resultado incluindo conteúdo, fonte e score de similaridade
- Testes com queries de exemplo mostrando resultados relevantes
""",

    51: """\
# O que fazer

Implementar query rewriting e/ou reranking para melhorar a qualidade
dos documentos recuperados.

## Tarefas

- [ ] Implementar **query rewriting**:
  - Usar o LLM para reformular/expandir a query antes de buscar
  - Exemplo: "preço" → "preço, valor, custo, tarifa"
- [ ] Implementar **reranking** dos resultados:
  - Usar cross-encoder (ex.: `cross-encoder/ms-marco-MiniLM-L-6-v2`)
  - Ou usar o LLM para avaliar relevância dos top-K chunks
- [ ] Comparar resultados com e sem reranking em queries de exemplo
- [ ] Documentar: quando vale a pena usar reranking (custo vs qualidade)

# (DoF)

- Query rewriting implementado e testável via flag de configuração
- Reranking funcional com documentação da comparação
- Exemplo de melhoria de resultado com reranking documentado
""",

    52: """\
# O que fazer

Implementar a geração de resposta com citações, garantindo que cada
afirmação está ancorada nos documentos recuperados.

## Tarefas

- [ ] Criar endpoint `POST /ask`:
  - Input: `{"question": "..."}`
  - Output: `{"answer": "...", "citations": [{"text": "...", "source": "...", "page": N}]}`
- [ ] Construir prompt que instrui o LLM a:
  - Usar apenas os documentos fornecidos
  - Citar a fonte de cada afirmação
  - Retornar "não encontrei informação suficiente" quando não há dados
- [ ] Validar que a resposta está "fundamentada" nos documentos (groundedness)
- [ ] Implementar fallback para quando não há documentos relevantes

# (DoF)

- `POST /ask` retorna resposta + lista de citações com fonte e trecho
- LLM não "alucina" quando documentos não têm a resposta
- Fallback implementado para queries sem resposta nos documentos
""",

    53: """\
# O que fazer

Criar um conjunto de avaliação offline e calcular métricas de qualidade
do RAG (recall e groundedness).

## Tarefas

- [ ] Criar `evals/rag_eval_set.json` com:
  - `question` — pergunta de avaliação
  - `expected_answer` — resposta esperada
  - `relevant_doc_ids` — IDs dos documentos que contêm a resposta
- [ ] Calcular **recall de recuperação**:
  - Para cada pergunta, verificar se os documentos relevantes estão no top-K
- [ ] Calcular **groundedness**:
  - A resposta usa informações dos documentos recuperados?
  - Usar LLM como juiz ou verificação manual
- [ ] Gerar relatório de avaliação em `reports/rag_eval.md`

# (DoF)

- Conjunto de avaliação com ≥ 10 perguntas
- Recall@K calculado (K=3 e K=5)
- Relatório de avaliação gerado com métricas
""",

    54: """\
# O que fazer

Configurar logging estruturado de produção para registrar queries,
documentos recuperados e respostas geradas.

## Tarefas

- [ ] Criar tabela `query_logs` no banco com campos:
  `id`, `query`, `retrieved_chunks` (JSON), `answer`, `latency_ms`, `created_at`
- [ ] Logar cada chamada ao endpoint `/ask` na tabela
- [ ] Criar endpoint `GET /logs` para listar queries recentes (admin)
- [ ] Adicionar script de análise: queries mais frequentes, latência média, falhas
- [ ] Documentar o esquema de logs e como analisá-los

# (DoF)

- Cada query logada no banco com todos os campos
- Endpoint de admin `GET /logs` funcionando
- Script de análise produzindo estatísticas básicas
""",

    55: """\
# O que fazer

Criar README multilíngue documentando a arquitetura do RAG e incluindo
exemplos de query e resposta com citações.

## Tarefas

- [ ] Criar `README.md` (Inglês) com:
  - Arquitetura do RAG (diagrama simples)
  - How to run (local com Docker)
  - Exemplos de query e resposta com citações
  - Métricas de avaliação alcançadas
  - Variáveis de ambiente
- [ ] Criar `README.pt-BR.md` (Português)
- [ ] Adicionar language switch no topo
- [ ] Incluir GIF ou screenshot mostrando uma query e a resposta com citações

# (DoF)

- `README.md` (EN) e `README.pt-BR.md` criados com language switch
- Exemplo de query → resposta com citações documentado
- Demo visual incluída
""",

    56: """\
# O que fazer

Criar a release do projeto e publicar um post no LinkedIn demonstrando
o RAG com citações.

## Tarefas

- [ ] Criar Release no GitHub com changelog
- [ ] Escrever post no LinkedIn:
  1. O problema: base de conhecimento inacessível
  2. O que construí: RAG com ingestão, busca vetorial e citações
  3. Stack: FastAPI, pgvector, embeddings
  4. Resultados de avaliação (recall, groundedness)
  5. Link do GitHub
  6. Próximo passo
- [ ] Atualizar `PROJECTS_TRACKING.md`

# (DoF)

- Release publicada no GitHub
- Post publicado no LinkedIn
- `PROJECTS_TRACKING.md` atualizado
""",

    # -------------------------------------------------------------------------
    # P06 — Agent Operator (Tickets/Email)
    # -------------------------------------------------------------------------

    57: """\
# O que fazer

Definir o conjunto de ferramentas que o agente terá acesso e criar as
implementações mock para as APIs externas.

## Tarefas

- [ ] Listar todas as ferramentas necessárias:
  - Leitura de tickets/emails (mock)
  - Classificação por categoria
  - Consulta à base de conhecimento (RAG)
  - Criação/atualização de ticket via API (mock)
  - Envio de resposta (mock)
- [ ] Definir o schema de cada tool:
  - Nome, descrição (para o LLM entender)
  - Parâmetros de entrada (tipos e descrições)
  - Formato de retorno
- [ ] Implementar as funções mock em `src/tools/`
- [ ] Documentar as ferramentas em `docs/tools.md`

# (DoF)

- Lista de ferramentas definida com schemas completos
- Implementações mock funcionando e testáveis
- `docs/tools.md` com descrição de cada tool
""",

    58: """\
# O que fazer

Implementar o padrão de orquestração do agente (ReAct ou planner-executor)
com roteamento por intenção.

## Tarefas

- [ ] Escolher o padrão de orquestração:
  - **ReAct**: Thought → Action → Observation → Thought...
  - **Planner-Executor**: LLM gera plano → executor roda os steps
- [ ] Implementar o loop de orquestração em `src/agent/orchestrator.py`
- [ ] Implementar roteamento por intenção (classificar o tipo de tarefa antes de agir)
- [ ] Adicionar limite de iterações para evitar loops infinitos
- [ ] Testar com um caso de uso simples end-to-end

# (DoF)

- Agente executando um caso de uso simples (classificar + consultar RAG + sugerir resposta)
- Loop com limite de iterações implementado
- Roteamento por intenção funcionando
""",

    59: """\
# O que fazer

Implementar a máquina de estados do workflow com persistência, retries
automáticos e garantia de idempotência.

## Tarefas

- [ ] Definir os estados do workflow:
  `RECEIVED → PROCESSING → AWAITING_APPROVAL → COMPLETED | FAILED`
- [ ] Criar tabela `tasks` no banco com: `id`, `status`, `payload`, `result`,
  `created_at`, `updated_at`, `retry_count`
- [ ] Implementar transições de estado com persistência
- [ ] Adicionar retries automáticos (máx. 3 tentativas com backoff exponencial)
- [ ] Garantir idempotência: reprocessar o mesmo ticket não cria duplicatas
- [ ] Escrever testes para cada transição de estado

# (DoF)

- Tabela `tasks` criada e gerenciando estados
- Retries com backoff funcionando
- Idempotência garantida (mesmo payload processado duas vezes = 1 resultado)
""",

    60: """\
# O que fazer

Configurar a fila assíncrona com Redis e Celery para processar tarefas
do agente em background.

## Tarefas

- [ ] Instalar e configurar Redis e Celery (ou RQ/Dramatiq)
- [ ] Adicionar Redis ao `docker-compose.yml`
- [ ] Criar task Celery `tasks/agent_task.py` que executa o agente
- [ ] Modificar endpoint `POST /tickets` para:
  - Salvar o ticket no banco com status `RECEIVED`
  - Disparar a task Celery
  - Retornar `202 Accepted` com `task_id`
- [ ] Criar endpoint `GET /tickets/{task_id}` para consultar status
- [ ] Testar o fluxo end-to-end assíncrono

# (DoF)

- `POST /tickets` retorna 202 com `task_id` imediatamente
- Task processada em background pelo Celery worker
- `GET /tickets/{task_id}` retorna o status e resultado quando concluído
""",

    61: """\
# O que fazer

Implementar o mecanismo de human-in-the-loop para ações críticas que
requerem aprovação antes de serem executadas.

## Tarefas

- [ ] Definir quais ações são "críticas" (ex.: fechar ticket, enviar resposta ao cliente, reembolsar)
- [ ] Implementar lógica de pausa do workflow quando uma ação crítica é identificada:
  - Mudar status para `AWAITING_APPROVAL`
  - Notificar (log ou webhook mock)
- [ ] Criar endpoint `PUT /tickets/{id}/approve` — retoma o workflow
- [ ] Criar endpoint `PUT /tickets/{id}/reject` — cancela a ação e registra motivo
- [ ] Implementar timeout de aprovação (ex.: 24h → cancela automaticamente)

# (DoF)

- Ação crítica pausa o workflow e muda status para `AWAITING_APPROVAL`
- `PUT /tickets/{id}/approve` retoma o workflow e executa a ação
- `PUT /tickets/{id}/reject` cancela com registro do motivo
- Timeout de aprovação funcionando
""",

    62: """\
# O que fazer

Implementar controle de acesso baseado em papéis (RBAC) para limitar
quais ferramentas cada usuário/papel pode utilizar.

## Tarefas

- [ ] Definir papéis: `admin`, `operator`, `viewer`
- [ ] Criar matriz de permissões: qual papel pode usar qual ferramenta
- [ ] Implementar verificação de permissão antes de cada tool call:
  - `check_permission(user_role, tool_name)` → True/False
- [ ] Retornar erro claro (`403 Forbidden`) quando permissão negada
- [ ] Logar tentativas de acesso negado
- [ ] Testar com diferentes papéis

# (DoF)

- Matriz de permissões documentada e implementada
- Tool calls bloqueadas para papéis sem permissão
- Erro `403` com mensagem clara retornado
- Tentativas negadas logadas
""",

    63: """\
# O que fazer

Criar um sistema de auditoria que registra todas as ações do agente
para rastreabilidade e conformidade.

## Tarefas

- [ ] Criar tabela `audit_logs` com:
  `id`, `task_id`, `user_id`, `action`, `tool_name`, `params` (JSON),
  `result` (JSON), `timestamp`, `success`
- [ ] Logar automaticamente cada tool call do agente na tabela
- [ ] Criar endpoint `GET /audit` com filtros por `task_id`, `user_id`, `date_range`
- [ ] Garantir que logs de auditoria são imutáveis (sem DELETE/UPDATE)
- [ ] Documentar o esquema e como consultar os logs

# (DoF)

- Cada tool call registrada na tabela de auditoria
- Endpoint `GET /audit` funcionando com filtros
- Logs imutáveis (nenhum endpoint de deleção exposto)
""",

    64: """\
# O que fazer

Implementar proteções contra prompt injection nas entradas do usuário e
no conteúdo recuperado pelo RAG.

## Tarefas

- [ ] Implementar sanitização de input do usuário:
  - Remover/escapar sequências suspeitas (ex.: "Ignore all previous instructions")
  - Limitar tamanho do input
- [ ] Validar conteúdo do RAG antes de injetar no prompt:
  - Não permitir que documentos contenham instruções de sistema
  - Usar separadores claros entre contexto e instrução
- [ ] Adicionar filtro de detecção de injection (heurística simples ou LLM-as-judge)
- [ ] Criar testes com payloads de injection conhecidos
- [ ] Documentar as proteções implementadas

# (DoF)

- Input sanitizado antes de ir ao LLM
- Conteúdo RAG isolado do sistema prompt
- Testes com payloads de injection passando (injection bloqueada)
- Proteções documentadas em `docs/security.md`
""",

    65: """\
# O que fazer

Escrever testes cobrindo cenários de falha e garantir que fallbacks
funcionam corretamente quando partes do sistema falham.

## Tarefas

- [ ] Escrever testes para cenários de falha:
  - LLM retorna resposta inválida → retry e fallback
  - Tool falha (API mock retorna erro) → estado de erro, retry
  - Timeout da task → cancelamento gracioso
  - Permissão negada → erro claro
  - Prompt injection detectada → rejeição do input
- [ ] Implementar mensagens de fallback "humanas" para o usuário final
- [ ] Usar mocks para simular falhas em dependências externas
- [ ] Garantir que o sistema não fica em estado inconsistente após falha

# (DoF)

- Testes cobrindo todos os cenários de falha listados
- Fallbacks funcionando e retornando mensagens amigáveis
- Sistema volta a estado consistente após falhas
""",

    66: """\
# O que fazer

Criar README multilíngue documentando a arquitetura do agente e incluindo
uma demonstração do fluxo end-to-end.

## Tarefas

- [ ] Criar `README.md` (Inglês) com:
  - Arquitetura do agente (diagrama de fluxo)
  - How to run (Docker + Celery + Redis)
  - Descrição das ferramentas
  - Exemplo de fluxo end-to-end (ticket → classificação → RAG → resposta → aprovação)
  - Variáveis de ambiente
- [ ] Criar `README.pt-BR.md` (Português)
- [ ] Adicionar language switch no topo
- [ ] Incluir GIF ou vídeo demonstrando o fluxo completo

# (DoF)

- `README.md` (EN) e `README.pt-BR.md` criados com language switch
- Diagrama de fluxo incluído
- Demo visual mostrando o fluxo end-to-end
""",

    67: """\
# O que fazer

Criar a release do projeto e publicar um post no LinkedIn demonstrando
o agente operador com segurança e aprovação humana.

## Tarefas

- [ ] Criar Release no GitHub com changelog
- [ ] Escrever post no LinkedIn:
  1. O problema: processar tickets manualmente é lento e caro
  2. O que construí: agente com ferramentas, workflow, RBAC e human-in-the-loop
  3. Stack: Python, FastAPI, Celery, Redis, pgvector
  4. Aprendizados sobre segurança em agentes
  5. Link do GitHub + demo
  6. Próximo passo
- [ ] Atualizar `PROJECTS_TRACKING.md`

# (DoF)

- Release publicada no GitHub
- Post publicado no LinkedIn
- `PROJECTS_TRACKING.md` atualizado
""",

    # -------------------------------------------------------------------------
    # P07 — Multi-tenant AI SaaS Starter
    # -------------------------------------------------------------------------

    68: """\
# O que fazer

Implementar autenticação de usuários e o conceito de organizações/tenants
com isolamento total de dados entre elas.

## Tarefas

- [ ] Criar modelos: `User`, `Organization`, `OrganizationMember`
- [ ] Implementar autenticação JWT (login/registro)
- [ ] Criar fluxo de criação de organização e convite de membros
- [ ] Implementar isolamento de dados:
  - Todas as queries filtradas por `organization_id`
  - Garantir que um usuário de uma org não vê dados de outra
- [ ] (Opcional) Row-Level Security no Postgres
- [ ] Escrever testes de isolamento

# (DoF)

- Login e registro funcionando
- Usuário associado a uma organização
- Dados de org A não acessíveis para usuários de org B (testado)
""",

    69: """\
# O que fazer

Configurar PostgreSQL com schema multi-tenant e Redis para cache e
filas, com docker-compose completo.

## Tarefas

- [ ] Configurar Postgres com estratégia de isolamento por tenant:
  - Schema por tenant (`org_<id>.table`) **ou** coluna `tenant_id` em todas as tabelas
  - Migrations com Alembic cobrindo a estratégia escolhida
- [ ] Configurar Redis:
  - Cache de respostas LLM (TTL configurável)
  - Backend de filas para Celery
- [ ] Criar `docker-compose.yml` com: API, Postgres, Redis, Celery worker
- [ ] Documentar a estratégia de isolamento e seus trade-offs

# (DoF)

- `docker-compose up` sobe todos os serviços sem erros
- Estratégia de isolamento de dados implementada e documentada
- Redis funcionando para cache e filas
""",

    70: """\
# O que fazer

Implementar rate limiting por tenant e limites de uso configuráveis por
plano de assinatura.

## Tarefas

- [ ] Implementar rate limiting por tenant com Redis:
  - Ex.: 100 requests/minuto por tenant
  - Retornar `429 Too Many Requests` com header `Retry-After`
- [ ] Implementar limites de uso mensais por plano:
  - Free: 1.000 tokens/mês
  - Pro: 100.000 tokens/mês
  - Enterprise: ilimitado
- [ ] Bloquear requests quando limite atingido (com mensagem clara)
- [ ] Criar endpoint `GET /usage/current` para o tenant ver seu consumo atual

# (DoF)

- `429` retornado com `Retry-After` quando rate limit atingido
- Limite mensal bloqueando requests ao ser atingido
- `GET /usage/current` mostrando consumo e limite
""",

    71: """\
# O que fazer

Criar o sistema de metering para registrar e calcular o custo de uso
por tenant (tokens, ações, custo estimado).

## Tarefas

- [ ] Criar tabela `usage_events` com:
  `id`, `tenant_id`, `event_type` (tokens/action), `quantity`, `cost_usd`, `created_at`
- [ ] Registrar automaticamente cada uso:
  - Tokens consumidos por chamada ao LLM
  - Ações executadas pelo agente
  - Documentos recuperados (RAG)
- [ ] Criar função que calcula uso/custo acumulado por tenant por período
- [ ] Expor via endpoint `GET /billing/usage`

# (DoF)

- Cada uso registrado na tabela `usage_events`
- Custo estimado calculado (com taxa de custo configurável por tipo)
- `GET /billing/usage` retornando uso e custo por período
""",

    72: """\
# O que fazer

Integrar o Stripe para cobrança de assinaturas com planos e webhooks
para sincronização de status de pagamento.

## Tarefas

- [ ] Configurar Stripe em modo test
- [ ] Criar produtos/preços no Stripe (Free, Pro, Enterprise)
- [ ] Implementar checkout:
  - `POST /billing/checkout` → cria Stripe Checkout Session
  - Redirect para página de sucesso
- [ ] Criar tabela `subscriptions` para armazenar status local
- [ ] Implementar webhook `POST /billing/webhook` para eventos:
  - `checkout.session.completed`
  - `customer.subscription.updated`
  - `customer.subscription.deleted`
  - `invoice.payment_failed`
- [ ] Verificar assinatura ativa nas rotas protegidas

# (DoF)

- Checkout funcionando em modo test (Stripe test cards)
- Webhooks processando eventos e atualizando status no banco
- Rotas bloqueadas para tenants sem assinatura ativa
""",

    73: """\
# O que fazer

Criar um painel administrativo que mostra uso, custo e auditoria
por tenant.

## Tarefas

- [ ] Criar painel admin (FastAPI + HTML simples, ou Streamlit):
  - Lista de tenants com status de assinatura
  - Uso atual: tokens, ações, documentos (por tenant e total)
  - Custo estimado por tenant no período
  - Log de auditoria de ações do agente (filtrado por tenant)
- [ ] Adicionar filtros: por tenant, por período (semana, mês)
- [ ] Proteger o painel com autenticação de admin
- [ ] Documentar como acessar o painel

# (DoF)

- Painel acessível com login de admin
- Dados de uso e custo corretos por tenant
- Log de auditoria consultável no painel
""",

    74: """\
# O que fazer

Configurar logs estruturados com correlação por tenant e request, e
opcionalmente adicionar tracing básico com OpenTelemetry.

## Tarefas

- [ ] Configurar logs estruturados (JSON) com campos obrigatórios:
  `request_id`, `tenant_id`, `user_id`, `method`, `path`, `status`, `duration_ms`
- [ ] Garantir que `tenant_id` aparece em todos os logs relevantes
- [ ] Logar eventos de negócio importantes:
  - Login, limite atingido, ação do agente, erro de billing
- [ ] (Opcional) Adicionar tracing com OpenTelemetry:
  - Span por request e por tool call do agente
- [ ] Documentar o formato de log e como filtrar por tenant

# (DoF)

- Todos os logs incluem `tenant_id` e `request_id`
- Eventos de negócio logados
- Documentação do formato de log no README
""",

    75: """\
# O que fazer

Criar o Dockerfile de produção e o pipeline de CI/CD no GitHub Actions
para testes e build automáticos.

## Tarefas

- [ ] Criar `Dockerfile` otimizado para produção (multi-stage build)
- [ ] Criar `docker-compose.prod.yml` para ambiente de produção
- [ ] Criar workflow GitHub Actions `.github/workflows/ci.yml`:
  - Lint e formatação
  - Testes com banco de dados de teste
  - Build da imagem Docker
  - (Opcional) Push para registry (Docker Hub, GHCR)
- [ ] Documentar o processo de deploy no README
- [ ] Adicionar badges de CI no README

# (DoF)

- CI passando em todos os pushes (lint + testes + build)
- `docker-compose.prod.yml` funcional
- Documentação de deploy no README
""",

    76: """\
# O que fazer

Criar README multilíngue com screenshot do painel e documentação
completa de como rodar o SaaS.

## Tarefas

- [ ] Criar `README.md` (Inglês) com:
  - Visão geral e proposta de valor
  - Arquitetura (diagrama: API, Postgres, Redis, Stripe, Celery)
  - How to run (local e produção)
  - Variáveis de ambiente documentadas
  - Screenshot do painel admin
- [ ] Criar `README.pt-BR.md` (Português)
- [ ] Adicionar language switch no topo

# (DoF)

- `README.md` (EN) e `README.pt-BR.md` criados com language switch
- Screenshot do painel admin incluído
- Instruções de how to run completas e testadas
""",

    77: """\
# O que fazer

Criar a release do projeto e publicar um post no LinkedIn demonstrando
o SaaS multi-tenant com billing e painel.

## Tarefas

- [ ] Criar Release no GitHub com changelog
- [ ] Escrever post no LinkedIn:
  1. O desafio: criar um SaaS com múltiplos clientes e cobrança
  2. O que construí: auth + tenants + rate limiting + metering + Stripe + painel
  3. Stack: FastAPI, Postgres, Redis, Stripe, Celery
  4. Aprendizados sobre isolamento de dados e billing
  5. Link do GitHub + screenshot
  6. Próximo passo
- [ ] Atualizar `PROJECTS_TRACKING.md`

# (DoF)

- Release publicada no GitHub
- Post publicado no LinkedIn
- `PROJECTS_TRACKING.md` atualizado
""",

    # -------------------------------------------------------------------------
    # P08 — Mini Produto "de nicho" (projeto final)
    # -------------------------------------------------------------------------

    78: """\
# O que fazer

Definir o nicho de mercado e formular a hipótese de dor que o produto
de IA vai resolver.

## Tarefas

- [ ] Pesquisar nichos promissores usando os critérios do roadmap:
  - Alto custo operacional com tarefas repetitivas
  - Backlog grande (tickets, análise, documentação, propostas)
  - Dados/documentos disponíveis (para RAG)
  - Dor "urgente" e mensurável (tempo, dinheiro, risco)
- [ ] Escolher 1 nicho e formular a hipótese:
  - "Profissionais de [nicho] gastam [X horas/semana] com [tarefa específica]"
  - "Isso custa aproximadamente [R$ Y/mês] em tempo de trabalho"
- [ ] Documentar em `docs/hipotese.md`:
  - Nicho, segmento alvo, hipótese de dor, hipótese de valor

# (DoF)

- Nicho escolhido com justificativa
- Hipótese de dor clara e quantificada documentada
- `docs/hipotese.md` commitado no repositório
""",

    79: """\
# O que fazer

Criar um roteiro de entrevistas e conduzir 5–15 entrevistas com
potenciais clientes para validar a hipótese.

## Tarefas

- [ ] Criar roteiro de entrevista `docs/roteiro_entrevista.md` com 8–10 perguntas:
  - Descreva seu processo atual para [tarefa]
  - Quanto tempo você gasta por semana com isso?
  - Qual é o maior problema no processo atual?
  - Você já tentou alguma solução? Por que não funcionou?
  - Quanto pagaria por uma solução que resolvesse isso?
- [ ] Identificar e contatar potenciais entrevistados (LinkedIn, comunidades, rede)
- [ ] Conduzir ≥ 5 entrevistas (ideal: 15)
- [ ] Registrar respostas em `docs/entrevistas/`
- [ ] Sintetizar insights e validar/invalidar/pivotar a hipótese

# (DoF)

- Roteiro criado e documentado
- ≥ 5 entrevistas realizadas e registradas
- Síntese de insights e decisão de continuar/pivotar documentada
""",

    80: """\
# O que fazer

Definir o escopo mínimo do MVP (1 fluxo principal) e o modelo de
pricing inicial para começar a cobrar.

## Tarefas

- [ ] Definir o único fluxo que o MVP vai resolver (baseado nos insights das entrevistas)
- [ ] Documentar o escopo do MVP em `docs/mvp_spec.md`:
  - O que está **dentro** do escopo
  - O que está **fora** do escopo (para não escalar prematuramente)
  - Entradas e saídas do fluxo principal
- [ ] Definir o pricing inicial (1 modelo apenas):
  - Por assento/mês, por uso (ações/tokens), ou pacote fixo
  - Justificar com base nas entrevistas (WTP — willingness to pay)
- [ ] Validar o escopo e pricing com 1–2 potenciais clientes antes de construir

# (DoF)

- `docs/mvp_spec.md` com escopo claro (dentro/fora)
- Pricing inicial definido e justificado
- Validação prévia com ao menos 1 potencial cliente documentada
""",

    81: """\
# O que fazer

Implementar o MVP em 1–2 semanas, focando no fluxo principal com
qualidade suficiente para validar valor com um cliente real.

## Tarefas

- [ ] Usar a stack já dominada nos projetos anteriores
- [ ] Implementar apenas o fluxo principal definido no `mvp_spec.md`
- [ ] Foco: **funcional**, não perfeito
  - Sem over-engineering
  - Interface mínima (CLI, form simples ou API)
- [ ] Fazer um deploy mínimo (Render, Railway, VPS, ou link compartilhado)
- [ ] Preparar para coletar feedback do primeiro uso

# (DoF)

- MVP funcionando e acessível (link ou instalável)
- Fluxo principal completo e demonstrável
- Deploy disponível para o cliente piloto acessar
""",

    82: """\
# O que fazer

Adicionar instrumentação básica de analytics para medir o uso do produto
e identificar pontos de abandono no funil.

## Tarefas

- [ ] Escolher ferramenta de analytics:
  - Self-hosted: PostHog (open-source) — recomendado
  - SaaS: Mixpanel, Amplitude (plano free)
  - Simples: logs estruturados + query no banco
- [ ] Definir e implementar eventos principais:
  - Usuário acessou o produto
  - Iniciou o fluxo principal
  - Completou o fluxo principal
  - Encontrou erro
- [ ] Criar funil simples: Entrada → Ação Principal → Conclusão
- [ ] Documentar como acessar os dados de analytics

# (DoF)

- Eventos sendo registrados a cada uso
- Funil configurado e acessível
- Dados de analytics disponíveis para análise
""",

    83: """\
# O que fazer

Realizar o onboarding com 1 cliente piloto e medir o impacto do produto
comparando o estado antes e depois.

## Tarefas

- [ ] Selecionar o cliente piloto (preferencialmente alguém das entrevistas)
- [ ] Medir o estado **antes** com métricas quantificáveis:
  - Tempo gasto na tarefa por semana
  - Número de erros/retrabalhos
  - Custo estimado em horas
- [ ] Fazer onboarding: apresentar o produto, tirar dúvidas, deixar usando
- [ ] Acompanhar por 1–2 semanas com check-ins regulares
- [ ] Medir o estado **depois** com as mesmas métricas
- [ ] Documentar o case: problema → solução → resultado (com números)

# (DoF)

- Cliente piloto usando o produto por ≥ 1 semana
- Métricas antes/depois coletadas e documentadas
- Case study com números reais escrito em `docs/case_study.md`
""",

    84: """\
# O que fazer

Criar os materiais de vendas: case study, landing page e demo gravada
para atrair novos clientes.

## Tarefas

- [ ] Escrever o case study completo com:
  - Perfil do cliente (anonimizado se necessário)
  - Problema original (com números)
  - Solução implementada
  - Resultado obtido (tempo economizado, erros reduzidos, etc.)
- [ ] Criar landing page simples com:
  - Proposta de valor em 1 frase
  - 3 benefícios principais
  - Case study resumido
  - CTA (call-to-action): "Quero testar" / "Agendar demo"
  - Link para a demo
- [ ] Gravar demo de 2–5 minutos mostrando o fluxo principal
- [ ] Hospedar landing page (Vercel, Netlify, GitHub Pages)

# (DoF)

- Landing page publicada e acessível
- Demo gravada e disponível (YouTube, Loom, ou link direto)
- Case study escrito e publicado na landing ou no README
""",

    85: """\
# O que fazer

Criar o README em inglês e português combinando marketing (proposta de
valor, case) com documentação técnica (how to run).

## Tarefas

- [ ] Criar `README.md` (Inglês) com duas seções:
  - **Marketing**: proposta de valor em 1 frase, 3 benefícios, case study resumido,
    link da demo e landing page, CTA
  - **Técnico**: how to run, variáveis de ambiente, arquitetura resumida
- [ ] Criar `README.pt-BR.md` (Português) com o mesmo conteúdo
- [ ] Adicionar language switch no topo de cada arquivo
- [ ] Incluir screenshot da landing page e do produto em funcionamento

# (DoF)

- `README.md` (EN) e `README.pt-BR.md` criados com language switch
- Seções de marketing e técnica presentes e bem estruturadas
- Screenshots incluídos
""",

    86: """\
# O que fazer

Criar o README em espanhol para completar a documentação multilíngue
do produto (EN + PT-BR + ES).

## Tarefas

- [ ] Criar `README.es.md` (Espanhol) traduzindo o conteúdo do `README.md` (EN):
  - Seção de marketing: proposta de valor, benefícios, case resumido, CTA
  - Seção técnica: how to run, variáveis de ambiente
- [ ] Atualizar o language switch nos READMEs existentes para incluir ES:
  `English | Português | Español`
- [ ] Revisar a tradução para garantir naturalidade (não só tradução literal)
- [ ] Atualizar links no language switch para apontar para o arquivo correto

# (DoF)

- `README.es.md` criado com conteúdo completo
- Language switch em todos os 3 READMEs aponta para os arquivos corretos
- Tradução revisada
""",

    87: """\
# O que fazer

Executar a estratégia de go-to-market (outreach) para atrair os primeiros
clientes e publicar um post no LinkedIn documentando o lançamento.

## Tarefas

- [ ] Definir canais de outreach:
  - LinkedIn (DMs para ICP — Ideal Customer Profile)
  - Comunidades (Slack, Discord, WhatsApp do nicho)
  - Email frio (se tiver lista)
  - Indicações do cliente piloto
- [ ] Criar mensagem de outreach personalizada e concisa (problema → solução → CTA)
- [ ] Conduzir outreach para ≥ 10 potenciais clientes
- [ ] Registrar respostas e leads gerados em planilha ou CRM simples
- [ ] Escrever post no LinkedIn:
  1. Problema do nicho (empatia)
  2. O que construí e os resultados do piloto
  3. Convite para testar
  4. Link da landing page / demo
- [ ] Atualizar `PROJECTS_TRACKING.md` com links de tudo

# (DoF)

- Outreach realizado para ≥ 10 potenciais clientes
- Leads e respostas registrados
- Post publicado no LinkedIn
- `PROJECTS_TRACKING.md` atualizado com todos os links (landing, demo, post, repo)
""",
}


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def github_request(method: str, path: str, data: dict | None = None) -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        print("Error: GITHUB_TOKEN and GITHUB_REPOSITORY must be set.")
        sys.exit(1)

    url = f"https://api.github.com/repos/{repo}{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode(errors="replace")
        print(f"GitHub API error {exc.code} on {method} {url}: {error_body}")
        raise


def get_issue(number: int) -> dict:
    return github_request("GET", f"/issues/{number}")


def update_issue_body(number: int, body: str) -> None:
    github_request("PATCH", f"/issues/{number}", {"body": body})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    dry_run = "--dry-run" in sys.argv
    only_issue: int | None = None
    if "--issue" in sys.argv:
        idx = sys.argv.index("--issue")
        only_issue = int(sys.argv[idx + 1])

    issues_to_update = (
        {only_issue: ISSUE_BODIES[only_issue]}
        if only_issue
        else ISSUE_BODIES
    )

    print(f"{'[DRY RUN] ' if dry_run else ''}Updating {len(issues_to_update)} issues…\n")

    for number, body in sorted(issues_to_update.items()):
        print(f"  Issue #{number}", end="")

        if not dry_run:
            try:
                current = get_issue(number)
                if current.get("body"):
                    print(" — skipped (already has body)")
                    continue
                update_issue_body(number, body)
                print(" — updated ✓")
                time.sleep(0.5)  # be nice to the API
            except urllib.error.HTTPError:
                print(" — ERROR (see above)")
        else:
            preview = body.splitlines()[0][:60]
            print(f" — [DRY RUN] would set body: {preview!r}…")

    print("\nDone.")


if __name__ == "__main__":
    main()
