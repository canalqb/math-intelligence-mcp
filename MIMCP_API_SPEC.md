# MIMCP API Specification - MathForge Protocol 2.1.0-REV

## 1. Visão Geral

O **MathForge MCP** implementa estritamente o protocolo **MCP oficial (2024-11-05+)** com ciclo de vida completo e catálogo de 17 ferramentas organizadas em 3 níveis (P0, P1, P2). Todas as ferramentas são acessíveis via JSON-RPC 2.0 em `POST /mcp/json-rpc`.

### 1.1. Ciclo de Vida Oficial MCP

O servidor segue as 4 fases distintas do protocolo MCP:

1. `initialize`: Negociação de versão de protocolo e troca de `capabilities` (tools, resources, prompts).
2. `notifications/initialized`: Confirmação de prontidão do cliente.
3. `tools/list`: Descoberta de catálogo com schemas JSON Schema / Pydantic estritos.
4. `tools/call`: Execução padronizada:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "math_evaluate",
    "arguments": {
      "expression": "sqrt(2)",
      "precision_digits": 80,
      "mode": "HIGH"
    }
  }
}
```

### 1.2. Transportes Oficiais Suportados

- **STDIO**: Padrão primário para clientes locais (Claude Desktop, Cursor, Antigravity IDE, VS Code, Goose).
- **Streamable HTTP**: Transporte remoto principal (POST `/mcp` com suporte a streaming de chunks e SSE unidirecional conforme a spec). O SSE puro legado é mantido apenas como fallback opcional.

### 1.3. Padrão de Retorno (Agent Self-Correction)

Todas as ferramentas operam com retornos estruturados separando falhas de negócio (com `agent_hint` e `retryable`) de erros de protocolo MCP:

```json
{
  "success": false,
  "error": {
    "code": "PRECISION_LIMIT_EXCEEDED",
    "type": "RESOURCE_LIMIT",
    "message": "A precisão solicitada (5000 dígitos) excede o limite síncrono de 1000 dígitos.",
    "agent_hint": "Reduza a precisão para <= 1000 ou submeta o cálculo via distributed_job_submit.",
    "retryable": true
  }
}
```

## 2. Catálogo de Ferramentas (17 Tools P0-P2)

### 2.1. Nível P0 - Ferramentas Fundamentais (2 tools)

#### 1. `math_evaluate`

**Descrição:** Avalia expressões matemáticas com validação formal de AST e seleção explícita de precisão.

**Parâmetros:**
- `expression` (string, obrigatório): Expressão matemática restrita à gramática formal.
- `mode` (string enum: `["FAST", "HIGH", "EXACT", "AUTO"]`, default: `"AUTO"`):
  - `FAST`: Ponto flutuante IEEE 754 de 64 bits (hardware float).
  - `HIGH`: Precisão arbitrária configurável via mpmath/MPFR (50 a 1.000 dígitos).
  - `EXACT`: Aritmética racional exata simbólica via SymPy/GMP.
  - `AUTO`: Seleciona com base no condicionamento e erro estimado.
- `precision_digits` (integer, opcional, default: 50, máx: 1.000 no modo síncrono).

**Retorno:** `result`, `decimal_representation`, `mode_used`, `precision_bits`, `evaluation_time_ms`.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0",
  "result":{"success":true,"data":1.41421356,"expression":"sqrt(2)","mode_used":"HIGH","precision_bits":80,"evaluation_time_ms":12},
  "id":1
}
```

**Resposta de erro:**
```json
{
  "jsonrpc":"2.0","error":{
    "code":-32602,
    "message":"Invalid parameters",
    "error":{"code":"PRECISION_LIMIT_EXCEEDED","type":"RESOURCE_LIMIT","message":"A precisão solicitada (5000 dígitos) excede o limite síncrono de 1000 dígitos.","agent_hint":"Reduza a precisão para <= 1000 ou submeta o cálculo via distributed_job_submit.","retryable":true}
  },
  "id":1
}
```

