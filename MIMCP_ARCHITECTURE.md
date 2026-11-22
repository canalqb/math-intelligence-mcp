# Math Intelligence MCP — Architecture Specification

**Document:** MIMCP_ARCHITECTURE.md  
**Version:** 0.2 (post-DLL analysis)  
**Status:** Approved — architecture validated after ice_secp256k1.dll investigation  
**Related:** ICE_DLL_TECHNICAL_REPORT.md (Stage A complete, B-D populated), MIMCP_API_SPEC.md  

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Math Intelligence MCP (MIMCP)           │
│  Multi-Platform Mathematical Intelligence Server           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────┐      ┌──────────────────────────────┐
│  Client Agents     │      │  MCP Gateway (TypeScript)     │
│  Kimi, OpenCode,   │◀────▶│  - Tool discovery & routing    │
│    Hermes, others  │      │  - JSON-RPC / Streamable HTTP  │
│                      │      │  - Resource registration       │
└─────────────────────┘      └──────────────────────────────┘
           │                       │
           │  stdio / HTTP       │  IPC JSON Lines
           ▼                       ▼
┌─────────────────────┐   ┌─────────────────────────────┐
│  Rust Compute Worker│   │  Math Engine (Core)          │
│  - Native performance│   │  - Arithmetic Engine         │
│  - Memory-optimized  │   │  - Memory Optimization Engine│
│  - Benchmarkable     │   │  - Formula Engine            │
└─────────────────────┘   └─────────────────────────────┘
                                   │
                                   ▼
                            ┌─────────────────────┐
                            │ Validation Engine   │
                            │ - Independent check │
                            │ - Property verification│
                            │ - Divergence reports │
                            └─────────────────────┘
                                   │
                                   ▼
                            ┌─────────────────────┐
                            │ Reasoning Assistant │
                            │ - Structured output │
                            │ - Inconsistency anal. │
                            │ - Evidence-based exp. │
                            └─────────────────────┘
```

---

## 2. Process Model

### 2.1 Communication Flow

```
Client Request
  │
  ▼
MCP Gateway (TypeScript/Node.js)
  │
  ├─ Validates parameters (schema, bounds, constraints)
  │
  ├─ Routes to appropriate tool (math_evaluate, math_optimize, etc.)
  │
  ├─ Calls Rust Compute Worker via JSON Lines (stdio)
  │   │
  │   ├─ Executes computation native
  │   ├─ Returns result + metadata (algorithm, duration_us, memory_bytes)
  │   └─ Error handling with structured codes
  │
  └─ Returns formatted response to client
       │
       ▼
Client receives: { success, result, domain, exact, verification, metadata }
```

### 2.2 Transport Layers

| Direction | Protocol | Details |
|-----------|----------|---------|
| **Local (same process)** | JSON Lines (stdio) | `stdout` for results, `stderr` for logs/diagnostics |
| **Remote (network)** | Streamable HTTP | MCP official spec; POST to `/tools/{name}` |
| **Agent → MCP** | Either | Detected auto; configured per-agent |
| **MCP → Worker** | JSON Lines stdio | Fixed: worker PID subprocess, stdout captured |

### 2.3 Process Isolation

```
┌─────────────────────┐
│  MCP Server Process │  ← TypeScript/Node.js, manages tools, auth, routing
└─────────────────────┘
           │
           spawn subprocess
┌─────────────────────┐
│  Rust Worker Process│  ← Math Engine, Memory Optimizer, Validation
│  - stdin/stdout piped│
│  - Limited lifetime │
│  - Resource caps (--memory-limit, --cpu-limit) │
└─────────────────────┘
```

*Rationale: A failure in the native worker should not terminate the MCP interface. Allows hot-swapping the worker without client disruption.*

---

## 3. Module Architecture

### 3.1 math_core — Arbitrary Precision Arithmetic

```
┌─────────────────────────┐
│  Integer Representation │
│  - Limbs (configurable) │
│  - Stack vs heap alloc  │
│  - Compact structures   │
└─────────────────────────┘

Functions:
- add(a, b) → sum
- sub(a, b) → difference
- mul(a, b) → product
- div(a, b) → quotient, remainder
- pow(base, exp, mod) → modular exponentiation
- mod_inv(a, m) → modular inverse
- gcd(a, b) → greatest common divisor
- cmp(a, b) → comparison (−1, 0, 1)
- norm(x) → normalized representation
```

### 3.2 memory_optimizer — Memory Management Strategies

```
┌────────────────────────────────────────────────────┐
│  Allocation Strategies Comparison                │
│  ┌─────────────┐  ┌─────────────────────┐        │
│  │  Stack-only   │  │  Heap with pooling   │        │
│  │  (fast, limited)│  │  (configurable)      │        │
│  └─────────────┘  └─────────────────────┘        │
│  ┌─────────────┐  ┌─────────────────────┐        │
│  │  Copy-on-write│  │  Buffer reuse        │        │
│  │  (COW, forked)│  │  (reuse across ops)  │        │
│  └─────────────┘  └─────────────────────┘        │
└────────────────────────────────────────────────────┘

