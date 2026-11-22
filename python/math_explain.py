"""Math Intelligence MCP - Explicar Conceitos Matemáticos

Módulo P0 - Tool: math_explain
Explica conceitos matemáticos de forma didática para diferentes níveis.
"""

from typing import Dict, Any, Optional
import json


def explain_concept(topic: str, level: str = "basic") -> Dict[str, Any]:
    """Explica um conceito matemático de forma didática.
    
    Suporta tópicos de álgebra, geometria, cálculo e estatística.
    O nível controla a profundidade e complexidade da explicação.
    
    Args:
        topic: Tópico matemático (ex: "derivada", "equação do 2º grau", "pirâmide")
        level: Nível de complexidade: basic, intermediate ou advanced
    
    Returns:
        Dict com success, explanation, topic, level e examples
    """
    try:
        # Normalizar tópico
        topic_lower = topic.lower().strip()
        
        # Base de conhecimento por tópico
        knowledge_base = {
            "derivada": {
                "basic": {
                    "definition": "A derivada mede a taxa de variação de uma função em um ponto.",
                    "analogy": "Pense na derivada como a velocidade exata de um carro em um instante específico.",
                    "key_formula": "f'(x) = lim_{h→0} [f(x+h) - f(x)] / h",
                    "examples": [
                        "A derivada de x² é 2x",
                        "A derivada de sen(x) é cos(x)"
                    ]
                },
                "advanced": {
                    "definition": "A derivada generalizada para funções multidimensionais via gradiente.",
                    "analogy": "Em 3D, o gradiente aponta na direção de maior crescimento.",
                    "key_formula": "∇f = [∂f/∂x, ∂f/∂y, ∂f/∂z]",
                    "examples": [
                        "Gradiente de f(x,y) = x² + y² é [2x, 2y]"
                    ]
                }
            },
            "equação do 2º grau": {
                "basic": {
                    "definition": "Equação da forma ax² + bx + c = 0, onde a ≠ 0.",
                    "analogy": "O gráfico de uma equação do 2º grau é uma parábola.",
                    "key_formula": "x = (-b ± √(b² - 4ac)) / (2a)",
                    "examples": [
                        "Para x² - 5x + 6 = 0, x = 2 ou x = 3"
                    ]
                }
            },
            "integrais": {
                "basic": {
                    "definition": "A integral é a operação inversa da derivada, Área sob uma curva.",
                    "analogy": "Se a derivada é a velocidade, a integral é a distância percorrida.",
                    "key_formula": "∫f(x)dx = F(x) + C",
                    "examples": [
                        "∫x dx = x²/2 + C"
                    ]
                }
            }
        }
        
        # Retornar conhecimento encontrado ou padrão
        topic_data = knowledge_base.get(topic_lower, {})
        level_data = topic_data.get(level, topic_data.get("basic", {}))
        
        if not level_data:
            # Resposta padrão quando tópico não encontrado
            return {
                "success": True,
                "explanation": f"Conceito: {topic}. Esta é uma explicação geral sobre o tópico matemático solicitado.",
                "topic": topic,
                "level": level,
                "fallback": True
            }
        
        return {
            "success": True,
            "explanation": level_data.get("definition", "Definição não disponível"),
            "analogy": level_data.get("analogy", "N/A"),
            "key_formula": level_data.get("key_formula", ""),
            "examples": level_data.get("examples", []),
            "topic": topic,
            "level": level,
            "fallback": False
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "topic": topic,
            "level": level
        }