#### 2. `result_verify`

**Descrição:** Verificador rigoroso que distingue igualdade simbólica formal, verificação numérica aproximada e validade de domínio.

**Parâmetros:**
- `candidate_solution` (string, obrigatório): Valor ou expressão candidata.
- `original_equation` (string, obrigatório): Expressão de referência.
- `verification_type` (string enum: `["symbolic", "numerical", "domain_check", "all"]`, default: `"all"`).
- `tolerance` (number, opcional, default: 1e-15).

**Retorno:** `verified` (bool), `verification_type`, `residual`, `tolerance_used`, `domain_valid` (bool), `is_formal_proof` (bool: false para métodos numéricos).

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"verified":true,"verification_type":"symbolic","residual":0,"tolerance_used":1e-15,"domain_valid":true,"is_formal_proof":false},
  "id":1
}
```

---

### 2.2. Nível P1 - Ferramentas Avançadas de Cálculo, Álgebra e Estatística (9 tools)

#### 3. `math_explain`

**Descrição:** Explica a resolução do problema estruturadamente em LaTeX, separando resolução didática de demonstração axiomática.

**Parâmetros:**
- `topic_or_problem` (string): Tópico ou problema a explicar.
- `output_format` (`"step_by_step" | "conceptual"`): Formato de saída.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"data":"A derivada de x² é 2x via regra da potência.","topic":"derivada de x²","output_format":"step_by_step","formatted":true},
  "id":1
}
```

#### 4. `math_optimize`

**Descrição:** Otimizar expressões algebricas para forma simplificada.

**Parâmetros:**
- `expression` (string): Expressão a otimizar.
- `strategy` (`"simplify" | "factor" | "expand" | "trig_reduce"`): Estratégia de otimização.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"data":"(x + 1)²","expression":"x * x + 2 * x + 1","optimized":true},
  "id":1
}
```

#### 5. `symbolic_solver`

**Descrição:** Solucionador simbólico modular com separação interna entre resolvedores lineares, não-lineares e EDOs.

**Parâmetros:**
- `equations` (array de strings): Equações a resolver.
- `variables` (array de strings): Variáveis independentes.
- `domain` (`"real" | "complex"`): Domínio da resolução.

**Retorno:** Status explícito: `solution_type` (`"exact" | "approximate" | "conditional" | "no_solution_found" | "inconclusive"`), lista de soluções e condições de contorno.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"solution_type":"exact","solutions":["x = 2"],"conditional_parameters":[],"is_formal_proof":false},
  "id":1
}
```

#### 6. `calculus_operations`

**Descrição:** Derivação analítica, integração simbólica e numérica de alta precisão, limites e expansão em séries.

**Parâmetros:**
- `expression`: Expressão alvo.
- `variable`: Variável de diferenciação/inlação.
- `operation` (`"diff" | "integrate" | "limit" | "series"`): Tipo de operação.
- `point`: Ponto para limites/e expansões.
- `order`: Ordem da série (opcional).

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"data":"2x","expression":"x^2","operation":"diff","variable":"x"},
  "id":1
}
```

#### 7. `linear_algebra`

**Descrição:** Operações matriciais diferenciando matrizes exatas de matrizes de ponto flutuante aceleradas por BLAS/LAPACK.

**Parâmetros:**
- `matrix_a`: Primeira matriz (obrigatório).
- `matrix_b` (opcional): Segunda matriz.
- `operation` (`"det" | "inv" | "eig" | "svd" | "condition_number" | "solve_system"`): Operação.
- `precision_type` (`"exact_rational" | "float64"`): Tipo de precisão.

**Retorno:** Matriz resultante, determinante, resíduo $\|Ax - b\|$ e número de condição $\kappa(A)$ para diagnóstico de estabilidade.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"data":[[1,0],[0,1]],"matrix_a":"[[1,0],[0,1]]","operation":"det","determinant":1,"residual":1e-15,"condition_number":1.0},
  "id":1
}
```

#### 8. `statistical_analysis`

