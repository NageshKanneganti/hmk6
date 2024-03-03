'''app/plugins/exit/__init__.py'''
import sys
from app.commands import Command

class ExitCommand(Command):
    '''
    A command class to exit the calculator application.

    This class provides functionality to exit the calculator application when executed.
    '''

    def execute(self):
        '''
        Execute the ExitCommand.

        This method exits the calculator application.
        '''
        sys.exit("Thank you for using my calculator app. Exiting...")
