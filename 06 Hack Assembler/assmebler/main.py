from Parser import Parser
from Code import Code
import sys
import os.path

asm_file_path = sys.argv[1]
asm_file_name, asm_extension = os.path.splitext(
    os.path.basename(asm_file_path))
hack_file_name = asm_file_name+'.hack'
hack_file_path = os.path.dirname(asm_file_path)+'\\'+hack_file_name


def main():
    p = Parser()
    c = Code()
    with open(asm_file_path, 'r') as f:
        codes = f.read()
    parsed_code = p.parse(codes)
    translated_code = c.first_pass(parsed_code)
    with open(hack_file_path, 'w') as hackfile:
        for line in translated_code:
            hackfile.write(line)


main()
