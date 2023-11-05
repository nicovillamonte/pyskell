from pyskell_utils import *
from multiprocessing import Process
from threading import Thread, local
import re
import shlex
import time
from pyskell_shared_global import variables, variables_inputs, execution_config

loaded_program = []

thread_local_data = local()

def set_pyskell_pc(value):
    global pyskell_pc
    global is_main_program
    
    if is_main_program:
        pyskell_pc = value
    else:
        thread_local_data.pyskell_pc = value
    
def increment_pyskell_pc(value):
    global pyskell_pc
    global is_main_program
    
    if is_main_program:
        pyskell_pc += value
    else:
        thread_local_data.pyskell_pc += value

def get_pyskell_pc():
    global pyskell_pc
    global is_main_program
    
    if is_main_program:
        return pyskell_pc
    else:
        return thread_local_data.pyskell_pc

def process_command(command):
    pattern = re.compile(r'(\[.*?\]|\(.*?\))')
    lists_and_tuples = pattern.findall(command)

    for i, lt in enumerate(lists_and_tuples):
        command = command.replace(lt, f'__PLACEHOLDER{i}__')

    args = shlex.split(command)

    for i, lt in enumerate(lists_and_tuples):
        placeholder = f'__PLACEHOLDER{i}__'
        args = [arg.replace(placeholder, lt) for arg in args]
    return args


def is_pll_function(command):
    from pyskell_special_commands import special_commands
    comando_split = None
    try:
        comando_split = process_command(command)
    except Exception as e:
        print(f"Error SPLITEANDO: {e}.")
        return "continue"

    special_func = special_commands.get(
        comando_split[0].lower().replace(' ', ''))

    if special_func:
        return False

    funcion_nombre = comando_split[0]

    funcion = search_pyskell_function_by_name(funcion_nombre)

    if funcion:
        return True
    return False


def get_variable(hash):
    return variables[[variable["hash"] for variable in variables].index(hash)] if hash in [variable["hash"] for variable in variables] else None


def handle_assignation(command):
    command_split = command.split('=')
    variable_hash = command_split[0].strip()
    variable_to_assign = get_variable(variable_hash)
    command = command_split[1].strip()
    variable_value = run_command(command, True) if is_pll_function(
        command_split[1].strip()) else safe_eval(command_split[1].strip())

    variable_to_assign["value"] = variable_value
    name = variable_to_assign["name"]

    print_if(execution_config['assignations_print'], f"{name} :: {type(variable_value).__name__} = {variable_value}")


def replace_variables_in_command(command):
    if not len(variables) > 0:
        return command, False

    comando = command
    replaced = False

    for variable in variables:
        if variable["hash"] in comando:
            comando = comando.replace(variable["hash"], str(variable["value"]))
            replaced = True

    return comando, replaced


def evaluate_arithmetic_expressions(command):
    command, _ = command
    command_split = command.split(' ')
    command_split[0], command_split[1] = command_split[0], ' '.join(
        command_split[1:])
    try:
        if any(op in command_split[1] for op in ['+', '-', '*', '/', '%', '(', ')']):
            return f"{command_split[0]} {str(eval(command_split[1]))}"
        else:
            return command
    except:
        return command


def tokenize_command_with_incognit(command):
    tokens = []
    in_quotes = False
    current_token = []
    for char in command:
        if char == '"':
            in_quotes = not in_quotes
            current_token.append(char)
        elif char == ' ':
            if in_quotes:
                current_token.append(char)
            else:
                tokens.append(''.join(current_token))
                current_token = []
        else:
            current_token.append(char)
    if current_token:
        tokens.append(''.join(current_token))
    return tokens


def obtain_id_from_prebuild_command(command):
    regex = re.compile(r"[_$][a-zA-Z0-9]+[$][:;]")
    match = regex.search(command)
    if match:
        id = match.group(0)
        id = id[1:][:-2]
        return id
    return False


