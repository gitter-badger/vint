from vint.ast.plugin.scope_plugin.scope_type import ScopeType


class ScopeStore(object):
    def __init__(self):
        self.root_scope = None
        self.current_scope = None


    def handle_enter_toplevel_scope(self):
        self.root_scope = self.current_scope = {
            'type': ScopeType.TOPLEVEL,
            'variables': {},
            'parent_scope': None,
            'child_scopes': [],
        }


    def handle_enter_scope(self):
        parent_scope = self.current_scope

        new_scope = {
            'type': ScopeType.FUNCTION,
            'variables': {},
            'parent_scope': parent_scope,
            'child_scopes': [],
        }

        parent_scope['child_scopes']['child_scopes'].append(new_scope)
        self.current_scope = new_scope


    def handle_leave_scope(self):
        self.current_scope = self.current_scope['parent_scope']


    def handle_new_variable(self, node):
        variables_map = self.current_scope['variables']

        variable = detect_variable_type(node, self.current_scope)

        if identifier_name in variables_map:
            # We can declare duplicated variables, and the older variable
            # will be overwrited by newer. But we interested in searching
            # duplicated variable declaration. So variables map should
            # have an array that contains all variable declaration.
            variables_map[identifier_name].append(variable)
        else:
            variables_map[identifier_name] = [variable]
