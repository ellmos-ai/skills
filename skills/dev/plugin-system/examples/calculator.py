"""Math-Plugin für Berechnungen"""

from plugin_system import PluginBase


class CalculatorPlugin(PluginBase):
    """Einfacher Taschenrechner"""

    name = "Calculator"
    version = "1.2.1"

    def execute(self, *args, **kwargs):
        """
        Führt einfache Rechnung aus

        Args:
            operation: 'add', 'subtract', 'multiply', 'divide'
            a: Erste Zahl
            b: Zweite Zahl
        """
        operation = kwargs.get('operation', 'add')
        a = kwargs.get('a', 0)
        b = kwargs.get('b', 0)

        operations = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y if y != 0 else None
        }

        if operation not in operations:
            return {'status': 'error', 'message': f'Operation {operation} unbekannt'}

        try:
            result = operations[operation](a, b)
            return {
                'status': 'ok',
                'operation': operation,
                'a': a,
                'b': b,
                'result': result
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
