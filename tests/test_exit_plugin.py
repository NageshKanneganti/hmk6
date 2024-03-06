'''Test file for app/plugin/exit/__init__.py'''
from app.plugins.exit import ExitCommand

def test_exit_command():
    '''Test the ExitCommand class.'''
    exit_command = ExitCommand()

    # Ensure the execute method exits the application
    try:
        exit_command.execute()
    except SystemExit as e:
        assert str(e) == "Thank you for using my calculator app. Exiting..."
