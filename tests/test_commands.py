'''Tests app/commands/__init__.py'''
import pytest
from app.commands import Command, CommandHandler

class MockCommand(Command):
    '''Mock command class for testing.'''
    def execute(self):
        '''Mock execute method.'''

def test_register_command():
    '''Test registering a command.'''
    handler = CommandHandler()
    command = MockCommand()
    handler.register_command("test", command)
    assert "test" in handler.commands
    assert handler.commands["test"] == command

def test_execute_command():
    '''Test executing a registered command.'''
    handler = CommandHandler()
    command = MockCommand()
    handler.register_command("test", command)
    handler.execute_command("test")

# pylint: disable=pointless-string-statement
"""
def test_execute_command_invalid(capfd):
    '''Test executing an invalid command.'''
    handler = CommandHandler()

    # Execute an invalid command
    handler.execute_command("invalid_command")

    # Capture stdout and assert that the error message is printed
    captured = capfd.readouterr()
    assert "No such command: invalid_command" in captured.out
"""
# pylint: disable=pointless-string-statement

def test_execute_command_unknown_command():
    '''Test executing an unknown command.'''
    handler = CommandHandler()

    # Test whether KeyError is raised with the correct message
    with pytest.raises(KeyError) as exc_info:
        handler.execute_command("unknown_command")

    # Assert on the exception message
    assert str(exc_info.value) == "'Unknown command: unknown_command'"
