'''app/plugins/add/__init__.py'''
from app.commands import Command
from app.calculator import Calculator
from app.utils.validation import validate_decimal_input
import logging

class AddCommand(Command):
    '''A command class to perform addition.'''

    def execute(self):
        '''
        Execute the AddCommand.

        This method prompts the user to enter two numbers and performs addition.
        '''
        logging.info("Command 'add' from plugin 'menu' selected.")
        num1 = validate_decimal_input("Enter the first number: ")
        num2 = validate_decimal_input("Enter the second number: ")

        logging.info("Performing addition...")
        result = Calculator.add(num1, num2)
        print(f"The result of {num1} + {num2} is: {result}")
        return result # for test_add_command.py
