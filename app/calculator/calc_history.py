'''app/calculator/calc_history.py: Manages history of calculations. Contains methods for adding to, clearing, and retrieving calculation history.'''
import os
import pandas as pd
from dotenv import load_dotenv
from typing import List
from decimal import Decimal
from app.calculator.calculation import Calculation
from app.calculator.operations import Operations

import logging

load_dotenv()

class CalculationHistory():
    '''Manage a singular history of many calculations.'''
    # Class variable history represents a list that will store instances of the 'Calculation' class.
    history: List[Calculation] = []

    @classmethod
    def add_calculation(cls, calculation: Calculation):
        '''Add a new calculation to the history: 'Calculation' object is added to history'''
        logging.info(f"Calculation {calculation} added to history.")
        cls.history.append(calculation)

    @classmethod
    def get_history(cls) -> List[Calculation]:
        '''Retrieve the entire history of calculations'''
        if cls.history:
            logging.info("Calculations retrieved.")
        else:
            logging.info("No calculations in history.")
        return cls.history
    
    @classmethod
    def clear_history(cls):
        '''Clears the history of calculations'''
        logging.info("History cleared.")
        return cls.history.clear()

    @classmethod
    def get_latest_history(cls):
        '''Retrieves the most recent calculation & returns None if there are no calculations in history'''
        if cls.history:
            logging.info(f"The most recent calculation is {cls.history[-1]}")
            return cls.history[-1]
        else:
            logging.info("There are no calculations in history.")
            return None

    @classmethod
    def delete_calculation_by_index(cls, index: int):
        if 0 <= index < len(cls.history):
            del cls.history[index]
            cls.save_history_to_csv()  # Optionally save the updated history to CSV
        else:
            raise IndexError("Calculation index out of range.")

    # CSV methods
    @classmethod
    def save_history_to_csv(cls):
        data_dir = os.getenv('DATA_DIR', './')
        file_name = os.getenv('CALC_HISTORY_FILE', 'calculator_history.csv')
        file_path = os.path.join(data_dir, file_name)

        # Ensure the directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Convert history to a DataFrame and save
        df = pd.DataFrame([{
            'Operation': calc.operation.__name__,
            'Operand1': calc.a,
            'Operand2': calc.b
        } for calc in cls.history])
        df.to_csv(file_path, index=False)

    @classmethod
    def load_history_from_csv(cls):
        data_dir = os.getenv('DATA_DIR', './')
        file_name = os.getenv('CALC_HISTORY_FILE', 'calculator_history.csv')
        file_path = os.path.join(data_dir, file_name)

        operation_mapping = {
            'addition': Operations.addition,
            'subtraction': Operations.subtraction,
            'multiplication': Operations.multiplication,
            'division': Operations.division,
        }

        if not os.path.exists(file_path):
            logging.info("No history file found to load.")
            return

        try:
            df = pd.read_csv(file_path)
            # Ensure only valid operations are loaded
            cls.history = [
                Calculation(
                    Decimal(row['Operand1']),
                    Decimal(row['Operand2']),
                    operation_mapping.get(row['Operation'])
                ) for index, row in df.iterrows() if row['Operation'] in operation_mapping
            ]
            logging.info("Calculation history loaded successfully.")
        except pd.errors.EmptyDataError:
            logging.info("The history CSV file is empty. No history to load.")
        except Exception as e:
            logging.error(f"An error occurred while loading history: {e}")
