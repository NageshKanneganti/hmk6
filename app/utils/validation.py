'''utils/validation.py: validate user input'''
from decimal import Decimal, InvalidOperation
import logging

def validate_decimal_input(prompt):
    '''
    Validate user input as a Decimal.

    Prompts the user with the provided prompt message and continuously
    reads input until a valid Decimal value is entered.

    Args:
        prompt (str): The message to display to the user as a prompt.

    Returns:
        Decimal: The validated Decimal value entered by the user.
    '''
    logging.info("User validation in progress.")
    while True:
        num_str = input(prompt)
        try:
            num = Decimal(num_str)  # Attempt to convert to Decimal
            logging.info("User entered VALID input.")
            return num
        except InvalidOperation:
            logging.info("User entered INVALID input")
            print("Invalid input. Please enter a valid number.")
