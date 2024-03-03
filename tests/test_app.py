'''Test for app/__init__.py'''
import logging
from unittest.mock import patch
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

    with pytest.raises(SystemExit) as e: # pylint: disable=unused-variable
        app.start()

    # Check for specific exit code or message
    assert e.value.code == "Thank you for using my calculator app. Exiting..."

    # Verify that the unknown command was handled as expected
    captured = capfd.readouterr()
    assert "No such command: unknown_command" in captured.out

# Tests for Environment Variables
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

# Test for logging
class TestLogging:
    '''Test logging'''
    def test_configure_logging_with_existing_config_file(self, tmp_path):
        '''Test the configure_logging method with an existing logging configuration file.'''
        # Create a temporary logging configuration file
        logging_conf_path = tmp_path / 'logging.conf'
        with open(logging_conf_path, 'w', encoding='utf-8') as f:
            f.write('[loggers]\nkeys=root\n\n[handlers]\nkeys=fileHandler,consoleHandler\n\n[formatters]\nkeys=simpleFormatter\n\n[logger_root]\nlevel=INFO\nhandlers=fileHandler,consoleHandler\n\n[handler_fileHandler]\nclass=handlers.RotatingFileHandler\nlevel=INFO\nformatter=simpleFormatter\nargs=(\'logs/app.log\', \'a\', 1048576, 5)\n\n[handler_consoleHandler]\nclass=StreamHandler\nlevel=INFO\nformatter=simpleFormatter\nargs=(sys.stderr,)\n\n[formatter_simpleFormatter]\nformat=%(asctime)s - %(name)s - %(levelname)s - %(message)s\ndatefmt=%Y-%m-%d %H:%M:%S\n')

        # Create an instance of the App class
        app = App()

        # Patch os.path.exists to return True for the temporary logging configuration file
        with patch('os.path.exists', return_value=True):
            app.configure_logging()

        # Check if logging is configured properly
        assert logging.getLogger().level == logging.INFO
        assert logging.getLogger().handlers

    def test_configure_logging_without_config_file(self):
        '''Test the configure_logging method without a logging configuration file.'''
        # Create an instance of the App class
        app = App()

        # Patch os.path.exists to return False for the logging configuration file
        with patch('os.path.exists', return_value=False):
            app.configure_logging()

        # Check if logging is configured properly
        assert logging.getLogger().level == logging.INFO
        assert logging.getLogger().handlers
