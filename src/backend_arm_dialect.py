"""
High-level MLIR to ARM MLIR converter
"""

from xdsl.dialects import arith, builtin
from xdsl.transforms.common_subexpression_elimination import cse
from xdsl.transforms.dead_code_elimination import dce
from xdsl.irdl import irdl_op_definition, IRDLOperation, operand_def, result_def, attr_def
from xdsl.ir import SSAValue
from xdsl.pattern_rewriter import (
    GreedyRewritePatternApplier,
    PatternRewriteWalker,
    RewritePattern
)

from frontend_ast import *
from frontend_mlir_gen import *
from backend_optimization import *



#
#   ARM dialect definition
#
@irdl_op_definition
class ArmAddOp(IRDLOperation):
    
    name = "arm.add"

    # operands and result type 
    lhs = operand_def(builtin.IntegerType)
    rhs = operand_def(builtin.IntegerType)
    res = result_def(builtin.IntegerType)

    def __init__(self, lhs: SSAValue, rhs: SSAValue):
        super().__init__(
            operands=[lhs, rhs],
            result_types=[lhs.type]
        )

@irdl_op_definition
class ArmSubOp(IRDLOperation):
    
    name = "arm.sub"

    # operands and result type 
    lhs = operand_def(builtin.IntegerType)
    rhs = operand_def(builtin.IntegerType)
    res = result_def(builtin.IntegerType)

    def __init__(self, lhs: SSAValue, rhs: SSAValue):
        super().__init__(
            operands=[lhs, rhs],
            result_types=[lhs.type]
        )

@irdl_op_definition
class ArmMulOp(IRDLOperation):
    
    name = "arm.mul"

    # operands and result type 
    lhs = operand_def(builtin.IntegerType)
    rhs = operand_def(builtin.IntegerType)
    res = result_def(builtin.IntegerType)

    def __init__(self, lhs: SSAValue, rhs: SSAValue):
        super().__init__(
            operands=[lhs, rhs],
            result_types=[lhs.type]
        )

@irdl_op_definition
class ArmAndOp(IRDLOperation):
    
    name = "arm.and"

    # operands and result type 
    lhs = operand_def(builtin.IntegerType)
    rhs = operand_def(builtin.IntegerType)
    res = result_def(builtin.IntegerType)

    def __init__(self, lhs: SSAValue, rhs: SSAValue):
        super().__init__(
            operands=[lhs, rhs],
            result_types=[lhs.type]
        )

@irdl_op_definition
class ArmEorOp(IRDLOperation):
    
    name = "arm.eor"

    # operands and result type 
    lhs = operand_def(builtin.IntegerType)
    rhs = operand_def(builtin.IntegerType)
    res = result_def(builtin.IntegerType)

    def __init__(self, lhs: SSAValue, rhs: SSAValue):
        super().__init__(
            operands=[lhs, rhs],
            result_types=[lhs.type]
        )

@irdl_op_definition
class ArmOrOp(IRDLOperation):
    
    name = "arm.or"

    # operands and result type 
    lhs = operand_def(builtin.IntegerType)
    rhs = operand_def(builtin.IntegerType)
    res = result_def(builtin.IntegerType)

    def __init__(self, lhs: SSAValue, rhs: SSAValue):
        super().__init__(
            operands=[lhs, rhs],
            result_types=[lhs.type]
        )

@irdl_op_definition
class ArmLslOp(IRDLOperation):
    
    name = "arm.lsl"

    # operands and result type 
    lhs = operand_def(builtin.IntegerType)
    rhs = operand_def(builtin.IntegerType)
    res = result_def(builtin.IntegerType)

    def __init__(self, lhs: SSAValue, rhs: SSAValue):
        super().__init__(
            operands=[lhs, rhs],
            result_types=[lhs.type]
        )

@irdl_op_definition
class ArmLsrOp(IRDLOperation):
    
    name = "arm.lsr"

    # operands and result type 
    lhs = operand_def(builtin.IntegerType)
    rhs = operand_def(builtin.IntegerType)
    res = result_def(builtin.IntegerType)

    def __init__(self, lhs: SSAValue, rhs: SSAValue):
        super().__init__(
            operands=[lhs, rhs],
            result_types=[lhs.type]
        )

@irdl_op_definition
class ArmMovOp(IRDLOperation):
    name = "arm.mov"

    # imm32 argument
    imm = attr_def(builtin.IntegerAttr)
    res = result_def(builtin.IntegerType)

    def __init__(self, imm_val: int):
        imm_attr = builtin.IntegerAttr.from_int_and_width(imm_val, 32)
        super().__init__(
            operands=[],
            attributes={"imm": imm_attr},
            result_types=[builtin.IntegerType(32)]
        )

@irdl_op_definition
class ArmMovwOp(IRDLOperation):
    name = "arm.movw"

    # imm32 argument
    imm = attr_def(builtin.IntegerAttr)
    res = result_def(builtin.IntegerType)

    def __init__(self, imm_val: int):
        imm_attr = builtin.IntegerAttr.from_int_and_width(imm_val, 32)
        super().__init__(
            operands=[],
            attributes={"imm": imm_attr},
            result_types=[builtin.IntegerType(32)]
        )

