"""Math Intelligence MCP - Solucionador Simbólico

Módulo P1 - Tool: symbolic_solver
Resolve equações simbolicamente usando abordagens algebraicas.
"""

from typing import Dict, Any, List, Optional
import re
import cmath


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

        lhs, rhs = [s.strip() for s in clean_eq.split("=", 1)]

        # Mover tudo para um lado: lhs - rhs = 0
        # Para simplificar, substituímos rhs por 0 e ajustamos lhs
        adjusted_lhs = _move_rhs_to_lhs(lhs, rhs)

        # Determinar grau da equação
        degree = _determine_degree(adjusted_lhs, variable)

        result: Dict[str, Any] = {
            "success": True,
            "equation": equation,
            "adjusted_lhs": adjusted_lhs,
            "variable": variable,
            "degree": degree
        }

        if degree == 1:
            # Equação do 1º grau: ax + b = 0
            result.update(_solve_linear(adjusted_lhs, variable))
        elif degree == 2:
            # Equação do 2º grau: ax² + bx + c = 0
            result.update(_solve_quadratic(adjusted_lhs, variable))
        else:
            result["success"] = False
            result["error"] = f"Grau da equação {degree} não suportado ainda"

        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "equation": equation
        }


def _move_rhs_to_lhs(lhs: str, rhs: str) -> str:
    """Move termos do RHS para LHS mudando os sinais."""
    # Remover 'x' do RHS para mudar coeficientes
    # Exemplo: se rhs = "3x", vira "-3x" no LHS
    rhs_terms = re.findall(r'([+-]?\d*\*?x?\^?\d*)', rhs)

    adjusted = lhs
    for term in rhs_terms:
        sign = term[0] if term.startswith(('+', '-')) else '+'
        coeff_part = term.lstrip('+-')

        # Substituir no LHS com sinal invertido
        if sign == '+':
            adjusted = adjusted.replace('+ ' + coeff_part, f'- {coeff_part}')
            adjusted = adjusted.replace('+' + coeff_part, f'-{coeff_part}')
        else:
            adjusted = adjusted.replace('- ' + coeff_part, f'+ {coeff_part}')
            adjusted = adjusted.replace('-' + coeff_part, f'+{coeff_part}')

    return adjusted


def _determine_degree(expression: str, variable: str = "x") -> int:
    """Determina o grau máximo da equação."""
    # Procurar por x² ou x**2
    if re.search(r'x\^2|\*\*2', expression):
        return 2
    # Procurar apenas x (não elevado)
    if re.search(r'(?<!^|\*)x(?!^|\*)', expression):
        # Verificar se tem x² também
        if not re.search(r'x\^2|\*\*2', expression):
            return 1
    return 0


def _solve_linear(expression: str, variable: str = "x") -> Dict[str, Any]:
    """Resolve equação do 1º grau ax + b = 0."""
    try:
        # Extrair coeficiente de x
        x_match = re.search(r'([+-]?\d*\.?\*)?x', expression)
        if not x_match:
            return {"success": False, "solution": "Não foi possível encontrar x", "roots": [], "nature": "unknown"}

        coeff_str = x_match.group(1).replace('x', '').strip() or '1'
        try:
            a = float(coeff_str.replace('*', ''))
        except ValueError:
            a = 1.0

        # Extrair constante livre (termos sem x)
        const_match = re.search(r'([+-]?\d+)$', expression)
        const_str = const_match.group(1) if const_match else '0'
        try:
            b = float(const_str)
        except ValueError:
            b = 0.0

        if a == 0:
            return {
                "success": False,
                "solution": "Coeficiente a é zero (não é equação do 1º grau)",
                "roots": [],
                "nature": "invalid"
            }

        x = -b / a

        return {
            "success": True,
            "solution": f"x = {x}",
            "roots": [complex(x)],
            "nature": "unique_real" if x == int(x) and x.imag == 0 else "unique_complex"
        }

    except Exception as e:
        return {"success": False, "solution": str(e), "roots": [], "nature": "error"}


def _solve_quadratic(expression: str, variable: str = "x") -> Dict[str, Any]:
    """Resolve equação do 2º grau ax² + bx + c = 0 usando fórmula bhaskara."""
    try:
        # Extrair coeficientes

        # Coeficiente a (de x²)
        a_match = re.search(r'([+-]?\d*\.?\*)?x\^2|([+-]?\d*\.?\*)?x\*\*2', expression)
        if a_match:
            a_str = a_match.group(1) or a_match.group(2) or '1' or '1'
        else:
            a_str = '1' or '1'
        a_str = a_str.replace('x^2', '').replace('x**2', '').replace('*', '').strip()
        if not a_str or a_str in ['+', '-']:
            a_str = '1' if a_str in ['', '+'] else '-1'
        a = float(a_str) if a_str else 1.0

        # Coeficiente b (de x)
        b_match = re.search(r'([+-]?\d*\.?\*)?x(?!\\^2)', expression)
        b_str = b_match.group(1).replace('x', '').strip() if b_match else '0'
        if not b_str or b_str in ['+', '-']:
            b_str = '0'
        b = float(b_str) if b_str else 0.0

        # Coeficiente c (constante)
        c_match = re.search(r'([+-]?\d+)$', expression)
        c_str = c_match.group(1) if c_match else '0'
        c = float(c_str)

        # Calcular delta
        delta = b**2 - 4*a*c

        # Raiz quadrada do delta
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