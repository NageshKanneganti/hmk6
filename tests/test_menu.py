'''Tests for app/plugins/menu/__init__.py'''
from app.commands import CommandHandler
from app.plugins.menu import MenuCommand

def test_execute(capsys):
    '''Test execute function of MenuCommand.'''
    # Create a CommandHandler instance and register some commands for testing
    command_handler = CommandHandler()
    command_handler.register_command("add", None)
    command_handler.register_command("subtract", None)
    command_handler.register_command("multiply", None)

    # Execute the MenuCommand and capture the standard output
    command = MenuCommand(command_handler)
    command.execute()

    # Get the captured output
    captured_output = capsys.readouterr().out

    # Get the list of registered commands from the CommandHandler
    registered_commands = command_handler.commands

    # Generate the expected output dynamically based on the registered commands
    expected_output = "Available Commands:\n"
    for command_name in registered_commands:
        expected_output += f"\t- {command_name}\n" # pylint: disable=consider-using-join

    # Assert that the captured output matches the expected menu
    assert captured_output == expected_output, "Generated menu does not match expected output"
