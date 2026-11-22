# MIMCP Implementation Backlog — 8-Week MVP Plan

## Overview
Math Intelligence MCP (MIMCP) server providing mathematical, computational, cryptographic and validation capabilities for AI agents. Based on `ice_secp256k1.dll` analysis.

## Phase 1: DLL Investigation & Report (Week 1)
- [x] **Complete** — `ICE_DLL_TECHNICAL_REPORT.md` populated with actual binary analysis
- [x] **Complete** — Key findings extracted:
  - PE32+ format, 11.5MB
  - secp256k1 curve operations confirmed
  - Export functions: point_mul, scalar_mul, b58_encode/decode, bech32_ad, rmd160, pubkeyxy_to_ETH_address
  - Import chain includes CUDA, NvOptimusEnablement, standard Windows APIs
  - PDB path: KeyHunt_Cuda_Latest project
- [ ] **Pending** — SHA-256 hash calculation (requires secure file handling)

## Phase 2: Architecture & API Specification (Weeks 2-3)
- [ ] **Pending** — Finalize `MIMCP_ARCHITECTURE.md`:
  - Rust compute core + TypeScript MCP server
  - Multiplatform: Windows (native), Linux (Wine/cross-compile), Docker
  - No direct DLL loading on Linux — reimplement or use isolated Windows process
- [ ] **Pending** — Finalize `MIMCP_API_SPEC.md` with concrete tool contracts:
  - P0 tools (essential for MVP):
    - `math_evaluate` — evaluate mathematical expressions
    - `math_explain` — explain math concepts step-by-step
    - `math_optimize` — optimize expressions/formulas
    - `result_verify` — verify computation results
    - `memory_profile` — profile memory usage
  - P1 tools (enhanced capabilities):
    - `crypto_derive_private` — deterministic private key derivation
    - `crypto_public_from_private` — public key from private key
    - `crypto_verify_signature` — ECDSA signature verification
    - `crypto_hash` — SHA-256/keccak hash computation
  - P2 tools (optional/enterprise):
    - `zk_proof_generate` — zk-SNARK proof generation
    - `zk_proof_verify` — zk-SNARK proof verification

## Phase 3: Rust Compute Core (Weeks 4-5)
- [ ] **Pending** — Implement `core/` module with secp256k1 operations:
  - Field arithmetic (mod p addition/multiplication/subtraction)
  - Scalar multiplication (point_mul, scalar_mul)
  - Base58 encoding/decoding
  - RIPEMD-160 (rmd160)
  - Bech32 address conversion
  - Hex-to-address conversion
  - Ethereum-style pubkey derivation
- [ ] **Pending** — Ensure constant-time implementations where possible
- [ ] **Pending** — Add SIMD optimization paths (x86 AVX2, ARM NEON)

## Phase 4: TypeScript MCP Server (Weeks 5-6)
- [ ] **Pending** — Implement `apps/mcp-server/` with JSON-RPC 2.0:
  - Register all P0-P2 tools
  - stdio transport (local) and Streamable HTTP (remote)
  - Tool execution dispatcher
  - Error handling and response formatting
- [ ] **Pending** — Add health checks and status endpoints
- [ ] **Pending** — Implement tool authentication and rate limiting

## Phase 5: Python Experimentation Layer (Weeks 6-7)
- [ ] **Pending** — Implement `python/` wrapper:
  - High-level Python API for all MIMCP tools
  - Integration with common ML/AI frameworks
  - Example notebooks demonstrating capabilities
- [ ] **Pending** — Test with actual secp256k1 operations
- [ ] **Pending** — Verify cross-platform compatibility

## Phase 6: Testing, Documentation & Release (Week 8)
- [ ] **Pending** — Comprehensive test suite:
  - Unit tests for all core functions
  - Integration tests for MCP tool endpoints
  - End-to-end tests with Python wrapper
- [ ] **Pending** — Update all documentation:
  - `MIMCP_ARCHITECTURE.md`
  - `MIMCP_API_SPEC.md`
  - `ICE_DLL_TECHNICAL_REPORT.md` (final version)
  - User guides and API references
- [ ] **Pending** — Final verification and release preparation

## Tool Contract Priority

### P0 — Essential (Must ship with MVP)
| Tool | Description | Key Functions |
|------|-------------|---------------|
| `math_evaluate` | Evaluate mathematical expressions | Parsing, simplification, numeric eval |
| `math_explain` | Explain math concepts step-by-step | Concept breakdown, examples, proofs |
| `math_optimize` | Optimize expressions/formulas | Simplification, common subexpression elimination |
| `result_verify` | Verify computation results | Correctness checking, numerical stability |
| `memory_profile` | Profile memory usage | Allocation tracking, peak usage, leaks |

### P1 — Enhanced Capabilities
| Tool | Description | Key Functions |
|------|-------------|---------------|
| `crypto_derive_private` | Deterministic private key derivation | From seed, mnemonic, or parameter |
| `crypto_public_from_private` | Public key from private key | Compressed/uncompressed formats |
| `crypto_verify_signature` | ECDSA signature verification | secp256k1 signatures, DER/hex input |
| `crypto_hash` | SHA-256/keccak hash computation | Fixed-output hash functions |

### P2 — Optional/Enterprise
| Tool | Description | Key Functions |
|------|-------------|---------------|
| `zk_proof_generate` | zk-SNARK proof generation | Circuit, witness, proving key |
| `zk_proof_verify` | zk-SNARK proof verification | Proof, verification key, statement |

## Technical Decisions

### DLL Dependency Strategy
1. **Primary**: Reimplement core secp256k1 algorithms in Rust (not dependent on binary)
2. **Secondary**: Use binary via isolated Windows process (if Windows-only deployment)
3. **Tertiary**: Link against libsecp256k1 C library (MIT-licensed, open source)

### Multiplatform Approach
- **Windows**: Native DLL loading + Rust compute
- **Linux/Docker**: Reimplemented Rust core (no Windows API dependencies)
- **macOS**: Same as Linux — reimplemented core

### License Considerations
- `ice_secp256k1.dll` appears proprietary (KeyHunt_Cuda_Latest project)
- **Must reimplement** — cannot directly incorporate binary
- Use `libsecp256k1` (MIT) as reference implementation
- Document all license decisions in `ICE_DLL_TECHNICAL_REPORT.md` §E

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **License non-compliance** | Legal/financial | Only reimplement; avoid binary integration |
| **Algorithm inaccuracies** | Security | Reference libsecp256k1 test vectors; constant-time verification |
| **SIMD platform limitations** | Performance | Fallback to pure Rust; document performance tradeoffs |
| **MCP protocol compliance** | Integration | Strict JSON-RPC 2.0 compliance; stdio + HTTP transport |
| **Cross-platform bugs** | Stability | Separate code paths per platform; extensive testing |

## Success Metrics (MVP)
- [ ] SHA-256 hash calculated and verified
- [ ] Rust core implements all identified export functions
- [ ] TypeScript MCP server responds to all P0 tool calls
- [ ] Python wrapper connects and invokes tools successfully
- [ ] All tests pass (80%+ coverage)
- [ ] No hardcoded secrets in any code
- [ ] Documentation complete and reviewed