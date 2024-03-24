'''app/plugins/history/__init__.py'''
from app.commands import Command
from app.calculator.calc_history import CalculationHistory
import logging

class HistoryCommand(Command):
    '''A command class to manage calculation history'''

    def execute(self):
        '''Execute the HistoryCommand'''
        
        logging.info("Command 'history' from plugin 'menu' selected.\n")
        while True:  # Keep running until the user decides to exit
            print("\n--- History Menu ---")
            print("1. Retrieve the most recent calculation")
            print("2. Retrieve all calculations so far")
            print("3. Clear calculation history")
            print("4. Save calculation history to CSV")
            print("5. Load calculation history from CSV")
            print("6. Delete a specific calculation")
            print("\nType 'BACK' to return to the main menu.")
            choice = input("\nEnter your choice: ")

            if choice.lower() == 'back':
                break  # Exit the loop, ending the command

            self.process_choice(choice)

    def process_choice(self, choice):
        options = {
            '1': self.retrieve_latest_calculation,
            '2': self.retrieve_all_calculations,
            '3': self.clear_history,
            '4': self.save_history,
            '5': self.load_history,
            '6': self.delete_specific_calculation
        }
        action = options.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please select a valid option.")

    def retrieve_latest_calculation(self):
        '''Retrieve the most recent calculation from the history and print its result'''
        latest_calculation = CalculationHistory.get_latest_history()
        if latest_calculation is None:  # Check if there is no recent calculation
            print("There are no calculations in history.")
        else:
            self.print_result(latest_calculation)

    def retrieve_all_calculations(self):
        '''Retrieve all calculations from the history and print their results'''
        logging.info("Retrieving calculations...")
        all_calculations = CalculationHistory.get_history()
        if not all_calculations:  # Check if the history list is empty
            print("\nThere are no calculations in history.")
        else:
            print("\nAll Calculations with Indexes:")
            for index, calculation in enumerate(all_calculations):
                try:
                    result = calculation.compute()
                    print(f"{index}: {calculation} results in {result}")
                except ValueError:
                    print(f"{index}: {calculation} is undefined.")

    def clear_history(self):
        '''Clear the calculation history'''
        logging.info("Clearing history...")
        CalculationHistory.clear_history()
        print("Calculation history cleared.")

    def print_result(self, calculation):
        '''Print the result of a calculation, handling cases where the calculation is undefined'''
        try:
            result = calculation.compute()
            print(f"{calculation} results in {result}")
        except:
            print(f"{calculation} is undefined.")

    def save_history(self):
        '''Save history of calculations to CSV'''
        CalculationHistory.save_history_to_csv()
        print("Calculation history saved to CSV.")

    def load_history(self):
        '''Load history of calculations frmo CSV'''
        try:
            CalculationHistory.load_history_from_csv()
            # Check if any calculations were loaded
            if CalculationHistory.get_history():
                print("\nCalculation history successfully loaded from CSV.")
            else:
                print("\nThe history CSV file is empty.")
        except Exception as e:
            print(f"\nError loading history: {e}")

    def delete_specific_calculation(self):
        self.retrieve_all_calculations()  # Show all calculations with indexes for user reference
        try:
            index_to_delete = int(input("Enter the index of the calculation to delete: "))
            CalculationHistory.delete_calculation_by_index(index_to_delete)
            print(f"Calculation at index {index_to_delete} has been deleted.")
        except ValueError:
            print("Invalid index. Please enter a numerical index.")
        except IndexError:
            print("No calculation found at the given index.")
