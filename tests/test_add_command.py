'''Tests for app/plugins/add/__init__.py'''
from decimal import Decimal
from unittest.mock import patch
from app.plugins.add import AddCommand

# decorator is used to temporarily replace objects with mock objects during the execution of the test.
@patch('builtins.input', side_effect=['2', '3'])
@patch('app.calculator.Calculator.add', return_value=Decimal('5'))
def test_execute(mock_calculator_add, mock_input):
    '''Test execute function of AddCommand.'''
    command = AddCommand()
    result = command.execute()
    assert result == Decimal('5'), "The result of addition should be Decimal('5')"
