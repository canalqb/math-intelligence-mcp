"""Math Intelligence MCP - Reconhecimento de Padrões

Módulo P1 - Tool: pattern_recognition
Detecção de padrões em sequências, identificação de fractais e simetrias.
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np


def detect_period(sequence: List[float], max_lag: Optional[int] = None) -> Dict[str, Any]:
    """Detecta o período de uma sequência temporal usando autocorrelação.
    
    Args:
        sequence: Lista de valores numéricos
        max_lag: Lag máximo para busca (padrão: len(sequence)//2)
    
    Returns:
        Dict com success, period, autocorrelation
    """
    try:
        if not sequence:
            return {"success": False, "error": " sequência vazia"}

        n = len(sequence)
        data = np.array(sequence, dtype=float)

        if max_lag is None:
            max_lag = n // 2

        if max_lag < 1 or max_lag >= n:
            return {"success": False, "error": "max_lag inválido"}

        # Mean subtraction
        mean = np.mean(data)
        centered = data - mean

        # Autocorrelação para lags de 1 a max_lag
        variances = np.var(data)
        autocorr = []

        for lag in range(1, max_lag + 1):
            cov = np.sum(centered[:-lag] * centered[lag:]) / variances
            ac = cov / np.var(data) if variances != 0 else 0
            autocorr.append(float(ac))

        # Encontrar lag com autocorrelação próxima de 1 (excluindo lag 0)
        # Procura por o primeiro lag onde a autocorrelação cai abaixo de um threshold
        threshold = 0.5
        detected_period = None

        for lag in range(1, max_lag + 1):
            if lag <= len(autocorr):
                if autocorr[lag - 1] < threshold and autocorr[lag - 2] >= threshold if lag > 1 else False:
                    detected_period = lag
                    break

        # Se não encontrou queda clara, retorna o lag com maior autocorrelação (exceto 0)
        if detected_period is None:
            # Procura pelo pico após o lag 1
            best_lag = 1
            best_ac = autocorr[0] if autocorr else 0
            for i in range(1, len(autocorr)):
                if autocorr[i] > best_ac:
                    best_ac = autocorr[i]
                    best_lag = i + 1
            detected_period = best_lag

        return {
            "success": True,
            "sequence_length": n,
            "detected_period": detected_period,
            "autocorrelation": autocorr,
            "max_lag_searched": max_lag,
            "note": "Detecção baseada em autocorrelação simples",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def find_local_extrema(sequence: List[float], mode: str = "both") -> Dict[str, Any]:
    """Encontra extremos locais (máximos e mínimos) em uma sequência."""
    try:
        if len(sequence) < 3:
            return {"success": False, "error": "Série muito curta para extrema"}

        data = np.array(sequence, dtype=float)
        extrema: List[Dict[str, Any]] = []

        for i in range(1, len(data) - 1):
            left = data[i - 1]
            current = data[i]
            right = data[i + 1]

            is_max = current > left and current > right
            is_min = current < left and current < right

            if mode == "max" and is_max:
                extrema.append({"index": i, "value": float(current), "type": "maximum"})
            elif mode == "min" and is_min:
                extrema.append({"index": i, "value": float(current), "type": "minimum"})
            elif mode == "both" and (is_max or is_min):
                extrema.append({"index": i, "value": float(current), "type": "maximum" if is_max else "minimum"})

        return {
            "success": True,
            "sequence_length": len(sequence),
            "extrema": extrema,
            "total_extrema": len(extrema),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def symmetry_analysis(sequence: List[float]) -> Dict[str, Any]:
    """Analisa simetria de uma sequência em relação ao centro."""
    try:
        if not sequence:
            return {"success": False, "error": "sequência vazia"}

        data = np.array(sequence, dtype=float)
        n = len(data)

        center = n / 2.0

        # Comparar valores simétricos
        symmetric_pairs: List[Tuple[int, int, float, float]] = []
        is_symmetric = True

        for i in range(n // 2):
            left_idx = i
            right_idx = n - 1 - i
            left_val = data[left_idx]
            right_val = data[right_idx]

            diff = abs(left_val - right_val)
            symmetric_pairs.append((left_idx, right_idx, float(left_val), float(right_val)))

            if diff > 1e-10:  # Tolerância para simetria exata
                is_symmetric = False

        # Para seqüências ímpares, comparar o elemento central com ele mesmo
        middle_diff = 0.0
        if n % 2 == 1:
            middle_idx = n // 2
            middle_diff = 0.0  # Elemento central compara-se a si mesmo

        # Calcular razão de simetria
        total_diff = sum(abs(pair[2] - pair[3]) for pair in symmetric_pairs)
        total_magnitude = sum(abs(pair[2]) + abs(pair[3]) for pair in symmetric_pairs)
        symmetry_ratio = total_diff / total_magnitude if total_magnitude != 0 else 0.0

        return {
            "success": True,
            "sequence_length": n,
            "is_symmetric": is_symmetric,
            "symmetry_ratio": float(symmetry_ratio),
            "symmetric_pairs": symmetric_pairs,
            "middle_difference": float(middle_diff),
            "note": "Análise de simetria reflexiva em relação ao centro",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}