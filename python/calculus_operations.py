"""Math Intelligence MCP - Operações de Cálculo

Módulo P1 - Tool: calculus_operations
Derivadas, integrais e limites simbólicos básicos.
"""

from typing import Dict, Any, Optional
import sympy as sp


def differentiate(expression: str, variable: str = "x") -> Dict[str, Any]:
    """Calcula a derivada de uma expressão matemática.
    
    Args:
        expression: Expressão matemática (ex: "x**2 + 3*x + 2")
        variable: Variável de diferenciação (padrão: "x")
    
    Returns:
        Dict com success, derivative, steps, point (se especificado)
    """
    try:
        x = sp.Symbol(variable)
        expr = sp.sympify(expression)
        
        # Calcular derivada
        deriv = sp.diff(expr, x)
        
        result: Dict[str, Any] = {
            "success": True,
            "expression": expression,
            "variable": variable,
            "derivative": sp.simplify(deriv),
            "derivative_latex": sp.latex(deriv),
        }
        
        return result
        
    except sp.SympyError as e:
        return {
            "success": False,
            "error": f"Erro de sintaxe simbólica: {str(e)}",
            "expression": expression
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression
        }


def integrate(expression: str, variable: str = "x", definite: bool = False,
              lower_limit: Optional[float] = None, upper_limit: Optional[float] = None) -> Dict[str, Any]:
    """Calcula a integral de uma expressão matemática.
    
    Args:
        expression: Expressão matemática
        variable: Variável de integração (padrão: "x")
        definite: Se True, calcula integral definida
        lower_limit: Limite inferior (para integral definida)
        upper_limit: Limite superior (para integral definida)
    
    Returns:
        Dict com success, integral, steps
    """
    try:
        x = sp.Symbol(variable)
        expr = sp.sympify(expression)
        
        if definite:
            if lower_limit is None or upper_limit is None:
                return {
                    "success": False,
                    "error": "Integral definida requer lower_limit e upper_limit",
                    "expression": expression
                }
            
            # Integral definida
            result = sp.integrate(expr, (x, lower_limit, upper_limit))
            
            return {
                "success": True,
                "expression": expression,
                "variable": variable,
                "definite_integral": sp.simplify(result),
                "integral_latex": sp.latex(result),
                "lower_limit": lower_limit,
                "upper_limit": upper_limit,
                "type": "definite"
            }
        else:
            # Integral indefinida
            result = sp.integrate(expr, x)
            
            return {
                "success": True,
                "expression": expression,
                "variable": variable,
                "indefinite_integral": sp.simplify(result),
                "integral_latex": sp.latex(result),
                "+ C": True,
                "type": "indefinite"
            }
            
    except sp.SympyError as e:
        return {
            "success": False,
            "error": f"Erro de sintaxe simbólica: {str(e)}",
            "expression": expression
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression
        }


def limit(expression: str, variable: str = "x", point: Optional[float] = None,
          direction: str = "two-sided") -> Dict[str, Any]:
    """Calcula limite de uma expressão.
    
    Args:
        expression: Expressão matemática
        variable: Variável (padrão: "x")
        point: Ponto do limite (ex: 0, float('inf'))
        direction: "two-sided", "from_left", "from_right"
    
    Returns:
        Dict com success, limit_value
    """
    try:
        x = sp.Symbol(variable)
        expr = sp.sympify(expression)
        
        if point is None:
            return {
                "success": False,
                "error": "Limite requer um ponto de avaliação",
                "expression": expression
            }
        
        # Calcular limite
        lim = sp.limit(expr, x, point)
        
        result: Dict[str, Any] = {
            "success": True,
            "expression": expression,
            "variable": variable,
            "point": point,
            "limit": sp.simplify(lim),
            "limit_latex": sp.latex(lim),
            "direction": direction,
        }
        
        return result
        
    except sp.SympyError as e:
        return {
            "success": False,
            "error": f"Erro de sintaxe simbólica: {str(e)}",
            "expression": expression
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression
        }