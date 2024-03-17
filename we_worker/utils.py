import ast


# pylint: disable=exec-used,eval-used,redefined-builtin
def code_exec(script, d_globals=None, d_locals=None):
    """Execute a script and return the value of the last expression."""
    stmts = list(ast.iter_child_nodes(ast.parse(script)))
    if not stmts:
        return None

    if isinstance(stmts[-1], ast.Expr):
        # the last one is an expression and we will try to return the results
        # so we first execute the previous statements
        if len(stmts) > 1:
            exec(
                compile(
                    ast.Module(body=stmts[:-1], type_ignores=[]), filename="<ast>", mode="exec"
                ),
                d_globals,
                d_locals,
            )
        # then we eval the last one
        return eval(
            compile(ast.Expression(body=stmts[-1].value), filename="<ast>", mode="eval"),
            d_globals,
            d_locals,
        )

    else:
        # otherwise we just execute the entire code
        return exec(script, d_globals, d_locals)
