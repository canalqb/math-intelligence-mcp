# Math Intelligence MCP

Visao Geral

Math Intelligence MCP (Math Intelligence Multi-Container Platform) e um framework para proporcionar capacidades matematicas avancadas a agentes de IA, com foco em criptografia de curva secp256k1, calculos matematicos gerais e integracao via protocolo JSON-RPC 2.0.

Este projeto reimplementa as funcoes da biblioteca ice_secp256k1.dll em Rust puro, permitindo operacao multiplataforma (Windows/Linux/macOS) sem dependencia de binarios proprietarios.

Status Atual

- Git history: Limpa (token removido via git filter-branch)
- Deploy: Ativo no Render (Web Service)
- MCP status: Em desenvolvimento, aguardando deploy
- Coverage: Em andamento (target: 80%+)

---

TL;DR

3 bullets resumindo o projeto:

1. Framework MCP para agentes IA com 12 tools matematicas (P0-P2) via JSON-RPC 2.0
2. Rust reimplementacao da ice_secp256k1.dll - multiplataforma, MIT license, sem dependencia de binarios proprietarios
3. Deploy no Render ativo - Web Service integrado ao GitHub canalqb/math-intelligence-mcp

---

Arquitetura do Sistema

```mermaid
graph TD
    %% Client Layer
    subgraph CLIENT[CAMADA DE CLIENTE]
        A[Agentes IA]:::client
        B[Kimi, OpenCode, Hermes]:::client
    end

    %% MCP Gateway
    subgraph GATEWAY[MCP GATEWAY (TypeScript)]
        C[Tool discovery & routing]:::server
        D[JSON-RPC / Streamable HTTP]:::server
        E[Resource registration]:::server
    end

    %% Compute Worker
    subgraph WORKER[RUST COMPUTE WORKER]
        F[Native performance]:::worker
        G[Memory-optimized]:::worker
        H[Benchmarkable]:::worker
    end

    %% Math Core
    subgraph CORE[MATH CORE]
        I[Arithmetic Engine]:::core
        J[Memory Optimization Engine]:::core
        K[Formula Engine]:::core
    end

    %% Validation
    subgraph VAL[VALIDATION ENGINE]
        L[Independent check]:::val
        M[Property verification]:::val
        N[Divergence reports]:::val
    end

    %% Reasoning
    subgraph REASON[REASONING ASSISTANT]
        O[Structured output]:::reason
        P[Inconsistency anal.]:::reason
        Q[Evidence-based exp.]:::reason
    end

    %% Connections
    A -->|JSON-RPC 2.0| C
    B -->|HTTP/STDIO| C
    C -->|stdio| F
    C -->|HTTP/STDIO| F
    F -->|result + metadata| C
    C -->|formatted response| B
    L -->|property checks| F
    P -->|analysis| F
    Q -->|metadata| F
    R -->|formatted output| C
    S -->|analysis| H
    T -->|evidence| H
```

