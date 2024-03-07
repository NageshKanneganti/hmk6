'''Test file for app/plugins/clear/__init__.py'''
import unittest
import os
from unittest.mock import patch
from app.plugins.clear import ClearCommand

class TestClearCommand(unittest.TestCase):
    '''Test class for ClearCommand'''

    @patch('os.system')
    def test_execute_clears_command_line(self, mock_os_system):
        '''Test for execute method in class ClearCommand'''
        # Arrange
        clear_command = ClearCommand()

        # Act
        clear_command.execute()

        # Assert
        mock_os_system.assert_called_once_with('cls' if os.name == 'nt' else 'clear')
