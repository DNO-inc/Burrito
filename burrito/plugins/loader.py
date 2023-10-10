import pathlib
import importlib.util
import inspect

from burrito.utils.logger import get_logger
from burrito.plugins.base_plugin import BurritoBasePlugin


class PluginLoader:
    plugins_dir: list[pathlib.Path] = []
    plugins: dict[str, BurritoBasePlugin] = dict()

    @staticmethod
    def is_valid_plugin(plugin: BurritoBasePlugin) -> bool:
        """
        Check if the plugin is valid.

        Args:
            plugin: The plugin to check. Must be a subclass of `BurritoBasePlugin`

        Returns:
            True is plugin is valid
        """

        return (
            inspect.isclass(plugin)
            and issubclass(plugin, BurritoBasePlugin)
            and plugin is not BurritoBasePlugin
        )

    @staticmethod
    def get_plugin_name(plugin: BurritoBasePlugin) -> str:
        """
        Get the name of the plugin.

        Args:
            plugin: The plugin to get the name for

        Returns:
            The name of the plugin
        """
        plugin_name = ""
        # Get the plugin name from class attribute
        if hasattr(plugin, "plugin_name"):
            plugin_name = getattr(plugin, "plugin_name")
        else:
            # get class name if class attribute `plugin_name` is not specified
            plugin_name = plugin.__name__

        return plugin_name

    @classmethod
    def get_plugin(cls, module) -> dict[str, BurritoBasePlugin] | None:
        """
        Get Burrito plugin from module.
        This method tries to find the plugin by looking for __PLUGIN_CLASS attribute
         or by looking through all the attributes if __PLUGIN_CLASS is not defined

        Args:
            module: module from which to look for plugin

        Returns:
            dict of plugin name and plugin class
        """
        plugin_candidate: BurritoBasePlugin = None
        plugin_name: str = ""

        if hasattr(module, "__PLUGIN_CLASS"):
            plugin_candidate = getattr(module, "__PLUGIN_CLASS")

            if isinstance(plugin_candidate, str):
                plugin_candidate = getattr(module, plugin_candidate)

            if cls.is_valid_plugin(plugin_candidate):
                plugin_name = cls.get_plugin_name(plugin_candidate)

                return {plugin_name: plugin_candidate}

        # try to find plugin directly if __PLUGIN_CLASS is not defined
        for attribute in dir(module):
            plugin_candidate = getattr(module, attribute)

            if cls.is_valid_plugin(plugin_candidate):
                plugin_name = cls.get_plugin_name(plugin_candidate)

                return {plugin_name: plugin_candidate}

        get_logger().warning(f"No plugins found in {module}")
        return None

    @classmethod
    def load(cls, path: pathlib.Path = pathlib.Path(__file__).parent, exclude: list[str] = ["__pycache__"]) -> None:
        """
        Load plugins from a modules

        Args:
            path: The directory to load plugins from
            exclude: A list of plugin names to exclude from loading
        """
        cls.plugins_dir = [item for item in path.iterdir() if item.is_dir() and item.name not in exclude]

        for _dir in cls.plugins_dir:
            for plugin in _dir.iterdir():
                spec = importlib.util.spec_from_file_location(str(plugin.parent), str(plugin))
                if not spec:
                    continue

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                target_plugin_dict = cls.get_plugin(module)
                if target_plugin_dict:
                    cls.plugins |= target_plugin_dict
                    get_logger().info(f"Loaded plugin {target_plugin_dict}")

    @classmethod
    def execute_plugin(cls, name: str, *args, **kwargs):
        plugin = cls.plugins.get(name)

        if not plugin:
            get_logger().critical(f"Failed to execute plugin {name}. Plugin is not found")
            return

        return plugin.execute(*args, **kwargs)
