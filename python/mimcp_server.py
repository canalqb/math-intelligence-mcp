"""Math Intelligence MCP - Servidor MCP Principal

Servidor que expõe todas as tools via protocolo JSON-RPC 2.0 sobre STDIO.
Este é o ponto de entrada quando se executa `python -m mimcp`.
"""

import json
import sys
import asyncio
from typing import Dict, Any, Optional, Union


def json_serializable(obj: Any) -> Any:
    """Converte objetos não serializáveis para tipos JSON-compatíveis."""
    if isinstance(obj, complex):
        return {"__complex__": True, "real": obj.real, "imag": obj.imag}
    if isinstance(obj, (set, frozenset)):
        return list(obj)
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return str(obj)


def json_dumps_safe(obj: Any) -> str:
    """JSON dumps com suporte a tipos customizados."""
    return json.dumps(obj, default=json_serializable, ensure_ascii=True)

# Importações dos módulos de tools
from .mimcp_evaluate import evaluate_expression
from .math_explain import explain_concept
from .math_optimize import optimize_expression
from .result_verify import verify_result
from .memory_profile import profile_memory
from .formula_engine import solve_formula
from .symbolic_solver import solve_symbolically
from .calculus_operations import perform_calculus
from .linear_algebra import solve_linear_system
from .statistical_analysis import analyze_statistics
from .precision_check import precision_check
from .algorithm_profile import profile_algorithm
from .hardware_benchmark import run_hardware_benchmark
from .pattern_recognition import detect_period, find_local_extrema, symmetry_analysis
from .distributed_job_submit import submit_distributed_job
from .distributed_job_status import get_distributed_job_status
from .distributed_job_result import get_distributed_job_result
from .advanced_cryptography import advanced_crypto_operation


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
                "description": "Avaliar expressões matemáticas com validação formal de AST e seleção explícita de precisão",
            },
            "math_explain": {
                "function": self._handle_math_explain,
                "description": "Explicar conceitos matemáticos didaticamente",
            },
            "math_optimize": {
                "function": self._handle_math_optimize,
                "description": "Otimizar expressões algébricas",
            },
            "result_verify": {
                "function": self._handle_result_verify,
                "description": "Verificar resultados de cálculos com tolerância",
            },
            "memory_profile": {
                "function": self._handle_memory_profile,
                "description": "Perfilagem de memória e performance",
            },
            # P1 - Avançadas (9 tools)
            "formula_engine": {
                "function": self._handle_formula_engine,
                "description": "Motor de fórmulas simbólicas - catálogo curado de fórmulas científicas e financeiras",
            },
            "symbolic_solver": {
                "function": self._handle_symbolic_solver,
                "description": "Solucionador simbólico modular para equações lineares, não-lineares e EDOs",
            },
            "calculus_operations": {
                "function": self._handle_calculus_operations,
                "description": "Operações de cálculo: derivadas, integrais, limites e séries",
            },
            "linear_algebra": {
                "function": self._handle_linear_algebra,
                "description": "Álgebra linear: determinante, inversa, autovalores, SVD, resolver sistemas",
            },
            "statistical_analysis": {
                "function": self._handle_statistical_analysis,
                "description": "Análise estatística descritiva, inferência, regressão e testes de hipótese",
            },
            "precision_check": {
                "function": self._handle_precision_check,
                "description": "Verificação de precisão multi-nível para detectar cancelamento catastrófico",
            },
            "distributed_job_submit": {
                "function": self._handle_distributed_job_submit,
                "description": "Submeter jobs de cálculo massivo para execução assíncrona",
            },
            "distributed_job_status": {
                "function": self._handle_distributed_job_status,
                "description": "Consultar status de job distribuído",
            },
            "distributed_job_result": {
                "function": self._handle_distributed_job_result,
                "description": "Recuperar resultado de job distribuído concluído",
            },
            # P2 - Especializadas (6 tools)
            "algorithm_profile": {
                "function": self._handle_algorithm_profile,
                "description": "Perfil teórico de complexidade assintótica e requisitos de memória",
            },
            "hardware_benchmark": {
                "function": self._handle_hardware_benchmark,
                "description": "Benchmarks empíricos reais: GFLOPS CPU, largura de banda memória, throughput MPFR",
            },
            "pattern_recognition": {
                "function": self._handle_pattern_recognition,
                "description": "Reconhecimento de padrões: detecção de período, extremos locais, simetria",
            },
            "advanced_cryptography": {
                "function": self._handle_advanced_cryptography,
                "description": "Criptografia avançada: exponenciação modular, logaritmo discreto",
            },
        }
    
    # ==================== Handlers P0 ====================
    
    def _handle_math_evaluate(self, params: dict) -> dict:
        expression = params.get("expression", "")
        mode = params.get("mode", "AUTO")
        precision_digits = params.get("precision_digits", 50)
        result = evaluate_expression(expression)
        # Adicionar campos extras se necessário
        if isinstance(result, dict):
            result["mode"] = mode
            result["precision_digits"] = precision_digits
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_math_explain(self, params: dict) -> dict:
        topic = params.get("topic_or_problem", params.get("topic", ""))
        level = params.get("level", params.get("output_format", "basic"))
        result = explain_concept(topic, level)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_math_optimize(self, params: dict) -> dict:
        expression = params.get("expression", "")
        strategy = params.get("strategy", "simplify")
        result = optimize_expression(expression)
        if isinstance(result, dict):
            result["strategy"] = strategy
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_result_verify(self, params: dict) -> dict:
        expression = params.get("original_equation", params.get("expression", ""))
        result_val = params.get("candidate_solution", params.get("result", ""))
        tolerance = params.get("tolerance", 0.001)
        verification_type = params.get("verification_type", "all")
        result = verify_result(expression, result_val, tolerance)
        if isinstance(result, dict):
            result["verification_type"] = verification_type
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_memory_profile(self, params: dict) -> dict:
        operation = params.get("operation", "")
        duration_ms = params.get("duration_ms", 0)
        memory_mb = params.get("memory_mb", 0)
        result = profile_memory(operation, duration_ms, memory_mb)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    # ==================== Handlers P1 ====================
    
    def _handle_formula_engine(self, params: dict) -> dict:
        formula_id = params.get("formula_id", "")
        substitutions = params.get("substitutions", {})
        solve_for = params.get("solve_for", "")
        result = solve_formula(formula_id, substitutions, solve_for)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_symbolic_solver(self, params: dict) -> dict:
        equations = params.get("equations", [])
        variables = params.get("variables", [])
        domain = params.get("domain", "real")
        
        # Se for uma única equação, usar solve_symbolically
        if len(equations) == 1 and len(variables) == 1:
            result = solve_symbolically(equations[0], variables[0])
        else:
            # Para sistemas, usar uma abordagem simplificada
            result = {
                "success": False,
                "error": "Sistemas de múltiplas equações não implementados ainda. Use uma equação por vez.",
                "equations": equations,
                "variables": variables
            }
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_calculus_operations(self, params: dict) -> dict:
        expression = params.get("expression", "")
        variable = params.get("variable", "x")
        operation = params.get("operation", "diff")
        point = params.get("point")
        order = params.get("order")
        result = perform_calculus(expression, variable, operation, point, order)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_linear_algebra(self, params: dict) -> dict:
        # Suporte a duas interfaces: matriz A/B ou lista de equações
        if "equations" in params:
            equations = params.get("equations", [])
            variables = params.get("variables")
            result = solve_linear_system(equations, variables)
        elif "matrix_a" in params:
            # Converter matrizes para equações
            matrix_a = params.get("matrix_a", [])
            matrix_b = params.get("matrix_b", [])
            # Gerar variáveis x0, x1, ...
            n = len(matrix_a)
            variables = [f"x{i}" for i in range(n)]
            equations = []
            for i in range(n):
                lhs_terms = []
                for j in range(n):
                    coeff = matrix_a[i][j]
                    if coeff != 0:
                        if coeff == 1:
                            lhs_terms.append(f"{variables[j]}")
                        elif coeff == -1:
                            lhs_terms.append(f"-{variables[j]}")
                        else:
                            lhs_terms.append(f"{coeff}*{variables[j]}")
                lhs = " + ".join(lhs_terms).replace("+ -", "- ")
                rhs = str(matrix_b[i]) if i < len(matrix_b) else "0"
                equations.append(f"{lhs} = {rhs}")
            result = solve_linear_system(equations, variables)
        else:
            result = {"success": False, "error": "Forneça 'equations' e 'variables' ou 'matrix_a' e 'matrix_b'"}
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_statistical_analysis(self, params: dict) -> dict:
        data = params.get("data", [])
        operation = params.get("operation", "descriptive")
        statistic = params.get("statistic", "mean")
        # Mapear parâmetros
        if "statistic" in params and "operation" not in params:
            operation = statistic
        result = analyze_statistics(operation, data)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_precision_check(self, params: dict) -> dict:
        expression = params.get("expression", "")
        target_digits = params.get("target_digits", 50)
        result = precision_check(expression, target_digits)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_distributed_job_submit(self, params: dict) -> dict:
        job_type = params.get("job_type", "")
        payload = params.get("payload", {})
        priority = params.get("priority", 5)
        max_execution_time_seconds = params.get("max_execution_time_seconds", 300)
        result = submit_distributed_job(job_type, payload, priority, max_execution_time_seconds)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_distributed_job_status(self, params: dict) -> dict:
        job_id = params.get("job_id", "")
        result = get_distributed_job_status(job_id)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_distributed_job_result(self, params: dict) -> dict:
        job_id = params.get("job_id", "")
        page = params.get("page", 1)
        page_size = params.get("page_size", 100)
        result = get_distributed_job_result(job_id, page, page_size)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    # ==================== Handlers P2 ====================
    
    def _handle_algorithm_profile(self, params: dict) -> dict:
        algorithm_name = params.get("algorithm_name", "")
        input_size_n = params.get("input_size_n", 1000)
        result = profile_algorithm(algorithm_name, input_size_n)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_hardware_benchmark(self, params: dict) -> dict:
        test_type = params.get("test_type", "cpu_flops")
        result = run_hardware_benchmark(test_type)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_pattern_recognition(self, params: dict) -> dict:
        sequence = params.get("sequence", [])
        predict_next_terms = params.get("predict_next_terms", 3)
        mode = params.get("mode", "both")
        # Usar detect_period como função principal
        result = detect_period(sequence, predict_next_terms)
        # Adicionar análise de extrema e simetria
        extrema = find_local_extrema(sequence)
        symmetry = symmetry_analysis(sequence)
        if isinstance(result, dict) and result.get("success"):
            result["extrema"] = extrema
            result["symmetry"] = symmetry
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    def _handle_advanced_cryptography(self, params: dict) -> dict:
        operation = params.get("operation", "")
        key = params.get("key", "")
        # Parâmetros adicionais
        base = params.get("base")
        exponent = params.get("exponent")
        modulus = params.get("modulus")
        result = advanced_crypto_operation(operation, key, base, exponent, modulus)
        return {"jsonrpc": "2.0", "result": result, "id": params.get("id")}
    
    # ==================== Processamento de Requisições ====================
    
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
            
            func = tool_info["function"]
            if asyncio.iscoroutinefunction(func):
                res = await func(params)
            else:
                res = func(params)

            if isinstance(res, dict) and "jsonrpc" in res:
                res["id"] = request_id
                return res
            return {"jsonrpc": "2.0", "result": res, "id": request_id}
            
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
                        json_dumps_safe({
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
                print(json_dumps_safe(response), file=sys.stdout)
                sys.stdout.flush()
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(
                    json_dumps_safe({
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