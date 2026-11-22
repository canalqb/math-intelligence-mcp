content = open("C:\\Users\\Qb\\Desktop\\sequenciadores\\lp\\mcp\\python\\calculus_operations.py", "r", encoding="utf-8").read()

new_function = '''

def perform_calculus(expression: str, variable: str = "x", operation: str = "diff",
                     point: Optional[float] = None, order: Optional[int] = None) -> Dict[str, Any]:
    """Executa operação de cálculo solicitada.
    
    Args:
        expression: Expressão matemática
        variable: Variável para operação
        operation: "diff" | "integrate" | "limit" | "series"
        point: Ponto para derivada/limite (None para geral)
        order: Ordem da série de Taylor (se operation=series)
    
    Returns:
        Dict com success, result, steps, error
    """
    try:
        x = sp.Symbol(variable)
        expr = sp.sympify(expression)
        
        if operation == "diff":
            deriv = sp.diff(expr, x)
            return {
                "success": True,
                "expression": expression,
                "variable": variable,
                "operation": "diff",
                "result": sp.simplify(deriv),
                "result_latex": sp.latex(deriv)
            }
        
        elif operation == "integrate":
            result = sp.integrate(expr, x)
            return {
                "success": True,
                "expression": expression,
                "variable": variable,
                "operation": "integrate",
                "result": sp.simplify(result),
                "result_latex": sp.latex(result)
            }
        
        elif operation == "limit":
            if point is None:
                return {
                    "success": False,
                    "error": "Limite requer ponto de avaliação",
                    "expression": expression
                }
            lim = sp.limit(expr, x, point)
            return {
                "success": True,
                "expression": expression,
                "variable": variable,
                "operation": "limit",
                "point": point,
                "result": sp.simplify(lim),
                "result_latex": sp.latex(lim)
            }
        
        elif operation == "series":
            if order is None:
                return {
                    "success": False,
                    "error": "Série requer ordem (número de termos)",
                    "expression": expression
                }
            series = sp.series(expr, x, 0, order)
            return {
                "success": True,
                "expression": expression,
                "variable": variable,
                "operation": "series",
                "order": order,
                "result": series
            }
        
        else:
            return {
                "success": False,
                "error": f"Operação '{operation}' não suportada. Use: diff, integrate, limit, series",
                "expression": expression
            }
    
    except sp.SympyError as e:
        return {
            "success": False,
            "error": f"Erro de sintaxe simbólica: {str(e)}",
            "expression": expression
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression
        }
'''

# Find the line with "def limit(" and insert after it
lines = content.split('\n')
insert_pos = None
for i, line in enumerate(lines):
    if 'def limit(expression: str, variable: str = "x", point' in line:
        # Find the end of this function (next def or end of file)
        insert_pos = i + 1
        # Skip past any empty lines between def and its body end
        while insert_pos < len(lines) and lines[insert_pos].strip() == '':
            insert_pos += 1
        break

if insert_pos is None:
    # Fallback: append at end
    insert_pos = len(lines)

# Insert the new function
new_lines = lines[:insert_pos] + [new_function.strip()] + lines[insert_pos:]

with open("C:\\Users\\Qb\\Desktop\\sequenciadores\\lp\\mcp\\python\\calculus_operations.py", "w", encoding="utf-8") as f:
    f.write('\n'.join(new_lines))

print(f"Function appended at line {insert_pos}")