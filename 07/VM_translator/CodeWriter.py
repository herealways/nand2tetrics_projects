class CodeWriter:
    def __init__(self, output_file_obj, vm_file_name):
        self.file = output_file_obj
        self.file_name = vm_file_name
        self.label_count = 0  #This is used for defining a different label name every time
    def constructor(self, cmd_type, arg1, arg2):
        asm_code = ''
        if cmd_type == 'C_ARITHMETIC':
            asm_code = self.write_arithmetic(arg1)
        elif cmd_type == 'C_PUSH' or cmd_type == 'C_POP':
            asm_code = self.write_push_pop(cmd_type, arg1, arg2)
        
        self.file.write(asm_code)

    def write_arithmetic(self, arg1):
        if arg1 in ['eq', 'gt', 'lt']:
            asm_code = eval('self.{}_asm'.format(arg1)).format(self.label_count)
            self.label_count += 1
        else:
            asm_code = eval('self.'+arg1+'_asm')
        return asm_code
    def write_push_pop(self, cmd_type, arg1, arg2):
        asm_code = ''
        if arg1 == 'constant':
            if cmd_type == 'C_PUSH':
                asm_code = self.push_constant_asm.format(arg2)

        elif arg1 in ['local', 'argument', 'this', 'that']:
            if cmd_type == 'C_PUSH':
                asm_code = self.push_local_argument_this_that_asm.format(arg1, arg2, self.symbol_table[arg1])
            elif cmd_type == 'C_POP':
                asm_code = self.pop_local_argument_this_that_asm.format(arg1, arg2, self.symbol_table[arg1])
        
        elif arg1 == 'static':
            var_name = self.file_name + '.' + str(arg2)
            if cmd_type == 'C_PUSH':
                asm_code = self.push_static_asm.format(arg2, var_name)
            elif cmd_type == 'C_POP':
                asm_code = self.pop_static_asm.format(arg2, var_name)

        elif arg1 == 'temp':
            if cmd_type == 'C_PUSH':
                asm_code = self.push_temp_asm.format(arg2)
            elif cmd_type == 'C_POP':
                asm_code = self.pop_temp_asm.format(arg2)
        
        elif arg1 == 'pointer':
            if cmd_type == 'C_PUSH':
                asm_code = self.push_pointer_asm.format(arg2, self.pointer_table[arg2])
            elif cmd_type == 'C_POP':
                asm_code = self.pop_pointer_asm.format(arg2, self.pointer_table[arg2])

        return asm_code


    add_asm = """
//add    asm code
@SP //SP--
M=M-1
@SP //y=*SP
A=M
D=M
@SP //SP --
M=M-1
@SP //result = x+y
A=M
D=D+M //it seems there is not M+D in hack asm specification
@SP //RAM[SP]= result
A=M
M=D
@SP
M=M+1
"""
    sub_asm = """
//sub asm code
@SP //SP--
M=M-1
@SP //y=*SP
A=M
D=M
@SP //SP --
M=M-1
@SP //result = x-y
A=M
D=M-D 
@SP //RAM[SP]= result
A=M
M=D
@SP
M=M+1
"""
    neg_asm = """
//neg asm code
@SP //SP--
M=M-1
@SP //y = -y
A=M
M=-M 
@SP //SP++
M=M+1
"""
    eq_asm = """
//eq
@SP //SP--
M=M-1
A=M //y=*SP
D=M
@SP //SP --
M=M-1
A=M //if x-y = 0
D=M-D 
@eq{0}
D;JEQ
@SP //else x-y !=0
A=M
M=0
@Finisheq{0}
0;JMP
(eq{0})
@SP
A=M
M=-1
(Finisheq{0})
@SP //SP++
M=M+1
"""
    gt_asm = """
//gt
@SP //SP--
M=M-1
A=M //y=*SP
D=M
@SP //SP --
M=M-1
A=M //if x-y > 0
D=M-D 
@gt{0}
D;JGT
@SP //else x-y <=0
A=M
M=0
@Finishgt{0}
0;JMP
(gt{0})
@SP
A=M
M=-1
(Finishgt{0})
@SP //SP++
M=M+1
"""
    lt_asm = """
//lt
@SP //SP--
M=M-1
A=M //y=*SP
D=M
@SP //SP --
M=M-1
A=M //if x-y < 0
D=M-D 
@lt{0}
D;JLT
@SP //else x-y >=0
A=M
M=0
@Finishlt{0}
0;JMP
(lt{0})
@SP
A=M
M=-1
(Finishlt{0})
@SP //SP++
M=M+1
"""
    and_asm = """
//and    asm code
@SP //SP--
M=M-1
@SP //y=*SP
A=M
D=M
@SP //SP --
M=M-1
@SP //result x and y
A=M
D=D&M 
@SP //RAM[SP]= result
A=M
M=D
@SP
M=M+1
"""
    or_asm = """
//or    asm code
@SP //SP--
M=M-1
@SP //y=*SP
A=M
D=M
@SP //SP --
M=M-1
@SP //result x or y
A=M
D=D|M 
@SP //RAM[SP]= result
A=M
M=D
@SP
M=M+1
"""
    not_asm = """
//not asm code
@SP //SP--
M=M-1
@SP //y = !y
A=M
M=!M
@SP //SP++
M=M+1
"""

    push_constant_asm = """
//push constant {0}
@{0}
D=A
@SP
A=M
M=D
@SP
M=M+1
"""

    symbol_table = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
    }

    push_local_argument_this_that_asm = """
//push {0} {1}
@{1}
D=A
@{2}
D=M+D
@addr
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
"""

    pop_local_argument_this_that_asm = """
//pop {0} {1}
@{1}
D=A
@{2}
D=M+D
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
"""

    push_static_asm = """
//push static {0}
@{1}
D=M
@SP
A=M
M=D
@SP
M=M+1
"""

    pop_static_asm = """
//pop static {0}
@SP
M=M-1
A=M
D=M
@{1}
M=D
"""

    push_temp_asm = """
//push temp {0}
@{0}
D=A
@5
D=D+A
@addr
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
"""

    pop_temp_asm = """
// pop temp {0}
@{0}
D=A
@5
D=D+A
@addr
M=D
@SP
M=M-1
A=M
D=M
@addr
A=M
M=D
"""

    pointer_table = {
        0: 'THIS',
        1: 'THAT',
    }

    push_pointer_asm = """
//push pointer {0}
@{1}
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
    pop_pointer_asm = """
//pop pointer {0}
@SP
M=M-1
A=M
D=M
@{1}
M=D
"""