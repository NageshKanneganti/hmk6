'''app/plugins/history/__init__.py'''
from app.commands import Command
from app.calculator.calc_history import CalculationHistory
import logging

class HistoryCommand(Command):
    '''A command class to manage calculation history'''

    def execute(self):
        '''Execute the HistoryCommand'''
        
        logging.info("Command 'history' from plugin 'menu' selected.\n")
        print("Choose an option:")
        print("1. Retrieve the most recent calculation")
        print("2. Retrieve all calculations so far")
        print("3. Clear calculation history")
        choice = input("Enter your choice: ")

        if choice == '1':
            self.retrieve_latest_calculation()
        elif choice == '2':
            self.retrieve_all_calculations()
        elif choice == '3':
            self.clear_history()
        else:
            print("Invalid choice")

    def retrieve_latest_calculation(self):
        '''Retrieve the most recent calculation from the history and print its result'''
        latest_calculation = CalculationHistory.get_latest_history()
        self.print_result(latest_calculation)

    def retrieve_all_calculations(self):
        '''Retrieve all calculations from the history and print their results'''
        all_calculations = CalculationHistory.get_history()
        print("All Calculations:")
        for calculation in all_calculations:
            self.print_result(calculation)

    def clear_history(self):
        '''Clear the calculation history'''
        CalculationHistory.clear_history()
        print("Calculation history cleared.")

    def print_result(self, calculation):
        '''Print the result of a calculation, handling cases where the calculation is undefined'''
        try:
            result = calculation.compute()
            print(f"{calculation} results in {result}")
        except:
            print(f"{calculation} is undefined.")
