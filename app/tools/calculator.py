from langchain_core.tools import tool

@tool
def calculator(a: float, b: float, operator: str) -> float | str:
    """Perform a simple math operation on two numbers. Supported operators: +, -, *, /"""
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        if b == 0:
            return "Error: Division by zero"
        return a / b
    return f"Error: Unsupported operator {operator}"
