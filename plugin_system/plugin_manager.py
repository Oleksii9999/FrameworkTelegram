
# plugin_manager.py
import importlib
import os
import sys

from .plugin_base import Plugin

class PluginManager:    
    
    def __init__(self, plugin_dir):
        """
        Initializes a new instance of the PluginManager class.
        Args:
            plugin_dir (str): The directory path where the plugins are located.
        """
        """
        Loads all the plugins from the plugin directory.
        Raises:
            ImportError: If there is an error importing a plugin module.
        """        
        self.plugin_dir = plugin_dir
        self.plugins = []

    def load_plugins(self):
        sys.path.insert(0, self.plugin_dir)
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                module = importlib.import_module(module_name)
                for attr in dir(module):
                    cls = getattr(module, attr)
                    if isinstance(cls, type) and issubclass(cls, Plugin) and cls is not Plugin:
                        self.plugins.append(cls())

    def execute_plugins(self):
        """
        Executes all the loaded plugins.
        Raises:
            AttributeError: If a plugin does not have the execute() method.
        """        
        for plugin in self.plugins:
            plugin.execute()
            
    def execute_plugin_by_name(self, plugin_name, function_name, *args, **kwargs):    
        """
        Executes a specific function of a plugin by its name.
        Args:
            plugin_name (str): The name of the plugin class.
            function_name (str): The name of the function to execute.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Raises:
            AttributeError: If the plugin does not have the specified function.
            ValueError: If the plugin with the given name is not found.
        """ 
               
        for plugin in self.plugins:
            if plugin.__class__.__name__ == plugin_name:
                if hasattr(plugin, function_name):
                    function = getattr(plugin, function_name)
                    function(*args, **kwargs)
                else:
                    raise AttributeError(f"Plugin '{plugin_name}' does not have a function '{function_name}'")
                return
        raise ValueError(f"Plugin '{plugin_name}' not found")    
