"""Math Intelligence MCP (MathForge) - HTTP / ASGI Server para Deploy no Render

Este módulo expõe o servidor MCP sobre HTTP/JSON-RPC 2.0 via FastAPI/Uvicorn,
permitindo deploy direto como Web Service no Render ou execução local.
Compatível com o comando de inicialização:
`python -m uvicorn mimcp_server:app --host 0.0.0.0 --port $PORT`
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Assegura que o diretório python/ está no sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_DIR = os.path.join(BASE_DIR, "python")
if PYTHON_DIR not in sys.path:
    sys.path.insert(0, PYTHON_DIR)

# Importação segura do MCPServer como pacote
try:
    from python.mimcp_server import MCPServer
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("mimcp_pkg.mimcp_server", os.path.join(PYTHON_DIR, "mimcp_server.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    MCPServer = mod.MCPServer

# Criação da instância FastAPI
app = FastAPI(
    title="Math Intelligence MCP (MathForge)",
    version="2.1.0",
    description="Servidor MCP de Alta Precisão e Criptografia para Agentes de IA",
)

# Configuração de CORS para agentes web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instância compartilhada do MCPServer
mcp_core = MCPServer()


@app.get("/")
async def root():
    """Endpoint raiz com metadados do serviço."""
    return {
        "service": "Math Intelligence MCP (MathForge)",
        "version": "2.1.0",
        "status": "online",
        "protocol": "MCP (Model Context Protocol) / JSON-RPC 2.0",
        "endpoints": {
            "health": "/health",
            "mcp": "/mcp",
            "json_rpc": "/mcp/json-rpc",
            "tools_list": "/mcp/tools",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint para o Render."""
    return {
        "status": "ok",
        "healthy": True,
        "service": "math-intelligence-mcp",
        "tools_registered": len(mcp_core.tools),
    }


@app.get("/mcp/tools")
async def list_tools():
    """Lista todas as ferramentas disponíveis no MCP."""
    tools_list = []
    for name, tool_info in mcp_core.tools.items():
        if tool_info:
            tools_list.append(
                {
                    "name": name,
                    "description": tool_info.get("description", ""),
                }
            )
    return {"tools": tools_list, "total": len(tools_list)}


@app.post("/mcp")
@app.post("/mcp/json-rpc")
async def handle_mcp_request(request: Request):
    """Processa requisições JSON-RPC 2.0 e chamadas MCP tools/call."""
    try:
        body = await request.json()
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}",
                },
                "id": None,
            },
        )

    # Suporte a lote de requisições ou requisição individual
    if isinstance(body, list):
        responses = []
        for req in body:
            resp = await _dispatch_single_request(req)
            responses.append(resp)
        return responses
    else:
        resp = await _dispatch_single_request(body)
        return resp


async def _dispatch_single_request(req: dict) -> dict:
    """Roteia requisição tanto no padrão MCP oficial (tools/call) quanto em JSON-RPC direto."""
    req_id = req.get("id")
    method = req.get("method", "")
    params = req.get("params", {})

    # 1. Padrão MCP oficial: tools/list
    if method == "tools/list":
        tools_list = []
        for name, tool_info in mcp_core.tools.items():
            if tool_info:
                tools_list.append(
                    {
                        "name": name,
                        "description": tool_info.get("description", ""),
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                        },
                    }
                )
        return {
            "jsonrpc": "2.0",
            "result": {"tools": tools_list},
            "id": req_id,
        }

    # 2. Padrão MCP oficial: tools/call
    if method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        arguments["id"] = req_id
        # Redireciona para o handler do core
        sub_req = {"method": tool_name, "params": arguments, "id": req_id}
        return await mcp_core.process_request(sub_req)

    # 3. Padrão MCP initialize
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {},
                    "prompts": {},
                },
                "serverInfo": {
                    "name": "math-intelligence-mcp",
                    "version": "2.1.0",
                },
            },
            "id": req_id,
        }

    # 4. JSON-RPC direto (ex.: method: "math_evaluate")
    return await mcp_core.process_request(req)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Iniciando MathForge MCP na porta {port}...")
    uvicorn.run(app, host=host, port=port)