Configurable per-operation:
- preference: "speed" | "memory" | "balanced"
- max_stack_depth: number (e.g., 8, 16, 32)
- pool_size: number of pre-allocated buffers
- ttl_seconds: buffer retention time
```

### 3.3 formula_engine — Formula Storage & Execution

```
Each formula is a standardized JSON definition:

{
  "id": "modular_inverse",
  "name": "Modular Inverse",
  "domain": "number_theory",
  "inputs": ["a", "m"],
  "conditions": ["m > 1", "gcd(a,m) = 1"],
  "precision": "arbitrary",
  "verification": "independent",
  "algorithm": "montgomery_or_werr",
  "duration_us": 0,        // measured, not promised
  "memory_bytes": 0,       // measured, not promised
  "description": "Computes a^(-1) mod m using..."
}

Engine responsibilities:
- Store formula registry (JSON Lines or embedded)
- Resolve formula by ID
- Validate input conditions before execution
- Execute via math_core with selected algorithm
- Return result + algorithm + measured metrics
- Provide explanation of what was computed and how
```

### 3.4 algorithm_optimizer — Strategy Comparison

```
Agent requests comparison:

{
  "operation": "integer_multiplication",
  "operand_size": 256,
  "objective": "memory_efficiency",
  "compare": true
}

Response structure:

{
  "success": true,
  "candidates": [
    {
      "algorithm": "method_a",
      "memory_bytes": 1024,
      "duration_us": 4500
    },
    {
      "algorithm": "method_b", 
      "memory_bytes": 2048,
      "duration_us": 2800
    }
  ],
  "recommendation": {
    "algorithm": "method_b",
    "reason": "Lower measured memory usage (2x less), only 20% slower"
  }
}
```

*Each candidate is measured on the same input, same hardware, same conditions.*

### 3.5 result_verify — Independent Verification

```
Verification capabilities:
- Independent algorithm execution (different code path)
- Property checks (invariants, boundaries, edge cases)
- Known vector comparison (reference test data)
- Divergence reporting (when results differ from expected)
- Limit/condition verification (bounds, signs, parity)

Verification is ALWAYS offered but NOT automatic — agent must request.
```

### 3.6 reasoning_assistant — Structured Reasoning Support

```
Flow when agent identifies a mathematical problem:

1. Problem received
2. Agent queries MCP: "What formula applies? What are conditions?"
3. MCP returns: formula_id, conditions, algorithm, explanation_template
4. Agent executes or requests execution
5. MCP returns: result, verification_status, metrics
6. Agent constructs explanation using:
   - Evidence: {result, algorithm, metrics}
   - Conditions: {bounds, constraints verified}
   - Limitations: {precision boundary, when invalid}
7. Optional: Agent requests inconsistency analysis:
   "Are premises consistent with result? Any hidden assumptions?"
```

### 3.7 benchmark_engine — Reproducible Benchmarks

```
Runs micro-benchmarks for:

- Arithmetic ops (add, mul, mod_inv) at varying sizes
- Memory allocation patterns (stack vs heap, pool sizes)
- Algorithm comparisons (method_a vs method_b)
- Precomputation impact (with vs without ctx)

Output format:

{
  "operation": "modular_inverse",
  "input_size": 256,
  "measurements": [
    { "runs": 10, "avg_us": 1200, "p50_us": 1100, "p95_us": 1500,
      "max_mem_bytes": 2048, "min_mem_bytes": 512 }
  ],
  "system": {
    "cpu": "Intel i7-9750H",
    "cpu_freq_mhz": 4100,
    "mem_total_gb": 16,
    "os": "Ubuntu 22.04.3 LTS",
    "rustc": "1.78.0",
    "criterion": "0.5.0"
  }
}
```

### 3.8 knowledge_engine — Mathematical Knowledge Base

```
Endpoints:
- math://catalog → list of all operations/formulas
- math://formulas → detailed formula entries
- math://algorithms → algorithm registries with metadata
- math://constraints → mathematical constraints & conditions
- math://benchmarks/latest → most recent benchmark results

Each entry includes:
- ID, name, domain
- Inputs, conditions, precision
- Algorithm used
- Reference vectors (for verification)
- Author/source attribution
- Last updated timestamp
```

---

## 4. secp256k1 Subsystem

### 4.1 Purpose

Provides curve-specific operations derived from ice_secp256k1.dll investigation:

```
secp256k1_validate_public_key(x, y) → bool
secp256k1_point_multiply(scalar, G) → point
secp256k1_scalar_from_hex(hex) → scalar (validated)
secp256k1_serialize_point(point, fmt) → hex (compressed/uncompressed)
secp256k1_serialize_scalar(scalar) → hex
secp256k1_derive_address(public_key) → bitcoin_address
secp256k1_verify_signature(msg, sig, pubkey) → bool
```

### 4.2 Scope Limitations

⚠ **NOT** included (out of MCP scope):
- Private key discovery
- Wallet generation or brute-force
- Third-party key cracking
- Non-authorized format conversions

✅ **INCLUDED** (legitimate operations):
- Public key validation
- Point multiplication (core math)
- Signature verification
- Address derivation from authorized keys
- Format validation (WIF, bech32, etc. — with proper isolation)

### 4.3 DLL Dependency Strategy

```
Three pathways (selected case-by-case):

