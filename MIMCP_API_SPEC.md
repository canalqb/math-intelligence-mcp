# Math Intelligence MCP — API Specification

**Document:** MIMCP_API_SPEC.md  
**Version:** 0.1  
**Status:** Approved — contracts independent of ice_secp256k1.dll analysis  
**Related:** MIMCP_ARCHITECTURE.md (v0.2 post-DLL analysis), ICE_DLL_TECHNICAL_REPORT.md (Stage A complete, B-D populated)  

---

## 1. JSON-RPC 2.0 Transport

All tools use JSON-RPC 2.0 over either:
- **MCP stdio**: `stdout` carries JSON Lines responses, `stderr` for diagnostics
- **Streamable HTTP**: `POST /tools/{name}` with `Content-Type: application/json`

### 1.1 Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "tools/<tool_name>",
  "params": { /* tool-specific */ },
  "id": "<request-id-or-null>"
}
```

### 1.2 Success Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "result": <tool-specific-output>,
    "domain": "<math|crypto|integer|boolean|...>",
    "exact": true,
    "verification": {
      "status": "passed|failed|offered",
      "method": "independent_check|agent_provided|not_requested"
    },
    "metadata": {
      "algorithm": "<algorithm-name>",
      "duration_us": <number>,     // measured, illustrative only
      "memory_bytes": <number>     // measured, illustrative only
    }
  },
  "id": "<request-id>"
}
```

### 1.3 Error Response

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": <number>,       // per error codes below
    "message": "<string>",
    "data": "<optional>"
  },
  "id": "<request-id>"
}
```

---

## 2. Error Codes

| Code | Name | Meaning |
|------|------|---------|
| `-32600` | Parse error | Invalid JSON |
| `-32601` | Method not found | Unknown tool `/tools/<name>` |
| `-32602` | Invalid params | Params don't match schema |
| `-32603` | Internal error | Worker crash, OOM, timeout |
| `-32001` | Validation failed | Input violates formula conditions |
| `-32002` | Verification failed | Verification engine flagged issue |
| `-32003` | Resource exceeded | Memory/CPU/time limits exceeded |
| `-32004` | Unsupported operation | Requested on unsupported platform |

---

## 3. P0 Tools (Essential MVP)

### 3.1 math_evaluate

**Description:** Execute arbitrary mathematical expressions with exact arbitrary precision.

**Request:**

```json
{
  "expression": "2^256 - 2^32 - 977",
  "domain": "integer",
  "precision": "arbitrary",
  "explain": true
}
```

**Response:**

```json
{
  "success": true,
  "result": "...",          // exact integer string or "error"
  "domain": "integer",
  "exact": true,
  "verification": {
    "status": "passed",
    "method": "independent_check"
  },
  "metadata": {
    "algorithm": "integer_arithmetic",
    "duration_us": 0,       // measured in actual impl
    "memory_bytes": 0
  }
}
```

**Constraints:**
- `precision: "arbitrary"` → big integer math, no float approximations
- `domain: "integer"` → only integer domain supported in v1
- `explain: true` → include human-readable explanation in metadata

---

### 3.2 math_explain

**Description:** Explain a formula, its conditions, and its result.

**Request:**

```json
{
  "formula_id": "modular_inverse",
  "inputs": {"a": 42, "m": 97},
  "include_conditions": true,
  "include_algorithm": true
}
```

**Response:**

```json
{
  "success": true,
  "formula": "modular_inverse",
  "computes": "a^(-1) mod m where gcd(a,m)=1",
  "conditions": ["m > 1", "gcd(a,m) = 1"],
  "inputs_provided": {"a": 42, "m": 97},
  "conditions_met": true,
  "algorithm_used": "extended_gcd_or_montgomery",
  "result": "42^(-1) mod 97 = 71",  // verified: 42*71 mod 97 = 1
  "explanation": "Extended Euclidean algorithm finds x,y s.t. ax + my = 1; x is the inverse.",
  "limitations": ["fails if gcd(a,m) != 1", "m must be > 1"],
  "metadata": {
    "duration_us": 0,
    "memory_bytes": 0
  }
}
```

---

### 3.3 math_optimize

**Description:** Compare computational strategies for an operation.

**Request:**

```json
{
  "operation": "integer_multiplication",
  "operand_size": 256,
  "objective": "memory_efficiency",
  "compare": true
}
```

**Response:**

```json
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

