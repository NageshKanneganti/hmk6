'''app/calculator/operation.py: Contains simple arithmetic operations: addition, subtraction, multiplication, and division'''
from decimal import Decimal # Define operation functions with type hints

class Operations():
    '''Basic arithemtic operations'''
    
    @staticmethod
    def addition(a: Decimal, b: Decimal) -> Decimal:
        '''Basic addition: returns sum of a & b'''
        return a + b

    @staticmethod
    def subtraction(a: Decimal, b: Decimal) -> Decimal:
        '''Basic subtraction: returns difference of a & b'''
        return a - b
    
    @staticmethod
    def multiplication(a: Decimal, b: Decimal) -> Decimal:
        '''Basic multiplication: returns product of a & b'''
        return a * b

    @staticmethod
    def division(a: Decimal, b: Decimal) -> Decimal:
        '''Basic division: returns quotient of a (dividend) & b (divisor); catch divide by zero exception'''
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        else:
            return a / b
