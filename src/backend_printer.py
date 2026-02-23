"""
ARM MLIR to ARM assembly converter (printer)
"""

from xdsl.dialects import builtin

from frontend_ast import *
from frontend_mlir_gen import *
from backend_optimization import *
from backend_arm_dialect import *

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

def print_asm(module: builtin.ModuleOp):
    
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
            print(f"    mov r{dst}, r{src}")

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
    


# generate AST
p = Parser()
res = p.walk("test.c")
print("AST:")
print(res)
print()

# generate high-level MLIR from AST 
gen = MLIRGenerator()
modl = gen.compile(res)
print("High-level MLIR before optimization:")
print(modl)
print()

# apply optimizations
apply_all_optimizations(modl)   # canonicalizations
cse(modl)                       # common subexpression elimination
dce(modl)                       # dead code elimination

print("High-level MLIR after optimization:")
print(modl)
print()

lower(modl)
print("MLIR after lowering to ARM dialect:")
print(modl)
print()

print("Assembly code:")
print_asm(modl)