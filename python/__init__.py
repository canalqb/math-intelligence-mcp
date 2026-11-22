"""Math Intelligence MCP - Package Initialization

This package provides mathematical intelligence capabilities for AI agents
through a JSON-RPC 2.0 MCP (Math Intelligence Command Protocol) server.
"""

from . import tools
from .mimcp_server import main

# Export all tool functions for easy access
from typing import Dict, Any, List

__all__ = [
    "math_evaluate",
    "math_explain",
    "math_optimize",
    "result_verify",
    "memory_profile",
    "formula_engine",
    "symbolic_solver",
    "calculus_operations",
    "linear_algebra",
    "statistical_analysis",
    "advanced_cryptography",
    "pattern_recognition",
]

# Register all tools with the server
def register_all_tools():
    """Register all mathematical tools with the MCP server."""
    from . import tools as t

    # Register all tool functions
    registered = []

    # P0 tools (core)
    registered.append("math_evaluate")
    registered.append("math_explain")
    registered.append("math_optimize")
    registered.append("result_verify")
    registered.append("memory_profile")

    # P1 tools (advanced)
    registered.append("formula_engine")
    registered.append("symbolic_solver")
    registered.append("calculus_operations")
    registered.append("linear_algebra")
    registered.append("statistical_analysis")
    registered.append("advanced_cryptography")
    registered.append("pattern_recognition")

    return registered


def get_tool_description(tool_name: str) -> Dict[str, Any]:
    """Get description and schema for a specific tool."""
    descriptions = {
        "math_evaluate": {
            "description": "Evaluate mathematical expressions safely",
            "category": "basic",
        },
        "math_explain": {
            "description": "Provide didactic explanation of mathematical concepts",
            "category": "basic",
        },
        "math_optimize": {
            "description": "Optimize algebraic expressions and equations",
            "category": "basic",
        },
        "result_verify": {
            "description": "Verify results with tolerance checking",
            "category": "basic",
        },
        "memory_profile": {
            "description": "Profile memory and performance metrics",
            "category": "basic",
        },
        # P1 tools
        "formula_engine": {
            "description": "Solve algebraic formulas symbolically",
            "category": "advanced",
        },
        "symbolic_solver": {
            "description": "Solve equations symbolically using algebra",
            "category": "advanced",
        },
        "calculus_operations": {
            "description": "Calculate derivatives, integrals and limits",
            "category": "advanced",
        },
        "linear_algebra": {
            "description": "Solve linear systems and matrix operations",
            "category": "advanced",
        },
        "statistical_analysis": {
            "description": "Descriptive statistics and probability distributions",
            "category": "advanced",
        },
        "advanced_cryptography": {
            "description": "Modular exponentiation and discrete logarithm",
            "category": "advanced",
        },
        "pattern_recognition": {
            "description": "Detect periods, extrema and symmetry in sequences",
            "category": "advanced",
        },
    }

    return descriptions.get(
        tool_name,
        {"description": "Unknown tool", "category": "unknown"},
    )


# Initialize on import
_registered = register_all_tools()

if __name__ == "__main__":
    print("Math Intelligence MCP - Package initialized")
    print(f"Total tools registered: {_registered}")
    print(f"Available tools: {len(_registered)}")