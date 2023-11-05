import os
import sys
import re
import uuid
from pyskell_shared_global import variables
from pyskell_utils import print_if


def read_file(file):
    lines = []
    with open(file, 'r') as f:
        for line in f:
            lines.append(line.rstrip())
    return lines


def count_leading_spaces(line):
    return len(re.match(r'\s*', line).group())


def parse_lines(lines, start=0, level=0, is_top_level=True):
    output = []
    i = start
    while i < len(lines):
        line = lines[i]
        spaces = count_leading_spaces(line)
        command = line.strip()
        if spaces == level:
            i += 1
            nested = []
            while i < len(lines) and count_leading_spaces(lines[i]) > level:
                nested, i = parse_lines(
                    lines, i, count_leading_spaces(lines[i]), is_top_level=False)
            output.append((command, nested) if nested else command)
        elif spaces < level:
            return (output, i) if not is_top_level else output
        else:
            i += 1
    return (output, i) if not is_top_level else output


def group_lines(lines):
    return parse_lines(lines)


def build_complete_block(name, block, args = None):
    unique_id = str(abs(hash(uuid.uuid4())))
    return [f'_${unique_id}$:{name}' + ((f' {args}') if args is not None else '')] + block + [f'_${unique_id}$;{name}']

def to_parallel_rpll_block(block):
    unique_name = 'pl'
    return build_complete_block(unique_name, block[1])

def to_concurrent_rpll_block(block):
    unique_name = 'co'
    return build_complete_block(unique_name, block[1])

def to_time_rpll_block(block):
    split = block[0].split(' ', 1)
    args = split[1] if len(split) > 1 else None
    unique_name = 'ti'
    return build_complete_block(unique_name, block[1], args)

def to_for_rpll_block(block):
    command, block = block

    _, var_name, repeat_count = command.split()
    repeat_count = int(repeat_count)

    output = []
    for i in range(repeat_count):
        copied_block = [item.copy() if isinstance(item, list)
                        else item for item in block]

        expanded_block = to_rpll_block(copied_block)

        regex = re.compile(r'\b' + re.escape(var_name) + r'\b')
        for j, line in enumerate(expanded_block):
            if isinstance(line, str):
                expanded_block[j] = regex.sub(str(i), line)
            elif isinstance(line, tuple):
                inner_command, inner_block = line
                expanded_block[j] = (
                    regex.sub(str(i), inner_command), inner_block)

        output.extend(expanded_block)

    return output


def handle_tuple_block(block):
    options = {
        'parallel': to_parallel_rpll_block,
        'concurrent': to_concurrent_rpll_block,
        'time': to_time_rpll_block,
        'for': to_for_rpll_block,
    }
    return options.get(block[0].split()[0], lambda: None)(block)


def to_rpll_block(grouped_lines):
    output = []
    for block in grouped_lines:
        if isinstance(block, tuple):
            out = handle_tuple_block(block)
            output.extend(
                handle_tuple_block(block)
            )
        else:
            output.append(block)

    if any(isinstance(x, tuple) for x in output):
        output = to_rpll_block(output)
    return output


def handle_for_loop_with_complex_evaluation(grouped_lines):
    expanded_lines = []

    for item in grouped_lines:
        if isinstance(item, tuple):
            command, block = item
            if command.startswith("for"):
                _, var_name, repeat_count = command.split()
                repeat_count = int(repeat_count)

                regex = re.compile(r'\b' + re.escape(var_name) + r'\b')

                for i in range(repeat_count):
                    expanded_block = []
                    for line in block:
                        replaced_line = regex.sub(str(i), line)

                        try:
                            evaluated_line = ' '.join([str(eval(comp)) if any(op in comp for op in [
                                                      '+', '-', '*', '/', '%', '(', ')']) else comp for comp in replaced_line.split()])
                        except:
                            evaluated_line = replaced_line

                        cleaned_line = evaluated_line.replace(
                            ".0 ", " ").replace(".0", "")

                        expanded_block.append(cleaned_line)

                    expanded_lines.extend(expanded_block)
            else:
                pass
        else:
            expanded_lines.append(item)

    return expanded_lines


# def handle_for_loop_with_cleaning(grouped_lines):
#     expanded_lines = to_rpll_block(grouped_lines)

#     cleaned_lines = [
#         line for line in expanded_lines if line.strip() and not line.startswith("--")]

#     return cleaned_lines


def generate_rpll(file, expanded_lines):
    expanded_lines = [
        line for line in expanded_lines if line.strip() and not line.startswith("--")]
    
    file_name = os.path.basename(file)
    file_name = file_name.replace('.pll', '.rpll').replace('.\\', '')
    try:
        os.stat('dist')
    except:
        os.mkdir('dist')

    with open(f"dist/{file_name}", 'w+') as f:
        for i, line in enumerate(expanded_lines):
            f.write(line + '\n') if i + \
                1 != len(expanded_lines) else f.write(line)

    return f"./dist/{file_name}"


def evaluate_expressions_in_line(line):
    components = line.split()
    new_components = []

    for comp in components:
        from pyskell_functions import pyskell_exported_functions
        if comp not in [f.name for f in pyskell_exported_functions]:
            try:
                new_component = eval(comp)
            except:
                new_component = comp
        else:
            new_component = comp

        new_components.append(str(new_component))

    return ' '.join(new_components)


def post_process_expanded_lines(expanded_lines):
    new_lines = []
    for line in expanded_lines:
        if isinstance(line, str):
            new_lines.append(evaluate_expressions_in_line(line))
        else:
            command, block = line
            new_block = post_process_expanded_lines(block)
            new_lines.append((command, new_block))
    return new_lines


def separe_rpll_and_calculable_lines(expanded_lines):
    rpll_lines = []
    calculable_lines = []
    for line in expanded_lines:
        if not '=' in line:
            rpll_lines.append(line)
        else:
            calculable_lines.append(line)
    return rpll_lines, calculable_lines


def throw_duplicates(elements):
    new_elements = []
    seen = set()

    for element in elements:
        name = element["name"]
        if name not in seen:
            seen.add(name)
            new_elements.append(element)

    return new_elements


def build(file, print_log=False):
    lines = read_file(file)

    grouped_lines = group_lines(lines)
    print_if(print_log, 'grouped_lines: ', grouped_lines)

    expanded_lines = to_rpll_block(grouped_lines)
    print_if(print_log, 'handle for loops in expanded_lines: ', expanded_lines)

    expanded_lines = post_process_expanded_lines(expanded_lines)

    rpll_lines, calculable_lines = separe_rpll_and_calculable_lines(
        expanded_lines)

    print_if(print_log, 'rpll_lines: ', rpll_lines)
    print_if(print_log, 'calculable_lines: ', calculable_lines)

    for i in calculable_lines:
        [left_side, _] = i.split('=')
        variables.append({
            "name": left_side.strip(),
            "value": None,
            "hash": f"%{str(abs(hash(f'{left_side.strip()}')))}%"
        })

    print_if(print_log, 'variables: ', throw_duplicates(variables))

    for i, line in enumerate(expanded_lines):
        for variable in variables:
            if variable["name"] in line:
                expanded_lines[i] = expanded_lines[i].replace(
                    variable["name"], variable["hash"])

    return generate_rpll(file, expanded_lines)
