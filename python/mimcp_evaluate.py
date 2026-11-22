"""Math Intelligence MCP - Avaliar Expressões Matemáticas

Módulo P0 - Tool: math_evaluate
Avalia expressões matemáticas simples e retorna o resultado.
"""

import re
import json
from typing import Dict, Any, Optional


def evaluate_expression(expression: str) -> Dict[str, Any]:
    """Avalia uma expressão matemática e retorna o resultado estruturado.

    Suporta operações básicas: +, -, *, /, ** (exponenciação), parênteses.
    Ordem de operações padrão aplicada.

    Args:
        expression: Expressão matemática como string (ex: "2 + 2 * 3")

    Returns:
        Dict com success, data (resultado), expression e evaluated_at
    """
    try:
        # Limpeza básica da expressão
        clean_expr = expression.strip()

        # Validar que apenas caracteres matemáticos estão presentes
        # Apenas dígitos, espaços, operadores básicos e parênteses
        if not re.match(r'^[\d\s\+\\-\*\/\(\)\.]+$', clean_expr):
            return {
                "success": False,
                "error": "Expressão contém caracteres inválidos",
                "expression": clean_expr
            }

        # Substituir ^ por ** para exponenciação Python
        python_expr = clean_expr.replace('^', '**')

        # Avaliar em ambiente seguro (sem builtins)
        result = eval(python_expr, {"__builtins__": {}}, {})

        return {
            "success": True,
            "data": float(result) if isinstance(result, (int, float)) else result,
            "expression": clean_expr,
            "evaluated_at": __import__('datetime').datetime.utcnow().isoformat() + "Z"
        }

    except ZeroDivisionError:
        return {
            "success": False,
            "error": "Divisão por zero",
            "expression": clean_expr
        }
    except SyntaxError:
        return {
            "success": False,
            "error": "Sintaxe inválida na expressão",
            "expression": clean_expr
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": clean_expr
        }