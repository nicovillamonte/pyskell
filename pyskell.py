import pyskell_builder as pbuilder
import pyskell_execute as pexecuter
import sys
from pyskell_repl import run_repl
from pyskell_special_commands import clear_screen
from pyskell_shared_global import DEV_MODE, version, command_options, execution_config
from pyskell_utils import print_help, delete_file


def manage_another_flags():
    if not command_options['print_assign'] in sys.argv:
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

        show_build = command_options['show_build'] in sys.argv

        manage_another_flags()

        if file.split('.')[-1] not in ['pll', 'rpll']:
            print("File extension not supported.")
            return

        # If file extension is .pll, build it, else run it
        build_file = None
        if file.split('.')[-1] == 'pll':
            print("Building file:", file) if show_build else None
            build_file = pbuilder.build(file=file, print_log=DEV_MODE)
            print("File builded:", build_file) if show_build else None
            input("Press Enter to continue...") if show_build else None

        clear_screen()
        pexecuter.run_pll(build_file if build_file else file)
        
        if build_file:
            # Delete builded file and try to delete dist folder
            delete_file(build_file)
            delete_file('./dist')
    else:
        run_repl()


if __name__ == "__main__":
    main()
