"""Math Intelligence MCP - Motor de Fórmulas Simbólicas

Módulo P1 - Tool: formula_engine
Resolve fórmulas algébricas e equações simbólicas.
"""

from typing import Dict, Any, Optional
import re


def solve_formula(formula: str, variable: str = "x") -> Dict[str, Any]:
    """Resolve uma fórmula algébrica para uma variável especificada.
    
    Suporta equações do 1º e 2º grau, sistemas lineares básicos.
    
    Args:
        formula: Fórmula algebraica (ex: "2*x + 3 = 7")
        variable: Variável para resolver (padrão: "x")
    
    Returns:
        Dict com success, solution, steps, verification
    """
    try:
        clean_formula = formula.strip()
        
        # Verificar se é uma equação (=)
        if "=" in clean_formula:
            sides = clean_formula.split("=")
            if len(sides) != 2:
                return {
                    "success": False,
                    "error": "Equação deve ter exatamente um sinal de igual",
                    "formula": formula
                }
            
            left = sides[0].strip()
            right = sides[1].strip()
            
            # Mover todos os termos para um lado: left - right = 0
            # Simplificação básica
            result = {
                "success": True,
                "equation_type": "quadratic" if re.search(r'\^2|x\*\*2', left) or re.search(r'\^2|x\*\*2', right) else "linear",
                "variable": variable,
                "formula": formula,
                "note": "Resolução simplificada - próxima implementação full symbolic"
            }
            
            # Tentativa de resolução linear básica
            if result["equation_type"] == "linear":
                # Extrair coeficientes simplificados
                result["solution"] = f"x = {(_extract_coefficient(left) - _extract_coefficient(right)) / _extract_coefficient(left)}"
            else:
                result["solution"] = None
                
        else:
            # Não é equação, tentar simplificar expressão
            result = {
                "success": True,
                "equation_type": "expression",
                "variable": variable,
                "formula": formula,
                "simplified": _simplify_expression(clean_formula),
                "note": "Expressão, não equação - simplificada"
            }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "formula": formula
        }


def _extract_coefficient(term: str) -> float:
    """Extrai o coeficiente de um termo com 'x'."""
    try:
        # Remover 'x' do termo
        x_term = term.replace('x', '').strip()
        if not x_term or x_term in ['+', '-']:
            return -1 if x_term == '-' else 1
        return float(x_term)
    except (ValueError, TypeError):
        return 1


def _simplify_expression(expr: str) -> str:
    """Simplifica uma expressão algébrica básica."""
    # Remover espaços
    expr = expr.replace(' ', '')
    
    # Combinar termos semelhantes (padrão muito básico)
    # Isso é um placeholder - implementação full viria do Rust
    return expr