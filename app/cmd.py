from commands import create_superuser, load_permissions, load_default_permissions
from fastapi import Depends

COMMANDS = {
    "create_superuser": create_superuser,
    "load_permissions":load_permissions,
    'update_permissions':load_default_permissions
}

def function_call(function_name: str):
    if function_name in COMMANDS:
        print(f"Executing {function_name}")
        func= COMMANDS[function_name]
        func()
    else:
        raise ValueError(f"Unknown command: {function_name}")

if __name__ == "__main__":
    try:
        function_name = input("Enter a command name: ")
        result = function_call(function_name)
        if callable(result):
            result()
    except Exception as e:
        print(f"An error occurred: {e}")
