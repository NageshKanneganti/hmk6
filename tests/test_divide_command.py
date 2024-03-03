'''Tests for app/plugins/divide/__init__.py'''
from decimal import Decimal
from unittest.mock import patch
from app.plugins.divide import DivideCommand

# decorator is used to temporarily replace objects with mock objects during the execution of the test.
@patch('builtins.input', side_effect=['6', '2'])
@patch('app.calculator.Calculator.divide', return_value=Decimal('3'))
def test_execute(mock_calculator_divide, mock_input):
    '''Test execute function of DivideCommand.'''
    command = DivideCommand()
    result = command.execute()
    assert result == Decimal('3'), "The result of division should be Decimal('3')"

@patch('builtins.input', side_effect=['6', '0'])
def test_execute_divide_by_zero(mock_input):
    '''Test execute function of DivideCommand with division by zero.'''
    command = DivideCommand()
    result = command.execute()
    assert result == "Cannot divide by zero.", "Division by zero should return 'Cannot divide by zero.'"
