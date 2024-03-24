'''Test File: app/calculator/calc_history.py'''
from unittest.mock import patch
from decimal import Decimal
import pandas as pd
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
    assert his.get_latest_history() == new_calc, "Failed to add the calculation to the history"

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
    latest = his.get_latest_history()
    assert latest.a == Decimal('20') and latest.b == Decimal('3'), "Did not get the correct latest calculation"

def test_get_latest_history_with_empty_history():
    '''Test getting the latest calculation when the history is empty'''
    his.clear_history()
    assert his.get_latest_history() is None, "Expected None for latest calculation with empty history"

# Tests additional methods
def test_delete_calculation_by_index(setup_calculations):
    '''Test deleting a calculation by its index'''
    initial_len = len(his.get_history())
    his.delete_calculation_by_index(0)
    assert len(his.get_history()) == initial_len - 1, "Calculation was not deleted"
    with pytest.raises(IndexError):
        his.delete_calculation_by_index(initial_len - 1)  # Attempt to delete beyond current range

@patch('pandas.read_csv')
@patch('os.path.exists', return_value=True)
def test_load_history_from_csv(mock_exists, mock_read_csv):
    '''Test loading history from a CSV file'''
    mock_data = pd.DataFrame({
        'Operation': ['addition', 'subtraction'],
        'Operand1': [Decimal('10'), Decimal('20')],
        'Operand2': [Decimal('5'), Decimal('3')]
    })
    mock_read_csv.return_value = mock_data

    his.load_history_from_csv()
    assert len(his.get_history()) == 2, "History was not loaded correctly from CSV"

@patch('app.calculator.calc_history.os.path.exists', return_value=False)
@patch('app.calculator.calc_history.logging.info')
def test_load_history_from_csv_no_file(mock_logging_info, mock_exists):
    '''
    Test `load_history_from_csv` when the CSV file does not exist.
    Checks if the appropriate log message is recorded.
    '''
    his.load_history_from_csv()
    mock_logging_info.assert_called_with("No history file found to load.")

@patch('app.calculator.calc_history.os.path.exists', return_value=True)
@patch('app.calculator.calc_history.pd.read_csv', side_effect=pd.errors.EmptyDataError)
@patch('app.calculator.calc_history.logging.info')
def test_load_history_from_csv_empty_data(mock_logging_info, mock_read_csv, mock_exists):
    '''Tests empty data errors exception'''
    his.load_history_from_csv()
    mock_logging_info.assert_called_with("The history CSV file is empty. No history to load.")

@patch('app.calculator.calc_history.os.path.exists', return_value=True)
@patch('app.calculator.calc_history.pd.read_csv', side_effect=Exception("Generic error"))
@patch('app.calculator.calc_history.logging.error')
def test_load_history_from_csv_generic_exception(mock_logging_error, mock_read_csv, mock_exists):
    '''Tests exception'''
    his.load_history_from_csv()
    mock_logging_error.assert_called_with("An error occurred while loading history: Generic error")
