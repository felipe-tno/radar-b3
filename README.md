# Radar B3 — Monitor de Força Relativa Setorial

Projeto de Engenharia de Dados para monitorar o desempenho de ativos e setores da bolsa brasileira em relação ao Ibovespa.

## Objetivo

O Radar B3 tem como objetivo construir um pipeline de dados de mercado capaz de coletar, organizar e analisar o desempenho histórico de ativos da B3, permitindo identificar setores com desempenho relativo superior ou inferior ao mercado.

O projeto será desenvolvido de forma incremental, com foco em qualidade de dados, modularização, testes automatizados e automação de pipelines.

## Arquitetura

O projeto está organizado em módulos com responsabilidades separadas:

- **Ingestion:** coleta de dados de mercado.
- **Transformations:** limpeza, padronização e preparação dos dados.
- **Analytics:** cálculo de indicadores e métricas de desempenho relativo.
- **Storage:** persistência dos dados coletados e processados.
- **Pipeline:** orquestração das etapas de processamento.

## Tecnologias

- Python
- yfinance
- pandas
- pytest
- Git e GitHub

Tecnologias adicionais poderão ser incorporadas conforme a evolução do projeto.

## Estrutura do projeto

```text
radar-b3/
├── config/             # Configurações dos ativos monitorados
├── data/
│   ├── raw/             # Dados brutos
│   └── processed/       # Dados processados
├── docs/                # Documentação e metodologia
├── src/
│   └── radar_b3/
│       ├── ingestion/   # Coleta de dados
│       ├── transformations/
│       ├── analytics/
│       ├── storage/
│       └── pipeline.py
├── tests/               # Testes automatizados
├── app.py
├── pyproject.toml
└── requirements.txt
```

## Status do desenvolvimento

**Em desenvolvimento.**

- [x] Estrutura inicial do projeto
- [x] Módulo inicial de ingestão de dados
- [x] Tratamento inicial de falhas e tentativas de reexecução
- [x] Testes automatizados do comportamento do pipeline
- [ ] Padronização e validação dos dados coletados
- [ ] Persistência dos dados brutos e processados
- [ ] Cálculo de métricas de força relativa
- [ ] Automação da execução do pipeline
- [ ] Dashboard de acompanhamento setorial

## Como executar

### 1. Pré-requisitos

- Python 3.10 ou superior
- Git

### 2. Clonar o repositório

```bash
git clone https://github.com/felipe-tno/radar-b3.git
cd radar-b3
```

### 3. Criar e ativar um ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

### 5. Executar os testes

```bash
python -m pytest -v
```

## Metodologia

Os indicadores de força relativa serão definidos a partir da comparação do desempenho dos ativos e setores monitorados com o desempenho do Ibovespa em períodos equivalentes.

Os critérios de cálculo, as premissas e as limitações metodológicas serão documentados em [`docs/methodology.md`](docs/methodology.md).

## Observações

Os dados de mercado são utilizados para fins de estudo e desenvolvimento de software. O projeto não constitui recomendação de investimento.
