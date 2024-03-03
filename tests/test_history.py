'''Test File: app/calculator/calc_history.py'''
from decimal import Decimal
import pytest
from app.calculator.calc_history import CalculationHistory as his
from app.calculator.calculation import Calculation as calc
from app.calculator.operations import Operations as op

@pytest.fixture
def setup_calculations():
    '''Set up simple calculations to test calc_history.py'''
    his.clear_history()
    his.add_calculation(calc(Decimal('10'), Decimal('5'), op.addition))
    his.add_calculation(calc(Decimal('20'), Decimal('3'), op.subtraction))

def test_add_calculation(setup_calculations):
    '''Tests that a calculation is added to history'''
    new_calc = calc.create_calculation(Decimal('2'), Decimal('2'), op.addition)
    his.add_calculation(new_calc)
    assert his.get_lastest_history() == new_calc, "Failed to add the calculation to the history"

def test_get_history(setup_calculations):
    '''Test retrieving the entire calculation history'''
    history = his.get_history()
    assert len(history) == 2, "History does not contain the expected number of calculations"

def test_clear_history(setup_calculations):
    '''Test clearing the entire calculation history'''
    his.clear_history()
    assert len(his.get_history()) == 0, "History was not cleared"

def test_get_latest_history(setup_calculations):
    '''Test getting the latest calculation from the history'''
    latest = his.get_lastest_history()
    assert latest.a == Decimal('20') and latest.b == Decimal('3'), "Did not get the correct latest calculation"

def test_get_latest_history_with_empty_history():
    '''Test getting the latest calculation when the history is empty'''
    his.clear_history()
    assert his.get_lastest_history() is None, "Expected None for latest calculation with empty history"
