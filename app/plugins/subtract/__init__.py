'''app/plugins/subtract/__init__.py'''
from app.commands import Command
from app.calculator import Calculator
from app.utils.validation import validate_decimal_input
import logging

class SubtractCommand(Command):
    '''A command class to perform subtraction.'''
    def execute(self):
        '''
        Execute the SubtractCommand.

        This method prompts the user to enter two numbers and performs subtraction.
        '''
        logging.info("Command 'subtract' from plugin 'menu' selected.")
        num1 = validate_decimal_input("Enter the first number: ")
        num2 = validate_decimal_input("Enter the second number: ")

        logging.info("Performing subtraction...")
        result = Calculator.subtract(num1, num2)
        print(f"The result of {num1} - {num2} is: {result}")
        return result
