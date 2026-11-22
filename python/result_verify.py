"""Math Intelligence MCP - Verificar Resultados

Módulo P0 - Tool: result_verify
Verifica se um resultado de cálculo está correto dentro de uma tolerância.
"""

from typing import Dict, Any, Optional
import math


def verify_result(expression: str, result: str, tolerance: float = 0.001) -> Dict[str, Any]:
    """Verifica se um resultado de cálculo está correto.
    
    Recalcula a expressão e compara com o resultado fornecido,
    considerando uma tolerância percentual.
    
    Args:
        expression: Expressão original (ex: "2 + 2 * 3")
        result: Resultado fornecido como string (ex: "8")
        tolerance: Tolerância percentual para aceitação (padrão: 0.001 = 0.1%)
    
    Returns:
        Dict com success, verified, computed_result, provided_result, error (se houver)
    """
    try:
        # Avaliar a expressão original
        eval_result = evaluate_expression(expression)
        
        if not eval_result["success"]:
            return {
                "success": False,
                "error": f"Não foi possível avaliar a expressão: {eval_result.get('error')}",
                "expression": expression,
                "provided_result": result,
                "verified": False
            }
        
        computed = eval_result["data"]
        
        # Tentar converter o resultado fornecido para número
        try:
            provided = float(result)
        except (ValueError, TypeError):
            return {
                "success": False,
                "error": f"Resultado fornecido inválido: '{result}' não é um número",
                "expression": expression,
                "provided_result": result,
                "verified": False
            }
        
        # Calcular percentual de erro
        if abs(computed) > 1e-10:  # Evitar divisão por zero
            percent_error = abs((computed - provided) / computed) * 100
        else:
            # Quando o resultado esperado é 0
            percent_error = abs(computed - provided) * 100
        
        # Verificar dentro da tolerância
        is_within_tolerance = percent_error <= (tolerance * 100)
        
        return {
            "success": True,
            "verified": is_within_tolerance,
            "computed_result": computed,
            "provided_result": provided,
            "percent_error": round(percent_error, 4),
            "tolerance_percent": round(tolerance * 100, 2),
            "expression": expression,
            "within_tolerance": is_within_tolerance
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression,
            "provided_result": result,
            "verified": False
        }