**Constraints:**
- Each candidate measured identically same hardware/input
- `memory_bytes` and `duration_us` are measured, not predicted
- Recommendation based on objective (here: memory_efficiency)

---

### 3.4 result_verify

**Description:** Request independent verification of a prior computation.

**Request:**

```json
{
  "operation": "modular_exponentiation",
  "input": {"base": 3, "exp": 256, "mod": 2^521 - 1},
  "result": "<previous-result-hex-or-string>",
  "strict": true
}
```

**Response:**

```json
{
  "success": true,
  "verified": true,
  "method": "independent_algorithm_different_path",
  "confidence": 0.99,
  "properties_checked": ["boundary_conditions", "invariants", "known-vectors"],
  "divergence": false,
  "metadata": {
    "duration_us": 0,
    "memory_bytes": 0
  }
}
```

**When `success: false`:** verification detected issue — returned details in `metadata`.

---

### 3.5 memory_profile

**Description:** Measure memory consumption of an operation.

**Request:**

```json
{
  "operation": "integer_multiplication",
  "operand_size": 512,
  "measure": ["peak_memory", "allocations", "peak_rss"]
}
```

**Response:**

```json
{
  "success": true,
  "measurements": {
    "peak_memory_bytes": 2048,
    "total_allocations": 12,
    "peak_rss_bytes": 4096,
    "memory_pattern": "heap_with_pool_reuse",
    "detailed": {
      "before_op": 512,
      "during_op": 2048,
      "after_op": 256
    }
  }
}
```

---

### 3.6 secp256k1_validate (P1)

**Description:** Validate a public key point lies on the secp256k1 curve.

**Request:**

```json
{
  "x": "<hex-256-bit>",
  "y": "<hex-256-bit>",
  "include_details": true
}
```

**Response:**

```json
{
  "success": true,
  "valid_curve_point": true,
  "on_curve": true,
  "order_divides_curve_order": true,
  "include_details": {
    "field_element_check": "x^3 + 7 = y^2 mod p",
    "prime": "p = 2^256 - 2^32 - 977",
    "validation_method": "direct_substitution"
  }
}
```

**Constraints:** Only valid for 256-bit coordinates; curve equation `y^2 = x^3 + 7 mod p`.

---

### 3.7 bitcoin_format_validate (P1)

**Description:** Validate a Bitcoin address format and derive its public key hash.

**Request:**

```json
{
  "address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
  "validate_format": true,
  "check_hash": true
}
```

**Response:**

```json
{
  "success": true,
  "valid_format": true,
  "address_type": "legacy-P2PKH",
  "hash160": "<hex-160-bit>",
  "network_byte": 0x00,
  "checksum_valid": true,
  "decoded": {
    "version": 0,
    "public_key_hash": "<hex>",
    "hash160_len": 20
  }
}
```

**Supported types:** legacy (P2PKH), segwit (bech32), testnet.

---

### 3.8 algorithm_compare (P1)

**Description:** Compare two algorithm implementations for an operation.

**Request:**

```json
{
  "operation": "modular_exponentiation",
  "input_size": 2048,
  "algorithms": ["method_a", "method_b"],
  "constraints": {
    "minimize_memory": true,
    "preserve_precision": true
  }
}
```

**Response:**

```json
{
  "success": true,
  "comparison": [
    {
      "algorithm": "method_a",
      "memory_bytes": 4096,
      "duration_us": 12500,
      "precision_lost": false
    },
    {
      "algorithm": "method_b",
      "memory_bytes": 2048,
      "duration_us": 9800,
      "precision_lost": false
    }
  ],
  "ranking": {
    "winner": "method_b",
    "criterion": "memory_efficiency_with_precision_preservation",
    "detail": "Uses 50% less memory at cost of 21% more time; precision fully preserved"
  }
}
```

