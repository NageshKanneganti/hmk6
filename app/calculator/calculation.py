'''app/calculator/calculation.py: Defines a single calculation. Provides abstraction for handeling individual calculations in the Calculator class.'''
from decimal import Decimal
from typing import Callable

class Calculation:
    '''Defines a single calculation'''

    def __init__(self, a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> None:
        '''Constructor method with type hints'''
        self.a = a
        self.b = b 
        self.operation = operation 

    @staticmethod
    def create_calculation(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        '''Factory that allows us to create instances of Calculation w/out directly calling Calculation class'''
        return Calculation(a, b, operation)

    def compute(self):
        '''Call the stored operation and pass it the stored operands'''
        return self.operation(self.a, self.b)

    def __repr__(self):
        '''Returns a simple string representation of the calculation'''
        return f"Calculation({self.a}, {self.b}, {self.operation.__name__})"
