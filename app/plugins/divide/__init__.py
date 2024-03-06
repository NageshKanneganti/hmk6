'''app/plugins/divide/__init__.py'''
from app.commands import Command
from app.calculator import Calculator
from app.utils.validation import validate_decimal_input
import logging

class DivideCommand(Command):
    '''A command class to perform division.'''
    def execute(self):
        '''
        Execute the DivideCommand.

        This method prompts the user to enter two numbers and performs division.
        '''
        logging.info("Command 'divide' from plugin 'menu' selected.")

        num1 = validate_decimal_input("Enter the first number: ")
        num2 = validate_decimal_input("Enter the second number: ")

        try:
            logging.info("Performing division...")
            result = Calculator.divide(num1, num2)
            print(f"The result of {num1} / {num2} is: {result}")
            return result
        except ValueError:
            logging.info("User attempted undefined calculation...")
            print("Cannot divide by zero.")
            return "Cannot divide by zero."
