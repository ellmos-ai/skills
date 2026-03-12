"""
Unit-Tests für das Plugin-System
Zeigt wie man Plugins und den Manager testet
"""

import unittest
import tempfile
import sys
from pathlib import Path
from plugin_system import PluginBase, PluginManager, PluginInfo


class TestPlugin(PluginBase):
    """Test-Plugin für Unit-Tests"""
    name = "TestPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {'status': 'ok', 'value': kwargs.get('value', 'default')}


class BrokenTestPlugin(PluginBase):
    """Plugin mit fehlender Version"""
    name = "BrokenTest"
    # version fehlt absichtlich


class TestPluginInterface(unittest.TestCase):
    """Tests für das Plugin-Interface"""

    def test_plugin_base_requirements(self):
        """Prüfe dass TestPlugin alle Anforderungen erfüllt"""
        plugin = TestPlugin()

        self.assertEqual(plugin.name, "TestPlugin")
        self.assertEqual(plugin.version, "1.0.0")
        self.assertTrue(hasattr(plugin, 'execute'))
        self.assertTrue(callable(plugin.execute))

    def test_plugin_execution(self):
        """Prüfe dass ein Plugin ausgeführt werden kann"""
        plugin = TestPlugin()
        result = plugin.execute(value="test")

        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['value'], 'test')

    def test_plugin_repr(self):
        """Prüfe String-Darstellung"""
        plugin = TestPlugin()
        self.assertEqual(repr(plugin), "TestPlugin v1.0.0")


class TestPluginManager(unittest.TestCase):
    """Tests für den PluginManager"""

    def setUp(self):
        """Erstelle temporäres Plugins-Verzeichnis"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = PluginManager(plugins_dir=self.temp_dir)

    def tearDown(self):
        """Cleanup"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_plugin_discovery_empty_dir(self):
        """Prüfe Discovery in leerem Verzeichnis"""
        results = self.manager.discover_plugins()
        self.assertEqual(len(results), 0)

    def test_plugin_discovery_nonexistent_dir(self):
        """Prüfe Discovery mit nicht-existent Verzeichnis"""
        manager = PluginManager(plugins_dir="/nonexistent/path")
        results = manager.discover_plugins()
        self.assertEqual(len(results), 0)

    def test_invalid_plugin_detection(self):
        """Prüfe dass ungültige Plugins erkannt werden"""
        # Erstelle eine Datei mit Syntax-Fehler
        bad_plugin_file = Path(self.temp_dir) / "bad.py"
        bad_plugin_file.write_text("this is not valid python {]")

        results = self.manager.discover_plugins()

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].is_valid)
        self.assertIn("Syntax", results[0].error)

    def test_plugin_validation(self):
        """Prüfe PluginBase-Validierung"""
        plugin = TestPlugin()

        # Sollte keine Fehler zurückgeben
        error = self.manager._validate_plugin_interface(plugin)
        self.assertIsNone(error)

    def test_plugin_validation_missing_name(self):
        """Prüfe Validierung bei fehlendem name"""
        plugin = TestPlugin()
        plugin.name = ""

        error = self.manager._validate_plugin_interface(plugin)
        self.assertIsNotNone(error)
        self.assertIn("name", error)

    def test_execute_plugin_success(self):
        """Prüfe erfolgreiche Plugin-Ausführung"""
        self.manager.plugins['TestPlugin'] = TestPlugin()

        success, result = self.manager.execute_plugin('TestPlugin', value='test')

        self.assertTrue(success)
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['value'], 'test')

    def test_execute_plugin_not_found(self):
        """Prüfe Fehler bei nicht gefundenem Plugin"""
        success, result = self.manager.execute_plugin('NonExistent')

        self.assertFalse(success)
        self.assertIn('nicht', result.lower() or 'verfügbar' in result.lower())

    def test_execute_plugin_error(self):
        """Prüfe Fehlerbehandlung bei Plugin-Ausführung"""
        class ErrorPlugin(PluginBase):
            name = "Error"
            version = "1.0.0"

            def execute(self, **kwargs):
                raise ValueError("Test error")

        self.manager.plugins['Error'] = ErrorPlugin()

        success, result = self.manager.execute_plugin('Error')

        self.assertFalse(success)
        self.assertIn('Test error', result)

    def test_plugin_info_structure(self):
        """Prüfe PluginInfo Datenstruktur"""
        info = PluginInfo(
            name="Test",
            version="1.0.0",
            module_name="test",
            module_path=Path("test.py"),
            is_valid=True
        )

        self.assertEqual(info.name, "Test")
        self.assertTrue(info.is_valid)
        self.assertIsNone(info.error)

    def test_plugin_info_with_error(self):
        """Prüfe PluginInfo mit Fehler"""
        info = PluginInfo(
            name="Broken",
            version="0.0.0",
            module_name="broken",
            module_path=Path("broken.py"),
            is_valid=False,
            error="Test error message"
        )

        self.assertEqual(info.name, "Broken")
        self.assertFalse(info.is_valid)
        self.assertEqual(info.error, "Test error message")


class TestPluginIntegration(unittest.TestCase):
    """Integrations-Tests"""

    def test_full_workflow(self):
        """Prüfe kompletten Workflow: Load → List → Execute"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Erstelle Test-Plugin
            plugin_file = Path(temp_dir) / "demo.py"
            plugin_file.write_text("""
from plugin_system import PluginBase

class DemoPlugin(PluginBase):
    name = "Demo"
    version = "1.0.0"

    def execute(self, **kwargs):
        return {'greeting': 'Hello from Demo!'}
""")

            # Lade und führe aus
            manager = PluginManager(plugins_dir=temp_dir)
            manager.discover_plugins()

            self.assertEqual(len(manager.plugins), 1)
            self.assertIn('Demo', manager.plugins)

            success, result = manager.execute_plugin('Demo')
            self.assertTrue(success)
            self.assertEqual(result['greeting'], 'Hello from Demo!')


class TestEdgeCases(unittest.TestCase):
    """Tests für Grenzfälle"""

    def test_plugin_with_no_docstring(self):
        """Prüfe Plugin ohne Docstring"""
        class MinimalPlugin(PluginBase):
            name = "Minimal"
            version = "1.0.0"

            def execute(self):
                return "OK"

        plugin = MinimalPlugin()
        result = plugin.execute()
        self.assertEqual(result, "OK")

    def test_plugin_returning_none(self):
        """Prüfe Plugin das None zurückgibt"""
        class NonePlugin(PluginBase):
            name = "None"
            version = "1.0.0"

            def execute(self):
                return None

        manager = PluginManager()
        manager.plugins['None'] = NonePlugin()

        success, result = manager.execute_plugin('None')
        self.assertTrue(success)
        self.assertIsNone(result)

    def test_plugin_with_complex_return(self):
        """Prüfe Plugin mit komplexem Rückgabewert"""
        class ComplexPlugin(PluginBase):
            name = "Complex"
            version = "1.0.0"

            def execute(self, **kwargs):
                return {
                    'data': [1, 2, 3],
                    'nested': {'key': 'value'},
                    'list': ['a', 'b', 'c']
                }

        manager = PluginManager()
        manager.plugins['Complex'] = ComplexPlugin()

        success, result = manager.execute_plugin('Complex')
        self.assertTrue(success)
        self.assertEqual(result['data'], [1, 2, 3])
        self.assertEqual(result['nested']['key'], 'value')


if __name__ == '__main__':
    # Stelle sicher dass plugin_system importierbar ist
    import sys
    sys.path.insert(0, str(Path(__file__).parent))

    # Starte Tests
    unittest.main(verbosity=2)
