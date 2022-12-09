
import re


def remove_reg_var(file_path: str, remove_var: list = ["year"], next_line=True) -> None:
    """
    Remove certain variables shown in latex table
    `remove_var` takes a list of the start words of the removed varaibles (case sensitive)
    """

    with open(file_path, 'r', encoding='utf8') as f:
        lines = f.readlines()

    remove_idx = []
    for i, li in enumerate(lines):
        for s in remove_var:
            if li.startswith(s):
                remove_idx.append(i)
                if next_line:
                    remove_idx.append(i + 1)

    lines = [li for i, li in enumerate(lines) if i not in remove_idx]

    with open(file_path, 'w', encoding='utf8') as f:
        f.writelines(lines)


def remove_preceding_zero(file_path: str) -> None:

    with open(file_path, 'r', encoding='utf8') as f:
        lines = f.readlines()

    lines = [re.sub('(?<!\d)0\.', '.', li) for li in lines]

    with open(file_path, 'w', encoding='utf8') as f:
        f.writelines(lines)


def remove_float_zero(file_path: str, lines_idx: list) -> None:
    """
    Remove .00... for int rows
    However this will remove also not float rows with some entry happen to be .00
    Thus lines_idx is must
    """

    with open(file_path, 'r', encoding='utf8') as f:
        lines = f.readlines()

    lines = [re.sub('(?<=\d)\.0+\s', ' ', li) if idx in lines_idx else li for idx, li in enumerate(lines)]

    with open(file_path, 'w', encoding='utf8') as f:
        f.writelines(lines)


def reduce_float_digit(file_path: str, digit: int, lines_idx: list) -> None:
    """
    Reduce float digits for specific lines
    """

    with open(file_path, 'r', encoding='utf8') as f:
        lines = f.readlines()

    def reduce_digit(x): return f'{float(x.group(0)):.{digit}f}'.lstrip('0')
    lines = [re.sub('\.\d+', reduce_digit, li) if idx in lines_idx else li for idx, li in enumerate(lines)]

    with open(file_path, 'w', encoding='utf8') as f:
        f.writelines(lines)


def replace_string(file_path: str, pat: str, repl: str, lines_idx: list = None) -> None:
    """
    Note: to input a real \ in `repl` need \\\\
    """

    with open(file_path, 'r', encoding='utf8') as f:
        lines = f.readlines()

    if lines_idx is not None:
        lines = [re.sub(pat, repl, li) if idx in lines_idx else li for idx, li in enumerate(lines)]
    else:
        lines = [re.sub(pat, repl, li) for li in lines]

    with open(file_path, 'w', encoding='utf8') as f:
        f.writelines(lines)


def add_line(file_path: str, new_line: str, line_idx: int, linebreak: str = "\\\\ ") -> None:

    with open(file_path, 'r', encoding='utf8') as f:
        lines = f.readlines()

    lines.insert(line_idx, " " + new_line + linebreak)

    with open(file_path, 'w', encoding='utf8') as f:
        f.writelines(lines)


def drop_line(file_path: str, lines_idx: list):

    with open(file_path, 'r', encoding='utf8') as f:
        lines = f.readlines()

    lines = [li for idx, li in enumerate(lines) if idx not in lines_idx]

    with open(file_path, 'w', encoding='utf8') as f:
        f.writelines(lines)
