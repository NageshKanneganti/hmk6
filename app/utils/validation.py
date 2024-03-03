'''utils/validation.py: validate user input'''
from decimal import Decimal, InvalidOperation

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
    while True:
        num_str = input(prompt)
        try:
            num = Decimal(num_str)  # Attempt to convert to Decimal
            return num
        except InvalidOperation:
            print("Invalid input. Please enter a valid number.")
