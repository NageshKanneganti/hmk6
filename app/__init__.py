'''app/__init__.py: App module responsible for managing the flow of the application.'''
import os
import pkgutil
import importlib
import sys
from typing import Type
from app.commands import CommandHandler, Command
from app.plugins.menu import MenuCommand
from dotenv import load_dotenv
import logging
import logging.config

class App:
    '''Main application class.'''
    
    def __init__(self): # Constructor
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()

    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT', default_value = None):
        return self.settings.get(env_var, default_value)

    def load_plugins(self):
        '''Dynamically load plugins from the app.plugins directory'''
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found.")
            return
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {e}")
                except Exception as e:
                    logging.error(f"Error loading plugin {plugin_name}: {e}")

    def register_plugin_commands(self, plugin_module, plugin_name):
        '''Register commands from a plugin module'''
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                # Register all commands except MenuCommand
                if plugin_name != "menu":
                    self.command_handler.register_command(plugin_name, item())
                    logging.info(f"Command '{item_name}' from plugin '{plugin_name}' registered.")
                else:
                    # Register MenuCommand specifically for "menu" plugin
                    self.command_handler.register_command(plugin_name, MenuCommand(self.command_handler))
                    logging.info(f"Command 'MenuCommand' from plugin '{plugin_name}' registered.")

    def start(self):
        '''Register commands from plugin module'''
        self.load_plugins()
        logging.info("Application started.\n")
        print("Welcome to my basic calculator program.\n\tType 'menu' to see available commands. Type 'exit' to quit application.")
        try:
            while True:  #REPL Read, Evaluate, Print, Loop
                cmd_input = input(">>> ").strip()
                if cmd_input.lower() == 'exit':
                    logging.info("Application exit.")
                    sys.exit(0)  # Use sys.exit(0) for a clean exit, indicating success.
                try:
                    self.command_handler.execute_command(cmd_input)
                except KeyError: # Assuming execute_command raises KeyError for unknown commands
                    logging.error(f"Unknown command: {cmd_input}")
                    continue  # Continue prompting for input
        except KeyboardInterrupt:
            logging.info("Application interrupted and exiting gracefully.")
            sys.exit(0) # Assuming a KeyboardInterrupt should also result in a clean exit.
        finally:
            logging.info("Application shutdown.")
