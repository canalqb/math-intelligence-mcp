"""Math Intelligence MCP - Servidor MCP Principal

Servidor que expõe todas as tools via protocolo JSON-RPC 2.0 sobre STDIO.
Este é o ponto de entrada quando se executa `python -m mimcp`.
"""

import json
import sys
import asyncio
from typing import Dict, Any, Optional

from .mimcp_evaluate import evaluate_expression
from .math_explain import explain_concept
from .math_optimize import optimize_expression
from .result_verify import verify_result
from .memory_profile import profile_memory

# Tools P1 (serão adicionadas em fases posteriores)
FORMULA_ENGINE_AVAILABLE = True
SYMBOLIC_SOLVER_AVAILABLE = True
CALCULUS_AVAILABLE = True
LINEAR_ALGEBRA_AVAILABLE = True
STATISTICAL_AVAILABLE = True

# Tools P2 (opcionais)
ADVANCED_CRYPTO_AVAILABLE = True
PATTERN_RECOGNITION_AVAILABLE = True


class MCPServer:
    """Servidor MCP que processa requisições JSON-RPC 2.0 via STDIO."""
    
    def __init__(self):
        self.tools = self._register_tools()
    
    def _register_tools(self) -> Dict[str, Any]:
        """Registra todas as tools disponíveis."""
        return {
            # P0 - Essenciais (5 tools)
            "math_evaluate": {
                "function": self._handle_math_evaluate,
                "description": "Avaliar expressões matemáticas",
            },
            "math_explain": {
                "function": self._handle_math_explain,
                "description": "Explicar conceitos matemáticos",
            },
            "math_optimize": {
                "function": self._handle_math_optimize,
                "description": "Otimizar expressões algébricas",
            },
            "result_verify": {
                "function": self._handle_result_verify,
                "description": "Verificar resultados de cálculos",
            },
            "memory_profile": {
                "function": self._handle_memory_profile,
                "description": "Perfilagem de memória e performance",
            },
            # P1 - Aprimoradas (5 tools)
            "formula_engine": {
                "function": self._handle_formula_engine,
                "description": "Motor de fórmulas simbólicas",
            } if FORMULA_ENGINE_AVAILABLE else None,
            "symbolic_solver": {
                "function": self._handle_symbolic_solver,
                "description": "Solucionador simbólico",
            } if SYMBOLIC_SOLVER_AVAILABLE else None,
            "calculus_operations": {
                "function": self._handle_calculus_operations,
                "description": "Operações de cálculo",
            } if CALCULUS_AVAILABLE else None,
            "linear_algebra": {
                "function": self._handle_linear_algebra,
                "description": "Álgebra linear",
            } if LINEAR_ALGEBRA_AVAILABLE else None,
            "statistical_analysis": {
                "function": self._handle_statistical_analysis,
                "description": "Análise estatística",
            } if STATISTICAL_AVAILABLE else None,
            # P2 - Opcionais (2 tools)
            "advanced_cryptography": {
                "function": self._handle_advanced_cryptography,
                "description": "Criptografia avançada",
            } if ADVANCED_CRYPTO_AVAILABLE else None,
            "pattern_recognition": {
                "function": self._handle_pattern_recognition,
                "description": "Reconhecimento de padrões",
            } if PATTERN_RECOGNITION_AVAILABLE else None,
        }
    
    def _handle_math_evaluate(self, params: dict) -> dict:
        expression = params.get("expression", "")
        result = evaluate_expression(expression)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_math_explain(self, params: dict) -> dict:
        topic = params.get("topic", "")
        level = params.get("level", "basic")
        result = explain_concept(topic, level)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_math_optimize(self, params: dict) -> dict:
        expression = params.get("expression", "")
        result = optimize_expression(expression)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_result_verify(self, params: dict) -> dict:
        expression = params.get("expression", "")
        result = params.get("result", "")
        tolerance = params.get("tolerance", 0.001)
        result = verify_result(expression, result, tolerance)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_memory_profile(self, params: dict) -> dict:
        operation = params.get("operation", "")
        duration_ms = params.get("duration_ms", 0)
        memory_mb = params.get("memory_mb", 0)
        result = profile_memory(operation, duration_ms, memory_mb)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    # Handlers P1
    def _handle_formula_engine(self, params: dict) -> dict:
        formula = params.get("formula", "")
        # Placeholder - implementação futura
        return {
            "jsonrpc": "2.0",
            "result": {
                "success": True,
                "expression": formula,
                "note": "Funcionalidade P1 - próxima implementação",
                "provided_result": None
            },
            "id": params.get("id")
        }
    
    def _handle_symbolic_solver(self, params: dict) -> dict:
        equation = params.get("equation", "")
        return {
            "jsonrpc": "2.0",
            "result": {
                "success": True,
                "equation": equation,
                "note": "Funcionalidade P1 - próxima implementação",
                "solution": None
            },
            "id": params.get("id")
        }
    
    def _handle_calculus_operations(self, params: dict) -> dict:
        operation = params.get("operation", "")
        variable = params.get("variable", "x")
        return {
            "jsonrpc": "2.0",
            "result": {
                "success": True,
                "operation": operation,
                "variable": variable,
                "note": "Funcionalidade P1 - próxima implementação",
                "result": None
            },
            "id": params.get("id")
        }
    
    def _handle_linear_algebra(self, params: dict) -> dict:
        system = params.get("system", [])
        return {
            "jsonrpc": "2.0",
            "result": {
                "success": True,
                "system": system,
                "note": "Funcionalidade P1 - próxima implementação",
                "solution": None
            },
            "id": params.get("id")
        }
    
    def _handle_statistical_analysis(self, params: dict) -> dict:
        data = params.get("data", [])
        statistic = params.get("statistic", "mean")
        return {
            "jsonrpc": "2.0",
            "result": {
                "success": True,
                "data": data,
                "statistic": statistic,
                "note": "Funcionalidade P1 - próxima implementação",
                "value": None
            },
            "id": params.get("id")
        }
    
    # Handlers P2
    def _handle_advanced_cryptography(self, params: dict) -> dict:
        operation = params.get("operation", "")
        key = params.get("key", "")
        return {
            "jsonrpc": "2.0",
            "result": {
                "success": True,
                "operation": operation,
                "key": key,
                "note": "Funcionalidade P2 - próximas implementação (reimplementação Rust)",
                "output": None
            },
            "id": params.get("id")
        }
    
    def _handle_pattern_recognition(self, params: dict) -> dict:
        data = params.get("data", [])
        pattern_type = params.get("pattern_type", "general")
        return {
            "jsonrpc": "2.0",
            "result": {
                "success": True,
                "data": data,
                "pattern_type": pattern_type,
                "note": "Funcionalidade P2 - próxima implementação",
                "patterns_found": []
            },
            "id": params.get("id")
        }
    
    async def process_request(self, request: dict) -> dict:
        """Processa uma requisição JSON-RPC 2.0."""
        try:
            method = request.get("method", "")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method not in self.tools:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Método não encontrado: {method}",
                        "data": {"available_methods": list(self.tools.keys())}
                    },
                    "id": request_id
                }
            
            tool_info = self.tools[method]
            if tool_info is None:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32602,
                        "message": f"Tool {method} temporarily unavailable"
                    },
                    "id": request_id
                }
            
            result = await tool_info["function"](params)
            return {"jsonrpc": "2.0", "result": result, "id": request_id}
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": "Erro interno do servidor",
                    "data": {"error": str(e)}
                },
                "id": request_id
            }
    
    def run_stdio(self) -> None:
        """Rodar servidor em modo STDIO (stdin/stdout)."""
        print("Math Intelligence MCP Server - inicializado via STDIO", file=sys.stderr)
        sys.stderr.flush()
        
        while True:
            try:
                # Ler linha do stdin
                line = sys.stdin.readline()
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Parsear JSON
                try:
                    request = json.loads(line)
                except json.JSONDecodeError as e:
                    print(
                        json.dumps({
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32700,
                                "message": f"Parse error: {str(e)}"
                            },
                            "id": None
                        }),
                        file=sys.stdout
                    )
                    sys.stdout.flush()
                    continue
                
                # Processar requisição
                response = asyncio.run(self.process_request(request))
                
                # Retornar resposta
                print(json.dumps(response), file=sys.stdout)
                sys.stdout.flush()
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(
                    json.dumps({
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32603,
                            "message": f"Erro fatal: {str(e)}"
                        },
                        "id": None
                    }),
                    file=sys.stdout
                )
                sys.stdout.flush()


def main():
    """Ponto de entrada principal."""
    server = MCPServer()
    server.run_stdio()


if __name__ == "__main__":
    main()