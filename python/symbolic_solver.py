"""Math Intelligence MCP - Solucionador Simbólico

Módulo P1 - Tool: symbolic_solver
Resolve equações simbolicamente usando abordagens algebraicas.
"""

from typing import Dict, Any, List, Optional
import sympy as sp


def solve_symbolically(equation: str, variable: str = "x") -> Dict[str, Any]:
    """Resolve uma equação equacional simbolicamente.

    Suporta:
    - Equações do 1º grau (ax + b = 0)
    - Equações do 2º grau (ax² + bx + c = 0)
    - Sistemas de 2 equações lineares

    Args:
        equation: Equação como string (ex: "x**2 + 2*x + 1 = 0")
        variable: Variável a resolver (padrão: "x")

    Returns:
        Dict com success, roots, steps, discriminant, nature
    """
    try:
        clean_eq = equation.strip()

        # Dividir em lhs e rhs
        if "=" not in clean_eq:
            return {
                "success": False,
                "error": "Equação deve conter sinal de igual (=)",
                "equation": equation
            }

        lhs_str, rhs_str = [s.strip() for s in clean_eq.split("=", 1)]

        # Usar sympy para mover tudo para um lado: lhs - rhs = 0
        x = sp.Symbol(variable)
        lhs_expr = sp.sympify(lhs_str)
        rhs_expr = sp.sympify(rhs_str)
        
        # Equação ajustada: lhs - rhs = 0
        adjusted_expr = sp.simplify(lhs_expr - rhs_expr)
        adjusted_lhs = str(adjusted_expr)

        # Determinar grau da equação
        degree = _determine_degree(adjusted_expr, variable)

        result: Dict[str, Any] = {
            "success": True,
            "equation": equation,
            "adjusted_lhs": adjusted_lhs,
            "variable": variable,
            "degree": degree
        }

        if degree == 1:
            # Equação do 1º grau: ax + b = 0
            result.update(_solve_linear(adjusted_expr, variable))
        elif degree == 2:
            # Equação do 2º grau: ax² + bx + c = 0
            result.update(_solve_quadratic(adjusted_expr, variable))
        else:
            result["success"] = False
            result["error"] = f"Grau da equação {degree} não suportado ainda"

        return result

    except sp.SympyError as e:
        return {
            "success": False,
            "error": f"Erro de sintaxe simbólica: {str(e)}",
            "equation": equation
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "equation": equation
        }


def _determine_degree(expression: sp.Expr, variable: str = "x") -> int:
    """Determina o grau máximo da equação."""
    x = sp.Symbol(variable)
    try:
        return sp.Poly(expression, x).degree()
    except Exception:
        return 0


def _solve_linear(expression: sp.Expr, variable: str = "x") -> Dict[str, Any]:
    """Resolve equação do 1º grau ax + b = 0."""
    try:
        x = sp.Symbol(variable)
        poly = sp.Poly(expression, x)
        
        if poly.degree() != 1:
            return {"success": False, "solution": "Não é equação do 1º grau", "roots": [], "nature": "invalid"}
        
        coeffs = poly.all_coeffs()
        a = float(coeffs[0])
        b = float(coeffs[1])

        if a == 0:
            return {
                "success": False,
                "solution": "Coeficiente a é zero (não é equação do 1º grau)",
                "roots": [],
                "nature": "invalid"
            }

        x_val = -b / a
        root = complex(x_val)

        return {
            "success": True,
            "solution": f"x = {x_val}",
            "roots": [root],
            "nature": "unique_real" if x_val == int(x_val) and root.imag == 0 else "unique_complex"
        }

    except Exception as e:
        return {"success": False, "solution": str(e), "roots": [], "nature": "error"}


def _solve_quadratic(expression: sp.Expr, variable: str = "x") -> Dict[str, Any]:
    """Resolve equação do 2º grau ax² + bx + c = 0 usando fórmula de Bhaskara."""
    try:
        x = sp.Symbol(variable)
        poly = sp.Poly(expression, x)
        
        if poly.degree() != 2:
            return {"success": False, "solution": "Não é equação do 2º grau", "roots": [], "nature": "invalid"}

        coeffs = poly.all_coeffs()
        a = float(coeffs[0])
        b = float(coeffs[1])
        c = float(coeffs[2])

        # Calcular delta
        delta = b**2 - 4*a*c

        # Raiz quadrada do delta (pode ser complexo)
        import cmath
        sqrt_delta = cmath.sqrt(delta)

        # Duas raízes
        x1 = (-b + sqrt_delta) / (2*a)
        x2 = (-b - sqrt_delta) / (2*a)

        # Determinar natureza
        if delta > 0:
            nature = "real_and_distinct"
        elif delta == 0:
            nature = "real_and_equal"
        else:
            nature = "complex_conjugates"

        return {
            "success": True,
            "solution": f"x' = {x1}, x'' = {x2}",
            "roots": [complex(x1), complex(x2)],
            "discriminant": delta,
            "nature": nature,
            "formula": "Bhaskara: x = (-b ± √Δ) / 2a"
        }

    except Exception as e:
        return {"success": False, "error": str(e), "roots": [], "nature": "error"}


def solve_system(equations: List[str], variables: List[str]) -> Dict[str, Any]:
    """Resolve um sistema de equações lineares.
    
    Args:
        equations: Lista de equações (ex: ["2*x + 3*y = 5", "x - y = 1"])
        variables: Lista de variáveis (ex: ["x", "y"])
    
    Returns:
        Dict com success, solutions, steps
    """
    try:
        if len(equations) != len(variables):
            return {
                "success": False,
                "error": "Número de equações deve igualar número de variáveis",
                "equations": equations,
                "variables": variables
            }

        sym_vars = [sp.Symbol(v) for v in variables]
        eq_objects = []
        
        for eq_str in equations:
            if "=" not in eq_str:
                return {"success": False, "error": f"Equação inválida: {eq_str}", "equations": equations}
            lhs_str, rhs_str = [s.strip() for s in eq_str.split("=", 1)]
            lhs_expr = sp.sympify(lhs_str)
            rhs_expr = sp.sympify(rhs_str)
            eq_objects.append(sp.Eq(lhs_expr, rhs_expr))

        solution = sp.solve(eq_objects, sym_vars, dict=True)
        
        if not solution:
            return {
                "success": False,
                "error": "Sistema sem solução ou indeterminado",
                "equations": equations,
                "variables": variables
            }

        # Formatar soluções
        formatted_solution = {}
        for sol in solution:
            for var, val in sol.items():
                formatted_solution[str(var)] = complex(val) if isinstance(val, (int, float, complex)) else str(val)

        return {
            "success": True,
            "equations": equations,
            "variables": variables,
            "solutions": [formatted_solution],
            "method": "symbolic_gaussian_elimination"
        }

    except sp.SympyError as e:
        return {
            "success": False,
            "error": f"Erro de sintaxe simbólica: {str(e)}",
            "equations": equations
        }
    except Exception as e:
        return {"success": False, "error": str(e), "equations": equations}