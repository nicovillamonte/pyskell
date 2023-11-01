from pyskell_functions import pyskell_exported_functions
from pyskell_types import PyskellFunction
from pyskell_shared_global import version
from colorama import Fore, Back, Style
from pyskell_shared_global import DEV_MODE
import os


def print_if_debug(message, *args):
    if DEV_MODE:
        print(message, *args)


def print_help():
    print(f"Pyskell v{version}")
    print("Usage: pyskell [file] [options]")
    print("Options:")
    print("\t--skip-init: Don't print the output of the file build.")
    print("\t--no-assign: Don't print the assignments.")

    print("\nFor help you can use:")
    print("\tpyskell help")

    print("\nYou can run the Pyskell REPL with only typing:")
    print("\tpyskell")


def search_pyskell_function_by_name(name):
    for f in pyskell_exported_functions:
        if f.name == name:
            return f
    return None


def is_valid_list_or_tuple(s):
    return (s.startswith('[') and s.endswith(']')) or (s.startswith('(') and s.endswith(')'))


def add_pyskell_command_error_to_log(error):
    if not os.path.exists(".log"):
        os.mkdir(".log")
    if not os.path.exists(".log/pyskell_command_errors.log"):
        open(".log/pyskell_command_errors.log", "w").close()
    with open(".log/pyskell_command_errors.log", "a") as log:
        log.write(f"{error}\n")


def pyskellRunProccess(function, *args):
    num_args = function.func.__code__.co_argcount if isinstance(
        function, PyskellFunction) else function.__code__.co_argcount

    if len(args) < num_args:
        return function
    try:
        return function(*args)
    except ValueError:
        return "Error: uno o más argumentos no son números válidos."
    except Exception as e:
        add_pyskell_command_error_to_log(type(e).__name__)
        return f"Error: {e}."


def apply_args(func, args):
    result = func
    for arg in args:
        result = result(arg)
    return result


def print_c(text, color=Fore.RESET, bg_color=Back.RESET, _end="\n"):
    print(bg_color + color + text + Style.RESET_ALL, end=_end)


def safe_eval(s):
    try:
        return eval(s, {"__builtins__": None}, {})
    except Exception:
        return s


def print_if(condition, message, *args):
    if condition:
        print(message, *args)