def get_block_from_prebuild_command(id):
    global loaded_program
    command_block = []
    block_started = False
    block_size = 0

    start_line, end_line = None, None

    for line in loaded_program:
        start_match = re.match(rf'_\${id}\$:.*', line)
        end_match = re.match(rf'_\${id}\$;.*', line)

        if start_match:
            start_line = line
            block_started = True
            continue

        if end_match:
            end_line = line
            break

        if block_started:
            command_block.append(line)
            block_size += 1

    full_block = [start_line] + command_block + [end_line]

    return {
        "inner": (command_block, block_size),
        "full": (full_block, len(full_block)),
    } if block_started and end_match else None


def run_parallel_block(block, concurrency):
    code = []
    proccesses_to_wait = []
    files_to_delete = []
    i = 0

    while i < len(block):
        command = block[i]
        if command.startswith('_$'):
            id = obtain_id_from_prebuild_command(command)
            block_prebuild = get_block_from_prebuild_command(id)
            full_block, size = block_prebuild.get("full")

            file_name = f"./dist/temp-{id}.rpll"
            # Create dist if not exist
            if not os.path.exists("./dist"):
                os.mkdir("./dist")
            with open(file_name, 'w+') as f:
                f.writelines([line + '\n' for line in full_block])
            
            block_proccess = Process(target=run_pll, args=(file_name, None,)) if not concurrency else Thread(target=run_pll, args=(file_name, None,))

            files_to_delete.append(file_name)

            proccesses_to_wait.append(block_proccess)
            block_proccess.start()

            i += size
        else:
            code.append(command)
            i += 1
    
    command_proccesses = []
    if concurrency:
        command_proccesses = [
            Thread(target=run_command, args=(command,)) for command in code if not command.startswith('--')
        ]
    else:
        command_proccesses = [
            Process(target=run_command, args=(command,)) for command in code if not command.startswith('--')
        ]

    for proccess in command_proccesses:
        proccess.start()

    for proccess in command_proccesses:
        proccess.join()

    for proccess in proccesses_to_wait:
        proccess.join()

    for file in files_to_delete:
        os.remove(file)

def handle_concurrent_block(command):
    handle_parallel_block(command, concurrency=True)

def handle_parallel_block(command, concurrency=False):
    global loaded_program
    
    _, arguments = command.split(' ')[0], command.split(' ')[1:]
    if arguments is not None and len(arguments) > 0:
        print("Error: parallel or concurrent blocks doesn't accept arguments.")
        return

    prebuild_command_id = obtain_id_from_prebuild_command(command)
    line_index = loaded_program.index(command)

    parallel_block = []
    for i, line in enumerate(loaded_program[line_index+1:]):
        if obtain_id_from_prebuild_command(line) == prebuild_command_id:
            break
        else:
            parallel_block.append(line)

    run_parallel_block(parallel_block, concurrency)
    increment_pyskell_pc(len(parallel_block))
    # pyskell_pc += len(parallel_block)

def clean_strings(lst):
    return [item if item.strip() != '' else '' for item in lst]

def handle_time_block(command):
    global loaded_program
    
    line_index = loaded_program.index(command)
    split = command.split(' ',1)
    command, arguments = split[0], split[1] if len(split) > 1 else None
    arguments = list(filter(None, clean_strings(arguments.split('"')))) if arguments is not None else None
    prebuild_command_id = obtain_id_from_prebuild_command(command)
    
    
    time_block = []
    for i, line in enumerate(loaded_program[line_index+1:]):
        if obtain_id_from_prebuild_command(line) == prebuild_command_id:
            break
        else:
            time_block.append(line)
    
    time_start = time.time()
    print(arguments[0] if arguments and len(arguments) > 0 else "Time block started.")
    
    # Hilo unico que detiene todo el programa
    thread = Thread(target=run_pll, args=(None, time_block, False,))

    # run_pll(program=time_block, principal=False)
    thread.start()
    thread.join()
    
    print_time_execution(time.time() - time_start, message= arguments[1] if arguments and len(arguments) > 1 else "Time block finished in ")
    
    increment_pyskell_pc(len(time_block))
    # pyskell_pc += len(time_block)

