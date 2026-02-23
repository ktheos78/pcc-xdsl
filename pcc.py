#!/usr/bin/env python3

import sys
from xdsl.transforms.common_subexpression_elimination import cse
from xdsl.transforms.dead_code_elimination import dce

from src.frontend_ast import *
from src.frontend_mlir_gen import *
from src.backend_optimization import *
from src.backend_arm_dialect import *
from src.backend_printer import *

if len(sys.argv) < 2:
    sys.exit("Error: no filename provided. Usage: ./pcc.py [--emit-all] <filename>")

emit_all = False
if (sys.argv[1] == "--emit-all"):
    emit_all = True
    in_file = sys.argv[2]

else:
    in_file = sys.argv[1]

# generate AST
p = Parser()
ast = p.walk(in_file)
in_filename = in_file[:len(in_file) - 2]

# generate high-level MLIR from AST 
gen = MLIRGenerator()
module = gen.compile(ast)
if (emit_all):
    filename = f"{in_filename}.mlir"
    f = open(filename, "w+")
    print(module, file=f)

# apply optimizations
apply_all_optimizations(module)   # canonicalizations
cse(module)                       # common subexpression elimination
dce(module)                       # dead code elimination
if (emit_all):
    filename = f"{in_filename}-optimized.mlir"
    f = open(filename, "w+")
    print(module, file=f)

# lower MLIR to ARM dialect
lower(module)
if (emit_all):
    filename = f"{in_filename}-arm.mlir"
    f = open(filename, "w+")
    print(module, file=f)

# print ARM assembly
filename = f"{in_filename}.s"
f = open(filename, "w+")
print_asm(module, out_file=f)