@irdl_op_definition
class ArmMovtOp(IRDLOperation):
    name = "arm.movt"

    # reg, imm32 argument
    reg = operand_def(builtin.IntegerType)
    imm = attr_def(builtin.IntegerAttr)
    res = result_def(builtin.IntegerType)

    def __init__(self, reg: SSAValue, imm_val: int):
        imm_attr = builtin.IntegerAttr.from_int_and_width(imm_val, 32)
        super().__init__(
            operands=[reg],
            attributes={"imm": imm_attr},
            result_types=[builtin.IntegerType(32)]
        )

@irdl_op_definition
class ArmMovRegOp(IRDLOperation):
    name = "arm.movreg"

    # imm32 argument
    reg = operand_def(builtin.IntegerType)
    res = result_def(builtin.IntegerType)

    def __init__(self, reg: SSAValue):
        super().__init__(
            operands=[reg],
            result_types=[builtin.IntegerType(32)]
        )

@irdl_op_definition
class ArmRetOp(IRDLOperation):
    name = "arm.ret"

    def __init__(self):
        super().__init__(
            operands=[],
            result_types=[]
        )

#
#   Pattern rewriters for lowering
#

# arm.add
class ArmAddLowerPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.addi
        if not isinstance(op, arith.AddiOp):
            return
        
        lhs = op.lhs
        rhs = op.rhs

        # replace arith.addi with arm.add
        add_op = ArmAddOp(lhs, rhs)
        rewriter.replace_op(op, [add_op])

# arm.sub
class ArmSubLowerPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.subi
        if not isinstance(op, arith.SubiOp):
            return
        
        lhs = op.lhs
        rhs = op.rhs

        # replace arith.subi with arm.sub
        sub_op = ArmSubOp(lhs, rhs)
        rewriter.replace_op(op, [sub_op])

# arm.mul
class ArmMulLowerPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.muli
        if not isinstance(op, arith.MuliOp):
            return
        
        lhs = op.lhs
        rhs = op.rhs

        # replace arith.muli with arm.mul
        mul_op = ArmMulOp(lhs, rhs)
        rewriter.replace_op(op, [mul_op])       

# arm.and
class ArmAndLowerPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.andi
        if not isinstance(op, arith.AndIOp):
            return
        
        lhs = op.lhs
        rhs = op.rhs

        # replace arith.andi with arm.and
        and_op = ArmAndOp(lhs, rhs)
        rewriter.replace_op(op, [and_op])

# arm.or
class ArmOrLowerPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.ori
        if not isinstance(op, arith.OrIOp):
            return
        
        lhs = op.lhs
        rhs = op.rhs

        # replace arith.ori with arm.or
        or_op = ArmOrOp(lhs, rhs)
        rewriter.replace_op(op, [or_op])

# arm.eor
class ArmEorLowerPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.xori
        if not isinstance(op, arith.XOrIOp):
            return
        
        lhs = op.lhs
        rhs = op.rhs

        # replace arith.addi with arm.add
        xor_op = ArmEorOp(lhs, rhs)
        rewriter.replace_op(op, [xor_op])

# arm.lsl
class ArmLslLowerPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.shli
        if not isinstance(op, arith.ShLIOp):
            return
        
        lhs = op.lhs
        rhs = op.rhs

        # replace arith.addi with arm.add
        lsl_op = ArmLslOp(lhs, rhs)
        rewriter.replace_op(op, [lsl_op])

# arm.lsr
class ArmLsrLowerPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.shrsi
        if not isinstance(op, arith.ShRSIOp):
            return
        
        lhs = op.lhs
        rhs = op.rhs

        # replace arith.addi with arm.add
        lsr_op = ArmLsrOp(lhs, rhs)
        rewriter.replace_op(op, [lsr_op])

# arm.mov*
class ArmMovLowerPattern(RewritePattern):

    def match_and_rewrite(self, op, rewriter):
        
        # match arith.constant
        if not isinstance(op, arith.ConstantOp):
            return
        imm_val = op.value.value.data

        # small value (< 16 bits) -> mov
        if (imm_val <= 0xFFFF):
            mov_op = ArmMovOp(imm_val)
            rewriter.replace_op(op, [mov_op])

        # otherwise use movw, movt
        else:
            movw_op = ArmMovwOp(imm_val & 0xFFFF)
            movt_op = ArmMovtOp(movw_op.res, (imm_val >> 16) & 0xFFFF)
            rewriter.replace_op(op, [movw_op, movt_op])

# arm.ret
class ArmRetPattern(RewritePattern):
    
    def match_and_rewrite(self, op, rewriter):
        
        # match func.return
        if not isinstance(op, func.ReturnOp):
            return
        
        movreg_op = ArmMovRegOp(op.operands[0])
        ret_op = ArmRetOp()
        rewriter.replace_op(op, [movreg_op, ret_op])

def lower(module: builtin.ModuleOp):
    merged_pattern = GreedyRewritePatternApplier([ArmAddLowerPattern(),
                                                  ArmSubLowerPattern(),
                                                  ArmMulLowerPattern(),
                                                  ArmAndLowerPattern(),
                                                  ArmEorLowerPattern(),
                                                  ArmLslLowerPattern(),
                                                  ArmLsrLowerPattern(),
                                                  ArmMovLowerPattern(),
                                                  ArmRetPattern()
                                                  ])
    walker = PatternRewriteWalker(merged_pattern)
    walker.rewrite_module(module)
