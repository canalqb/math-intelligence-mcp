"""Math Intelligence MCP - Pattern Recognition

Módulo P2 - Tool: pattern_recognition
Detecção de padrões numéricos inteiros, relações de congruência modular e
consulta estruturada a padrões da enciclopédia OEIS.
"""

from typing import Dict, Any, List, Optional
import math


def detect_period(sequence: List[int], predict_next_terms: int = 3, mode: str = "both") -> Dict[str, Any]:
    """Detecta padrões em sequência numérica inteira.

    Args:
        sequence: Sequência numérica inteira
        predict_next_terms: Número de termos para prever (padrão: 3)
        mode: Tipo de extrema ("max", "min", "both", padrão: "both")

    Returns:
        Dict com success, sequence, detected_patterns, period,
        pattern_type, oeis_references, predicted_next, mode
    """
    try:
        if not sequence or len(sequence) < 2:
            return {
                "success": False,
                "error": "Sequência deve ter pelo menos 2 elementos",
                "sequence": sequence,
                "mode": mode
            }

        n = len(sequence)

        # 1. Verificar diferença consecutiva
        differences = [sequence[i+1] - sequence[i] for i in range(n-1)]

        # 2. Verificar diferenças secundárias (se houver)
        second_differences = None
        if len(differences) > 1:
            second_differences = [differences[i+1] - differences[i] for i in range(len(differences)-1)]

        # 3. Detectar padrão de diferença constante (progressão aritmética)
        is_arithmetic = False
        common_diff = None
        if second_differences is not None:
            # Verificar se todas as segundas diferenças são iguais
            if len(set(second_differences)) == 1:
                is_arithmetic = True
                common_diff = differences[0] if differences else None

        # 4. Detectar padrão geométrico (razão constante entre termos)
        is_geometric = False
        common_ratio = None
        if n >= 2 and all(sequence[i] != 0 for i in range(n)):
            ratios = [sequence[i+1] / sequence[i] for i in range(min(n-1, 10))]  # Limitar para evitar overflow
            # Verificar se as razões são aproximadamente iguais
            if ratios and len(set([round(r, 10) for r in ratios])) <= 2:
                is_geometric = True
                common_ratio = ratios[0]

        # 5. Detectar padrão de Fibonacci-like (cada termo = soma dos 2 anteriores)
        is_fibonacci_like = False
        if n >= 3:
            fib_like_count = 0
            for i in range(2, n):
                if sequence[i] == sequence[i-1] + sequence[i-2]:
                    fib_like_count += 1
            # Se mais da maioria seguir o padrão
            if fib_like_count >= n - 2:
                is_fibonacci_like = True

        # 6. Padrões de periodicidade (repetição)
        period = None
        is_periodic = False
        if n >= 4:
            # Tentar períodos de 2 a n//2
            for p in range(2, min(n//2 + 1, 20)):
                is_p_periodic = True
                for i in range(p, n):
                    if sequence[i] != sequence[i - p]:
                        is_p_periodic = False
                        break
                if is_p_periodic:
                    period = p
                    is_periodic = True
                    break

        # 7. Determinar próximos termos previstos
        predicted_next = []
        mode_lower = mode.lower()

        if is_arithmetic and common_diff is not None:
            last = sequence[-1]
            for _ in range(predict_next_terms):
                last += common_diff
                predicted_next.append(last)
        elif is_geometric and common_ratio is not None:
            last = sequence[-1]
            for _ in range(predict_next_terms):
                last *= common_ratio
                predicted_next.append(last)
        elif is_fibonacci_like:
            # Próximos termos = soma dos 2 últimos
            a, b = sequence[-2], sequence[-1]
            for _ in range(predict_next_terms):
                a, b = b, a + b
                predicted_next.append(b)
        elif is_periodic and period is not None:
            # Repetir padrão existente
            for i in range(predict_next_terms):
                predicted_next.append(sequence[(n - 1 - i % period) % (period if period else 1)])
        else:
            # Padrão não identificado - tentar extrapolação linear simples
            if len(differences) >= 2:
                # Extrapolação linear baseada na última diferença
                last_diff = differences[-1]
                last_val = sequence[-1]
                for _ in range(predict_next_terms):
                    last_val += last_diff
                    predicted_next.append(last_val)
            else:
                # Fallback: manter valor constante
                last_val = sequence[-1]
                for _ in range(predict_next_terms):
                    predicted_next.append(last_val)

        # Filtrar resultados pelo mode
        if mode_lower == "max":
            predicted_next = [max(p) if isinstance(p, (list, tuple)) else p for p in predicted_next]
        elif mode_lower == "min":
            predicted_next = [min(p) if isinstance(p, (list, tuple)) else p for p in predicted_next]

        # Referências OEIS (simuladas - em produção consultar API OEIS)
        oeis_references = []
        if is_arithmetic:
            oeis_references.append("A000027: Naturais (1, 2, 3, 4, ...) - diferença 1")
        if is_geometric:
            oeis_references.append("A000244: Potências de 3 (1, 3, 9, 27, ...) - razão 3")
        if is_fibonacci_like:
            oeis_references.append("A000045: Fibonacci (0, 1, 1, 2, 3, 5, 8, ...)")

        result: Dict[str, Any] = {
            "success": True,
            "sequence": sequence,
            "detected_patterns": {
                "is_arithmetic": is_arithmetic,
                "common_diff": common_diff,
                "is_geometric": is_geometric,
                "common_ratio": round(common_ratio, 6) if common_ratio is not None else None,
                "is_fibonacci_like": is_fibonacci_like,
                "is_periodic": is_periodic,
                "period": period
            },
            "pattern_type": "arithmetic" if is_arithmetic else ("geometric" if is_geometric else
                                "fibonacci-like" if is_fibonacci_like else
                                "periodic" if is_periodic else "unknown"),
            "predicted_next": predicted_next[:predict_next_terms],
            "mode": mode,
            "oeis_references": oeis_references,
            "analysis": {
                "differences": differences,
                "second_differences": second_differences,
                "ratios": [round(r, 6) for r in [sequence[i+1] / sequence[i] for i in range(min(n-1, 10))] if sequence[i] != 0] if n >= 2 and all(sequence[i] != 0 for i in range(n)) else None
            }
        }

        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "sequence": sequence,
            "mode": mode
        }


def find_local_extrema(sequence: List[int]) -> Dict[str, Any]:
    """Encontra extremos locais (mínimos e máximos) em uma sequência.

    Args:
        sequence: Sequência numérica inteira

    Returns:
        Dict com success, sequence, local_maxima, local_minima
    """
    try:
        if not sequence or len(sequence) < 3:
            return {
                "success": False,
                "error": "Sequência deve ter pelo menos 3 elementos",
                "sequence": sequence
            }

        n = len(sequence)
        local_maxima = []
        local_minima = []

        # Encontrar extremos locais (pontos onde o vizinho é maior/menor)
        for i in range(1, n - 1):
            prev_val = sequence[i - 1]
            curr_val = sequence[i]
            next_val = sequence[i + 1]

            # Máximo local: curr > prev e curr > next
            if curr_val > prev_val and curr_val > next_val:
                local_maxima.append({
                    "index": i,
                    "value": curr_val,
                    "position": i
                })

            # Mínimo local: curr < prev e curr < next
            if curr_val < prev_val and curr_val < next_val:
                local_minima.append({
                    "index": i,
                    "value": curr_val,
                    "position": i
                })

        return {
            "success": True,
            "sequence": sequence,
            "local_maxima": local_maxima,
            "local_minima": local_minima,
            "total_maxima": len(local_maxima),
            "total_minima": len(local_minima)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "sequence": sequence
        }


def symmetry_analysis(sequence: List[int]) -> Dict[str, Any]:
    """Analisa simetria de uma sequência em relação ao centro.

    Args:
        sequence: Sequência numérica inteira

    Returns:
        Dict com success, sequence, is_symmetric, symmetry_point, mirrored_diffs
    """
    try:
        if not sequence:
            return {
                "success": False,
                "error": "Sequência vazia",
                "sequence": sequence
            }

        n = len(sequence)
        is_symmetric = False
        symmetry_point = None
        mirrored_diffs = []

        # Verificar simetria reflexiva (palíndromo invertido)
        is_palindrome = sequence == sequence[::-1]

        # Verificar simetria em relação ao centro
        if n % 2 == 1:
            # Sequência de comprimento ímpar - simetria em torno do elemento central
            mid = n // 2
            left = sequence[:mid]
            right = sequence[mid+1:][::-1]  # Lado direito invertido
            is_symmetric = left == right
            symmetry_point = mid  # Índice do elemento central
        else:
            # Sequência de comprimento par
            mid_left = n // 2 - 1
            mid_right = n // 2
            left = sequence[:mid_left + 1]
            right = sequence[mid_right:][::-1]
            is_symmetric = left == right
            symmetry_point = (mid_left + mid_right) / 2

        # Se for palíndromo
        if is_palindrome:
            is_symmetric = True
            symmetry_point = (n - 1) / 2

        # Calcular diferenças espeilhadas
        if is_symmetric and n > 1:
            for i in range(n - 1):
                # Diferença entre termos espeelhados
                mirrored_diffs.append(sequence[i] - sequence[n - 1 - i])

        return {
            "success": True,
            "sequence": sequence,
            "is_symmetric": is_symmetric,
            "symmetry_point": symmetry_point,
            "is_palindrome": is_palindrome,
            "mirrored_differences": mirrored_diffs,
            "length": n
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "sequence": sequence
        }