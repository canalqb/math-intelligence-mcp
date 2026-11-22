"""Math Intelligence MCP - Análise Estatística

Módulo P1 - Tool: statistical_analysis
Estatísticas descritivas, distribuições e testes básicos.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import math
from scipy import stats as scipy_stats


def descriptive_statistics(data: List[float]) -> Dict[str, Any]:
    """Calcula estatísticas descritivas de uma lista de números."""
    try:
        if not data:
            return {"success": False, "error": "Lista de dados vazia"}

        data_arr = np.array(data, dtype=float)
        n = len(data_arr)

        result: Dict[str, Any] = {
            "success": True,
            "count": n,
            "mean": float(np.mean(data_arr)),
            "median": float(np.median(data_arr)),
            "std": float(np.std(data_arr, ddof=1)),  # amostra
            "variance": float(np.var(data_arr, ddof=1)),
            "min": float(np.min(data_arr)),
            "max": float(np.max(data_arr)),
            "range": float(np.ptp(data_arr)),
            "q1": float(np.percentile(data_arr, 25)),
            "q3": float(np.percentile(data_arr, 75)),
            "iqr": float(np.percentile(data_arr, 75) - np.percentile(data_arr, 25)),
        }

        # Coeficiente de variação
        if result["mean"] != 0:
            result["coefficient_of_variation"] = float(
                result["std"] / abs(result["mean"])
            )
        else:
            result["coefficient_of_variation"] = None

        return result

    except Exception as e:
        return {"success": False, "error": str(e)}


def test_normality(data: List[float], alpha: float = 0.05) -> Dict[str, Any]:
    """Teste de normalidade usando scipy.stats."""
    try:
        data_arr = np.array(data, dtype=float)
        n = len(data_arr)

        if n < 3:
            return {"success": False, "error": "Dados insuficientes para teste de normalidade"}

        # Teste Shapiro-Wilk (disponível para n <= 50)
        if n <= 50:
            stat, p = scipy_stats.shapiro(data_arr)
            result = {
                "success": True,
                "shapiro_stat": float(stat),
                "shapiro_p_value": float(p),
                "normal": p > alpha,
                "test": "shapiro-wilk",
            }
        else:
            # Para amostras maiores, usar teste de Jarque-Bera
            jb_stat, jb_p = scipy_stats.jarque_bera(data_arr)
            result = {
                "success": True,
                "jarque_bera_stat": float(jb_stat),
                "jarque_bera_p_value": float(jb_p),
                "normal": jb_p > alpha,
                "test": "jarque-bera",
            }

        return result

    except Exception as e:
        return {"success": False, "error": str(e)}


def correlation(x_data: List[float], y_data: List[float]) -> Dict[str, Any]:
    """Calcula correlação de Pearson entre duas variáveis."""
    try:
        if len(x_data) != len(y_data):
            return {
                "success": False,
                "error": "Vetores devem ter o mesmo tamanho",
            }

        n = len(x_data)
        if n < 2:
            return {"success": False, "error": "Dados insuficientes"}

        x = np.array(x_data, dtype=float)
        y = np.array(y_data, dtype=float)

        # Pearson r e teste t
        r, p_value = scipy_stats.pearsonr(x, y)

        # Classificação da força
        strength = (
            "strong" if abs(r) >= 0.7
            else "moderate" if abs(r) >= 0.3
            else "weak"
        )

        return {
            "success": True,
            "correlation": float(r),
            "p_value": float(p_value),
            "n": n,
            "strength": strength,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def probability_distribution(distribution: str, params: Dict[str, Any],
                              x: Optional[float] = None) -> Dict[str, Any]:
    """Calcula probabilidades de distribuições comuns."""
    try:
        if distribution.lower() == "normal":
            mean = params.get("mean", 0)
            std = params.get("std", 1)
            if x is None:
                return {"success": False, "error": "Informe o valor de x"}

            # Z-score
            z = (x - mean) / std
            # CDF usando scipy
            from scipy.stats import norm
            cdf = float(norm.cdf(z))

            return {
                "success": True,
                "distribution": "normal",
                "x": x,
                "z_score": z,
                "probability": cdf,
                "params": {"mean": mean, "std": std},
            }

        elif distribution.lower() == "uniform":
            a = params.get("a", 0)
            b = params.get("b", 1)
            if x is None:
                return {"success": False, "error": "Informe o valor de x"}

            # CDF uniforme
            if x <= a:
                cdf = 0.0
            elif x >= b:
                cdf = 1.0
            else:
                cdf = (x - a) / (b - a)

            return {
                "success": True,
                "distribution": "uniform",
                "x": x,
                "a": a,
                "b": b,
                "probability": cdf,
            }

        else:
            return {
                "success": False,
                "error": f"Distribuição '{distribution}' não suportada",
            }
    except Exception as e:
        return {"success": False, "error": str(e)}