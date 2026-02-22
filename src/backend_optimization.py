"""
Basic optimizer for high-level MLIR
"""

from xdsl.dialects import arith, builtin
from xdsl.ir import Operation, Dialect
from xdsl.transforms.common_subexpression_elimination import cse
from xdsl.transforms.dead_code_elimination import dce
from xdsl.irdl import irdl_op_definition, IRDLOperation, operand_def, result_def
from xdsl.ir import SSAValue
from xdsl.pattern_rewriter import (
    GreedyRewritePatternApplier,
    PatternRewriter,
    PatternRewriteWalker,
    RewritePattern
)

from frontend_ast import *
from frontend_mlir_gen import *



#
# Optimization patterns
#

# x + 0 -> x
class AddZeroPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.addi
        if not isinstance(op, arith.AddiOp):
            return
        
        # check if rhs is a constant
        if not isinstance(cst := op.rhs.owner, arith.ConstantOp):
            return
        
        # check if constant is 0
        if cst.value.value.data != 0:
            return
        
        # replace x + 0 with x
        rewriter.replace_op(op, [], new_results=[op.lhs])

# x * 2^n -> x << n
class MulPowTwoPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.muli
        if not isinstance(op, arith.MuliOp):
            return
        x = op.lhs
        
        # check if rhs is a constant
        if not isinstance(cst := op.rhs.owner, arith.ConstantOp):
            return
        
        # check if constant is power of 2
        rhs = cst.value.value.data
        if (not( rhs > 0 and ((rhs & (rhs - 1)) == 0))):
            return
        
        # replace x * 2^n with x << n and convert to SSA for ShLIOp
        pow_two = (rhs & -rhs).bit_length() - 1     # ctz bithack
        pow_two_op = arith.ConstantOp.from_int_and_width(pow_two, 32)

        # get result (shift amount) and replace 
        shift_val = pow_two_op.result 
        shl = arith.ShLIOp(x, shift_val)
        rewriter.replace_op(op, [pow_two_op, shl])

# x / 2^n -> x >> n
class DivPowTwoPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.divsi
        if not isinstance(op, arith.DivSIOp):
            return
        x = op.lhs
        
        # check if rhs is a constant
        if not isinstance(cst := op.rhs.owner, arith.ConstantOp):
            return
        
        # check if constant is power of 2
        rhs = cst.value.value.data
        if (not( rhs > 0 and ((rhs & (rhs - 1)) == 0))):
            return
        
        # replace x / 2^n with x >> n and convert to SSA for ShLIOp
        pow_two = (rhs & -rhs).bit_length() - 1     # ctz bithack
        pow_two_op = arith.ConstantOp.from_int_and_width(pow_two, 32)

        # get result (shift amount) and replace 
        shift_val = pow_two_op.result 
        shl = arith.ShRSIOp(x, shift_val)
        rewriter.replace_op(op, [pow_two_op, shl])

# x & 0 -> 0
class AndZeroPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):

        # match arith.andi
        if not isinstance(op, arith.AndIOp):
            return

        # check if rhs is a constant
        if not isinstance(cst := op.rhs.owner, arith.ConstantOp):
            return

        # check if constant is 0
        if cst.value.value.data != 0:
            return

        # replace x & 0 with 0
        rewriter.replace_op(op, [], new_results=[op.rhs])    

# x ^ x -> 0
class XorSelfPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.xori
        if not isinstance(op, arith.XOrIOp):
            return
        lhs = op.lhs
        rhs = op.rhs
        
        # check if lhs == rhs
        if (lhs != rhs):
            return
        
        # replace x ^ x with 0
        zero_op = arith.ConstantOp.from_int_and_width(0, 32)
        rewriter.replace_op(op, [zero_op])

def apply_all_optimizations(module: builtin.ModuleOp):
    merged_pattern = GreedyRewritePatternApplier([AddZeroPattern(),
                                                  MulPowTwoPattern(),
                                                  DivPowTwoPattern(),
                                                  AndZeroPattern(),
                                                  XorSelfPattern()])
    walker = PatternRewriteWalker(merged_pattern)
    walker.rewrite_module(module)






