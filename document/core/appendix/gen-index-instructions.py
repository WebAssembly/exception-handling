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
.. DO NOT EDIT: This file is auto-generated by the gen-index-instructions.py script.

.. index:: instruction
.. _index-instr:

Index of Instructions
---------------------
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


def Instruction(name, opcode, type=None, validation=None, execution=None, operator=None):
    if operator:
        execution_str = ', '.join([RefWrap(execution, 'execution'),
                                   RefWrap(operator, 'operator')])
    else:
        execution_str = RefWrap(execution, 'execution')

    return (
        MathWrap(name, '(reserved)'),
        MathWrap(opcode),
        MathWrap(type),
        RefWrap(validation, 'validation'),
        execution_str
    )


INSTRUCTIONS = [
    Instruction(r'\UNREACHABLE', r'\hex{00}', r'[t_1^\ast] \to [t_2^\ast]', r'valid-unreachable', r'exec-unreachable'),
    Instruction(r'\NOP', r'\hex{01}', r'[] \to []', r'valid-nop', r'exec-nop'),
    Instruction(r'\BLOCK~\X{bt}', r'\hex{02}', r'[t_1^\ast] \to [t_2^\ast]', r'valid-block', r'exec-block'),
    Instruction(r'\LOOP~\X{bt}', r'\hex{03}', r'[t_1^\ast] \to [t_2^\ast]', r'valid-loop', r'exec-loop'),
    Instruction(r'\IF~\X{bt}', r'\hex{04}', r'[t_1^\ast~\I32] \to [t_2^\ast]', r'valid-if', r'exec-if'),
    Instruction(r'\ELSE', r'\hex{05}'),
    Instruction(None, r'\hex{06}'),
    Instruction(None, r'\hex{07}'),
    Instruction(None, r'\hex{08}'),
    Instruction(None, r'\hex{09}'),
    Instruction(None, r'\hex{0A}'),
    Instruction(r'\END', r'\hex{0B}'),
    Instruction(r'\BR~l', r'\hex{0C}', r'[t_1^\ast~t^\ast] \to [t_2^\ast]', r'valid-br', r'exec-br'),
    Instruction(r'\BRIF~l', r'\hex{0D}', r'[t^\ast~\I32] \to [t^\ast]', r'valid-br_if', r'exec-br_if'),
    Instruction(r'\BRTABLE~l^\ast~l', r'\hex{0E}', r'[t_1^\ast~t^\ast~\I32] \to [t_2^\ast]', r'valid-br_table', r'exec-br_table'),
    Instruction(r'\RETURN', r'\hex{0F}', r'[t_1^\ast~t^\ast] \to [t_2^\ast]', r'valid-return', r'exec-return'),
    Instruction(r'\CALL~x', r'\hex{10}', r'[t_1^\ast] \to [t_2^\ast]', r'valid-call', r'exec-call'),
    Instruction(r'\CALLINDIRECT~x~y', r'\hex{11}', r'[t_1^\ast~\I32] \to [t_2^\ast]', r'valid-call_indirect', r'exec-call_indirect'),
    Instruction(None, r'\hex{12}'),
    Instruction(None, r'\hex{13}'),
    Instruction(None, r'\hex{14}'),
    Instruction(None, r'\hex{15}'),
    Instruction(None, r'\hex{16}'),
    Instruction(None, r'\hex{17}'),
    Instruction(None, r'\hex{18}'),
    Instruction(None, r'\hex{19}'),
    Instruction(r'\DROP', r'\hex{1A}', r'[t] \to []', r'valid-drop', r'exec-drop'),
    Instruction(r'\SELECT', r'\hex{1B}', r'[t~t~\I32] \to [t]', r'valid-select', r'exec-select'),
    Instruction(r'\SELECT~t', r'\hex{1C}', r'[t~t~\I32] \to [t]', r'valid-select', r'exec-select'),
    Instruction(None, r'\hex{1D}'),
    Instruction(None, r'\hex{1E}'),
    Instruction(None, r'\hex{1F}'),
    Instruction(r'\LOCALGET~x', r'\hex{20}', r'[] \to [t]', r'valid-local.get', r'exec-local.get'),
    Instruction(r'\LOCALSET~x', r'\hex{21}', r'[t] \to []', r'valid-local.set', r'exec-local.set'),
    Instruction(r'\LOCALTEE~x', r'\hex{22}', r'[t] \to [t]', r'valid-local.tee', r'exec-local.tee'),
    Instruction(r'\GLOBALGET~x', r'\hex{23}', r'[] \to [t]', r'valid-global.get', r'exec-global.get'),
    Instruction(r'\GLOBALSET~x', r'\hex{24}', r'[t] \to []', r'valid-global.set', r'exec-global.set'),
    Instruction(r'\TABLEGET~x', r'\hex{25}', r'[\I32] \to [t]', r'valid-table.get', r'exec-table.get'),
    Instruction(r'\TABLESET~x', r'\hex{26}', r'[\I32~t] \to []', r'valid-table.set', r'exec-table.set'),
    Instruction(None, r'\hex{27}'),
    Instruction(r'\I32.\LOAD~\memarg', r'\hex{28}', r'[\I32] \to [\I32]', r'valid-load', r'exec-load'),
    Instruction(r'\I64.\LOAD~\memarg', r'\hex{29}', r'[\I32] \to [\I64]', r'valid-load', r'exec-load'),
    Instruction(r'\F32.\LOAD~\memarg', r'\hex{2A}', r'[\I32] \to [\F32]', r'valid-load', r'exec-load'),
    Instruction(r'\F64.\LOAD~\memarg', r'\hex{2B}', r'[\I32] \to [\F64]', r'valid-load', r'exec-load'),
    Instruction(r'\I32.\LOAD\K{8\_s}~\memarg', r'\hex{2C}', r'[\I32] \to [\I32]', r'valid-loadn', r'exec-loadn'),
    Instruction(r'\I32.\LOAD\K{8\_u}~\memarg', r'\hex{2D}', r'[\I32] \to [\I32]', r'valid-loadn', r'exec-loadn'),
    Instruction(r'\I32.\LOAD\K{16\_s}~\memarg', r'\hex{2E}', r'[\I32] \to [\I32]', r'valid-loadn', r'exec-loadn'),
    Instruction(r'\I32.\LOAD\K{16\_u}~\memarg', r'\hex{2F}', r'[\I32] \to [\I32]', r'valid-loadn', r'exec-loadn'),
    Instruction(r'\I64.\LOAD\K{8\_s}~\memarg', r'\hex{30}', r'[\I32] \to [\I64]', r'valid-loadn', r'exec-loadn'),
    Instruction(r'\I64.\LOAD\K{8\_u}~\memarg', r'\hex{31}', r'[\I32] \to [\I64]', r'valid-loadn', r'exec-loadn'),
    Instruction(r'\I64.\LOAD\K{16\_s}~\memarg', r'\hex{32}', r'[\I32] \to [\I64]', r'valid-loadn', r'exec-loadn'),
    Instruction(r'\I64.\LOAD\K{16\_u}~\memarg', r'\hex{33}', r'[\I32] \to [\I64]', r'valid-loadn', r'exec-loadn'),
    Instruction(r'\I64.\LOAD\K{32\_s}~\memarg', r'\hex{34}', r'[\I32] \to [\I64]', r'valid-loadn', r'exec-loadn'),
    Instruction(r'\I64.\LOAD\K{32\_u}~\memarg', r'\hex{35}', r'[\I32] \to [\I64]', r'valid-loadn', r'exec-loadn'),
    Instruction(r'\I32.\STORE~\memarg', r'\hex{36}', r'[\I32~\I32] \to []', r'valid-store', r'exec-store'),
    Instruction(r'\I64.\STORE~\memarg', r'\hex{37}', r'[\I32~\I64] \to []', r'valid-store', r'exec-store'),
    Instruction(r'\F32.\STORE~\memarg', r'\hex{38}', r'[\I32~\F32] \to []', r'valid-store', r'exec-store'),
    Instruction(r'\F64.\STORE~\memarg', r'\hex{39}', r'[\I32~\F64] \to []', r'valid-store', r'exec-store'),
    Instruction(r'\I32.\STORE\K{8}~\memarg', r'\hex{3A}', r'[\I32~\I32] \to []', r'valid-storen', r'exec-storen'),
    Instruction(r'\I32.\STORE\K{16}~\memarg', r'\hex{3B}', r'[\I32~\I32] \to []', r'valid-storen', r'exec-storen'),
    Instruction(r'\I64.\STORE\K{8}~\memarg', r'\hex{3C}', r'[\I32~\I64] \to []', r'valid-storen', r'exec-storen'),
    Instruction(r'\I64.\STORE\K{16}~\memarg', r'\hex{3D}', r'[\I32~\I64] \to []', r'valid-storen', r'exec-storen'),
    Instruction(r'\I64.\STORE\K{32}~\memarg', r'\hex{3E}', r'[\I32~\I64] \to []', r'valid-storen', r'exec-storen'),
    Instruction(r'\MEMORYSIZE', r'\hex{3F}', r'[] \to [\I32]', r'valid-memory.size', r'exec-memory.size'),
    Instruction(r'\MEMORYGROW', r'\hex{40}', r'[\I32] \to [\I32]', r'valid-memory.grow', r'exec-memory.grow'),
    Instruction(r'\I32.\CONST~\i32', r'\hex{41}', r'[] \to [\I32]', r'valid-const', r'exec-const'),
    Instruction(r'\I64.\CONST~\i64', r'\hex{42}', r'[] \to [\I64]', r'valid-const', r'exec-const'),
    Instruction(r'\F32.\CONST~\f32', r'\hex{43}', r'[] \to [\F32]', r'valid-const', r'exec-const'),
    Instruction(r'\F64.\CONST~\f64', r'\hex{44}', r'[] \to [\F64]', r'valid-const', r'exec-const'),
    Instruction(r'\I32.\EQZ', r'\hex{45}', r'[\I32] \to [\I32]', r'valid-testop', r'exec-testop', r'op-ieqz'),
    Instruction(r'\I32.\EQ', r'\hex{46}', r'[\I32~\I32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ieq'),
    Instruction(r'\I32.\NE', r'\hex{47}', r'[\I32~\I32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ine'),
    Instruction(r'\I32.\LT\K{\_s}', r'\hex{48}', r'[\I32~\I32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ilt_s'),
    Instruction(r'\I32.\LT\K{\_u}', r'\hex{49}', r'[\I32~\I32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ilt_u'),
    Instruction(r'\I32.\GT\K{\_s}', r'\hex{4A}', r'[\I32~\I32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-igt_s'),
    Instruction(r'\I32.\GT\K{\_u}', r'\hex{4B}', r'[\I32~\I32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-igt_u'),
    Instruction(r'\I32.\LE\K{\_s}', r'\hex{4C}', r'[\I32~\I32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ile_s'),
    Instruction(r'\I32.\LE\K{\_u}', r'\hex{4D}', r'[\I32~\I32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ile_u'),
    Instruction(r'\I32.\GE\K{\_s}', r'\hex{4E}', r'[\I32~\I32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ige_s'),
    Instruction(r'\I32.\GE\K{\_u}', r'\hex{4F}', r'[\I32~\I32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ige_u'),
    Instruction(r'\I64.\EQZ', r'\hex{50}', r'[\I64] \to [\I32]', r'valid-testop', r'exec-testop', r'op-ieqz'),
    Instruction(r'\I64.\EQ', r'\hex{51}', r'[\I64~\I64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ieq'),
    Instruction(r'\I64.\NE', r'\hex{52}', r'[\I64~\I64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ine'),
    Instruction(r'\I64.\LT\K{\_s}', r'\hex{53}', r'[\I64~\I64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ilt_s'),
    Instruction(r'\I64.\LT\K{\_u}', r'\hex{54}', r'[\I64~\I64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ilt_u'),
    Instruction(r'\I64.\GT\K{\_s}', r'\hex{55}', r'[\I64~\I64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-igt_s'),
    Instruction(r'\I64.\GT\K{\_u}', r'\hex{56}', r'[\I64~\I64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-igt_u'),
    Instruction(r'\I64.\LE\K{\_s}', r'\hex{57}', r'[\I64~\I64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ile_s'),
    Instruction(r'\I64.\LE\K{\_u}', r'\hex{58}', r'[\I64~\I64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ile_u'),
    Instruction(r'\I64.\GE\K{\_s}', r'\hex{59}', r'[\I64~\I64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ige_s'),
    Instruction(r'\I64.\GE\K{\_u}', r'\hex{5A}', r'[\I64~\I64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-ige_u'),
    Instruction(r'\F32.\EQ', r'\hex{5B}', r'[\F32~\F32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-feq'),
    Instruction(r'\F32.\NE', r'\hex{5C}', r'[\F32~\F32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-fne'),
    Instruction(r'\F32.\LT', r'\hex{5D}', r'[\F32~\F32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-flt'),
    Instruction(r'\F32.\GT', r'\hex{5E}', r'[\F32~\F32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-fgt'),
    Instruction(r'\F32.\LE', r'\hex{5F}', r'[\F32~\F32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-fle'),
    Instruction(r'\F32.\GE', r'\hex{60}', r'[\F32~\F32] \to [\I32]', r'valid-relop', r'exec-relop', r'op-fge'),
    Instruction(r'\F64.\EQ', r'\hex{61}', r'[\F64~\F64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-feq'),
    Instruction(r'\F64.\NE', r'\hex{62}', r'[\F64~\F64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-fne'),
    Instruction(r'\F64.\LT', r'\hex{63}', r'[\F64~\F64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-flt'),
    Instruction(r'\F64.\GT', r'\hex{64}', r'[\F64~\F64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-fgt'),
    Instruction(r'\F64.\LE', r'\hex{65}', r'[\F64~\F64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-fle'),
    Instruction(r'\F64.\GE', r'\hex{66}', r'[\F64~\F64] \to [\I32]', r'valid-relop', r'exec-relop', r'op-fge'),
    Instruction(r'\I32.\CLZ', r'\hex{67}', r'[\I32] \to [\I32]', r'valid-unop', r'exec-unop', r'op-iclz'),
    Instruction(r'\I32.\CTZ', r'\hex{68}', r'[\I32] \to [\I32]', r'valid-unop', r'exec-unop', r'op-ictz'),
    Instruction(r'\I32.\POPCNT', r'\hex{69}', r'[\I32] \to [\I32]', r'valid-unop', r'exec-unop', r'op-ipopcnt'),
    Instruction(r'\I32.\ADD', r'\hex{6A}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-iadd'),
    Instruction(r'\I32.\SUB', r'\hex{6B}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-isub'),
    Instruction(r'\I32.\MUL', r'\hex{6C}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-imul'),
    Instruction(r'\I32.\DIV\K{\_s}', r'\hex{6D}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-idiv_s'),
    Instruction(r'\I32.\DIV\K{\_u}', r'\hex{6E}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-idiv_u'),
    Instruction(r'\I32.\REM\K{\_s}', r'\hex{6F}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-irem_s'),
    Instruction(r'\I32.\REM\K{\_u}', r'\hex{70}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-irem_u'),
    Instruction(r'\I32.\AND', r'\hex{71}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-iand'),
    Instruction(r'\I32.\OR', r'\hex{72}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-ior'),
    Instruction(r'\I32.\XOR', r'\hex{73}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-ixor'),
    Instruction(r'\I32.\SHL', r'\hex{74}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-ishl'),
    Instruction(r'\I32.\SHR\K{\_s}', r'\hex{75}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-ishr_s'),
    Instruction(r'\I32.\SHR\K{\_u}', r'\hex{76}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-ishr_u'),
    Instruction(r'\I32.\ROTL', r'\hex{77}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-irotl'),
    Instruction(r'\I32.\ROTR', r'\hex{78}', r'[\I32~\I32] \to [\I32]', r'valid-binop', r'exec-binop', r'op-irotr'),
    Instruction(r'\I64.\CLZ', r'\hex{79}', r'[\I64] \to [\I64]', r'valid-unop', r'exec-unop', r'op-iclz'),
    Instruction(r'\I64.\CTZ', r'\hex{7A}', r'[\I64] \to [\I64]', r'valid-unop', r'exec-unop', r'op-ictz'),
    Instruction(r'\I64.\POPCNT', r'\hex{7B}', r'[\I64] \to [\I64]', r'valid-unop', r'exec-unop', r'op-ipopcnt'),
    Instruction(r'\I64.\ADD', r'\hex{7C}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-iadd'),
    Instruction(r'\I64.\SUB', r'\hex{7D}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-isub'),
    Instruction(r'\I64.\MUL', r'\hex{7E}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-imul'),
    Instruction(r'\I64.\DIV\K{\_s}', r'\hex{7F}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-idiv_s'),
    Instruction(r'\I64.\DIV\K{\_u}', r'\hex{80}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-idiv_u'),
    Instruction(r'\I64.\REM\K{\_s}', r'\hex{81}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-irem_s'),
    Instruction(r'\I64.\REM\K{\_u}', r'\hex{82}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-irem_u'),
    Instruction(r'\I64.\AND', r'\hex{83}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-iand'),
    Instruction(r'\I64.\OR', r'\hex{84}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-ior'),
    Instruction(r'\I64.\XOR', r'\hex{85}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-ixor'),
    Instruction(r'\I64.\SHL', r'\hex{86}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-ishl'),
    Instruction(r'\I64.\SHR\K{\_s}', r'\hex{87}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-ishr_s'),
    Instruction(r'\I64.\SHR\K{\_u}', r'\hex{88}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-ishr_u'),
    Instruction(r'\I64.\ROTL', r'\hex{89}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-irotl'),
    Instruction(r'\I64.\ROTR', r'\hex{8A}', r'[\I64~\I64] \to [\I64]', r'valid-binop', r'exec-binop', r'op-irotr'),
    Instruction(r'\F32.\ABS', r'\hex{8B}', r'[\F32] \to [\F32]', r'valid-unop', r'exec-unop', r'op-fabs'),
    Instruction(r'\F32.\NEG', r'\hex{8C}', r'[\F32] \to [\F32]', r'valid-unop', r'exec-unop', r'op-fneg'),
    Instruction(r'\F32.\CEIL', r'\hex{8D}', r'[\F32] \to [\F32]', r'valid-unop', r'exec-unop', r'op-fceil'),
    Instruction(r'\F32.\FLOOR', r'\hex{8E}', r'[\F32] \to [\F32]', r'valid-unop', r'exec-unop', r'op-ffloor'),
    Instruction(r'\F32.\TRUNC', r'\hex{8F}', r'[\F32] \to [\F32]', r'valid-unop', r'exec-unop', r'op-ftrunc'),
    Instruction(r'\F32.\NEAREST', r'\hex{90}', r'[\F32] \to [\F32]', r'valid-unop', r'exec-unop', r'op-fnearest'),
    Instruction(r'\F32.\SQRT', r'\hex{91}', r'[\F32] \to [\F32]', r'valid-unop', r'exec-unop', r'op-fsqrt'),
    Instruction(r'\F32.\ADD', r'\hex{92}', r'[\F32~\F32] \to [\F32]', r'valid-binop', r'exec-binop', r'op-fadd'),
    Instruction(r'\F32.\SUB', r'\hex{93}', r'[\F32~\F32] \to [\F32]', r'valid-binop', r'exec-binop', r'op-fsub'),
    Instruction(r'\F32.\MUL', r'\hex{94}', r'[\F32~\F32] \to [\F32]', r'valid-binop', r'exec-binop', r'op-fmul'),
    Instruction(r'\F32.\DIV', r'\hex{95}', r'[\F32~\F32] \to [\F32]', r'valid-binop', r'exec-binop', r'op-fdiv'),
    Instruction(r'\F32.\FMIN', r'\hex{96}', r'[\F32~\F32] \to [\F32]', r'valid-binop', r'exec-binop', r'op-fmin'),
    Instruction(r'\F32.\FMAX', r'\hex{97}', r'[\F32~\F32] \to [\F32]', r'valid-binop', r'exec-binop', r'op-fmax'),
    Instruction(r'\F32.\COPYSIGN', r'\hex{98}', r'[\F32~\F32] \to [\F32]', r'valid-binop', r'exec-binop', r'op-fcopysign'),
    Instruction(r'\F64.\ABS', r'\hex{99}', r'[\F64] \to [\F64]', r'valid-unop', r'exec-unop', r'op-fabs'),
    Instruction(r'\F64.\NEG', r'\hex{9A}', r'[\F64] \to [\F64]', r'valid-unop', r'exec-unop', r'op-fneg'),
    Instruction(r'\F64.\CEIL', r'\hex{9B}', r'[\F64] \to [\F64]', r'valid-unop', r'exec-unop', r'op-fceil'),
    Instruction(r'\F64.\FLOOR', r'\hex{9C}', r'[\F64] \to [\F64]', r'valid-unop', r'exec-unop', r'op-ffloor'),
    Instruction(r'\F64.\TRUNC', r'\hex{9D}', r'[\F64] \to [\F64]', r'valid-unop', r'exec-unop', r'op-ftrunc'),
    Instruction(r'\F64.\NEAREST', r'\hex{9E}', r'[\F64] \to [\F64]', r'valid-unop', r'exec-unop', r'op-fnearest'),
    Instruction(r'\F64.\SQRT', r'\hex{9F}', r'[\F64] \to [\F64]', r'valid-unop', r'exec-unop', r'op-fsqrt'),
    Instruction(r'\F64.\ADD', r'\hex{A0}', r'[\F64~\F64] \to [\F64]', r'valid-binop', r'exec-binop', r'op-fadd'),
    Instruction(r'\F64.\SUB', r'\hex{A1}', r'[\F64~\F64] \to [\F64]', r'valid-binop', r'exec-binop', r'op-fsub'),
    Instruction(r'\F64.\MUL', r'\hex{A2}', r'[\F64~\F64] \to [\F64]', r'valid-binop', r'exec-binop', r'op-fmul'),
    Instruction(r'\F64.\DIV', r'\hex{A3}', r'[\F64~\F64] \to [\F64]', r'valid-binop', r'exec-binop', r'op-fdiv'),
    Instruction(r'\F64.\FMIN', r'\hex{A4}', r'[\F64~\F64] \to [\F64]', r'valid-binop', r'exec-binop', r'op-fmin'),
    Instruction(r'\F64.\FMAX', r'\hex{A5}', r'[\F64~\F64] \to [\F64]', r'valid-binop', r'exec-binop', r'op-fmax'),
    Instruction(r'\F64.\COPYSIGN', r'\hex{A6}', r'[\F64~\F64] \to [\F64]', r'valid-binop', r'exec-binop', r'op-fcopysign'),
    Instruction(r'\I32.\WRAP\K{\_}\I64', r'\hex{A7}', r'[\I64] \to [\I32]', r'valid-cvtop', r'exec-cvtop', r'op-wrap'),
    Instruction(r'\I32.\TRUNC\K{\_}\F32\K{\_s}', r'\hex{A8}', r'[\F32] \to [\I32]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_s'),
    Instruction(r'\I32.\TRUNC\K{\_}\F32\K{\_u}', r'\hex{A9}', r'[\F32] \to [\I32]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_u'),
    Instruction(r'\I32.\TRUNC\K{\_}\F64\K{\_s}', r'\hex{AA}', r'[\F64] \to [\I32]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_s'),
    Instruction(r'\I32.\TRUNC\K{\_}\F64\K{\_u}', r'\hex{AB}', r'[\F64] \to [\I32]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_u'),
    Instruction(r'\I64.\EXTEND\K{\_}\I32\K{\_s}', r'\hex{AC}', r'[\I32] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-extend_s'),
    Instruction(r'\I64.\EXTEND\K{\_}\I32\K{\_u}', r'\hex{AD}', r'[\I32] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-extend_u'),
    Instruction(r'\I64.\TRUNC\K{\_}\F32\K{\_s}', r'\hex{AE}', r'[\F32] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_s'),
    Instruction(r'\I64.\TRUNC\K{\_}\F32\K{\_u}', r'\hex{AF}', r'[\F32] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_u'),
    Instruction(r'\I64.\TRUNC\K{\_}\F64\K{\_s}', r'\hex{B0}', r'[\F64] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_s'),
    Instruction(r'\I64.\TRUNC\K{\_}\F64\K{\_u}', r'\hex{B1}', r'[\F64] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_u'),
    Instruction(r'\F32.\CONVERT\K{\_}\I32\K{\_s}', r'\hex{B2}', r'[\I32] \to [\F32]', r'valid-cvtop', r'exec-cvtop', r'op-convert_s'),
    Instruction(r'\F32.\CONVERT\K{\_}\I32\K{\_u}', r'\hex{B3}', r'[\I32] \to [\F32]', r'valid-cvtop', r'exec-cvtop', r'op-convert_u'),
    Instruction(r'\F32.\CONVERT\K{\_}\I64\K{\_s}', r'\hex{B4}', r'[\I64] \to [\F32]', r'valid-cvtop', r'exec-cvtop', r'op-convert_s'),
    Instruction(r'\F32.\CONVERT\K{\_}\I64\K{\_u}', r'\hex{B5}', r'[\I64] \to [\F32]', r'valid-cvtop', r'exec-cvtop', r'op-convert_u'),
    Instruction(r'\F32.\DEMOTE\K{\_}\F64', r'\hex{B6}', r'[\F64] \to [\F32]', r'valid-cvtop', r'exec-cvtop', r'op-demote'),
    Instruction(r'\F64.\CONVERT\K{\_}\I32\K{\_s}', r'\hex{B7}', r'[\I32] \to [\F64]', r'valid-cvtop', r'exec-cvtop', r'op-convert_s'),
    Instruction(r'\F64.\CONVERT\K{\_}\I32\K{\_u}', r'\hex{B8}', r'[\I32] \to [\F64]', r'valid-cvtop', r'exec-cvtop', r'op-convert_u'),
    Instruction(r'\F64.\CONVERT\K{\_}\I64\K{\_s}', r'\hex{B9}', r'[\I64] \to [\F64]', r'valid-cvtop', r'exec-cvtop', r'op-convert_s'),
    Instruction(r'\F64.\CONVERT\K{\_}\I64\K{\_u}', r'\hex{BA}', r'[\I64] \to [\F64]', r'valid-cvtop', r'exec-cvtop', r'op-convert_u'),
    Instruction(r'\F64.\PROMOTE\K{\_}\F32', r'\hex{BB}', r'[\F32] \to [\F64]', r'valid-cvtop', r'exec-cvtop', r'op-promote'),
    Instruction(r'\I32.\REINTERPRET\K{\_}\F32', r'\hex{BC}', r'[\F32] \to [\I32]', r'valid-cvtop', r'exec-cvtop', r'op-reinterpret'),
    Instruction(r'\I64.\REINTERPRET\K{\_}\F64', r'\hex{BD}', r'[\F64] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-reinterpret'),
    Instruction(r'\F32.\REINTERPRET\K{\_}\I32', r'\hex{BE}', r'[\I32] \to [\F32]', r'valid-cvtop', r'exec-cvtop', r'op-reinterpret'),
    Instruction(r'\F64.\REINTERPRET\K{\_}\I64', r'\hex{BF}', r'[\I64] \to [\F64]', r'valid-cvtop', r'exec-cvtop', r'op-reinterpret'),
    Instruction(r'\I32.\EXTEND\K{8\_s}', r'\hex{C0}', r'[\I32] \to [\I32]', r'valid-unop', r'exec-unop', r'op-iextendn_s'),
    Instruction(r'\I32.\EXTEND\K{16\_s}', r'\hex{C1}', r'[\I32] \to [\I32]', r'valid-unop', r'exec-unop', r'op-iextendn_s'),
    Instruction(r'\I64.\EXTEND\K{8\_s}', r'\hex{C2}', r'[\I64] \to [\I64]', r'valid-unop', r'exec-unop', r'op-iextendn_s'),
    Instruction(r'\I64.\EXTEND\K{16\_s}', r'\hex{C3}', r'[\I64] \to [\I64]', r'valid-unop', r'exec-unop', r'op-iextendn_s'),
    Instruction(r'\I64.\EXTEND\K{32\_s}', r'\hex{C4}', r'[\I64] \to [\I64]', r'valid-unop', r'exec-unop', r'op-iextendn_s'),
    Instruction(None, r'\hex{C5}'),
    Instruction(None, r'\hex{C6}'),
    Instruction(None, r'\hex{C7}'),
    Instruction(None, r'\hex{C8}'),
    Instruction(None, r'\hex{C9}'),
    Instruction(None, r'\hex{CA}'),
    Instruction(None, r'\hex{CB}'),
    Instruction(None, r'\hex{CC}'),
    Instruction(None, r'\hex{CD}'),
    Instruction(None, r'\hex{CE}'),
    Instruction(None, r'\hex{CF}'),
    Instruction(r'\REFNULL~t', r'\hex{D0}', r'[] \to [t]', r'valid-ref.null', r'exec-ref.null'),
    Instruction(r'\REFISNULL', r'\hex{D1}', r'[t] \to [\I32]', r'valid-ref.is_null', r'exec-ref.is_null'),
    Instruction(r'\REFFUNC~x', r'\hex{D2}', r'[] \to [\FUNCREF]', r'valid-ref.func', r'exec-ref.func'),
    Instruction(None, r'\hex{D3}'),
    Instruction(None, r'\hex{D4}'),
    Instruction(None, r'\hex{D5}'),
    Instruction(None, r'\hex{D6}'),
    Instruction(None, r'\hex{D7}'),
    Instruction(None, r'\hex{D8}'),
    Instruction(None, r'\hex{D9}'),
    Instruction(None, r'\hex{DA}'),
    Instruction(None, r'\hex{DB}'),
    Instruction(None, r'\hex{DC}'),
    Instruction(None, r'\hex{DD}'),
    Instruction(None, r'\hex{DE}'),
    Instruction(None, r'\hex{DF}'),
    Instruction(None, r'\hex{E0}'),
    Instruction(None, r'\hex{E1}'),
    Instruction(None, r'\hex{E2}'),
    Instruction(None, r'\hex{E3}'),
    Instruction(None, r'\hex{E4}'),
    Instruction(None, r'\hex{E5}'),
    Instruction(None, r'\hex{E6}'),
    Instruction(None, r'\hex{E7}'),
    Instruction(None, r'\hex{E8}'),
    Instruction(None, r'\hex{E9}'),
    Instruction(None, r'\hex{EA}'),
    Instruction(None, r'\hex{EB}'),
    Instruction(None, r'\hex{EC}'),
    Instruction(None, r'\hex{ED}'),
    Instruction(None, r'\hex{EE}'),
    Instruction(None, r'\hex{EF}'),
    Instruction(None, r'\hex{F0}'),
    Instruction(None, r'\hex{F1}'),
    Instruction(None, r'\hex{F2}'),
    Instruction(None, r'\hex{F3}'),
    Instruction(None, r'\hex{F4}'),
    Instruction(None, r'\hex{F5}'),
    Instruction(None, r'\hex{F6}'),
    Instruction(None, r'\hex{F7}'),
    Instruction(None, r'\hex{F8}'),
    Instruction(None, r'\hex{F9}'),
    Instruction(None, r'\hex{FA}'),
    Instruction(None, r'\hex{FB}'),
    Instruction(r'\I32.\TRUNC\K{\_sat\_}\F32\K{\_s}', r'\hex{FC}~\hex{00}', r'[\F32] \to [\I32]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_sat_s'),
    Instruction(r'\I32.\TRUNC\K{\_sat\_}\F32\K{\_u}', r'\hex{FC}~\hex{01}', r'[\F32] \to [\I32]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_sat_u'),
    Instruction(r'\I32.\TRUNC\K{\_sat\_}\F64\K{\_s}', r'\hex{FC}~\hex{02}', r'[\F64] \to [\I32]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_sat_s'),
    Instruction(r'\I32.\TRUNC\K{\_sat\_}\F64\K{\_u}', r'\hex{FC}~\hex{03}', r'[\F64] \to [\I32]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_sat_u'),
    Instruction(r'\I64.\TRUNC\K{\_sat\_}\F32\K{\_s}', r'\hex{FC}~\hex{04}', r'[\F32] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_sat_s'),
    Instruction(r'\I64.\TRUNC\K{\_sat\_}\F32\K{\_u}', r'\hex{FC}~\hex{05}', r'[\F32] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_sat_u'),
    Instruction(r'\I64.\TRUNC\K{\_sat\_}\F64\K{\_s}', r'\hex{FC}~\hex{06}', r'[\F64] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_sat_s'),
    Instruction(r'\I64.\TRUNC\K{\_sat\_}\F64\K{\_u}', r'\hex{FC}~\hex{07}', r'[\F64] \to [\I64]', r'valid-cvtop', r'exec-cvtop', r'op-trunc_sat_u'),
    Instruction(r'\MEMORYINIT~x', r'\hex{FC}~\hex{08}', r'[\I32~\I32~\I32] \to []', r'valid-memory.init', r'exec-memory.init'),
    Instruction(r'\DATADROP~x', r'\hex{FC}~\hex{09}', r'[] \to []', r'valid-data.drop', r'exec-data.drop'),
    Instruction(r'\MEMORYCOPY', r'\hex{FC}~\hex{0A}', r'[\I32~\I32~\I32] \to []', r'valid-memory.copy', r'exec-memory.copy'),
    Instruction(r'\MEMORYFILL', r'\hex{FC}~\hex{0B}', r'[\I32~\I32~\I32] \to []', r'valid-memory.fill', r'exec-memory.fill'),
    Instruction(r'\TABLEINIT~x~y', r'\hex{FC}~\hex{0C}', r'[\I32~\I32~\I32] \to []', r'valid-table.init', r'exec-table.init'),
    Instruction(r'\ELEMDROP~x', r'\hex{FC}~\hex{0D}', r'[] \to []', r'valid-elem.drop', r'exec-elem.drop'),
    Instruction(r'\TABLECOPY~x~y', r'\hex{FC}~\hex{0E}', r'[\I32~\I32~\I32] \to []', r'valid-table.copy', r'exec-table.copy'),
    Instruction(r'\TABLEGROW~x', r'\hex{FC}~\hex{0F}', r'[t~\I32] \to [\I32]', r'valid-table.grow', r'exec-table.grow'),
    Instruction(r'\TABLESIZE~x', r'\hex{FC}~\hex{10}', r'[] \to [\I32]', r'valid-table.size', r'exec-table.size'),
    Instruction(r'\TABLEFILL~x', r'\hex{FC}~\hex{11}', r'[\I32~t~\I32] \to []', r'valid-table.fill', r'exec-table.fill'),
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
