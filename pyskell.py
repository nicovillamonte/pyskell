import pyskell_builder as pbuilder
import pyskell_execute as pexecuter
import sys
from pyskell_repl import run_repl
from pyskell_special_commands import clear_screen
from pyskell_shared_global import DEV_MODE, version, command_options, execution_config
from pyskell_utils import print_help


def manage_another_flags():
    if command_options['no_assign'] in sys.argv:
        execution_config['assignations_print'] = False


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'version':
            print(f"Pyskell v{version}.")
            return
        elif sys.argv[1] == 'help':
            print_help()
            return

        file = sys.argv[1]

        without_print_flag = command_options['without_print_flag'] in sys.argv

        manage_another_flags()

        if file.split('.')[-1] not in ['pll', 'rpll']:
            print("File extension not supported.")
            return

        # If file extension is .pll, build it, else run it
        if file.split('.')[-1] == 'pll':
            print("Building file:", file) if not without_print_flag else None
            build_file = pbuilder.build(file=file, print_log=DEV_MODE)
            print("File builded:", build_file) if not without_print_flag else None
        else:
            build_file = file

        input("Press Enter to continue...") if not without_print_flag else None

        clear_screen()
        pexecuter.run_pll(build_file)
    else:
        run_repl()


if __name__ == "__main__":
    main()