1. Native compilation — if source available → compile Win + Linux versions
2. Isolated Windows process — DLL used only on Windows hosts via WSL2/dual-boot
3. Reimplementation — algorithms documented & audited → reimplemented in Rust

Architecture choice: PATH 3 (reimplementation) as primary, PATH 1 as fallback if source obtained.
Never depend on DLL being directly loadable on Linux — PE binary ≠ native Linux.
```

---

## 5. Contract Versioning

```
Internal contract format (JSON Lines, stdio):

{"jsonrpc":"2.0","method":"tools/math_evaluate","params":{...},"id":1}
{"jsonrpc":"2.0","result":{...},"id":1}     │
       │                                      ↓
{"jsonrpc":"2.0","error":{...},"id":1}   │  (on failure)
```

**Versioning scheme:**
- `mimcp-contract-2024-01` — initial release (MCP stdio transport)
- `mimcp-contract-2024-02` — add Streamable HTTP support
- `mimcp-contract-2024-03` — add secp256k1 subsystem v1
- `mimcp-contract-2025-01` — MVP with all P0/P1 tools

**Backward compatibility:** Minor version bumps add tools; major version bumps may change transport. Clients specify accepted contract version.

---

## 6. Error Handling & Safety

### 6.1 Error Codes (JSON-RPC 2.0 compatible)

| Code | Meaning | When Triggered |
|------|---------|----------------|
| `-32600` | Parse error | Malformed JSON request |
| `-32601` | Method not found | Unknown tool name |
| `-32602` | Invalid params | Params schema violation |
| `-32603` | Internal error | Worker crash, timeout, OOM |
| `-32001` | Validation failed | Input violates conditions |
| `-32002` | Verification failed | Verification engine flagged issue |
| `-32003` | Resource exceeded | Memory/CPU/time limits exceeded |
| `-32004` | Unsupported operation | secp256k1 requested on Linux without reimplementation |

### 6.2 Safety Gates

| Gate | Description |
|------|-------------|
| **Parameter validation** | All inputs checked against formula conditions before execution |
| **Resource limits** | Worker subprocess killed if memory > limit or time > timeout |
| **No private key exposure** | Zero secrets in logs, prompts, or returned metadata |
| **Verification offered, not forced** | Agent chooses whether to verify results |
| **DLL isolation** | Windows-only binary; Linux uses reimplemented equivalents |
| **License compliance** | Reimplementation only after license check |

---

## 7. Deployment Configuration

### 7.1 Docker (reference from spec)

```yaml
services:
  math-intelligence:
    build:
      context: .
      dockerfile: docker/Dockerfile
    environment:
      MIMCP_TRANSPORT: streamable-http
      MIMCP_HOST: 0.0.0.0
      MIMCP_PORT: 3001
      MIMCP_LOG_LEVEL: info
    ports:
      - "127.0.0.1:3001:3001"
    restart: unless-stopped
    read_only: true
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    tmpfs:
      - /tmp
```

### 7.2 Windows Installation

- Native Rust worker binary (compiled or reimplemented from DLL)
- MCP server as Windows service or executable
- DLL used only if pathway 1 (source) or pathway 2 (isolated process) selected

### 7.3 Linux Installation

- Native Rust worker (no DLL dependency — reimplemented algorithms)
- MCP server via npm/pnpm or system package
- Docker container option available

### 7.4 Resource Caps (per worker)

```bash
# Example: launch with caps
./math-worker \
  --memory-limit=512MB \
  --cpu-limit=2000ms \
  --timeout-ms=30000 \
  --stdin-stdout
```

---

## 8. Evolution Roadmap (from spec)

```
MIMCP 1.0 — Mathematical Core
  □ Arithmetic, optimization, validation, secp256k1 adapters
  □ P0/P1 tools implemented and tested
  □ Windows + Linux + Docker deployment
  □ OpenCode + Hermes + Kimi integration

MIMCP 1.5 — Advanced Reasoning
  □ Demonstrations, hypothesis analysis, reasoning validation
  □ Complex problem decomposition
  □ Cross-agent evidence sharing

MIMCP 2.0 — Scientific Computing
  □ Linear algebra, statistics, numerical optimization
  □ SWE-bench-style task slices
  □ Distributed computation

MIMCP 3.0 — Multi-Agent Intelligence
  □ Controlled result sharing
  □ Distributed execution
  □ Agent coordination & consensus
```