'''Tests for app/plugins/multiply/__init__.py'''
from decimal import Decimal
from unittest.mock import patch
from app.plugins.multiply import MultiplyCommand

# decorator is used to temporarily replace objects with mock objects during the execution of the test.
@patch('builtins.input', side_effect=['2', '3'])
@patch('app.calculator.Calculator.multiply', return_value=Decimal('6'))
def test_execute(mock_calculator_multiply, mock_input):
    '''Test execute function of MultiplyCommand.'''
    command = MultiplyCommand()
    result = command.execute()
    assert result == Decimal('6'), "The result of multiplication should be Decimal('6')"