<style>
.client { color: #4A90E2; }
.server { color: #7ED321; }
.worker { color: #F8C471; }
.core { color: #8250DF; }
.val { color: #EDC9AF; }
.reason { color: #A9A9A9; }
</style>

---

Ferramentas Disponiveis (P0-P2)

Nivel P0 (Ferramentas Essenciais - 5 tools)

1. math_evaluate - Avaliar expressoes matematicas
2. math_explain - Explicar conceitos matematicos
3. math_optimize - Otimizar expressoes algebricas
4. result_verify - Verificar resultados de calculos
5. memory_profile - Perfilagem de memoria

Nivel P1 (Ferramentas Aprimoradas - 5 tools)

6. formula_engine - Motor de formulas simbolicas
7. symbolic_solver - Solucionador simbolico
8. calculus_operations - Operacoes de calculo
9. linear_algebra - Algebra linear
10. statistical_analysis - Analise estatistica

Nivel P2 (Ferramentas Opcionais - 2 tools)

11. advanced_cryptography - Criptografia avancada
12. pattern_recognition - Reconhecimento de padroes

---

Quick Start

Via Docker (Recomendado)

```bash
docker build -t math-intelligence-mcp .
docker run -p 8000:8000 math-intelligence-mcp
```

Via Python Direto

```bash
pip install -e .
python -m mimcp
```

Via TypeScript Direto

```bash
npm install
npm run build
npm run dev
```

---

## 🌐 Conexão de Agentes de IA (Produção no Render)

O servidor MCP está publicado e pronto para conexão de qualquer agente de IA (Claude, GPT-4o, Gemini, Cursor, Antigravity, Kimi, DeepSeek) através da URL pública:

> **URL de Produção:** `https://math-intelligence-mcp.onrender.com`  
> **Endpoint MCP / JSON-RPC:** `https://math-intelligence-mcp.onrender.com/mcp`  
> **Health Check:** `https://math-intelligence-mcp.onrender.com/health`  
> **Catálogo de Tools:** `https://math-intelligence-mcp.onrender.com/mcp/tools`

### 1. Configuração para Claude Desktop / Antigravity / Cursor

Para conectar seu agente de IA local ao MCP remoto na nuvem sem precisar rodar nada no seu computador, adicione ao seu arquivo de configuração MCP (`claude_desktop_config.json` ou configurações de MCP do editor):

```json
{
  "mcpServers": {
    "math-intelligence": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://math-intelligence-mcp.onrender.com/mcp"
      ]
    }
  }
}
```

### 2. Chamada Direta via Agentes Python (LangChain, CrewAI, Autônomos)

```python
import requests

MCP_URL = "https://math-intelligence-mcp.onrender.com/mcp"

def call_math_mcp(tool_name: str, arguments: dict):
    """Executa qualquer ferramenta do Math Intelligence MCP."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    response = requests.post(MCP_URL, json=payload, timeout=30)
    return response.json()

# Exemplo: avaliar expressão com alta precisão
res = call_math_mcp("math_evaluate", {"expression": "sqrt(144) + sin(pi/2) * 10"})
print(res)
```

### 3. Chamada via HTTP / JSON-RPC 2.0 (cURL)

```bash
curl -X POST https://math-intelligence-mcp.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "math_evaluate",
      "arguments": {
        "expression": "2 + 2 * 3"
      }
    }
  }'
```

Resposta:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "data": 8.0,
    "expression": "2 + 2 * 3",
    "evaluated_at": "2026-11-22T13:23:23Z"
  },
  "id": 1
}
```

---

API JSON-RPC 2.0 (Referência Local)

Endpoint

```
POST http://localhost:8000/mcp/json-rpc
```

Header

```
Content-Type: application/json
```

Requisicao

```json
{
  "jsonrpc": "2.0",
  "method": "math_evaluate",
  "params": {"expression": "2 + 2 * 3"},
  "id": 1
}
```

Resposta

```json
{
  "jsonrpc": "2.0",
  "result": {"success": true, "data": 8, "expression": "2 + 2 * 3"},
  "id": 1
}
```

Erros

```json
{
  "jsonrpc": "2.0",
  "error": {"code": -32602, "message": "Invalid parameters"},
  "id": 1
}
```

---

Estrutura do Projeto

```text
math-intelligence-mcp/
├── ICE_DLL_TECHNICAL_REPORT.md
├── MIMCP_API_SPEC.md
├── MIMCP_ARCHITECTURE.md
├── IMPLEMENTATION_BACKLOG.md
├── docker/Dockerfile
├── python/mimcp/
│   ├── __init__.py
│   ├── tools.py
│   └── examples.ipynb
├── tests/unit/
├── tests/integration/
├── docs/user-guide.md
├── docs/api-reference.md
├── .github/workflows/ci.yml
├── .gitignore
└── pyproject.toml
```

---

Seguranca

Principles Fundamentais

1. Nenhuma exposicao de chaves privadas - O nunca armazena ou transmite chaves privadas diretamente
2. Verificacao oferecida, nao forçada - Os usuarios escolhem quando verificar resultados
3. Isolamento DLL - A DLL ice_secp256k1.dll original roda apenas em Windows isolada; o Rust reimplementa em todos os lugares
4. Conformidade LGPD - Dados processados sao minimizados e temporarios

Melhores Praticas

- Use result_verify para confirmacao de resultados criticos
- Nunca compartilhe outputs brutos sem passar por math_explain primeiro
- Monitore consumo de memoria com memory_profile em calculos longos
- Valide todas as entradas com zod antes de processar
- Rotacione tokens a cada 24h para sessoes ativas

---

Licenca

MIT - Copyright (c) 2024 Math Intelligence MCP Project

---

Agradecimentos

- Projeto original inspirado em ice_secp256k1.dll (KeyHunt_Cuda_Latest)
- Biblioteca libsecp256k1 (MIT license) como referencia de reimplementacao
- Comunidade Model-Context-Protocol (MCP)
- Todos os contribuidores open-source

---

Ultima atualizacao

15 de janeiro de 2024

Versao

0.1.0