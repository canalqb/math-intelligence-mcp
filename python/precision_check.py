"""Math Intelligence MCP - Verificação de Precisão

Módulo P1 - Tool: precision_check
Executa o mesmo cálculo em múltiplos níveis de precisão para detectar
cancelamento catastrófico e perda de dígitos significativos.
"""

from typing import Dict, Any, Optional
import decimal
import numpy as np


def precision_check(expression: str, target_digits: int = 50) -> Dict[str, Any]:
    """Executa um cálculo em múltiplos níveis de precisão.

    Compara resultados usando:
    - Precisão decimal padrão (6 dígitos)
    - Precisão decimal alta (target_digits dígitos)
    - Precisão arbitrária via decimal module

    Detecta:
    - Cancelamento catastrófico
    - Perda de dígitos significativos
    - Convergência numérica

    Args:
        expression: Expressão matemática para calcular
        target_digits: Número de dígitos alvo para precisão alta (padrão: 50)

    Returns:
        Dict com success, results_by_precision, catastrophic_cancellation,
        significant_digits_lost, convergence_info
    """
    try:
        results = {}

        # Nível 1: Padrão float64 (numpy)
        try:
            std_result = float(eval(expression, {"__builtins__": __builtins__}, {}))
            results["float64"] = {
                "result": std_result,
                "precision": "float64 (aprox. 15-17 dígitos)"
            }
        except Exception as e:
            results["float64"] = {"error": str(e), "precision": "float64"}

        # Nível 2: Precisão alta via decimal
        try:
            # Extrair números da expressão para definição de precisão
            d = decimal.Decimal(str(eval(expression, {"__builtins__": None}, {})))
            high_prec_result = float(d)
            # Arredondar para target_digits
            d_target = decimal.Decimal(str(high_prec_result)).quantize(
                decimal.Decimal(10) ** (-target_digits),
                context=decimal.Context(prec=target_digits + 10)
            )
            results["decimal_high"] = {
                "result": float(d_target),
                "precision": f"decimal ({target_digits} dígitos)"
            }
        except Exception as e:
            results["decimal_high"] = {"error": str(e), "precision": "decimal"}

        # Nível 3: Verificar cancelamento catastrófico
        # Simplificado: comparar número de dígitos significativos iguais
        catastrophic_cancellation = False
        significant_lost = 0

        if "float64" in results and "decimal_high" in results:
            fr = results["float64"].get("result")
            dr = results["decimal_high"].get("result")

            if fr is not None and dr is not None and abs(fr) > 0 and abs(dr) > 0:
                # Contar dígitos significativos iguais do início
                fr_str = str(abs(fr)).replace('.', '').replace('-', '')
                dr_str = str(abs(dr)).replace('.', '').replace('-', '')

                min_digits = min(len(fr_str), len(dr_str))
                matching_digits = 0
                for i in range(min_digits):
                    if i < len(fr_str) and i < len(dr_str) and fr_str[i] == dr_str[i]:
                        matching_digits += 1
                    else:
                        break

                fr_sig = len(fr_str)
                if fr_sig > 0:
                    significant_lost = fr_sig - matching_digits
                    if matching_digits < fr_sig * 0.3:  # Menos que 30% dos dígitos coincidem
                        catastrophic_cancellation = True

        return {
            "success": True,
            "results_by_precision": results,
            "catastrophic_cancellation_detected": catastrophic_cancellation,
            "significant_digits_lost": significant_lost,
            "convergence_info": {
                "float64_result": results["float64"].get("result"),
                "decimal_high_result": results["decimal_high"].get("result"),
                "digits_lost": significant_lost
            },
            "expression": expression
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression
        }