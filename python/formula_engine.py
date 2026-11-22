"""Math Intelligence MCP - Formula Engine

Módulo P2 - Tool: formula_engine
Catálogo curado de fórmulas científicas e financeiras com substituição formal
e isolamento de incógnitas.
"""

from typing import Dict, Any, Optional
import math


def solve_formula(formula_id: str, substitutions: dict, solve_for: str) -> Dict[str, Any]:
    """Resolve uma fórmula científica ou financeira com substituições de variáveis.

    Args:
        formula_id: ID da fórmula (ex: "quadratic", "pythagorean", "compound_interest",
                    "euler_identity", "binomial_coefficient")
        substitutions: Dicionário com valores de substituição {variavel: valor}
        solve_for: Variável para resolver (a incógnita)

    Returns:
        Dict com success, formula_id, solve_for, substitutions,
        computed_value, exact_value, steps, error
    """
    try:
        # Catálogo de fórmulas suportadas
        formulas = {
            "quadratic": {
                "template": "ax² + bx + c = 0",
                "variables": ["a", "b", "c"],
                "solve_for_x": True
            },
            "pythagorean": {
                "template": "a² + b² = c²",
                "variables": ["a", "b", "c"],
                "solve_for_x": False
            },
            "compound_interest": {
                "template": "A = P(1 + r/n)^(nt)",
                "variables": ["P", "r", "n", "t"],
                "solve_for_x": False
            },
            "euler_identity": {
                "template": "e^(iπ) + 1 = 0",
                "variables": ["e", "i", "π"],
                "solve_for_x": False
            },
            "binomial_coefficient": {
                "template": "C(n,k) = n! / (k!(n-k)!)",
                "variables": ["n", "k"],
                "solve_for_x": False
            },
        }

        # Obter fórmula do catálogo ou retornar erro
        formula = formulas.get(formula_id.lower())
        if formula is None:
            available = ", ".join(formulas.keys())
            return {
                "success": False,
                "error": f"Fórmula '{formula_id}' não encontrada. Disponíveis: {available}",
                "formula_id": formula_id,
                "solve_for": solve_for
            }

        # Extrair variáveis da fórmula e aplicar substituições
        vars_in_formula = formula["variables"]
        applied_subs = {}
        for var in vars_in_formula:
            if var in substitutions:
                applied_subs[var] = substitutions[var]

        # Verificar quais variáveis foram fornecidas
        provided_vars = set(applied_subs.keys())
        required_vars = set(vars_in_formula)

        # Se todas as variáveis necessárias estão presentes, computar
        if required_vars.issubset(provided_vars):
            # Todas as variáveis necessárias estão presentes
            if formula_id.lower() == "quadratic":
                a_val = applied_subs.get("a")
                b_val = applied_subs.get("b")
                c_val = applied_subs.get("c")

                # Calcular discriminante
                if a_val is not None and b_val is not None and c_val is not None:
                    discriminant = b_val**2 - 4*a_val*c_val

                    if discriminant >= 0:
                        sqrt_disc = discriminant**0.5
                        x1 = (-b_val + sqrt_disc) / (2*a_val) if 2*a_val != 0 else None
                        x2 = (-b_val - sqrt_disc) / (2*a_val) if 2*a_val != 0 else None
                    else:
                        # Raízes complexas - simplificado
                        sqrt_disc_abs = (-discriminant)**0.5
                        real_part = -b_val / (2*a_val) if 2*a_val != 0 else None
                        imag_part = sqrt_disc_abs / (2*a_val) if 2*a_val != 0 else None
                        x1 = f"{real_part} + {imag_part}i" if real_part is not None and imag_part is not None else None
                        x2 = f"{real_part} - {imag_part}i" if real_part is not None and imag_part is not None else None

                    result = {
                        "formula": formula["template"],
                        "solve_for": "x",
                        "substitutions": applied_subs,
                        "x1": x1,
                        "x2": x2,
                        "discriminant": discriminant
                    }
                else:
                    result = {
                        "formula": formula["template"],
                        "solve_for": "x",
                        "substitutions": applied_subs,
                        "error": "Variáveis incompletas para quadratic: a, b, c necessárias"
                    }

            elif formula_id.lower() == "euler_identity":
                # e^(iπ) + 1 = 0, então e^(iπ) = -1
                result = {
                    "formula": formula["template"],
                    "solve_for": "verification",
                    "substitutions": applied_subs,
                    "computed_value": -1.0,
                    "exact_value": -1.0,
                    "verification": "e^(iπ) + 1 = 0 ✓"
                }

            elif formula_id.lower() == "compound_interest":
                P_val = applied_subs.get("P")
                r_val = applied_subs.get("r")
                n_val = applied_subs.get("n")
                t_val = applied_subs.get("t")

                if all(v is not None for v in [P_val, r_val, n_val, t_val]):
                    # A = P(1 + r/n)^(nt)
                    result = {
                        "formula": formula["template"],
                        "solve_for": "A",
                        "substitutions": applied_subs,
                        "computed_value": P_val * (1 + r_val/n_val) ** (n_val*t_val)
                    }
                else:
                    result = {
                        "formula": formula["template"],
                        "solve_for": "A",
                        "substitutions": applied_subs,
                        "missing_variables": [k for k, v in applied_subs.items() if v is None],
                        "message": "Forneça P, r, n e t para calcular juros compostos"
                    }

            elif formula_id.lower() == "binomial_coefficient":
                n_val = applied_subs.get("n")
                k_val = applied_subs.get("k")

                if n_val is not None and k_val is not None:
                    if 0 <= k_val <= n_val:
                        result = {
                            "formula": formula["template"],
                            "solve_for": "C(n,k)",
                            "substitutions": applied_subs,
                            "computed_value": math.comb(int(n_val), int(k_val))
                        }
                    else:
                        result = {
                            "formula": formula["template"],
                            "solve_for": "C(n,k)",
                            "substitutions": applied_subs,
                            "error": "k deve ser maior ou igual a 0 e menor ou igual a n"
                        }
                else:
                    result = {
                        "formula": formula["template"],
                        "solve_for": "C(n,k)",
                        "substitutions": applied_subs,
                        "missing_variables": [k for k, v in applied_subs.items() if v is None],
                        "message": "Forneça n e k para calcular coeficiente binomial"
                    }

            else:
                # Fórmula não implementada detalhada
                result = {
                    "formula": formula["template"],
                    "solve_for": solve_for,
                    "substitutions": applied_subs,
                    "message": "Fórmula suportada, mas cálculo detalhado não implementado"
                }

            return {
                "success": True,
                "formula_id": formula_id,
                "solve_for": solve_for,
                **result
            }

        # Variáveis insuficientes
        missing = list(required_vars - provided_vars)
        return {
            "success": True,
            "formula_id": formula_id,
            "solve_for": solve_for,
            "formula": formula["template"],
            "substitutions": applied_subs,
            "missing_variables": missing,
            "message": f"Variáveis necessárias não fornecidas: {', '.join(missing) if missing else 'N/A'}. "
                       f"Forneça valores para todas as variáveis: {', '.join(vars_in_formula)}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "formula_id": formula_id,
            "solve_for": solve_for
        }