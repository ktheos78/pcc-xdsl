"""
ARM MLIR to ARM assembly converter (printer)
"""

import sys
from xdsl.dialects import builtin
from xdsl.ir import SSAValue

from src.backend_arm_dialect import *

ssa_ids = dict()
id = 0

def get_ssa_id(ssa: SSAValue):
    global ssa_ids, id

    if (ssa in ssa_ids):
        return ssa_ids[ssa]
    
    else:
        ssa_ids[ssa] = id
        ret = id
        id += 1
        return ret
    
def add_ssa_id(ssa: SSAValue, dst: int):
    global ssa_ids, id
    ssa_ids[ssa] = id

def print_asm(module: builtin.ModuleOp, out_file=sys.stdout):
    
    binary_ops = {
        ArmAddOp:   "adds",
        ArmSubOp:   "subs",
        ArmMulOp:   "muls",
        ArmAndOp:   "ands",
        ArmOrOp:    "orrs",
        ArmEorOp:   "eors",
        ArmLslOp:   "lsls",
        ArmLsrOp:   "lsrs",
    }

    # match type for each operation
    for op in module.walk():

        if type(op) in binary_ops:
            dst = get_ssa_id(op.results[0])
            lhs = get_ssa_id(op.operands[0])
            rhs = get_ssa_id(op.operands[1])
            print(f"    {binary_ops[type(op)]} r{dst}, r{lhs}, r{rhs}", file=out_file)

        elif isinstance(op, ArmMovOp):
            dst = get_ssa_id(op.results[0])
            imm = op.attributes["imm"].value.data
            print(f"    mov r{dst}, #{imm}", file=out_file)

        elif isinstance(op, ArmMovwOp):
            dst = get_ssa_id(op.results[0])
            imm = op.attributes["imm"].value.data
            print(f"    movw r{dst}, #{imm}", file=out_file)

        elif isinstance(op, ArmMovtOp):
            dst = get_ssa_id(op.operands[0])
            imm = op.attributes["imm"].value.data
            add_ssa_id(op.results[0], dst)
            print(f"    movt r{dst}, #{imm}", file=out_file)

        elif isinstance(op, ArmMovRegOp):
            dst = 0
            src = get_ssa_id(op.operands[0])
            print(f"    mov r{dst}, r{src}", file=out_file)

        elif isinstance(op, ArmRetOp):
            print("    bx lr", file=out_file)

        elif isinstance(op, func.FuncOp):
            
            name = str(op.sym_name).replace("\"", "")

            # header
            print(".syntax unified", file=out_file)
            print(".thumb", file=out_file)
            print(f".global {name}", file=out_file)
            print(f".type {name}, %function\n", file=out_file)
            print(f"{name}:", file=out_file)