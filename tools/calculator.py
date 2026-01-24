"""
Calculator Tool - Performs mathematical calculations.
"""

import math
import re
from typing import Dict
from sympy import sympify, symbols, solve, diff, integrate, simplify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

from .base_tool import BaseTool


class CalculatorTool(BaseTool):
    """Advanced calculator with support for complex mathematical operations."""
    
    def __init__(self):
        super().__init__()
        self.name = "calculator"
        self.description = """Perform mathematical calculations. Supports:
        - Basic arithmetic: +, -, *, /, ^, %
        - Functions: sin, cos, tan, log, sqrt, abs, exp
        - Constants: pi, e
        - Algebra: solve equations, simplify expressions
        - Calculus: derivatives, integrals
        Examples: "2 + 2", "sqrt(16)", "sin(pi/2)", "solve x^2 - 4 = 0", "derivative of x^3"""
        
        self.parameters = {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
        
        # Safe math functions
        self.safe_functions = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
            'log': math.log, 'log10': math.log10, 'log2': math.log2,
            'exp': math.exp, 'sqrt': math.sqrt, 'abs': abs,
            'pow': pow, 'round': round, 'floor': math.floor, 'ceil': math.ceil,
            'pi': math.pi, 'e': math.e,
            'factorial': math.factorial, 'gcd': math.gcd,
        }
    
    def execute(self, expression: str) -> str:
        """Execute the calculation."""
        try:
            expression = expression.strip()
            
            # Handle special operations
            if expression.lower().startswith("solve"):
                return self._solve_equation(expression)
            elif "derivative" in expression.lower() or "diff" in expression.lower():
                return self._calculate_derivative(expression)
            elif "integral" in expression.lower() or "integrate" in expression.lower():
                return self._calculate_integral(expression)
            elif "simplify" in expression.lower():
                return self._simplify_expression(expression)
            else:
                return self._basic_calculate(expression)
                
        except Exception as e:
            return f"❌ Calculation error: {str(e)}"
    
    def _basic_calculate(self, expression: str) -> str:
        """Perform basic calculation."""
        # Replace common notations
        expression = expression.replace('^', '**')
        expression = expression.replace('×', '*')
        expression = expression.replace('÷', '/')
        
        try:
            # Try with sympy for symbolic math
            result = sympify(expression)
            numeric_result = float(result.evalf())
            
            # Format the result nicely
            if numeric_result == int(numeric_result):
                return f"✅ Result: {int(numeric_result)}"
            else:
                return f"✅ Result: {numeric_result:.10g}"
        except:
            # Fallback to eval with safe functions
            result = eval(expression, {"__builtins__": {}}, self.safe_functions)
            return f"✅ Result: {result}"
    
    def _solve_equation(self, expression: str) -> str:
        """Solve an equation."""
        # Extract the equation part
        equation = re.sub(r'solve\s*', '', expression, flags=re.IGNORECASE)
        equation = equation.replace('=', '-').replace('^', '**')
        
        x = symbols('x')
        solutions = solve(sympify(equation), x)
        
        if solutions:
            sol_str = ', '.join([str(s) for s in solutions])
            return f"✅ Solutions: x = {sol_str}"
        else:
            return "❌ No solutions found"
    
    def _calculate_derivative(self, expression: str) -> str:
        """Calculate derivative."""
        # Extract function
        match = re.search(r'(?:derivative|diff)(?:\s+of)?\s+(.+)', expression, re.IGNORECASE)
        if match:
            func = match.group(1).replace('^', '**')
            x = symbols('x')
            derivative = diff(sympify(func), x)
            return f"✅ Derivative: d/dx({func}) = {derivative}"
        return "❌ Could not parse the expression"
    
    def _calculate_integral(self, expression: str) -> str:
        """Calculate integral."""
        match = re.search(r'(?:integral|integrate)(?:\s+of)?\s+(.+)', expression, re.IGNORECASE)
        if match:
            func = match.group(1).replace('^', '**')
            x = symbols('x')
            integral = integrate(sympify(func), x)
            return f"✅ Integral: ∫({func})dx = {integral} + C"
        return "❌ Could not parse the expression"
    
    def _simplify_expression(self, expression: str) -> str:
        """Simplify an expression."""
        match = re.search(r'simplify\s+(.+)', expression, re.IGNORECASE)
        if match:
            expr = match.group(1).replace('^', '**')
            simplified = simplify(sympify(expr))
            return f"✅ Simplified: {simplified}"
        return "❌ Could not parse the expression"