class CodeWriter:
    label_count = 0  # This is used for defining a different label name every time
    func_count = 0  # functionName$ret.1 .2 .3 ...
    return_count = 0  # endFrame.1 .2 .3   retAddr.1 .2 .3

    def __init__(self, output_file_obj):
        self.file = output_file_obj

    def constructor(self, cmd_type, arg1, arg2):
        asm_code = ''
        if cmd_type == 'C_ARITHMETIC':
            asm_code = self.write_arithmetic(arg1)
        elif cmd_type == 'C_PUSH' or cmd_type == 'C_POP':
            asm_code = self.write_push_pop(cmd_type, arg1, arg2)
        elif cmd_type == 'C_LABEL':
            asm_code = self.write_label(arg1)
        elif cmd_type == 'C_GOTO':
            asm_code = self.write_goto(arg1)
        elif cmd_type == 'C_IF':
            asm_code = self.write_if_goto(arg1)
        elif cmd_type == 'C_FUNCTION':
            asm_code = self.write_function(arg1, arg2)
        elif cmd_type == 'C_CALL':
            asm_code = self.write_call(arg1, arg2)
        elif cmd_type == 'C_RETURN':
            asm_code = self.write_return()

        self.file.write(asm_code)

    def write_arithmetic(self, arg1):
        if arg1 in ['eq', 'gt', 'lt']:
            asm_code = eval('self.{}_asm'.format(arg1)
                            ).format(self.label_count)
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
                asm_code = self.push_local_argument_this_that_asm.format(
                    arg1, arg2, self.symbol_table[arg1])
            elif cmd_type == 'C_POP':
                asm_code = self.pop_local_argument_this_that_asm.format(
                    arg1, arg2, self.symbol_table[arg1])

        elif arg1 == 'static':
            var_name = self.vm_file_name + '.' + str(arg2)
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
                asm_code = self.push_pointer_asm.format(
                    arg2, self.pointer_table[arg2])
            elif cmd_type == 'C_POP':
                asm_code = self.pop_pointer_asm.format(
                    arg2, self.pointer_table[arg2])

        return asm_code

    def write_label(self, arg1):
        asm_code = self.label_asm.format(arg1, self.vm_file_name)
        return asm_code

    def write_goto(self, arg1):
        asm_code = self.goto_asm.format(arg1, self.vm_file_name)
        return asm_code

    def write_if_goto(self, arg1):
        asm_code = self.if_asm.format(arg1, self.vm_file_name)
        return asm_code

    def write_function(self, arg1, arg2):
        asm_code = self.function_asm.format(arg1, arg2)
        if arg2 == 0:
            return asm_code
        else:
            for i in range(arg2):
                asm_code += self.function_set_local_asm.format(i)
            return asm_code

    def write_call(self, arg1, arg2):
        ret_symbol = '{0}$ret.{1}'.format(arg1, self.func_count)
        self.func_count += 1
        asm_code = self.call_asm.format(arg1, arg2, ret_symbol)
        return asm_code

    def write_return(self):
        asm_code = self.return_asm.format(self.return_count)
        self.return_count += 1
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

    label_asm = """
//label {0}
({1}${0})
"""

    goto_asm = """
//goto {0}
@{1}${0}
0;JMP
"""

    if_asm = """
//if-goto {0}
@SP
M=M-1 // SP--
A=M
D=M  // n=*SP
@{1}${0}
D;JGT //if n > 0 goto
D=D+1
@{1}${0}
D;JEQ // if n = True goto
"""

    function_asm = """
//function {0} {1}
({0})
"""

    function_set_local_asm = """
@{0}
D=A
@LCL
A=M+D
M=0
@SP
M=M+1
"""

    call_asm = """
//call {0} {1}
@{2} //push returnAddress
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL //push LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG //push ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS //push THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT //push THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

@5
D=A
@{1} //arg2=nArgs
D=D+A //5+nArgs
@SP
D=M-D //SP-5-nArgs
@ARG
M=D

@SP
D=M
@LCL
M=D //LCL = SP

@{0}
0;JMP //goto functionName
({2}) //(returnAddress)
"""

# maybe we can use temp memory segment to store endFrame and retAddr?
    return_asm = """
//return
@LCL
D=M
@endFrame.{0}
M=D //endFrame = LCL
@5
D=A
@endFrame.{0}
D=M-D
A=D
D=M //D = *(endFrame - 5)
@retAddr.{0}
M=D //retAddr = D

@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D //*ARG=pop()
@ARG
D=M
@SP
M=D+1 //SP = ARG + 1

@endFrame.{0}
D=M-1
A=D
D=M
@THAT
M=D // THAT = *(endFrame - 1)
@2
D=A
@endFrame.{0}
D=M-D
A=D
D=M
@THIS
M=D //THIS = *(endFrame - 2)
@3
D=A
@endFrame.{0}
D=M-D
A=D
D=M
@ARG
M=D //ARG = *(endFrame - 3)
@4
D=A
@endFrame.{0}
D=M-D
A=D
D=M
@LCL
M=D //LCL = *(endFrame - 4)
@retAddr.{0}
A=M
0;JMP //goto *retAddr
"""
