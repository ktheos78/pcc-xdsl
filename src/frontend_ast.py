"""
AST generator for picoC program
"""

TYPES = frozenset(["int", "char", "bool"])

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#
#   AST nodes
#
class ASTNode:
    pass

# constant
class Constant(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Constant({self.value})"

# variable
class Var(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"

# binary operation
class BinaryOp(ASTNode):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __repr__(self):
        return f"BinaryOp({self.lhs} {self.op} {self.rhs})"

# variable declaration
class VarDecl(ASTNode):
    def __init__(self, type, name, val):
        self.type = type
        self.name = name
        self.val = val

    def __repr__(self):
        return f"VarDecl({self.type} {self.name} = {self.val})"

# assignment 
class Assignment(ASTNode):
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def __repr__(self):
        return f"Assignment({self.name} = {self.val})"

# return
class Ret(ASTNode):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"Ret({self.val})"

# function definition
# body is a list of statements
class Func(ASTNode):
    def __init__(self, ret_type, name, body):
        self.ret_type = ret_type
        self.name = name
        self.body = body

    def __repr__(self):
        return f"Func({self.ret_type} {self.name}, body = {self.body})"
    
#
#   Parser
#
class Parser:

    def get_expr(self, tokens):
        
        # binary operation
        if (len(tokens) > 1):
            lhs = Constant(int(tokens[0])) if is_number(tokens[0]) else Var(tokens[0])
            op = tokens[1]
            rhs = Constant(int(tokens[2][:len(tokens[2]) - 1])) if is_number(tokens[2][:len(tokens[2]) - 1]) else Var(tokens[2][:len(tokens[2]) - 1])
            return BinaryOp(lhs, op, rhs)

        # constant
        if (is_number(tokens[0][:len(tokens[0]) - 1])):
            return Constant(int(tokens[0][:len(tokens[0]) - 1]))
        
        # variable
        return Var(tokens[0][:len(tokens[0]) - 1])
            

    def walk(self, filename):

        func = Func(None, None, None)
        f = open(filename, 'r')
        i = 0

        for line in f:

            tokens = line.split()
            if (len(tokens) < 2 or tokens[0][:2] == "//"): 
                continue
            #print(tokens)

            ### Function declaration ###
            if (i == 0):
                func.ret_type = tokens[0]
                func.name = (tokens[1].split("(", 1))[0]    # name(...) == name (...)
                func.body = []

            else:
                ### Declaration ###
                if (tokens[0] in TYPES):
                    stmt = VarDecl(None, None, None)
                    stmt.type = tokens[0]
                    stmt.name = tokens[1]

                    # no assignment
                    if (stmt.name[len(stmt.name) - 1] == ';' or stmt.name[len(stmt.name) - 1] == ','):
                        for name in tokens[1:]:
                            var_name = name[:len(name) - 1]
                            func.body.append(VarDecl(stmt.type, var_name, None))

                    # with assignment 
                    else:
                        stmt.val = self.get_expr(tokens[3:])
                        func.body.append(stmt)

                ### Return ###
                elif (tokens[0] == "return"):
                    ret_val = tokens[1][:len(tokens[1]) - 1]
                    ret_val = Constant(int(ret_val)) if is_number(ret_val) else Var(ret_val)
                    func.body.append(Ret(ret_val))
                    return func

                ### Assignment ###
                else:
                    stmt = Assignment(None, None)
                    stmt.name = tokens[0]
                    stmt.val = self.get_expr(tokens[2:])
                    func.body.append(stmt)

            i += 1
        
        print("Warning: Missing return value")
        return func