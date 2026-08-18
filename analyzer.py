import ast


def analyze_python_code(code):

    issues = []

    try:

        tree = ast.parse(code)

    except SyntaxError as e:

        issues.append({
            "type": "Bug",
            "severity": "High",
            "message": f"Syntax error on line {e.lineno}: {e.msg}"
        })

        return issues

    dangerous_functions = {
        "eval": "eval() can execute arbitrary code.",
        "exec": "exec() can execute arbitrary code.",
        "os.system": "os.system() can execute system commands."
    }

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                function_name = node.func.id

                if function_name in dangerous_functions:

                    issues.append({
                        "type": "Security",
                        "severity": "High",
                        "message": dangerous_functions[function_name]
                    })

            elif isinstance(node.func, ast.Attribute):

                if isinstance(node.func.value, ast.Name):

                    function_name = (
                        node.func.value.id
                        + "."
                        + node.func.attr
                    )

                    if function_name in dangerous_functions:

                        issues.append({
                            "type": "Security",
                            "severity": "High",
                            "message": dangerous_functions[function_name]
                        })

    for node in ast.walk(tree):

        if isinstance(node, ast.Assign):

            for target in node.targets:

                if isinstance(target, ast.Name):

                    variable_name = target.id.lower()

                    sensitive_names = (
                        "password",
                        "secret",
                        "api_key",
                        "apikey"
                    )

                    if any(
                        name in variable_name
                        for name in sensitive_names
                    ):

                        if isinstance(node.value, ast.Constant):

                            if isinstance(node.value.value, str):

                                issues.append({
                                    "type": "Security",
                                    "severity": "High",
                                    "message": (
                                        f"Possible hardcoded secret in "
                                        f"'{target.id}' on line "
                                        f"{node.lineno}."
                                    )
                                })

    for node in ast.walk(tree):

        if isinstance(node, ast.BinOp):

            if isinstance(node.op, ast.Div):

                if (
                    isinstance(node.right, ast.Constant)
                    and node.right.value == 0
                ):

                    issues.append({
                        "type": "Bug",
                        "severity": "High",
                        "message": (
                            f"Division by zero detected on line "
                            f"{node.lineno}."
                        )
                    })

    return issues