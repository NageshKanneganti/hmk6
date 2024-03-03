'''app/calculator/calc_history.py: Manages history of calculations. Contains methods for adding to, clearing, and retrieving calculation history.'''
from typing import List
from app.calculator.calculation import Calculation

class CalculationHistory():
    '''Manage a singular history of many calculations.'''
    # Class variable history represents a list that will store instances of the 'Calculation' class.
    history: List[Calculation] = []

    @classmethod
    def add_calculation(cls, calculation: Calculation):
        '''Add a new calculation to the history: 'Calculation' object is added to history'''
        cls.history.append(calculation)

    @classmethod
    def get_history(cls) -> List[Calculation]:
        '''Retrieve the entire history of calculations'''
        return cls.history
    
    @classmethod
    def clear_history(cls):
        '''Clears the history of calculations'''
        return cls.history.clear()
    
    @classmethod
    def get_lastest_history(cls):
        '''Retrieves the most recent calculation & returns None if there are no calculations in history'''
        if cls.history:
            return cls.history[-1]
        else:
            return None
