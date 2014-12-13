import unittest
from pathlib import Path

from vint.ast.parsing import Parser
from vint.ast.plugin.scope_plugin.definition_identifier_marker import DefinitionIdentifierMarker


def get_fixture_path(filename):
    return Path(__file__).parent.join(filename)


FixturePaths = {
    'BUILTIN': get_fixture_path('fixture_builtins.vim'),
    'DECLARING_FUNCTION_IN_FUNCTION': get_fixture_path('fixture_declaring_func_in_func.vim'),
    'DECLARING_FUNCTION': get_fixture_path('fixture_declaring_func.vim'),
    'DECLARING_VARIABLE': get_fixture_path('fixture_declaring_var.vim'),
    'DECLARING_VARIABLE_IN_FUNCTION': get_fixture_path('fixture_declaring_var_in_func.vim'),
    'DECLARING_DICT_ENTRY': get_fixture_path('fixture_declaring_dict_entry.vim'),
}


class TestDefinitionIdentifierMarker(unittest.TestCase):
    def test_process(self):
        ast = Parser.perse_file()

        plugin = DefinitionIdentifierMarker()
        plugin.process(ast)




if __name__ == '__main__':
    unittest.main()
