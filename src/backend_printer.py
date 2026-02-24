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
    global ssa_ids
    ssa_ids[ssa] = dst

def print_asm(module: builtin.ModuleOp, out_file):
    
    # redirect stdout
    sys.stdout = out_file

    binary_ops = {
        ArmAddOp:   "adds",
        ArmSubOp:   "subs",
        ArmMulOp:   "mul",
        ArmAndOp:   "ands",
        ArmOrOp:    "orrs",
        ArmEorOp:   "eors",
        ArmLslOp:   "lsls",
        ArmLsrOp:   "lsrs",
        ArmAsrOp:   "asrs"
    }

    # match type for each operation
    for op in module.walk():

        if type(op) in binary_ops:
            dst = get_ssa_id(op.results[0])
            lhs = get_ssa_id(op.operands[0])
            rhs = get_ssa_id(op.operands[1])
            print(f"    {binary_ops[type(op)]} r{dst}, r{lhs}, r{rhs}")

        elif isinstance(op, ArmMovOp):
            dst = get_ssa_id(op.results[0])
            imm = op.attributes["imm"].value.data
            print(f"    mov r{dst}, #{imm}")

        elif isinstance(op, ArmMovwOp):
            dst = get_ssa_id(op.results[0])
            imm = op.attributes["imm"].value.data
            print(f"    movw r{dst}, #{imm}")

        elif isinstance(op, ArmMovtOp):
            dst = get_ssa_id(op.operands[0])
            imm = op.attributes["imm"].value.data
            add_ssa_id(op.results[0], dst)
            print(f"    movt r{dst}, #{imm}")

        elif isinstance(op, ArmMovRegOp):
            dst = 0
            src = get_ssa_id(op.operands[0])
            print(f"    movs r{dst}, r{src}")

        elif isinstance(op, ArmRetOp):
            print("    bx lr")

        elif isinstance(op, func.FuncOp):
            
            name = str(op.sym_name).replace("\"", "")

            # header
            print(".syntax unified")
            print(".thumb")
            print(f".global {name}")
            print(f".type {name}, %function\n")
            print(f"{name}:")