"""Math Intelligence MCP - Ferramentas Disponíveis

Esta módulo contém todas as ferramentas (tools) expostas via protocolo MCP
JSON-RPC 2.0, organizadas pelos níveis P0 (essenciais), P1 (aprimoradas) e P2 (opcionais).
"""

from .mimcp_evaluate import evaluate_expression
from .math_explain import explain_concept
from .math_optimize import optimize_expression
from .result_verify import verify_result
from .memory_profile import profile_memory
from .precision_check import precision_check
from .distributed_job_submit import submit_distributed_job
from .distributed_job_status import get_distributed_job_status
from .distributed_job_result import get_distributed_job_result
from .formula_engine import solve_formula
from .symbolic_solver import solve_symbolically
from .calculus_operations import perform_calculus
from .linear_algebra import solve_linear_system
from .statistical_analysis import analyze_statistics
from .algorithm_profile import profile_algorithm
from .hardware_benchmark import run_hardware_benchmark
from .pattern_recognition import detect_period, find_local_extrema, symmetry_analysis

# 17 tools MathForge 2.1.0-REV: P0:2, P1:9, P2:6
TOOLS_AVAILABLE = {
    # P0 - Essenciais (2 tools)
    "math_evaluate": {
        "function": evaluate_expression,
        "description": "Avaliar expressões matemáticas com validação formal de AST e seleção explícita de precisão.",
        "params_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Expressão matemática para avaliar"},
                "mode": {"type": "string", "enum": ["FAST", "HIGH", "EXACT", "AUTO"], "default": "AUTO"},
                "precision_digits": {"type": "integer", "minimum": 1, "maximum": 1000, "default": 50}
            },
            "required": ["expression"]
        }
    },
    "result_verify": {
        "function": verify_result,
        "description": "Verificador rigoroso que distingue igualdade simbólica formal, verificação numérica aproximada e validade de domínio.",
        "params_schema": {
            "type": "object",
            "properties": {
                "candidate_solution": {"type": "string", "description": "Valor ou expressão candidata"},
                "original_equation": {"type": "string", "description": "Expressão de referência"},
                "verification_type": {"type": "string", "enum": ["symbolic", "numerical", "domain_check", "all"], "default": "all"},
                "tolerance": {"type": "number", "minimum": 0, "maximum": 1, "default": 1e-15}
            },
            "required": ["candidate_solution", "original_equation"]
        }
    },
    # P1 - Avançadas (9 tools)
    "math_explain": {
        "function": explain_concept,
        "description": "Explica a resolução do problema estruturadamente em LaTeX, separando resolução didática de demonstração axiomática.",
        "params_schema": {
            "type": "object",
            "properties": {
                "topic_or_problem": {"type": "string", "description": "Tema ou problema matemático"},
                "output_format": {"type": "string", "enum": ["step_by_step", "conceptual"], "default": "step_by_step"}
            },
            "required": ["topic_or_problem"]
        }
    },
    "math_optimize": {
        "function": optimize_expression,
        "description": "Simplificação e fatoração de expressões algébricas para sua forma canônica mínima.",
        "params_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Expressão para otimizar"},
                "strategy": {"type": "string", "enum": ["simplify", "factor", "expand", "trig_reduce"], "default": "simplify"}
            },
            "required": ["expression"]
        }
    },
    "symbolic_solver": {
        "function": solve_symbolically,
        "description": "Solucionador simbólico modular com separação interna entre resolvedores lineares, não-lineares e EDOs.",
        "params_schema": {
            "type": "object",
            "properties": {
                "equations": {"type": "array", "items": {"type": "string"}, "description": "Array de equações para resolver"},
                "variables": {"type": "array", "items": {"type": "string"}, "description": "Variáveis a resolver"},
                "domain": {"type": "string", "enum": ["real", "complex"], "default": "real"}
            },
            "required": ["equations", "variables"]
        }
    },
    "calculus_operations": {
        "function": perform_calculus,
        "description": "Derivação analítica, integração simbólica e numérica de alta precisão, limites e expansão em séries.",
        "params_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Expressão matemática"},
                "variable": {"type": "string", "description": "Variável para derivação/integração"},
                "operation": {"type": "string", "enum": ["diff", "integrate", "limit", "series"], "description": "Tipo de operação"},
                "point": {"type": "number", "description": "Ponto para derivada/limite em (ou None para geral)"},
                "order": {"type": "integer", "description": "Ordem da série de Taylor (se operation=series)"}
            },
            "required": ["expression", "variable", "operation"]
        }
    },
    "linear_algebra": {
        "function": solve_linear_system,
        "description": "Operações matriciais diferenciando matrizes exatas de matrizes de ponto flutuante aceleradas por BLAS/LAPACK.",
        "params_schema": {
            "type": "object",
            "properties": {
                "matrix_a": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}, "description": "Matriz de coeficientes"},
                "matrix_b": {"type": "array", "items": {"type": "number"}, "description": "Vetor de termos independentes (opcional)"},
                "operation": {"type": "string", "enum": ["det", "inv", "eig", "svd", "condition_number", "solve_system"], "description": "Operação matricial"}, "default": "solve_system"
            },
            "required": ["matrix_a"]
        }
    },
    "statistical_analysis": {
        "function": analyze_statistics,
        "description": "Estatística descritiva, inferência, regressões e testes de hipótese com cálculo de p-valor exato.",
        "params_schema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["descriptive", "normality_test", "correlation", "probability_distribution"], "description": "Tipo de operação"}, "default": "descriptive"
            },
            "required": ["operation"]
        }
    },
    "precision_check": {
        "function": precision_check,
        "description": "Executa o mesmo cálculo em múltiplos níveis de precisão (53 bits, 128 bits e N bits) para detectar cancelamento catastrófico, perda de dígitos significativos e convergência numérica.",
        "params_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Expressão para calcular"},
                "target_digits": {"type": "integer", "description": "Número de dígitos alvo"}
            },
            "required": ["expression"]
        }
    },
    "distributed_job_submit": {
        "function": submit_distributed_job,
        "description": "Submete cálculos massivos para enfileiramento durável no Redis e execução assíncrona.",
        "params_schema": {
            "type": "object",
            "properties": {
                "job_type": {"type": "string", "description": "Tipo de job"},
                "payload": {"type": "object", "description": "Payload do cálculo"},
                "priority": {"type": "integer", "minimum": 0, "maximum": 10, "default": 5},
                "max_execution_time_seconds": {"type": "integer", "minimum": 1, "description": "Timeout máximo em segundos"}
            },
            "required": ["job_type", "payload"]
        }
    },
    "distributed_job_result": {
        "function": get_distributed_job_result,
        "description": "Recupera o resultado final de um trabalho concluído, com suporte a paginação para saídas volumosas.",
        "params_schema": {
            "type": "object",
            "properties": {
                "job_id": {"type": "string", "description": "ID do job"},
                "page": {"type": "integer", "minimum": 1, "default": 1},
                "page_size": {"type": "integer", "minimum": 1, "default": 100}
            },
            "required": ["job_id"]
        }
    },
    # P2 - Especializadas (6 tools)
    "algorithm_profile": {
        "function": profile_algorithm,
        "description": "Avalia a complexidade assintótica teórica O(f(n)) e requisitos teóricos de memória para um algoritmo e dimensão de dados especificados.",
        "params_schema": {
            "type": "object",
            "properties": {
                "algorithm_name": {"type": "string", "description": "Nome do algoritmo"},
                "input_size_n": {"type": "integer", "description": "Tamanho de entrada n"}
            },
            "required": ["algorithm_name"]
        }
    },
    "hardware_benchmark": {
        "function": run_hardware_benchmark,
        "description": "Executa benchmarks empíricos reais no host local (GFLOPS de CPU, largura de banda de memória e latência de ponto flutuante).",
        "params_schema": {
            "type": "object",
            "properties": {
                "test_type": {"type": "string", "enum": ["cpu_flops", "memory_bandwidth", "mpfr_throughput"], "description": "Tipo de teste"}
            },
            "required": ["test_type"]
        }
    },
    "formula_engine": {
        "function": solve_formula,
        "description": "Catálogo curado de fórmulas científicas e financeiras com substituição formal e isolamento de incógnitas.",
        "params_schema": {
            "type": "object",
            "properties": {
                "formula_id": {"type": "string", "description": "ID da fórmula"},
                "substitutions": {"type": "object", "description": "Substituições de variáveis"},
                "solve_for": {"type": "string", "description": "Variável para resolver"}
            },
            "required": ["formula_id"]
        }
    },
    "pattern_recognition": {
        "function": detect_period,
        "description": "Detecção de padrões numéricos inteiros, relações de congruência modular e consulta estruturada a padrões da enciclopédia OEIS.",
        "params_schema": {
            "type": "object",
            "properties": {
                "sequence": {"type": "array", "items": {"type": "integer"}, "description": "Sequência numérica"},
                "predict_next_terms": {"type": "integer", "minimum": 1, "default": 3},
                "mode": {"type": "string", "enum": ["max", "min", "both"], "description": "Tipo de extrema", "default": "both"}
            },
            "required": ["sequence"]
        }
    },
    "distributed_job_status": {
        "function": get_distributed_job_status,
        "description": "Consulta o progresso percentual, worker atribuído, tempo decorrido e status do job.",
        "params_schema": {
            "type": "object",
            "properties": {
                "job_id": {"type": "string", "description": "ID do job consultado"}
            },
            "required": ["job_id"]
        }
    },
    "memory_profile": {
        "function": profile_memory,
        "description": "Perfilagem de memória e performance metrics.",
        "params_schema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "description": "Nome da operação being profilhada"},
                "duration_ms": {"type": "integer", "minimum": 0, "description": "Duração em milissegundos"},
                "memory_mb": {"type": "number", "minimum": 0, "description": "Memória usada em MB"}
            },
            "required": ["operation"]
        }
    }
}

def list_tools():
    """Retorna lista completa de tools disponíveis."""
    return TOOLS_AVAILABLE

def execute_tool(name: str, params: dict):
    """Executa uma tool específica pelo nome."""
    if name in TOOLS_AVAILABLE:
        tool = TOOLS_AVAILABLE[name]
        return tool["function"](**params)
    else:
        raise ValueError(f"Tool '{name}' não encontrada. Disponíveis: {list(TOOLS_AVAILABLE.keys())}")