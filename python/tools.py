"""Math Intelligence MCP - Ferramentas Disponíveis

Esta módulo contém todas as ferramentas (tools) expostas via protocolo MCP
JSON-RPC 2.0, organizadas pelos níveis P0 (essenciais), P1 (aprimoradas) e P2 (opcionais).
"""

from .mimcp_evaluate import evaluate_expression
from .math_explain import explain_concept
from .math_optimize import optimize_expression
from .result_verify import verify_result
from .memory_profile import profile_memory

# Nível P1 - Ferramentas Aprimoradas
from .formula_engine import solve_formula
from .symbolic_solver import solve_symbolically
from .calculus_operations import perform_calculus
from .linear_algebra import solve_linear_system
from .statistical_analysis import analyze_statistics

# Nível P2 - Ferramentas Opcionais
from .advanced_cryptography import modular_exponentiation, discrete_logarithm, hash_data, rsa_key_generation
from .pattern_recognition import detect_period, find_local_extrema, symmetry_analysis

# Lista completa de tools disponíveis
TOOLS_AVAILABLE = {
    # P0 - Essenciais (5 tools)
    "math_evaluate": {
        "function": evaluate_expression,
        "description": "Avaliar expressões matemáticas",
        "params_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Expressão matemática para avaliar"}
            },
            "required": ["expression"]
        }
    },
    "math_explain": {
        "function": explain_concept,
        "description": "Explicar conceitos matemáticos",
        "params_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "Tema matemático"},
                "level": {"type": "string", "enum": ["basic", "intermediate", "advanced"], "default": "basic"}
            },
            "required": ["topic"]
        }
    },
    "math_optimize": {
        "function": optimize_expression,
        "description": "Otimizar expressões algébricas",
        "params_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Expressão para otimizar"}
            },
            "required": ["expression"]
        }
    },
    "result_verify": {
        "function": verify_result,
        "description": "Verificar resultados de cálculos",
        "params_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Expressão original"},
                "result": {"type": "string", "description": "Resultado a ser verificado"},
                "tolerance": {"type": "number", "minimum": 0, "maximum": 1, "default": 0.001}
            },
            "required": ["expression", "result"]
        }
    },
    "memory_profile": {
        "function": profile_memory,
        "description": "Perfilagem de memória e performance",
        "params_schema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "description": "Nome da operação being profilhada"},
                "duration_ms": {"type": "integer", "minimum": 0, "description": "Duração em milissegundos"},
                "memory_mb": {"type": "number", "minimum": 0, "description": "Memória usada em MB"}
            },
            "required": ["operation"]
        }
    },
    # P1 - Aprimoradas (9 tools)
    "formula_engine": {
        "function": solve_formula,
        "description": "Motor de fórmulas simbólicas",
        "params_schema": {
            "type": "object",
            "properties": {
                "formula": {"type": "string", "description": "Fórmula algébrica"},
                "variables": {"type": "array", "items": {"type": "string"}, "description": "Variáveis da fórmula"}
            },
            "required": ["formula"]
        }
    },
    "symbolic_solver": {
        "function": solve_symbolically,
        "description": "Resolver equações simbolicamente",
        "params_schema": {
            "type": "object",
            "properties": {
                "equation": {"type": "string", "description": "Equação para resolver"},
                "variable": {"type": "string", "description": "Variável a resolver"}
            },
            "required": ["equation"]
        }
    },
    "calculus_operations": {
        "function": perform_calculus,
        "description": "Cálculo: derivadas, integrais e limites",
        "params_schema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["derivative", "integral", "limit"], "description": "Tipo de operação"},
                "expression": {"type": "string", "description": "Expressão matemática"},
                "variable": {"type": "string", "description": "Variável para derivação/integração"},
                "point": {"type": "number", "description": "Ponto para derivada em (ou None para geral)"}
            },
            "required": ["operation", "expression"]
        }
    },
    "linear_algebra": {
        "function": solve_linear_system,
        "description": "Álgebra linear: sistemas de equações e matrizes",
        "params_schema": {
            "type": "object",
            "properties": {
                "system": {"type": "array", "items": {"type": "array", "items": {"type": "number"}, "description": "Sistema de equações lineares"}, "description": "Matriz aumentada do sistema"},
                "method": {"type": "string", "enum": ["gaussian", "cramer", "matrix_inverse"], "description": "Método de resolução"}, "default": "gaussian"
            },
            "required": ["system"]
        }
    },
    "statistical_analysis": {
        "function": analyze_statistics,
        "description": "Análise estatística descritiva e distribuições",
        "params_schema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["descriptive", "normality_test", "correlation", "probability_distribution"], "description": "Tipo de operação"}, "default": "descriptive"
            },
            "required": ["operation"]
        }
    },
    # P2 - Opcionais (4 tools)
    "advanced_cryptography": {
        "function": modular_exponentiation,
        "description": "Criptografia avançada: exponenciação modular e logaritmo discreto",
        "params_schema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["modular_exponentiation", "discrete_logarithm", "hash", "rsa_key_gen"], "description": "Operação criptográfica"},
                "base": {"type": "integer", "description": "Base para exponenciação"},
                "exponent": {"type": "integer", "description": "Expoente"},
                "modulus": {"type": "integer", "description": "Modulus (primo)"},
                "g": {"type": "integer", "description": "Base para logaritmo discreto"},
                "h": {"type": "integer", "description": "Resultado para logaritmo discreto"},
                "data": {"type": "string", "description": "Dados para hash"},
                "bits": {"type": "integer", "description": "Tamanho em bits para RSA"}
            },
            "required": ["operation"]
        }
    },
    "pattern_recognition": {
        "function": detect_period,
        "description": "Reconhecimento de padrões em sequências",
        "params_schema": {
            "type": "object",
            "properties": {
                "sequence": {"type": "array", "items": {"type": "number"}, "description": "Sequência numérica"},
                "max_lag": {"type": "integer", "description": "Lag máximo para busca"},
                "mode": {"type": "string", "enum": ["max", "min", "both"], "description": "Tipo de extrema", "default": "both"}
            },
            "required": ["sequence"]
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