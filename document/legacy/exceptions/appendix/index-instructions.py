#!/usr/bin/env python3

# This script generates the `index-instructions.rst` file. The table in that
# file is particularly annoying to update by hand, since the Restructured Text
# format requires the header and columns to line up properly. This is
# especially tedious when merging changes from the upstream spec, or merging a
# proposal back to the spec when it is standardized.

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_INSTRUCTIONS_RST = os.path.join(SCRIPT_DIR, 'index-instructions.rst')

HEADER = """\
.. DO NOT EDIT: This file is auto-generated by the index-instructions.py script.

.. _appendix:
.. _index-instr:

Index of Instructions
=====================
"""

FOOTER = """\
"""

COLUMNS = [
    'Instruction',
    'Binary Opcode',
    'Type',
    'Validation',
    'Execution',
]


def MathWrap(s, default=''):
    if s is None:
        return default
    else:
        return f':math:`{s}`'


def RefWrap(s, kind):
    if s is None:
        return ''
    else:
        return f':ref:`{kind} <{s}>`'


def Instruction(name, opcode, type=None, validation=None, execution=None, operator=None, validation2=None, execution2=None):
    if operator:
        execution_str = ', '.join([RefWrap(execution, 'execution'),
                                   RefWrap(operator, 'operator')])
    elif execution2:
        execution_str = ', '.join([RefWrap(execution, 'execution'),
                                   RefWrap(execution, 'execution')])

    else:
        execution_str = RefWrap(execution, 'execution')

    if validation2:
        validation_str = ', '.join([RefWrap(validation, 'validation'),
                                    RefWrap(validation2, 'validation')])
    else:
        validation_str = RefWrap(validation, 'validation')

    return (
        MathWrap(name, '(reserved)'),
        MathWrap(opcode),
        MathWrap(type),
        validation_str,
        execution_str
    )


INSTRUCTIONS = [
    Instruction(r'\TRY~\X{bt}', r'\hex{06}', r'[t_1^\ast] \to [t_2^\ast]', r'valid-try-catch', r'exec-try-catch', None, r'valid-try-delegate', r'exec-try-delegate'),
    Instruction(r'\CATCH~x', r'\hex{07}', None, r'valid-try-catch', r'exec-try-catch'),
    Instruction(r'\RETHROW~n', r'\hex{09}', r'[t_1^\ast] \to [t_2^\ast]', r'valid-rethrow', r'exec-rethrow'),
    Instruction(r'\DELEGATE~l', r'\hex{18}', None, r'valid-try-delegate', r'exec-try-delegate'),
    Instruction(r'\CATCHALL', r'\hex{19}', None, r'valid-try-catch', r'exec-try-catch'),
]


def ColumnWidth(n):
    return max([len(instr[n]) for instr in INSTRUCTIONS])

COLUMN_WIDTHS = [ColumnWidth(i) for i in range(len(COLUMNS))]
DIVIDER = '  '.join('=' * width for width in COLUMN_WIDTHS)

def Row(columns):
    return '  '.join(('{:%d}' % COLUMN_WIDTHS[i]).format(column)
                     for i, column in enumerate(columns))

if __name__ == '__main__':
    with open(INDEX_INSTRUCTIONS_RST, 'w') as f:
        print(HEADER, file=f)
        print(DIVIDER, file=f)
        print(Row(COLUMNS), file=f)
        print(DIVIDER, file=f)

        for instr in INSTRUCTIONS:
          print(Row(instr), file=f)

        print(DIVIDER, file=f)
        print(FOOTER, file=f)
