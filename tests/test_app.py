'''Test for app/__init__.py'''
import pytest
from app import App

def test_app_start_exit_command(capfd, monkeypatch):
    '''Test that the REPL exits correctly on 'exit' command.'''
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.type == SystemExit

def test_app_start_unknown_command(capfd, monkeypatch):
    '''Test how the REPL handles an unknown command before exiting.'''
    # Simulate user entering an unknown command followed by 'exit'
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()

    with pytest.raises(SystemExit) as excinfo: # pylint: disable=unused-variable
        app.start()

    # Optionally, check for specific exit code or message
    # assert excinfo.value.code == expected_exit_code

    # Verify that the unknown command was handled as expected
    captured = capfd.readouterr()
    assert "No such command: unknown_command" in captured.out

def test_get_environment_variable():
    '''Test the getEnvironmentVariable function.'''
    # Create an instance of the App class
    app = App()

    # Define environment variables for testing
    test_environment = {
        'ENVIRONMENT': 'TESTING',
        'API_KEY': '123456789'
    }

    # Update the settings dictionary with test environment variables
    app.settings.update(test_environment)

    # Test retrieving existing environment variable
    assert app.get_environment_variable('ENVIRONMENT') == 'TESTING'

    # Test retrieving non-existing environment variable with default value
    assert app.get_environment_variable('NON_EXISTING_KEY', 'DEFAULT_VALUE') == 'DEFAULT_VALUE'
