'''app/commands/__init__.py'''
from abc import ABC, abstractmethod
from typing import Dict

class Command(ABC):
    '''Abstract base class for commands.'''
    @abstractmethod
    def execute(self):
        '''Execute method for the command.'''
        pass  # pragma: no cover

class CommandHandler:
    def __init__(self):
        '''Class to handle registration and execution of commands.'''
        self.commands: Dict[str, Command]= {}

    def register_command(self, command_name: str, command: Command):
        '''Register a command'''
        self.commands[command_name] = command

    def execute_command(self, command_name: str):
        '''Execute a registered command by name.'''
        try:
            self.commands[command_name].execute()
        except KeyError:
            print(f"No such command: {command_name}")
