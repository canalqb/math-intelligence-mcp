"""Math Intelligence MCP - Perfilagem de Memória

Módulo P0 - Tool: memory_profile
Perfila consumo de memória e performance de operações matemáticas.
"""

from typing import Dict, Any, Optional
import time
import tracemalloc


def profile_memory(operation: str, duration_ms: int, memory_mb: float = 0.0) -> Dict[str, Any]:
    """Gera um perfil de memória e performance para uma operação.

    Coleta informações sobre:
    - Uso de memória pico (via tracemalloc)
    - Duração da operação
    - Eficiência computacional
    - Sugestões de otimização

    Args:
        operation: Nome da operação sendo profilhada (ex: "busca_secp256k1")
        duration_ms: Duração da operação em milissegundos
        memory_mb: Memória usada em MB (opcional, detectado automaticamente se não fornecido)

    Returns:
        Dict com success, memory_usage, duration_ms, efficiency, suggestions
    """
    try:
        # Se memory_mb não foi fornecido ou é 0, tentar coletar via tracemalloc
        if memory_mb <= 0:
            try:
                current, peak = tracemalloc.get_traced_memory()
                memory_mb = peak / (1024 * 1024)  # Converter de bytes para MB
            except Exception:
                memory_mb = 0.0  # Fallback se tracemalloc não disponível
        else:
            # Marcar que foi fornecido pelo usuário
            memory_mb = float(memory_mb)

        # Calcular eficiência (operations per MB per ms)
        if memory_mb > 0:
            efficiency = duration_ms / memory_mb if memory_mb > 0 else float('inf')
        else:
            efficiency = duration_ms
            memory_mb = 0.0

        # Gerar sugestões baseadas nos dados
        suggestions = []

        if duration_ms > 1000:
            suggestions.append("Operação lenta (>1s) - considerar otimização de algoritmo")

        if memory_mb > 100:
            suggestions.append("Alto uso de memória (>100MB) - considerar processamento em batches")

        if efficiency > 50:
            suggestions.append("Baixa eficiência - revisar complexidade do algoritmo")

        # Se nenhuma sugestão específica, adicionar geral
        if not suggestions:
            suggestions.append("Desempenho dentro dos parâmetros esperados")

        return {
            "success": True,
            "memory_usage_mb": round(memory_mb, 2),
            "duration_ms": duration_ms,
            "efficiency_score": round(efficiency, 2),
            "suggestions": suggestions,
            "operation": operation,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "operation": operation
        }