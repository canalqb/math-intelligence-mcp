# ==========================================
# Math Intelligence MCP - Dockerfile Multi-stage
# ==========================================
# Fase 1: Build do Rust (core matemático)
# ==========================================
FROM rust:1.75-bookworm AS builder-rust

# Criar diretório de trabalho
WORKDIR /app/rust

# Instalar dependências do sistema para compilação
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar definição do projeto Rust
COPY crates/math-core/Cargo.toml .

# Criar projeto vazio primeiro para cache de camadas
RUN rustup target add x86_64-unknown-linux-gnu
RUN mkdir -p .cargo && echo '[target.x86_64-unknown-linux-gnu]' > ./cargo/config.toml

# Build dependencies only (first layer cache)
RUN cargo fetch 2>/dev/null || true

# Copiar source e build
COPY crates/math-core/src ./src
RUN cargo build --release 2>&1 | tail -20

# Fase 2: Build do TypeScript (servidor MCP)
# ==========================================
FROM node:20-alpine AS builder-ts

WORKDIR /app/mcp

# Instalar dependências
COPY package.json bunlock.lock* ./
RUN npm ci --omit=dev

# Copiar source TypeScript
COPY tsconfig.json tsconfig.json
COPY src ./src
RUN npm run build 2>&1 | tail -20

# Fase 3: Imagem final (minimal)
# ==========================================
FROM python:3.12-slim AS final

# Instalar apenas o necessário
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar binário Rust compilado
COPY --from=builder-rust /app/rust/target/release/math-core /usr/local/bin/math-core

# Copiar aplicações compiladas
COPY --from=builder-ts /app/mcp/dist ./dist

# Copiar código Python wrapper
COPY python/ ./python

# Criar usuário não-root para segurança
RUN useradd -m mcpuser
WORKDIR /home/mcpuser

# Copiar configurações
COPY --chown=mcpuser:mcpuser .mcp-config /home/mcpuser/.mcp-config

# Expor porta
EXPOSE 8000

# Definir usuário
USER mcpuser

# Comando de entrada
CMD ["python", "-m", "mimcp"]