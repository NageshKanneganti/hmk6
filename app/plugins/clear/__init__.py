'''app/plugins/clear/__init__.py'''
import os
from app.commands import Command
import logging

class ClearCommand(Command):
    '''A command class to clear the command line.'''
    
    def execute(self):
        '''Execute the ClearCommand'''
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear command line
        logging.info("Command line cleared. Application in progress...")
        print("\nWelcome to my basic calculator program.\n\tType 'menu' to see available commands. Type 'exit' to quit application.")
