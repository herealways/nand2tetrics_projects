from Parser import Parser
import sys
import os.path
from timeit import default_timer


vm_file_path=sys.argv[1]
vm_file_name, vm_extension=os.path.splitext(os.path.basename(vm_file_path))
asm_file_name=vm_file_name+'.asm'
if sys.platform == 'win32':
    asm_file_path=os.path.dirname(vm_file_path)+'\\'+asm_file_name
else:
    asm_file_path=os.path.dirname(vm_file_path)+'/'+asm_file_name

def main():
    start = default_timer()
    with open(vm_file_path,'r') as input_file, open(asm_file_path,'w', encoding='utf-8') as output_file:
        p = Parser(input_file, output_file, vm_file_name)
    end = default_timer()
    print('time elapsed: {}'.format(end - start))
main()
