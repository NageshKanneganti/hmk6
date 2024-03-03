'''Tests app/commands/__init__.py'''
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

def test_execute_command_invalid(capfd):
    '''Test executing an invalid command.'''
    handler = CommandHandler()

    # Execute an invalid command
    handler.execute_command("invalid_command")

    # Capture stdout and assert that the error message is printed
    captured = capfd.readouterr()
    assert "No such command: invalid_command" in captured.out
