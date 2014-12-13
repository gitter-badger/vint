from vint.ast.node_type import NodeType
from vint.ast.plugin.scope_plugin.scope_type import ScopeType
from vint.ast.plugin.scope_plugin.variable_type import VariableType


class UnexpectedNodeTypeError(Exception):
    pass


def create_variable_type(variable_type, is_implicit):
    return {
        'variable_type': variable_type,
        'is_implicit_variable_type': is_implicit,
    }


def detect_variable_type(node, scope):
    """ Detect VariableType of a terminating node in declaration contexts.
    The declaration context is:
        - left-hand-side expression of let-statement
        - condition expression of for-statement
        - function name expression of function-statement
        - argument name expression of function-statement
    """
    node_type = NodeType(node['type'])

    if node_type in VariableTypeDetectorByNodeType:
        return VariableTypeDetectorByNodeType[node_type]

    raise UnexpectedNodeTypeError(node_type)


def detect_variable_type_by_node_identifier(identifier, scope):
    identifier_name_prefix = identifier['vaue'][0:1]

    # See:
    #   :help E738
    if identifier_name_prefix in IdentifierPrefixOfVariableType:
        variable_type = IdentifierPrefixOfVariableType[identifier_name_prefix]
        return create_variable_type(variable_type, is_implicit=False)

    # See :help internal-variables
    # > In a function: local to a function; otherwise: global
    is_toplevel_context = scope['type'] is ScopeType.TOPLEVEL
    variable_type = VariableType.GLOBAL if is_toplevel_context else VariableType.FUNCTION_LOCAL

    return create_variable_type(variable_type, is_implicit=True)


def detect_variable_type_by_node_env(node_env, scope):
    # See:
    #   :help let-$
    return create_variable_type(VariableType.GLOBAL, is_implicit=False)


def detect_variable_type_by_node_reg(node_reg, scope):
    # See:
    #   :help let-@
    return create_variable_type(VariableType.GLOBAL, is_implicit=False)


def detect_variable_type_by_node_opt(node_opt, scope):
    # TODO: determine local or global
    # See:
    #   :help let-&
    return create_variable_type(VariableType.GLOBAL, is_implicit=False)


def detect_variable_type_by_node_curlyname(node_curlyname, scope):
    # We cannot determine the variable type because it is dynamic
    # declaration. For example:
    #   let {var} = 0
    return create_variable_type(VariableType.UNANALYZABLE, is_implicit=False)


IdentifierPrefixOfVariableType = {
    'g:': VariableType.GLOBAL,
    'b:': VariableType.BUFFER_LOCAL,
    'w:': VariableType.WINDOW_LOCAL,
    't:': VariableType.TAB_LOCAL,
    's:': VariableType.SCRIPT_LOCAL,
    'l:': VariableType.FUNCTION_LOCAL,
    'a:': VariableType.PARAMETER,
    'v:': VariableType.BUILTIN,
}


VariableTypeDetectorByNodeType = {
    NodeType.IDENTIFIER: detect_variable_type_by_node_identifier,
    NodeType.ENV: detect_variable_type_by_node_env,
    NodeType.REG: detect_variable_type_by_node_reg,
    NodeType.OPT: detect_variable_type_by_node_opt,
    NodeType.CURLYNAME: detect_variable_type_by_node_curlyname,
}
