'''app/plugins/menu/__init__.py'''
from app.commands import Command
import logging

class MenuCommand(Command):
    '''
    A command class to display a dynamic menu of available commands.
    
    This class generates a menu by inspecting the registered commands in the CommandHandler
    and displays them to the user.
    '''

    def __init__(self, command_handler):
        '''
        Initialize the MenuCommand with a CommandHandler instance.

        Parameters:
        - command_handler (CommandHandler): An instance of CommandHandler to access registered commands.
        '''
        self.command_handler = command_handler

    def execute(self):
        '''
        Execute the MenuCommand.

        This method generates and displays the menu of available commands.
        '''
        logging.info("Command 'menu' from plugin 'menu' selected.")
        print("Available Commands:")
        for command_name in self.command_handler.commands:
            print("\t-", command_name)
