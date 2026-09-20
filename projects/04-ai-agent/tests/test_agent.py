"""Tests for the AI Agent application."""

from app.tools.calculator import CalculatorTool
from app.tools.registry import ToolRegistry


def test_calculator_addition():
    """Calculator can add numbers."""
    calc = CalculatorTool()
    result = calc.execute(expression="2 + 3")
    assert result == 5.0


def test_calculator_complex_expression():
    """Calculator handles complex expressions."""
    calc = CalculatorTool()
    result = calc.execute(expression="(10 + 5) * 2 - 3")
    assert result == 27.0


def test_calculator_division_by_zero():
    """Calculator raises on division by zero."""
    import pytest

    calc = CalculatorTool()
    with pytest.raises(ValueError):
        calc.execute(expression="1 / 0")


def test_tool_registry():
    """Tools can be registered and retrieved."""
    registry = ToolRegistry()
    calc = CalculatorTool()
    registry.register(calc)
    assert registry.get("calculator") is calc
    assert len(registry.list_tools()) == 1