---

### 3.9 reasoning_check (P1)

**Description:** Analyze consistency between premises, formula, and result.

**Request:**

```json
{
  "premises": ["m > 1", "gcd(a,m) = 1"],
  "formula": "modular_inverse",
  "result": "42^(-1) mod 97 = 71",
  "check_inconsistencies": true
}
```

**Response:**

```json
{
  "success": true,
  "consistent": true,
  "premises_valid": true,
  "formula_applicable": true,
  "result_valid": true,
  "inconsistencies": [],
  "analysis": "All premises hold; formula conditions met; result verified by independent check.",
  "caveats": ["result valid only for gcd(42,97)=1"]
}
```

---

### 3.10 formula_lookup (P2)

**Description:** Search the formula registry.

**Request:**

```json
{
  "query": "modular inverse",
  "domain": "number_theory",
  "max_results": 5
}
```

**Response:**

```json
{
  "success": true,
  "formulas": [
    {
      "id": "modular_inverse",
      "name": "Modular Inverse",
      "domain": "number_theory",
      "inputs": ["a", "m"],
      "conditions": ["m > 1", "gcd(a,m) = 1"],
      "precision": "arbitrary"
    },
    {
      "id": "modular_inverse_prime",
      "name": "Modular Inverse (Prime Modulus)",
      "domain": "number_theory",
      "inputs": ["a", "p"],
      "conditions": ["p is prime", "gcd(a,p) = 1"],
      "precision": "arbitrary"
    }
  ],
  "total_found": 2
}
```

---

## 4. P2 Tools (Post-MVP)

### 4.1 knowledge_lookup

**Description:** Retrieve documentation and properties of mathematical concepts.

**Request:** (same structure as formula_lookup but broader search)

### 4.2 benchmark_run

**Description:** Execute a named benchmark suite.

**Request:** `{ "benchmark_id": "arithmetic_ops_256", "parameters": {...} }`

### 4.3 Additional P2 endpoints
- `math://resources` — downloadable test vectors
- `system://capabilities` — server-side capability listing

---

## 5. Tool Registration & Discovery

### 5.1 MCP Resource URIs

| URI | Content |
|-----|---------|
| `math://catalog` | List of all available operations/formulas |
| `math://formulas` | Detailed formula entries with conditions |
| `math://algorithms` | Algorithm registries with metadata |
| `math://constraints` | Mathematical constraints & conditions |
| `math://benchmarks/latest` | Most recent benchmark results |
| `crypto://secp256k1/reference` | Technical documentation for secp256k1 |
| `system://capabilities` | Server capabilities (tools, transport, version) |

### 5.2 Client Discovery

Clients query `system://capabilities` on startup to discover:
- Available tools (P0, P1, P2)
- Transport supported (stdio, streamable-http)
- Version of contract (`mimcp-contract-...`)
- Platform support (Windows, Linux, Docker)
- secp256k1 availability (reimplemented or DLL-dependent)

---

## 6. Versioning & Compatibility

```
Contract versions:
- mimcp-contract-2024-01: initial release, P0 tools only, stdio transport
- mimcp-contract-2024-02: add Streamable HTTP, P1 tools
- mimcp-contract-2024-03: secp256k1 subsystem v1
- mimcp-contract-2025-01: MVP complete, all P0+P1

Client must declare accepted version; server responds with its version.
Major version change may require client update; minor adds tools only.
```

---

## 7. Example Session Flow

```
Client → MCP: POST /tools/math_evaluate
         { "expression": "2^521 - 1", "domain": "integer", "precision": "arbitrary", "explain": true }

MCP → Worker (Rust): stdin JSON Lines
Worker → MCP: stdout JSON Lines result
MCP → Client: 200 JSON response with result, verification, metadata

Client ← MCP: {
  "jsonrpc":"2.0","result":{"success":true,"result":"...","domain":"integer","exact":true,
   "verification":{"status":"passed","method":"independent_check"},
   "metadata":{"algorithm":"integer_arithmetic","duration_us":850,"memory_bytes":256}},
  "id":1
}
```