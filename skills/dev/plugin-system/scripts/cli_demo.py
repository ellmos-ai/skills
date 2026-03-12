#!/usr/bin/env python3
"""
Demo-CLI-Anwendung mit Plugin-System
Zeigt wie Plugins automatisch erkannt und ausgeführt werden
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from plugin_system import PluginManager

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)


class PluginCLI:
    """Beispiel-CLI mit Plugin-Support"""

    def __init__(self):
        # Plugin-Manager im selben Verzeichnis wie dieses Script
        script_dir = Path(__file__).parent
        self.manager = PluginManager(plugins_dir=script_dir / "plugins")

    def run(self):
        """Haupteinstiegspunkt"""
        parser = argparse.ArgumentParser(
            description='CLI-App mit Plugin-System'
        )

        subparsers = parser.add_subparsers(dest='command', help='Verfügbare Befehle')

        # Befehl: list
        subparsers.add_parser('list', help='Alle Plugins auflisten')

        # Befehl: run
        run_parser = subparsers.add_parser('run', help='Ein Plugin ausführen')
        run_parser.add_argument('plugin_name', help='Name des auszuführenden Plugins')
        run_parser.add_argument('--args', type=json.loads, default={},
                               help='Argumente als JSON (z.B. \'{"a":5,"b":3}\')')

        # Befehl: hello
        hello_parser = subparsers.add_parser('hello', help='Hello-Plugin testen')
        hello_parser.add_argument('--user', default='Welt',
                                 help='Benutzername (default: Welt)')

        # Befehl: calc
        calc_parser = subparsers.add_parser('calc', help='Taschenrechner testen')
        calc_parser.add_argument('--op', choices=['add', 'subtract', 'multiply', 'divide'],
                                default='add', help='Operation')
        calc_parser.add_argument('--a', type=float, default=10, help='Erste Zahl')
        calc_parser.add_argument('--b', type=float, default=5, help='Zweite Zahl')

        # Befehl: sysinfo
        sysinfo_parser = subparsers.add_parser('sysinfo', help='Systeminformationen')
        sysinfo_parser.add_argument('--detailed', action='store_true',
                                   help='Detaillierte Ausgabe')

        args = parser.parse_args()

        # Plugins laden
        logger.info("Lade Plugins...")
        self.manager.discover_plugins()

        # Befehl verarbeiten
        if args.command == 'list':
            self.manager.list_plugins()
        elif args.command == 'run':
            self._run_plugin(args.plugin_name, args.args)
        elif args.command == 'hello':
            self._run_plugin('Hello', {'user': args.user})
        elif args.command == 'calc':
            self._run_plugin('Calculator', {
                'operation': args.op,
                'a': args.a,
                'b': args.b
            })
        elif args.command == 'sysinfo':
            self._run_plugin('SystemInfo', {'detailed': args.detailed})
        else:
            parser.print_help()

    def _run_plugin(self, plugin_name: str, kwargs: dict = None) -> None:
        """Hilfsmethod zum Ausführen eines Plugins"""
        if kwargs is None:
            kwargs = {}

        success, result = self.manager.execute_plugin(plugin_name, **kwargs)

        if success:
            print("\n" + "─"*50)
            print(f"Ergebnis von '{plugin_name}':")
            print("─"*50)
            if isinstance(result, dict):
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(result)
            print("─"*50 + "\n")
        else:
            print(f"\n❌ FEHLER: {result}\n")
            sys.exit(1)


if __name__ == '__main__':
    try:
        cli = PluginCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nAbgebrochen.")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Kritischer Fehler: {str(e)}", exc_info=True)
        sys.exit(1)
