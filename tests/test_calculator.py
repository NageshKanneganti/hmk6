'''Test File: app/calculator/__init__.py'''
# Disable specific pylint warnings that are not relevant for this file.
# pylint: disable=unnecessary-dunder-call, invalid-name
import pytest
from app.calculator import Calculator

def test_calculator_operations(a, b, operation, expected):
    '''Test Calculator class _perform_calculations method'''
    assert operation(a, b) == expected, f"Failed {operation.__name__} operation with {a} and {b}"

def test_addition():
    '''Test that calculator add function works '''    
    assert Calculator.add(2,2) == 4

def test_subtraction():
    '''Test that calculator subtract function works '''    
    assert Calculator.subtract(2,2) == 0

def test_multiply():
    '''Test that calculator multiply function works '''    
    assert Calculator.multiply(2,2) == 4

def test_divide():
    '''Test that calculator divide function works '''    
    assert Calculator.divide(2,2) == 1

def test_calculator_divide_by_zero():
    '''Test calculator divide by zero exception'''
    with pytest.raises(ValueError):
        Calculator.divide(2, 0)
