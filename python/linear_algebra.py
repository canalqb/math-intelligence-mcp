"""Math Intelligence MCP - Álgebra Linear

Módulo P1 - Tool: linear_algebra
Solução de sistemas lineares, operações com matrizes, valores e vetores.
"""

from typing import Dict, Any, List, Optional
import re
import numpy as np


def solve_linear_system(equations: List[str], variables: Optional[List[str]] = None) -> Dict[str, Any]:
    """Resolve um sistema de equações lineares.

    Args:
        equations: Lista de equações como strings (ex: ["x + y = 5", "2*x - y = 1"])
        variables: Lista de variáveis (ex: ["x", "y"]); se None, tenta inferir

    Returns:
        Dict com success, solution, matrix, determinant
    """
    try:
        if variables is None:
            # Tentar inferir variáveis das equações
            all_vars = set()
            for eq in equations:
                all_vars.update(re.findall(r'[a-z]', eq))
            variables = sorted(list(all_vars))

        n = len(variables)
        A = np.zeros((n, n))
        b = np.zeros(n)

        for i, eq in enumerate(equations):
            # Parsear LHS e RHS
            if "=" not in eq:
                return {
                    "success": False,
                    "error": f"Equação {i+1} não tem sinal de igual",
                    "equations": equations
                }

            lhs, rhs = [s.strip() for s in eq.split("=", 1)]
            b[i] = _parse_numeric(rhs)

            # Parsear coeficientes de variáveis
            for j, var in enumerate(variables):
                coeff = _parse_coefficient(lhs, var)
                A[i, j] = coeff

        # Resolver sistema
        try:
            solution = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            # Verificar se é inconsistente ou depende
            det = np.linalg.det(A)
            if abs(det) < 1e-10:
                return {
                    "success": False,
                    "error": "Sistema singular - infinite solutions or no solution",
                    "equations": equations,
                    "variables": variables
                }
            raise

        solution_dict = {variables[i]: float(solution[i]) for i in range(n)}

        return {
            "success": True,
            "solution": solution_dict,
            "matrix_A": A.tolist(),
            "vector_b": b.tolist(),
            "determinant": float(np.linalg.det(A)),
            "variables": variables
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "equations": equations if 'equations' in dir() else [],
            "variables": variables if 'variables' in dir() else []
        }


def _parse_numeric(expr: str) -> float:
    """Parsa um número de uma expressão string."""
    try:
        # Remover espaços e caracteres de variável
        clean = re.sub(r'[a-zA-Z]', '', expr).strip()
        return float(clean) if clean else 0.0
    except (ValueError, TypeError):
        return 0.0


def _parse_coefficient(expr: str, variable: str) -> float:
    """Extrai o coeficiente de uma variável em uma expressão."""
    # Padrões: "3*x", "-2x", "+5*x", "x" (coeff=1), "-x" (coeff=-1)
    pattern = r'([+-]?\d*\.?\*\*?\*?x?)'.replace('x', variable)
    match = re.search(pattern, expr)
    if not match:
        return 0.0

    coeff_str = match.group(1).replace(variable, '').strip()
    if not coeff_str or coeff_str in ['+', '-']:
        return -1 if coeff_str == '-' else 1
    try:
        return float(coeff_str.replace('*', ''))
    except ValueError:
        return 1.0


def matrix_multiplication(m1: List[List[float]], m2: List[List[float]]) -> Dict[str, Any]:
    """Multiplica duas matrizes."""
    try:
        A = np.array(m1)
        B = np.array(m2)

        if A.shape[1] != B.shape[0]:
            return {
                "success": False,
                "error": f"Dimensões incompatíveis: A={A.shape}, B={B.shape}",
                "m1": m1,
                "m2": m2
            }

        result = A @ B

        return {
            "success": True,
            "result": result.tolist(),
            "m1_dims": A.shape,
            "m2_dims": B.shape,
            "operation": "matrix_multiplication"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "m1": m1,
            "m2": m2
        }


def determinant(matrix: List[List[float]]) -> Dict[str, Any]:
    """Calcula o determinante de uma matriz."""
    try:
        A = np.array(matrix)
        det = np.linalg.det(A)

        return {
            "success": True,
            "determinant": float(det),
            "matrix_dims": A.shape,
            "is_invertible": abs(float(det)) > 1e-10
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "matrix": matrix
        }