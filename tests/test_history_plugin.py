'''Test for app/plugins/history/__init__.py'''
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from app.plugins.history import HistoryCommand
from app.calculator.calculation import Calculation
from app.calculator.operations import Operations

class TestHistoryCommandExecute(unittest.TestCase):
    '''Test case for the execute method of the HistoryCommand class.'''

    @patch('app.calculator.calc_history.CalculationHistory.get_latest_history')
    def test_execute_prints_latest_calculation(self, mock_get_latest_history):
        '''Test whether execute method prints the latest calculation correctly.'''
        # Mocking the latest calculation
        mock_operation = Operations.addition
        mock_calculation = Calculation(2, 3, mock_operation)
        mock_get_latest_history.return_value = mock_calculation

        # Create an instance of HistoryCommand
        history_command = HistoryCommand()

        # Redirect stdout to capture print statements
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            # Simulate user choosing option 1
            with patch('builtins.input', side_effect=['1']):
                # Call the execute method
                history_command.execute()

            # Check the output
            expected_output = "Calculation(2, 3, addition) results in 5"
            self.assertIn(expected_output, mock_stdout.getvalue().strip())

    @patch('app.calculator.calc_history.CalculationHistory.get_history')
    def test_execute_prints_all_calculations(self, mock_get_history):
        '''Test whether execute method prints all calculations correctly.'''
        # Mocking all calculations
        mock_calculations = [
            Calculation(2, 3, Operations.addition),
            Calculation(4, 5, Operations.subtraction),
            Calculation(6, 7, Operations.multiplication)
        ]
        mock_get_history.return_value = mock_calculations

        # Create an instance of HistoryCommand
        history_command = HistoryCommand()

        # Redirect stdout to capture print statements
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            # Simulate user choosing option 2
            with patch('builtins.input', side_effect=['2']):
                # Call the execute method
                history_command.execute()

            # Check the output
            expected_output = "All Calculations:"
            self.assertIn(expected_output, mock_stdout.getvalue().strip())

    @patch('app.calculator.calc_history.CalculationHistory.clear_history')
    def test_execute_clears_history(self, mock_clear_history):
        '''Test whether execute method clears calculation history correctly.'''
        # Create an instance of HistoryCommand
        history_command = HistoryCommand()

        # Simulate user choosing option 3
        with patch('builtins.input', side_effect=['3']):
            # Call the execute method
            history_command.execute()

        # Check if clear_history method was called
        mock_clear_history.assert_called_once()

    def test_execute_invalid_choice(self):
        '''Test whether execute method handles invalid choice correctly.'''
        # Create an instance of HistoryCommand
        history_command = HistoryCommand()

        # Redirect stdout to capture print statements
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            # Simulate user entering an invalid choice
            with patch('builtins.input', side_effect=['invalid']):
                # Call the execute method
                history_command.execute()

            # Check the output
            expected_output = "Invalid choice"
            self.assertIn(expected_output, mock_stdout.getvalue().strip())

    @patch('app.calculator.calc_history.CalculationHistory.get_latest_history')
    @patch('builtins.input')
    def test_execute_handles_division_by_zero(self, mock_input, mock_get_latest_history):
        '''Test whether execute method handles division by zero correctly.'''
        # Mocking the latest calculation
        mock_operation = Operations.division
        mock_calculation = Calculation(2, 0, mock_operation)
        mock_get_latest_history.return_value = mock_calculation

        # Mock input choice
        mock_input.return_value = '1'  # Simulate user selecting option 1

        # Create an instance of HistoryCommand
        history_command = HistoryCommand()

        # Redirect stdout to capture print statements
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            # Call the execute method
            history_command.execute()

            # Check the output
            expected_output = f"{mock_calculation} is undefined."
            self.assertIn(expected_output, mock_stdout.getvalue().strip())
    @patch('app.calculator.calc_history.CalculationHistory.get_history')
    def test_execute_handles_compute_exception(self, mock_get_history):
        '''Test whether execute method handles compute exception correctly.'''
        # Mocking history with calculations
        mock_calculations = [
            Calculation(2, 0, Operations.division),  # This will cause division by zero error
            Calculation(4, 5, Operations.subtraction),
            Calculation(6, 7, Operations.multiplication)
        ]
        mock_get_history.return_value = mock_calculations

        # Create an instance of HistoryCommand
        history_command = HistoryCommand()

        # Create a MagicMock object to mock the compute() method
        mock_compute = MagicMock(side_effect=Exception("Some error occurred"))

        # Patch the Calculation class to replace compute() with the mock_compute object
        with patch('app.calculator.calculation.Calculation.compute', mock_compute):
            # Patch input() to avoid stdin capture
            with patch('builtins.input', return_value='2'):  # Simulating user choosing option 2
                # Redirect stdout to capture print statements
                with patch('sys.stdout', new=StringIO()) as mock_stdout:
                    # Call the execute method
                    history_command.execute()

                    # Check the output
                    expected_output = "Calculation(2, 0, division) is undefined."
                    self.assertIn(expected_output, mock_stdout.getvalue().strip())
