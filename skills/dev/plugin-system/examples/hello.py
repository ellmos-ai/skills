"""Einfaches Hello-World Plugin"""

from plugin_system import PluginBase


class HelloPlugin(PluginBase):
    """Einfaches Willkommens-Plugin"""

    name = "Hello"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        """Gibt eine Willkommensnachricht aus"""
        username = kwargs.get('user', 'Freund')
        message = f"Hallo {username}! 👋"
        return {
            'status': 'ok',
            'message': message
        }
