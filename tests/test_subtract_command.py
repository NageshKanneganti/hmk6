'''Tests for app/plugins/subtract/__init__.py'''
from decimal import Decimal
from unittest.mock import patch
from app.plugins.subtract import SubtractCommand

# decorator is used to temporarily replace objects with mock objects during the execution of the test.
@patch('builtins.input', side_effect=['5', '3'])
@patch('app.calculator.Calculator.subtract', return_value=Decimal('2'))
def test_execute(mock_calculator_subtract, mock_input):
    '''Test execute function of SubtractCommand.'''
    command = SubtractCommand()
    result = command.execute()
    assert result == Decimal('2'), "The result of subtraction should be Decimal('2')"