def handle_prebuild_command(command):
    regex = re.compile(r"[:;][a-zA-Z]+$")
    
    # Separe command of arguments
    command_without_args = command.split(' ')[0]
    match = regex.search(command_without_args)

    if match:
        if match.group(0).startswith(';'):
            return "continue"

        prebuild_commands = {
            ':pl': handle_parallel_block,
            ':co': handle_concurrent_block,
            ':ti': handle_time_block,
        }
        prebuild_commands.get(match.group(0), lambda: None)(command)
    else:
        return "continue"


def run_command(comando, with_return=False):
    from pyskell_special_commands import special_commands

    if comando.startswith('_$'):
        handle_prebuild_command(comando)
        return "continue"

    incogint_tokenated = tokenize_command_with_incognit(comando)

    for incognit in incogint_tokenated:
        if incognit.startswith('?'):
            prompt = incognit[1:][1:-1] if incognit[1:].startswith('"') else incognit[1:]
            prompt = (prompt if len(prompt.strip()) > 0 else "?") + \
                (":" if not incognit[1:].startswith('"') else "")

            user_input = None
            for variable_input in variables_inputs:
                if variable_input["prompt"] == prompt:
                    user_input = variable_input["value"]
                    break
            if user_input is None:
                user_input = input(prompt + ' ')

            comando = comando.replace(incognit, user_input)

            variables_inputs.append({"prompt": prompt, "value": user_input})

    if '=' in comando:
        return handle_assignation(comando)

    are_variables = re.compile(r'%.*?%')
    if are_variables.search(comando):
        comando = replace_variables_in_command(comando)

        comando, _ = replace_variables_in_command(comando)

        comando = evaluate_arithmetic_expressions(comando)

    comando_split = None
    try:
        comando_split = process_command(comando)
    except Exception as e:
        print(f"Error SPLITEANDO: {e}.")
        return "continue"

    special_func = special_commands.get(
        comando_split[0].lower().replace(' ', ''))

    if special_func:
        special_func() if len(
            comando_split[1:]) == 0 else special_func(comando_split[1:])
        return "continue"

    argumentos = [safe_eval(arg) if is_valid_list_or_tuple(
        arg) else arg for arg in comando_split[1:]]

    funcion_nombre = comando_split[0]

    funcion = search_pyskell_function_by_name(funcion_nombre)

    if funcion is not None and funcion.calleable():
        funcion.set_command(comando)

        resultado = None
        if len(argumentos) == 0:
            resultado = pyskellRunProccess(funcion)
        else:
            resultado = pyskellRunProccess(funcion, argumentos[0])

        if callable(resultado):
            resultado.set_command(comando)
            resultado_final = pyskellRunProccess(
                apply_args, resultado, argumentos[1:])
            if with_return:
                return resultado_final
            else:
                print(resultado_final)
        else:
            if with_return:
                return resultado
            else:
                print(resultado)
    else:
        if with_return:
            return None
        else:
            print(f"Function '{funcion_nombre}' not recognized or callable.")


def load_program(file):
    program = []

    with open(file, 'r') as f:
        program = f.readlines()
        for i, line in enumerate(program):
            program[i] = line.replace('\n', '')

    return program


def run_pll(file=None, program=None, principal=True):
    global loaded_program
    global is_main_program
    is_main_program = principal

    if program is None and file is not None and principal:
        loaded_program = load_program(file)
        program = loaded_program
    elif program is None and file is None:
        return "Error."
    
    set_pyskell_pc(0)

    while get_pyskell_pc() < len(program):
        try:
            comando = program[get_pyskell_pc()]
            regex = re.compile(r"[;][a-zA-Z]+$")
            if not comando.startswith('--') and not regex.search(comando):
                run_command(comando)
        except:
            return "Error."
        
        increment_pyskell_pc(1)
    
    is_main_program = not is_main_program


