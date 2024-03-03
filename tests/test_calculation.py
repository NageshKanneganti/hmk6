'''Test File: app/calculator/calculation.py'''
# Disable specific pylint warnings that are not relevant for this file.
# pylint: disable=unnecessary-dunder-call, invalid-name
from decimal import Decimal
import pytest
from app.calculator.calculation import Calculation
from app.calculator.operations import Operations as op

def test_calculation_operations(a, b, operation, expected):
    ''' Test calculation compute method with various scenarios'''
    calc = Calculation.create_calculation(a, b, operation)
    assert calc.compute() == expected, f"Failed {operation.__name__} operation with {a} and {b}"

def test_calculation_divide_by_zero():
    '''Tests divide by zero exception'''
    with pytest.raises(ValueError):
        calc = Calculation(Decimal('5'), Decimal('0'), op.division)
        calc.compute()

def test_calculation_string_representation():
    '''Test __repr__ of Calculation class. Determines if string representation is accurate.'''
    str_rep = Calculation.create_calculation(Decimal('10'), Decimal('5'), op.addition)
    expected_rep = "Calculation(10, 5, addition)"
    assert str_rep.__repr__() == expected_rep, "The __repr__ method output does not match the expected string"
