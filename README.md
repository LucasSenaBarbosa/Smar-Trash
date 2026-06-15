<div align="center">

```
Smart Trash
```

**Central de Coleta Inteligente · Taboão da Serra / SP**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![CrewAI](https://img.shields.io/badge/CrewAI-0.80%2B-green?style=flat-square)
![Groq](https://img.shields.io/badge/LLM-Groq%20%2F%20LLaMA%203.3-orange?style=flat-square)
![FastAPI](https://img.shields.io/badge/API-FastAPI-teal?style=flat-square&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-gray?style=flat-square)

*Sistema multiagente de IA para gerenciamento inteligente de coleta de lixo urbano,
com dashboard em tempo real, eventos aleatórios e protocolo de segurança biológica.*

</div>

---

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Agentes de IA](#agentes-de-ia)
- [Dashboard](#dashboard)
- [Eventos Aleatórios](#eventos-aleatórios)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Rodar](#como-rodar)
- [Endpoints da API](#endpoints-da-api)
- [Tecnologias](#tecnologias)

---

## Visão Geral

O **EcoTrack** é um sistema de gerenciamento de coleta de lixo urbano baseado em **inteligência artificial multiagente**. Desenvolvido com o framework **CrewAI** e o modelo de linguagem **LLaMA 3.3 70B** via **Groq**, o sistema coordena uma frota de 3 caminhões para coletar 20 caçambas distribuídas por Taboão da Serra / SP.

O sistema opera em 4 fases sequenciais:

```
[SENSORES] → [ROTAS] → [COLETA] → [RELATÓRIO]
```

Cada fase é executada por agentes especializados que se comunicam, tomam decisões e geram relatórios. Um subsistema paralelo de **segurança biológica** monitora a presença de seres vivos nas caçambas durante toda a operação.

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                        ECOTRACK SYSTEM                          │
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────────┐ │
│  │  FRONTEND   │◄──►│   FASTAPI    │◄──►│     CREWAI         │ │
│  │  index.html │    │   api.py     │    │     AGENTS         │ │
│  │  Dashboard  │    │   + SSE      │    │                    │ │
│  └─────────────┘    └──────────────┘    └────────────────────┘ │
│                                                  │              │
│                                         ┌────────▼───────┐     │
│                                         │  GROQ API      │     │
│                                         │  LLaMA 3.3 70B │     │
│                                         └────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

A comunicação entre o backend e o frontend acontece via **Server-Sent Events (SSE)**, permitindo que os logs dos agentes sejam transmitidos ao vivo para o dashboard sem necessidade de polling.

---

## Agentes de IA

O sistema possui **10 agentes** organizados em dois subsistemas:

### 🗑️ Subsistema de Coleta

| Agente | Papel | Responsabilidade |
|--------|-------|-----------------|
| `sensor_agent` | Supervisor de Sensores | Analisa os dados das 20 caçambas e classifica por prioridade de coleta |
| `rotas_agent` | Especialista de Logística | Divide as caçambas entre os 3 caminhões e otimiza as rotas |
| `motorista_1` | Motorista Caminhão 01 | Executa a rota atribuída e reporta cada coleta |
| `motorista_2` | Motorista Caminhão 02 | Executa a rota atribuída e reporta cada coleta |
| `motorista_3` | Motorista Caminhão 03 | Executa a rota atribuída e reporta cada coleta |
| `relatorio` | Gerente Operacional | Consolida os relatórios dos 3 caminhões em relatório geral |

### 🔒 Subsistema de Segurança Biológica

| Agente | Papel | Responsabilidade |
|--------|-------|-----------------|
| `sensor_vida_agent` | Especialista em Sensores Biológicos | Analisa sinais térmicos, sonoros e de movimento |
| `visao_agent` | Especialista em Visão Computacional | Processa imagens IR e identifica silhuetas e temperatura corporal |
| `seguranca_vida_ai` | Supervisor de Segurança | Bloqueia a compactação quando detecta risco biológico |
| `relatorio_emergencia` | Analista de Incidentes | Registra e documenta cada evento de segurança |

### Fluxo de decisão

```
sensor_agent
    │
    ▼ (relatório de prioridades)
rotas_agent
    │
    ├──► motorista_1 ──► coletas + incidentes
    ├──► motorista_2 ──► coletas + incidentes
    └──► motorista_3 ──► coletas + incidentes
              │
              ▼
           relatorio (consolidação)

Em paralelo, a qualquer momento:
    sensor_vida_agent + visao_agent
              │
              ▼
    seguranca_vida_ai (bloqueia compactação)
              │
              ▼
    relatorio_emergencia (documenta o incidente)
```

---

## Dashboard

O dashboard é uma single-page application em **HTML + CSS + JavaScript puro** (zero dependências externas além do Google Fonts), servida pelo FastAPI.

### Componentes

```
┌──────────────────────────────────────────────────────────────────┐
│ HEADER: Logo · Fases · Ticker de incidentes · Relógio · Status   │
├──────────────────────────────────────────────────────────────────┤
│ KPIs: Coletas · Rotas Bloqueadas · Alertas de Vida · Eficiência  │
├──────────────────────────────────────────────────────────────────┤
│ Banner de atividade atual (coleta em andamento / incidente)       │
├─────────────────────────┬────────────────────────────────────────┤
│ Gráfico de barras       │ Mapa das 20 caçambas (grid 4×5)        │
│ (Canvas API, animado)   │ com cores por prioridade e status       │
├─────────────────────────┴────────────────────────────────────────┤
│ Cards dos 3 caminhões: progresso, coletas e lista de incidentes   │
├──────────────────────────────────────────────────────────────────┤
│ Relatório final (aparece ao término da operação)                  │
├──────────────────────────────────────────────────────────────────┤
│ SIDEBAR: Feed de logs ao vivo · Contadores de incidentes ·        │
│          Timeline de fases · Botões de controle                   │
└──────────────────────────────────────────────────────────────────┘
```

### Legenda do mapa de caçambas

| Cor | Significado |
|-----|------------|
| 🔴 Vermelho | Ocupação ≥ 90% — Alta prioridade |
| 🟠 Laranja | Ocupação 70–90% — Média prioridade |
| ⬛ Escuro | Ocupação < 70% — Sem coleta necessária |
| 🟡 Amarelo pulsando | Coletando no momento |
| 🔴 Vermelho pulsando | Alerta de vida detectado |
| 🟡 Amarelo opaco `✗` | Bloqueada — não coletada |
| 🟢 Verde `✓` | Coletada com sucesso |

---

## Eventos Aleatórios

A cada caçamba visitada, o sistema sorteia aleatoriamente um evento:

### 🚧 Bloqueio de Rua (18% de chance)

O caminhão não consegue acessar o ponto. O sistema registra o motivo, notifica a central e prossegue para a próxima parada. Motivos possíveis:

- Obra emergencial de asfalto
- Acidente de trânsito
- Árvore caída após chuva
- Manifestação popular
- Vazamento de água (SABESP)
- Veículo quebrado na via
- Feira livre não recolhida
- Buraco profundo na pista

### 🚨 Detecção de Vida (15% de chance)

Os agentes de segurança biológica entram em ação automaticamente:

1. `sensor_vida_agent` detecta temperatura IR e movimento
2. `visao_agent` analisa imagem e classifica o ser detectado
3. `seguranca_vida_ai` **bloqueia o compactador imediatamente**
4. Equipe externa é acionada e o incidente é resolvido
5. `relatorio_emergencia` documenta tudo com ID de incidente
6. Coleta é retomada após liberação do local

Seres detectáveis: cão 🐕, gato 🐈, ave 🦅, humano 👤, roedor 🐀, gambá 🦡

---

## Estrutura do Projeto

```
coleta_lixo/
│
├── 📄 main.py                   # Ponto de entrada (sem frontend)
├── 📄 api.py                    # FastAPI + SSE + serve o frontend
├── 📄 crew.py                   # Configuração da Crew (agentes + tarefas)
├── 📄 requirements.txt          # Dependências Python
├── 📄 .env.example              # Modelo de variáveis de ambiente
│
├── 📁 agents/
│   ├── __init__.py
│   ├── sensor_agent.py          # Agente de análise de sensores
│   ├── seguranca_agents.py      # Agentes do subsistema de segurança biológica
│   ├── rotas_agent.py           # Agente de logística e rotas
│   └── motoristas_agents.py     # Agentes motoristas + agente gerente
│
├── 📁 tasks/
│   ├── __init__.py
│   ├── tarefa_sensor.py         # Tarefa: análise das 20 caçambas
│   ├── tarefa_seguranca.py      # Tarefas: detecção de vida + relatório de emergência
│   ├── tarefa_rotas.py          # Tarefa: otimização e divisão de rotas
│   └── tarefas_motoristas.py    # Tarefas: execução da rota + relatório gerencial
│
└── 📁 frontend/
    └── index.html               # Dashboard completo (HTML + CSS + JS)
```

---

## Instalação

### Pré-requisitos

- Python **3.10** ou superior
- Conta gratuita no [Groq Console](https://console.groq.com) para obter a API Key

### 1. Clone ou extraia o projeto

```bash
# Se estiver usando Git
git clone https://github.com/seu-usuario/ecotrack.git
cd ecotrack

# Ou descompacte o zip e entre na pasta
cd coleta_lixo
```

### 2. Crie o ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

```bash
# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Configuração

### Variável de ambiente

Crie o arquivo `.env` na raiz do projeto:

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Edite o `.env` e adicione sua chave:

```env
GROQ_API_KEY=gsk_sua_chave_aqui
```

### Como obter a chave Groq (gratuita)

1. Acesse [console.groq.com](https://console.groq.com)
2. Crie uma conta (gratuita, sem cartão de crédito)
3. Vá em **API Keys** → **Create API Key**
4. Copie a chave e cole no `.env`

### Modelos disponíveis no Groq

O projeto usa `llama-3.3-70b-versatile` por padrão. Para trocar, edite `crew.py`:

| Modelo | Velocidade | Qualidade |
|--------|-----------|-----------|
| `llama-3.3-70b-versatile` | ⚡ Rápido | ⭐⭐⭐⭐⭐ — **recomendado** |
| `llama-3.1-8b-instant` | ⚡⚡ Muito rápido | ⭐⭐⭐ |
| `mixtral-8x7b-32768` | ⚡ Rápido | ⭐⭐⭐⭐ |

---

## Como Rodar

### Com dashboard (recomendado)

Inicia o servidor FastAPI que serve o frontend e expõe a API:

```bash
python api.py
```

Acesse no navegador: **[http://localhost:8000](http://localhost:8000)**

Clique em **▶ Iniciar Operação** para começar a simulação.

### Somente o backend (terminal)

Roda a Crew diretamente e exibe os logs no terminal:

```bash
python main.py
```

> **Modo demo:** se o backend não estiver rodando, o dashboard entra automaticamente em modo de demonstração com dados simulados e todos os eventos aleatórios funcionando normalmente.

---

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/iniciar` | Inicia a execução da Crew em background |
| `GET` | `/api/stream` | Stream SSE com logs dos agentes em tempo real |
| `GET` | `/api/status` | Retorna o status atual da operação |
| `GET` | `/` | Serve o dashboard (`frontend/index.html`) |

### Exemplo de uso da API

```bash
# Iniciar operação
curl -X POST http://localhost:8000/api/iniciar

# Verificar status
curl http://localhost:8000/api/status

# Receber logs ao vivo (SSE)
curl -N http://localhost:8000/api/stream
```

### Formato dos eventos SSE

```json
{ "type": "log",       "text": "[sensor_agent] CAC-06 → 95% — ALTA prioridade" }
{ "type": "status",    "text": "iniciando" }
{ "type": "resultado", "text": "Relatório final consolidado..." }
{ "type": "status",    "text": "concluido" }
{ "type": "erro",      "text": "Mensagem de erro" }
{ "type": "fim" }
```

---

## Tecnologias

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| [CrewAI](https://crewai.com) | ≥ 0.80 | Orquestração dos agentes de IA |
| [Groq](https://groq.com) | ≥ 0.11 | Provider de LLM (LLaMA 3.3 70B) |
| [FastAPI](https://fastapi.tiangolo.com) | ≥ 0.111 | API REST + Server-Sent Events |
| [Uvicorn](https://www.uvicorn.org) | ≥ 0.29 | Servidor ASGI |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | ≥ 1.0 | Gerenciamento de variáveis de ambiente |
| HTML / CSS / JS | — | Dashboard (zero frameworks) |

---

## Licença

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

---

<div align="center">
  <sub>Desenvolvido com CrewAI · Groq · FastAPI · Taboão da Serra, SP 🇧🇷</sub>
</div>
