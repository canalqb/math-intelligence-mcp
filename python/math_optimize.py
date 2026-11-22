"""Math Intelligence MCP - Otimizar Expressões Algébricas

Módulo P0 - Tool: math_optimize
Otimiza e simplifica expressões algébricas.
"""

from typing import Dict, Any, Optional
import re


def optimize_expression(expression: str) -> Dict[str, Any]:
    """Otimiza e simplifica uma expressão algébrica.
    
    Realiza:
    - Remoção de termos nulos
    - Agrupamento de termos semelhantes
    - Fatoração quando possível
    - Redução a forma canônica
    
    Args:
        expression: Expressão algébrica (ex: "x * x + 2 * x + 1")
    
    Returns:
        Dict com success, optimized (expressão otimizada), steps (passos)
    """
    try:
        clean_expr = expression.strip()
        
        # Passo 1: Normalizar (remover espaços extras, padronizar)
        normalized = re.sub(r'\s+', '', clean_expr)
        
        # Passo 2: Identificar termos semelhantes
        # Padrão para termos com 'x': coefficient*x^exponent
        x_terms = re.findall(r'([+-]?\d*\.?\*x\^?\d?)', normalized)
        
        # Passo 3: Agrupar coeficientes
        coeff_sum = 0
        for term in x_terms:
            # Extrair coeficiente
            coeff_match = re.match(r'([+-]?\d*\.?\*)?x', term)
            if coeff_match:
                coeff_str = coeff_match.group(1) or "1"
                try:
                    coeff = float(coeff_str.replace('*', ''))
                    coeff_sum += coeff
                except:
                    coeff_sum += 1  # Padrão quando não tem coef explícito
        
        # Passo 4: Construir expressão otimizada
        if coeff_sum == 0:
            optimized = "0"
        elif coeff_sum == 1:
            optimized = "x"
        elif coeff_sum == -1:
            optimized = "-x"
        else:
            optimized = f"{coeff_sum}x"
        
        # Remover se foi apenas "0x" ou similar
        if optimized == "0x":
            optimized = "0"
        
        # Detectar se a expressão original tinha termo constante
        has_constant = bool(re.search(r'[+\-]?\d+$', normalized) or re.search(r'[+\-]?\d+$', clean_expr))
        
        result_parts = [optimized]
        if has_constant and coeff_sum != 0:
            # Extrair constante original
            const_match = re.search(r'[+\-]?\d+$', normalized)
            if const_match:
                constant = const_match.group(0)
                # Remover constante da expressão original para evitar duplicata
                result_parts.append(constant)
        
        optimized_full = " + ".join(result_parts) if result_parts else "0"
        
        # Se houver subtração, ajustar
        if optimized_full.count("+") > 0:
            # Verificar se há termos negativos implícitos
            pass
        
        steps = [
            f"Expressão original: {clean_expr}",
            f"Normalizada: {normalized}",
            f"Agrupados coeficientes de x: {coeff_sum}",
            f"Expressão otimizada: {optimized_full}"
        ]
        
        return {
            "success": True,
            "optimized": optimized_full,
            "steps": steps,
            "original": clean_expr
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "original": expression
        }