"""
picoC AST to high-level MLIR converter
"""

from xdsl.dialects import arith, builtin, func
from xdsl.ir import Block, SSAValue, Region, Operation

from frontend_ast import *

class MLIRGenerator:

    def __init__(self):
        self.current_block: Block = None
        self.module = builtin.ModuleOp([])
        self.symbol_table: dict[str, SSAValue] = {}     # var names -> SSA values

    def compile(self, root):
        self.parse(root)
        return self.module

    # dispatcher
    def parse(self, node):
        method_name = f"parse_{type(node).__name__}"
        if (hasattr(self, method_name)):
            return getattr(self, method_name)(node)
        else:
            print(node)
            raise NotImplementedError(f"Error: No handler for {type(node).__name__}")

    def parse_Func(self, node):
        self.current_block = Block()

        # fill Block with operations
        for stmt in node.body:
            self.parse(stmt)

        func_op = func.FuncOp.from_region(
            node.name,
            [],
            [builtin.i32],
            Region([self.current_block])
        )

        # add function to module
        self.module.body.blocks[0].add_op(func_op)


    #
    #   Expressions (SSA retval)
    #
    def parse_Constant(self, node):
        # eg. %0 = arith.constant 1 : i32
        op = arith.ConstantOp.from_int_and_width(node.value, 32)
        self.current_block.add_op(op)
        return op
    

    def parse_Var(self, node):
        if (node.name not in self.symbol_table):
            raise ValueError(f"Error: Undefined variable {node.name}")
        return self.symbol_table[node.name]
    

    def parse_BinaryOp(self, node):
        left_val = self.parse(node.lhs) 
        right_val = self.parse(node.rhs)

        if (node.op == "+"):
            op = arith.AddiOp(left_val, right_val, builtin.i32)
        elif (node.op == "-"):
            op = arith.SubiOp(left_val, right_val, builtin.i32)
        elif (node.op == "*"):
            op = arith.MuliOp(left_val, right_val, builtin.i32)
        elif (node.op == "/"):
            op = arith.DivSIOp(left_val, right_val, builtin.i32)
        elif (node.op == "&"):
            op = arith.AndIOp(left_val, right_val, builtin.i32)
        elif (node.op == "|"):
            op = arith.OrIOp(left_val, right_val, builtin.i32)
        elif (node.op == "^"):
            op = arith.XOrIOp(left_val, right_val, builtin.i32)
        elif (node.op == "<<"):
            op = arith.ShLIOp(left_val, right_val, builtin.i32)
        elif (node.op == ">>"):
            op = arith.ShRUIOp(left_val, right_val, builtin.i32)
        else:
            raise NotImplementedError(f"Error: invalid operation {node.op}")

        # add op to current block and return
        self.current_block.add_op(op)
        return op.result

    #
    #   State update functions
    #
    def parse_VarDecl(self, node):
        if (node.val is not None):
            init_ssa = self.parse(node.val)
        else:
            # init to 0
            op = arith.ConstantOp.from_int_and_width(0, 32)
            self.current_block.add_op(op)
            init_ssa = op.result

        # update symbol table, type table
        self.symbol_table[node.name] = init_ssa

    def parse_Assignment(self, node):
        # get new SSA value
        new_ssa_val = self.parse(node.val)

        # update symbol table (old SSA value doesn't exist anymore)
        self.symbol_table[node.name] = new_ssa_val


    def parse_Ret(self, node):
        # get return value (SSA)
        retval_ssa = self.parse(node.val)

        op = func.ReturnOp(retval_ssa)
        self.current_block.add_op(op)
    