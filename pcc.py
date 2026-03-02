#!/usr/bin/env python3

import sys, subprocess, os, re
from xdsl.context import Context
from xdsl.parser import Parser
from xdsl.dialects import builtin, func, arith, memref, scf
from xdsl.transforms.common_subexpression_elimination import cse
from xdsl.transforms.dead_code_elimination import dce

from src.backend_optimization import *
from src.backend_arm_dialect import *
from src.backend_printer import *

# Important: this environment variable must be set to find cgeist!
# export CGEIST_PATH=~/Documents/Polygeist/build/bin

# look for CGEIST_PATH env variable
if "CGEIST_PATH" not in os.environ:
    sys.exit("Error: CGEIST_PATH environment variable must be set.")
cgeist_path = os.environ.get('CGEIST_PATH')

if len(sys.argv) < 2:
    sys.exit("Error: no filename provided. Usage: ./pcc.py [--emit-all] <filename>")

emit_all = False
if (sys.argv[1] == "--emit-all"):
    emit_all = True
    in_file = sys.argv[2]
else:
    in_file = sys.argv[1]
in_filename = in_file[:len(in_file) - 2] # assume .c

# initialize xDSL Context and load all dialects
context = Context()
context.load_dialect(builtin.Builtin)
context.load_dialect(func.Func)
context.load_dialect(arith.Arith)
context.load_dialect(memref.MemRef)
context.load_dialect(scf.Scf)
context.load_dialect(ArmDialect)

# convert C to high-level MLIR with a subprocess for Polygeist
mlir_filepath = f"{in_filename}.mlir"
ret = subprocess.call([cgeist_path + "/cgeist", 
                       in_file, "-S", "-O0",
                       "-o", mlir_filepath])
if ret != 0:
    print("Error: cgeist failed to compile file " + in_file + " with exit code " + str(ret))

# read MLIR file produced by Polygeist
with open(mlir_filepath, "r") as f:
    mlir_text = f.read()

# filter produced MLIR using regex magic
mlir_text = re.sub(r"module attributes \{.*?\} \{", "builtin.module {", mlir_text)
mlir_text = re.sub(r"attributes \{.*?\}", "", mlir_text)

# parse filtered text into ModuleOp 
parser = Parser(context, mlir_text)
module = parser.parse_module()

# apply optimizations
apply_all_optimizations(module)   # canonicalizations
cse(module)                       # common subexpression elimination
dce(module)                       # dead code elimination
if (emit_all):
    filename = f"{in_filename}-optimized.mlir"
    with open(filename, "w+") as f:
        print(module, file=f)

# lower MLIR to ARM dialect
lower(module)
if (emit_all):
    filename = f"{in_filename}-arm.mlir"
    with open(filename, "w+") as f:
        print(module, file=f)

# print ARM assembly
filename = f"{in_filename}.s"
with open(filename, "w+") as f:
    print_asm(module, out_file=f)