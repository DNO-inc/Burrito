from burrito.plugins.base_plugin import BurritoBasePlugin


class AuthSSUPlugin(BurritoBasePlugin):
    plugin_name: str = "ssu_auth"

    def execute(self):
        ...


__PLUGIN_CLASS = AuthSSUPlugin
