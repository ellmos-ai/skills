"""
Plugin-System für CLI-Anwendungen
- Automatische Erkennung von Plugins im plugins/ Ordner
- Interface-Validierung und Fehlertoleranz
- Strukturiertes Laden und Ausführen
"""

import os
import sys
import importlib.util
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class PluginInfo:
    """Metadaten eines Plugins"""
    name: str
    version: str
    module_name: str
    module_path: Path
    is_valid: bool
    error: Optional[str] = None


class PluginBase(ABC):
    """Abstrakte Basisklasse für alle Plugins"""

    # Diese Attribute müssen von jedem Plugin definiert werden
    name: str = "Unknown"
    version: str = "0.0.0"

    @abstractmethod
    def execute(self, *args, **kwargs) -> any:
        """
        Haupteinstiegspunkt des Plugins

        Args:
            *args: Positionsargumente von der CLI
            **kwargs: Benannte Argumente

        Returns:
            Beliebiger Rückgabewert (String, Dict, etc.)
        """
        pass

    def __repr__(self) -> str:
        return f"{self.name} v{self.version}"


class PluginManager:
    """Verwaltet das Laden, Validierung und Ausführung von Plugins"""

    def __init__(self, plugins_dir: str = "./plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_info: Dict[str, PluginInfo] = {}
        self._discovery_results: List[PluginInfo] = []

    def discover_plugins(self) -> List[PluginInfo]:
        """
        Findet alle Plugins im plugins/ Ordner

        Returns:
            Liste mit PluginInfo-Objekten (valid + invalid)
        """
        self._discovery_results = []

        if not self.plugins_dir.exists():
            logger.warning(f"Plugins-Verzeichnis nicht gefunden: {self.plugins_dir}")
            return []

        python_files = list(self.plugins_dir.glob("*.py"))
        python_files = [f for f in python_files if not f.name.startswith("_")]

        logger.info(f"Gefundene Plugin-Kandidaten: {len(python_files)}")

        for plugin_file in python_files:
            info = self._load_plugin_from_file(plugin_file)
            self._discovery_results.append(info)

        return self._discovery_results

    def _load_plugin_from_file(self, plugin_file: Path) -> PluginInfo:
        """
        Lädt ein einzelnes Plugin von einer Datei

        Returns:
            PluginInfo mit Status und ggf. Fehlerinfo
        """
        module_name = plugin_file.stem

        try:
            # Modul dynamisch importieren
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            if spec is None or spec.loader is None:
                return PluginInfo(
                    name=module_name,
                    version="0.0.0",
                    module_name=module_name,
                    module_path=plugin_file,
                    is_valid=False,
                    error="Modul-Spec konnte nicht erstellt werden"
                )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Plugin-Klasse im Modul suchen
            plugin_class = self._find_plugin_class(module)
            if plugin_class is None:
                return PluginInfo(
                    name=module_name,
                    version="0.0.0",
                    module_name=module_name,
                    module_path=plugin_file,
                    is_valid=False,
                    error="Keine PluginBase-Subklasse gefunden"
                )

            # Plugin instanziieren
            try:
                plugin_instance = plugin_class()
            except Exception as e:
                return PluginInfo(
                    name=module_name,
                    version="0.0.0",
                    module_name=module_name,
                    module_path=plugin_file,
                    is_valid=False,
                    error=f"Instanziierung fehlgeschlagen: {str(e)}"
                )

            # Validiere Interface
            validation_error = self._validate_plugin_interface(plugin_instance)
            if validation_error:
                return PluginInfo(
                    name=module_name,
                    version="0.0.0",
                    module_name=module_name,
                    module_path=plugin_file,
                    is_valid=False,
                    error=validation_error
                )

            # Alles OK
            info = PluginInfo(
                name=plugin_instance.name,
                version=plugin_instance.version,
                module_name=module_name,
                module_path=plugin_file,
                is_valid=True
            )

            # Speichern
            self.plugins[plugin_instance.name] = plugin_instance
            self.plugin_info[plugin_instance.name] = info

            logger.info(f"✓ Plugin geladen: {plugin_instance.name} v{plugin_instance.version}")
            return info

        except SyntaxError as e:
            return PluginInfo(
                name=module_name,
                version="0.0.0",
                module_name=module_name,
                module_path=plugin_file,
                is_valid=False,
                error=f"Syntax-Fehler in {plugin_file.name}: {str(e)}"
            )
        except Exception as e:
            return PluginInfo(
                name=module_name,
                version="0.0.0",
                module_name=module_name,
                module_path=plugin_file,
                is_valid=False,
                error=f"Fehler beim Laden: {str(e)}"
            )

    @staticmethod
    def _find_plugin_class(module) -> Optional[type]:
        """Findet die Plugin-Klasse (PluginBase-Subklasse) im Modul"""
        for name in dir(module):
            obj = getattr(module, name)
            # Prüfe ob es eine Klasse ist, PluginBase erbt und nicht die Basisklasse selbst ist
            if (isinstance(obj, type) and
                issubclass(obj, PluginBase) and
                obj is not PluginBase):
                return obj
        return None

    @staticmethod
    def _validate_plugin_interface(plugin: PluginBase) -> Optional[str]:
        """Validiert ob Plugin das Interface korrekt implementiert"""

        # Prüfe name-Attribut
        if not hasattr(plugin, 'name') or not plugin.name:
            return "Attribut 'name' ist leer oder nicht definiert"

        # Prüfe version-Attribut
        if not hasattr(plugin, 'version') or not plugin.version:
            return "Attribut 'version' ist leer oder nicht definiert"

        # Prüfe ob execute() implementiert (nicht abstrakt)
        if not hasattr(plugin, 'execute'):
            return "Methode 'execute()' nicht implementiert"

        return None

    def execute_plugin(self, plugin_name: str, *args, **kwargs) -> Tuple[bool, any]:
        """
        Führt ein Plugin aus

        Args:
            plugin_name: Name des Plugins
            *args, **kwargs: Argumente für das Plugin

        Returns:
            Tuple (success: bool, result: any)
        """
        if plugin_name not in self.plugins:
            logger.error(f"Plugin nicht geladen: {plugin_name}")
            return False, f"Plugin '{plugin_name}' nicht verfügbar"

        try:
            plugin = self.plugins[plugin_name]
            logger.info(f"Führe aus: {plugin_name}")
            result = plugin.execute(*args, **kwargs)
            logger.info(f"✓ {plugin_name} erfolgreich ausgeführt")
            return True, result
        except Exception as e:
            error_msg = f"Fehler bei Ausführung von {plugin_name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return False, error_msg

    def list_plugins(self) -> None:
        """Zeigt alle geladenen und fehlgeschlagenen Plugins an"""
        print("\n" + "="*60)
        print("PLUGIN-ÜBERSICHT")
        print("="*60)

        valid_plugins = [p for p in self._discovery_results if p.is_valid]
        invalid_plugins = [p for p in self._discovery_results if not p.is_valid]

        if valid_plugins:
            print(f"\n✓ Geladen ({len(valid_plugins)}):")
            for info in valid_plugins:
                print(f"  • {info.name:20} v{info.version:10} ({info.module_name}.py)")

        if invalid_plugins:
            print(f"\n✗ Fehler ({len(invalid_plugins)}):")
            for info in invalid_plugins:
                print(f"  • {info.module_name}.py")
                print(f"    → {info.error}")

        if not valid_plugins and not invalid_plugins:
            print("\nKeine Plugins gefunden.")

        print("="*60 + "\n")

    def get_plugin(self, plugin_name: str) -> Optional[PluginBase]:
        """Gibt eine Plugin-Instanz zurück oder None"""
        return self.plugins.get(plugin_name)
