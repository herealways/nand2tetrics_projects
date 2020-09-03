from Parser import Parser
from CodeWriter import CodeWriter
import sys
import glob
import os.path
from timeit import default_timer


"""
If the first argument is a file, translate the file only
If the first arugment is a dir, translate all the vm files in it
If Sys.vm file is found, we need to execute bootstrap_code
"""

bootstrap_code = """
//bootstrap
@256
D=A
@0
M=D //SP=256

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
""".format('Sys.init', 0, 'Sys.init_ret')

vm_file_path = sys.argv[1].strip('"').strip("'")
vm_file_list = []
if os.path.isfile(vm_file_path):  # single vm file
    vm_file_name, vm_extension = os.path.splitext(
        os.path.basename(vm_file_path))
    asm_file_name = vm_file_name+'.asm'
    asm_file_path = os.path.join(os.path.dirname(vm_file_path), asm_file_name)
    vm_file_list.append(vm_file_path)

elif os.path.isdir(vm_file_path):  # a dir
    asm_file_path = os.path.join(
        vm_file_path, os.path.basename(vm_file_path)+'.asm')
    vm_file_list = glob.glob(os.path.join(vm_file_path, '*.vm'))
    sys_vm_file = os.path.join(vm_file_path, 'Sys.vm')

print(vm_file_path)
print(vm_file_list)


def main():
    start = default_timer()
    with open(asm_file_path, 'w', encoding='utf-8') as output_file_obj:
        c = CodeWriter(output_file_obj)
        if len(vm_file_list) > 1:  # if more than one vm files, translate Sys.vm first
            if sys_vm_file in vm_file_list:
                # if it has Sys.vm, then we have to add bootstrap code
                output_file_obj.write(bootstrap_code)
                vm_file_name = 'Sys'
                with open(sys_vm_file, 'r') as sys_vm_file_obj:
                    Parser(c, sys_vm_file_obj, vm_file_name)
                vm_file_list.remove(sys_vm_file)
        for vm_file in vm_file_list:
            with open(vm_file, 'r') as vm_file_obj:
                vm_file_name, vm_file_extension = os.path.splitext(
                    os.path.basename(vm_file))
                Parser(c, vm_file_obj, vm_file_name)
    end = default_timer()
    print('time elapsed: {}'.format(end - start))


main()
