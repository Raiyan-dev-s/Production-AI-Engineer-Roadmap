import ast
import operator

from app.tools.base import BaseTool

# Safe operators for arithmetic evaluation
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


class CalculatorTool(BaseTool):
    """Evaluates mathematical expressions safely using AST parsing.

    Supports: +, -, *, /, //, %, **
    No external dependencies — uses Python's ast module.
    """

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return (
            "Evaluates mathematical expressions. "
            "Input should be a math expression string like '2 + 3 * 4'. "
            "Supports +, -, *, /, //, %, **."
        )

    def execute(self, expression: str = "", **kwargs) -> float:
        """Safely evaluate a math expression."""
        if not expression:
            raise ValueError("No expression provided")

        try:
            tree = ast.parse(expression.strip(), mode="eval")
            return self._eval_node(tree.body)
        except (ValueError, TypeError, ZeroDivisionError) as e:
            raise ValueError(f"Math error: {e}") from e
        except SyntaxError as e:
            raise ValueError(f"Invalid expression: {expression}") from e

    def _eval_node(self, node: ast.AST) -> float:
        """Recursively evaluate an AST node."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant: {node.value}")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return SAFE_OPERATORS[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            operand = self._eval_node(node.operand)
            return SAFE_OPERATORS[op_type](operand)

        raise ValueError(f"Unsupported expression type: {type(node).__name__}")