**Descrição:** Estatística descritiva, inferência, regressões e testes de hipótese com cálculo de p-valor exato.

**Parâmetros:**
- `dataset` (matriz ou vetor numérico): Dados de entrada.
- `operations` (array de strings): Operações solicitadas (ex: `["mean", "median", "std", "linear_regression"]`).

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"data":{"mean":5.2,"median":5.0,"std":1.3,"p_value":0.03},"dataset":[1,2,3,4,5]},
  "id":1
}
```

#### 9. `precision_check`

**Descrição:** Executa o mesmo cálculo em múltiplos níveis de precisão (53 bits, 128 bits e N bits) para detectar cancelamento catastrófico, perda de dígitos significativos e convergência numérica.

**Parâmetros:**
- `expression` (string): Expressão alvo.
- `target_digits` (integer): Dígitos alvo para comparação.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"comparison_table":[{ "precision":"53 bits","result":1.41,"error":0.004 },{ "precision":"128 bits","result":1.414213,"error":0.000002 }],"target_digits":80,"index_stability":0.997},
  "id":1
}
```

---

### 2.3. Nível P2 - Ferramentas Especializadas, Auditorias e Profiling (6 tools)

#### 10. `algorithm_profile`

**Descrição:** Avalia a complexidade assintótica teórica $O(f(n))$ e requisitos teóricos de memória para um algoritmo e dimensão de dados especificados.

**Parâmetros:**
- `algorithm_name`: Nome do algoritmo a perfilar.
- `input_size_n`: Tamanho de entrada $n$.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"big_o":"O(n log n)","memory_theory":"O(n)","input_size_n":1000},
  "id":1
}
```

#### 11. `hardware_benchmark`

**Descrição:** Executa benchmarks empíricos reais no host local (GFLOPS de CPU, largura de banda de memória e latência de ponto flutuante).

**Parâmetros:**
- `test_type` (`"cpu_flops" | "memory_bandwidth" | "mpfr_throughput"`): Tipo de benchmark.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"gflops":1250,"memory_bandwidth_gb_s":25.6,"mpfr_ops_per_s":850},
  "id":1
}
```

#### 12. `formula_engine`

**Descrição:** Catálogo curado de fórmulas científicas e financeiras com substituição formal e isolamento de incógnitas.

**Parâmetros:**
- `formula_id`: Identificador da fórmula.
- `substitutions`: Mapa de substituições de variáveis.
- `solve_for`: Variável a resolver.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"data":"s = (v^2 - u^2) / (2a)","formula_id":"projectile_motion","substitutions":{"v":10,"u":0,"a":2},"solve_for":"s"},
  "id":1
}
```

#### 13. `pattern_recognition`

**Descrição:** Detecção de padrões numéricos inteiros, relações de congruência modular e consulta estruturada a padrões da enciclopedia OEIS.

**Parâmetros:**
- `sequence` (array de inteiros): Sequência a analisar.
- `predict_next_terms` (integer, default: 3): Quantos termos seguintes prever.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"detected_pattern":"arithmetic_progression","common_difference":3,"next_terms":[8, 11, 14],"oeis_references":["A000027"]},
  "id":1
}
```

#### 14. `distributed_job_status`

**Descrição:** Consulta o status de um emprego distribuído previamente submetido.

**Parâmetros:**
- `job_id`: Identificador do emprego distribuído.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"status":"completed","result":42,"completed_at":"2024-01-15T10:30:00Z"},
  "id":1
}
```

#### 15. `memory_profile`

**Descrição:** Perfilamento de memória para operações de computação, reportando uso de heap, gc e vetores ativos.

**Parâmetros:**
- `operation`: Tipo de operação de perfilamento.
- `size`: Tamanho do vetor/operando.
- `iterations`: Número de iterações.

**Resposta de sucesso:**
```json
{
  "jsonrpc":"2.0","result":{"success":true,"heap_usage_mb":45.2,"gc_count":12,"vector_size":1000},
  "id":1
}
```