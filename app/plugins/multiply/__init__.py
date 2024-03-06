'''app/plugins/multiply/__init__.py'''
from app.commands import Command
from app.calculator import Calculator
from app.utils.validation import validate_decimal_input
import logging

class MultiplyCommand(Command):
    '''A command class to perform multiplication.'''
    def execute(self):
        '''
        Execute the MultiplyCommand.

        This method prompts the user to enter two numbers and performs multiplication.
        '''
        logging.info("Command 'multiply' from plugin 'menu' selected.")    
        num1 = validate_decimal_input("Enter the first number: ")
        num2 = validate_decimal_input("Enter the second number: ")

        logging.info("Performing multiplication...")
        result = Calculator.multiply(num1, num2)
        print(f"The result of {num1} * {num2} is: {result}")
        return result
