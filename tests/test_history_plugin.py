'''Test for app/plugins/history/__init__.py'''
# Disable specific pylint warnings that are not relevant for this file.
# pylint: disable=unnecessary-dunder-call, invalid-name
import unittest
from decimal import Decimal
from unittest.mock import patch, MagicMock
from io import StringIO
from app.plugins.history import HistoryCommand
from app.calculator.calculation import Calculation
from app.calculator.operations import Operations

class TestHistoryCommandExecute(unittest.TestCase):
    '''Test case for the execute method of the HistoryCommand class.'''

    @patch('app.plugins.history.HistoryCommand.retrieve_latest_calculation')
    def test_process_choice_valid(self, mock_retrieve_latest):
        '''Testing process choice'''
        history_command = HistoryCommand()
        history_command.process_choice('1')  # Assuming '1' is a valid choice
        mock_retrieve_latest.assert_called_once()

    @patch('app.calculator.calc_history.CalculationHistory.get_latest_history')
    def test_execute_prints_latest_calculation_and_exits(self, mock_get_latest_history):
        '''Test whether execute method prints the latest calculation and then exits correctly.'''

        # Mocking the latest calculation
        mock_operation = Operations.addition
        mock_calculation = Calculation(2, 3, mock_operation)
        mock_get_latest_history.return_value = mock_calculation

        # Redirect stdout to capture print statements and simulate user input
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect=['1', 'back']):  # Simulate choosing option 1 then exiting
                HistoryCommand().execute()

                # Check if the expected output is in stdout
                expected_output = f"{mock_calculation} results in 5"  # Adjust based on the actual output format
                output = mock_stdout.getvalue().strip()
                self.assertIn(expected_output, output)

    @patch('app.calculator.calc_history.CalculationHistory.get_latest_history', return_value=None)
    @patch('builtins.print')
    def test_retrieve_latest_calculation_no_history(self, mock_print, mock_get_latest_history):
        '''Testing retrieve latest history'''
        history_command = HistoryCommand()
        history_command.retrieve_latest_calculation()
        mock_print.assert_called_once_with("There are no calculations in history.")

    @patch('app.calculator.calc_history.CalculationHistory.clear_history')
    @patch('builtins.print')
    def test_clear_history(self, mock_print, mock_clear_history):
        '''Testing clear history'''
        history_command = HistoryCommand()
        history_command.clear_history()
        mock_clear_history.assert_called_once()  # Verify clear_history was called
        mock_print.assert_called_once_with("Calculation history cleared.")  # Verify the user is notified

    @patch('builtins.print')
    def test_print_result_with_undefined_calculation(self, mock_print):
        '''Tests print_result method exception'''
        # Mock a calculation object with a compute method that raises an exception
        mock_calculation = MagicMock()
        mock_calculation.compute.side_effect = Exception("Undefined calculation")

        # Create an instance of HistoryCommand
        history_command = HistoryCommand()

        # Call print_result with the mock calculation
        history_command.print_result(mock_calculation)

        # Check if the correct message is printed
        expected_message = f"{mock_calculation} is undefined."
        mock_print.assert_called_once_with(expected_message)

    @patch('app.plugins.history.CalculationHistory.get_history')
    @patch('builtins.print')
    def test_retrieve_all_calculations_value_error(self, mock_print, mock_get_history):
        '''Test handling of ValueError in retrieve_all_calculations method.'''
        # Create a mock Calculation object with compute method raising ValueError
        mock_calculation = MagicMock()
        mock_calculation.compute.side_effect = ValueError("Undefined calculation")

        # Configure get_history to return a list containing the mock Calculation
        mock_get_history.return_value = [mock_calculation]

        history_command = HistoryCommand()
        history_command.retrieve_all_calculations()

        # Verify the print function was called with a message containing "is undefined."
        assert any("is undefined." in call_args[0][0] for call_args in mock_print.call_args_list), "Expected message about an undefined calculation was not printed."

    # Tests for csv methods
    @patch('app.calculator.calc_history.CalculationHistory.save_history_to_csv')
    def test_save_history_to_csv(self, mock_save_history):
        '''Test saving the history to a CSV file.'''
        with patch('builtins.input', side_effect=['4', 'back']), patch('sys.stdout', new=StringIO()):
            HistoryCommand().execute()
        mock_save_history.assert_called_once()

    @patch('app.calculator.calc_history.CalculationHistory.load_history_from_csv')
    def test_load_history_from_csv(self, mock_load_history):
        '''Test loading the history from a CSV file.'''
        with patch('builtins.input', side_effect=['5', 'back']), patch('sys.stdout', new=StringIO()):
            HistoryCommand().execute()
        mock_load_history.assert_called_once()

    @patch('app.calculator.calc_history.CalculationHistory.load_history_from_csv')
    @patch('builtins.print')
    def test_load_history_from_csv_with_exception(self, mock_print, mock_load_history):
        '''Test handling of an exception when loading the history from a CSV file.'''

        # Setup the mock to raise an exception when called
        mock_load_history.side_effect = Exception("Failed to load CSV")

        # Call the load_history method
        history_command = HistoryCommand()
        history_command.load_history()

        # Check if the correct error message is printed
        mock_print.assert_called_with("\nError loading history: Failed to load CSV")

    @patch('app.plugins.history.CalculationHistory.load_history_from_csv')
    @patch('app.plugins.history.CalculationHistory.get_history', return_value=[])
    @patch('builtins.print')
    def test_load_history_with_empty_or_invalid_calculations(self, mock_print, mock_get_history, mock_load_history_from_csv):
        '''Test loading history from CSV when the file is empty or contains no valid calculations.'''

        history_command = HistoryCommand()
        history_command.load_history()

        # Check if the correct message is printed indicating the history is empty or invalid
        mock_print.assert_called_with("\nThe history CSV file is empty.")

    @patch('app.calculator.calc_history.CalculationHistory.delete_calculation_by_index')
    @patch('app.calculator.calc_history.CalculationHistory.get_history', return_value=[Calculation(Decimal('2'), Decimal('3'), Operations.addition)])
    def test_delete_specific_calculation(self, mock_get_history, mock_delete_calculation):
        '''Test deleting a specific calculation by index.'''
        with patch('builtins.input', side_effect=['6', '0', 'back']), patch('sys.stdout', new=StringIO()):
            HistoryCommand().execute()
        mock_delete_calculation.assert_called_once_with(0)

    @patch('app.calculator.calc_history.CalculationHistory.delete_calculation_by_index')
    @patch('builtins.print')
    def test_delete_specific_calculation_value_error(self, mock_print, _):
        '''Test handling of ValueError when deleting a specific calculation.'''

        # Mock input to return a non-numeric value, simulating a ValueError
        with patch('builtins.input', return_value='not_a_number'):
            history_command = HistoryCommand()
            history_command.delete_specific_calculation()

            # Check if the correct error message is printed
            mock_print.assert_called_with("Invalid index. Please enter a numerical index.")

    @patch('app.calculator.calc_history.CalculationHistory.get_history', return_value=[])
    def test_attempt_to_delete_from_empty_history(self, mock_get_history):
        '''Test attempting to delete a calculation when history is empty.'''
        with patch('builtins.input', side_effect=['6', '0', 'back']), patch('sys.stdout', new=StringIO()) as mock_stdout:
            HistoryCommand().execute()
        self.assertIn("There are no calculations in history.", mock_stdout.getvalue())

    def test_invalid_choice(self):
        '''Test handling of invalid menu choice.'''
        with patch('builtins.input', side_effect=['invalid', 'back']), patch('sys.stdout', new=StringIO()) as mock_stdout:
            HistoryCommand().execute()
        self.assertIn("Invalid choice", mock_stdout.getvalue())

    @patch('app.calculator.calc_history.CalculationHistory.delete_calculation_by_index')
    @patch('app.calculator.calc_history.CalculationHistory.get_history', return_value=[])
    @patch('builtins.input', return_value='1')  # Assume an out-of-range index
    @patch('builtins.print')
    def test_delete_specific_calculation_index_error(self, mock_print, mock_input, mock_get_history, mock_delete_calculation_by_index):
        '''Test handling of IndexError when deleting a specific calculation.'''

        # The mock for delete_calculation_by_index should raise an IndexError
        mock_delete_calculation_by_index.side_effect = IndexError("Calculation index out of range.")

        history_command = HistoryCommand()
        history_command.delete_specific_calculation()

        # Check if the correct error message is printed
        mock_print.assert_called_with("No calculation found at the given index.")
