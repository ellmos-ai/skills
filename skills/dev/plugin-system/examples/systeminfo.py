"""System-Informationen Plugin"""

import platform
import os
from plugin_system import PluginBase


class SystemInfoPlugin(PluginBase):
    """Zeigt Systeminformationen an"""

    name = "SystemInfo"
    version = "2.0.0"

    def execute(self, *args, **kwargs):
        """Gibt Systeminformationen zurück"""
        detailed = kwargs.get('detailed', False)

        info = {
            'status': 'ok',
            'system': platform.system(),
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'processor': platform.processor(),
        }

        if detailed:
            info.update({
                'machine': platform.machine(),
                'release': platform.release(),
                'hostname': platform.node(),
                'pid': os.getpid(),
                'cwd': os.getcwd()
            })

        return info
