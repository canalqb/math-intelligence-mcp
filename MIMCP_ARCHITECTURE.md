# MIMCP Architecture - Perguntas Frequentes

## FAQ

**Q: Quantas camadas tem a arquitetura?**  
A: 6 camadas distintas com responsabilidades claras, desde o cliente até a validacao e raciocinio, todas desenhadas para operacao multiplataforma e deploy no Render.

**Q: Como as camadas se comunicam?**  
A: atraves de endpoints JSON-RPC 2.0 via Streamable HTTP, com registro de tools e roteamento de methods P0-P2. A comunicacao flui do cliente -> gateway -> worker Rust -> resultados de volta.

**Q: O que cada camada faz?**  
A: Cada camada tem um papel especifico: CLIENTE (agentes e interacao), GATEWAY (descoberta e roteamento), WORKER (computacao nativa em Rust), CORE (motores matematicos), VAL (verificacao independente) e RAZAO (output estruturado e analise de inconsistencias).

**Q: Como fazer deploy?**  
A: Deploy no servico Render rnd_jSek47xZndoAKnhsjTLJVaxAmr12 usando Docker multi-stage build. Build command: `pip install -e .`, start command: `python -m mimcp`. apos push no GitHub, deploy automatico ou manual via dashboard.

**Q: Quais tools estao em cada nivel?**  
A: P0 (5 tools essenciais), P1 (5 tools avancadas), P2 (2 tools opcionais). Todas registradas em python/tools.py e expostas via JSON-RPC 2.0.

---

## Arqutetura do Sistema (Diagrama Mermaid)

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

## Layers Details

### Layer 1: CLIENT (Client Layer)

**Responsabilidade**: Interacao com agentes e usuarios. Responsavel por enviar requisicoes JSON-RPC 2.0 ao gateway e exibir respostas formatadas.

**Components**:
- Agentes IA (Kimi, OpenCode, Hermes)
- Interface de linha de comando
- Interface web via navegador

**Input/Output**:
- Input: Requisicoes JSON-RPC com method e params
- Output: Respostas formatadas com status success/failure e dados resultantes

---

### Layer 2: GATEWAY (MCP Gateway)

**Responsabilidade**: Ponto de entrada unico para todas as requisicoes. Responsavel por discovery de tools, roteamento para o worker Rust adequado e formatacao de respostas JSON-RPC.

**Components**:
- Tool discovery & routing
- JSON-RPC / Streamable HTTP handler
- Resource registration

**Endpoints**:
- POST /mcp/json-rpc - Entrada unica para todas as 12 tools
- GET /healthz - Health check endpoint

---

### Layer 3: RUST COMPUTE WORKER

**Responsabilidade**: Computacao nativa em Rust para maximizar performance. Implementa todas as 12 tools (P0-P2) com optimizacao de memoria e benchmarks comparativos.

**Components**:
- Native performance - Computacao sem overhead de interpretador
- Memory-optimized - Perfilagem e otimizacao de memoria
- Benchmarkable - Facilidade de comparacao de performance

**Dependencies**:
- serde, serde_json para manipulacao de JSON
- Zod para validacao de inputs
- Cargo test para testes unitarios

---

### Layer 4: MATH CORE

**Responsabilidade**: Motores matematicos especificos organizados por nivel de complexidade.

**Sub-components**:
- Arithmetic Engine - Operacoes aritmeticas basicas
- Memory Optimization Engine - Otimizacao de memoria em calculos pesados
- Formula Engine - Motor de formulas simbolicas (P1)

---

### Layer 5: VALIDATION ENGINE

**Responsabilidade**: Verificacao independente de resultados. Responsavel por garantir que os outputs atendem propriedades esperadas antes de retornar ao cliente.

**Components**:
- Independent check - Verificacao sem dependencia de source original
- Property verification - Validacao de propriedades matematicas
- Divergence reports - Relatorios de divergencia entre esperado e obtido

---

### Layer 6: REASONING ASSISTANT

**Responsabilidade**: apos processamento, assistente de raciocinio formata output estruturado e identifica inconsistencias.

**Components**:
- Structured output - Output padraoizado com metadados
- Inconsistency anal - Analise de inconsistencias entre inputs e outputs
- Evidence-based exp - Explicacao baseada em evidencia dos passos

---

## Roteamento de Tools (P0-P2)

### Nivel P0 - Ferramentas Essenciais (5 tools)

1. math_evaluate - Avaliar expressoes matematicas
2. math_explain - Explicar conceitos matematicos
3. math_optimize - Otimizar expressoes algebricas
4. result_verify - Verificar resultados de calculos
5. memory_profile - Perfilagem de memoria

### Nivel P1 - Ferramentas Avançadas (5 tools)

6. formula_engine - Motor de formulas simbolicas
7. symbolic_solver - Solucionador simbolico
8. calculus_operations - Operacoes de calculo
9. linear_algebra - Algebra linear
10. statistical_analysis - Analise estatistica

### Nivel P2 - Ferramentas Opcionais (2 tools)

11. advanced_cryptography - Criptografia avancada
12. pattern_recognition - Reconhecimento de padroes

---

## Sequencia de Deploy

### Passo 1: Preparacao

- Git history limpa (token removido)
- Rust toolchain configurada
- Python environment setup
- Dockerfile multi-stage pronto

### Passo 2: Build

```bash
docker build -t math-intelligence-mcp .
```

### Passo 3: Deploy no Render

Aceder dashboard em https://render.com/dashboard com token de acesso.
Selecionar servico rnd_jSek47xZndoAKnhsjTLJVaxAmr12.
Clicar "Manual Deploy" -> "Trigger deploy" com:
- Build Command: `pip install -e .`
- Start Command: `python -m mimcp`

### Passo 4: Verificacao

MCP acessivel em https://math-intelligence-mcp-[hash].onrender.com
Endpoint JSON-RPC: POST /mcp/json-rpc

---

## Versionamento

- Versao Atual: 0.1.0
- Data: 15 de janeiro de 2024
- Arquitetura: 6 layers with mermaid diagrams
- Spec: JSON-RPC 2.0

---

## Ultima atualizacao

15 de janeiro de 2024

Versao

0.1.0