from SymbolTable import SymbolTable

s = SymbolTable()


class Code(object):

    def first_pass(self, parsed_code):
        # need to deal with line numbers in the first pass
        line_num = 0
        parsed_code_first_pass = []
        for line in parsed_code:
            # deal with labels
            if '(' in line:
                label_name = line.strip('()')
                label_address = line_num
                s.add_symbol(label_name, label_address)
            else:
                # record line num
                parsed_code_first_pass.append(line)
                line_num += 1
        return self.second_pass(parsed_code_first_pass)

    def second_pass(self, parsed_code):
        translated_codes = []
        for line in parsed_code:
            if '@' in line:
                a_code = line.strip('@')  # a code likes "12" "i"
                # if symbol is used
                if a_code[0] not in '0123456789':
                    # check if the symbol is defined
                    try:
                        symbol_num = s.get_symbol(a_code)
                    except KeyError:
                        s.add_symbol(a_code)
                        symbol_num = s.get_symbol(a_code)
                    machine_code = self.A_instruction(symbol_num)
                else:
                    machine_code = self.A_instruction(a_code)
            else:
                machine_code = self.C_instruction(line)
            translated_codes.append(machine_code+'\n')
        print(s.symbol_table)
        return translated_codes

    def A_instruction(self, code):
        # address=code.strip('@')
        return "{0:016b}".format(int(code))

    def C_instruction(self, code):
        # if no dest/jump, null is used
        if ';' in code and '=' in code:
            code_snippet1 = code.split('=')
            code_snippet2 = code_snippet1[-1].split(';')
            code_parts = code_snippet1[:1]+code_snippet2
            # print(code_parts)
            code_dest = self.translation_table_dest[code_parts[0]]
            code_comp = self.translation_table_comp[code_parts[1]]
            code_jump = self.translation_table_jump[code_parts[2]]
            return '111' + code_comp + code_dest + code_jump

        elif '=' in code:
            code_parts = code.split('=')
            code_dest = self.translation_table_dest[code_parts[0]]
            code_comp = self.translation_table_comp[code_parts[1]]
            code_jump = self.translation_table_jump['null']
            return '111' + code_comp + code_dest + code_jump

        elif ';' in code:
            code_parts = code.split(';')
            code_comp = self.translation_table_comp[code_parts[0]]
            code_jump = self.translation_table_jump[code_parts[1]]
            code_dest = self.translation_table_dest['null']
            return '111' + code_comp + code_dest + code_jump

    translation_table_dest = {
        # dest
        'null': '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111',
    }
    translation_table_comp = {
        # a and comp
        # a=0
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        '!D': '0001101',
        '!A': '0110001',
        '-D': '0001111',
        '-A': '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
        # a=1
        'M': '1110000',
        '!M': '1110001',
        '-M': '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101',
    }
    translation_table_jump = {
        # jump
        'null': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }


if __name__ == "__main__":
    test_code = [
        "@21",
        "D=M-1;JGT",
        "D=A+1",
        "D;JNE",
    ]

    test_code2 = [
    ]

    c = Code()
    print(c.first_pass(test_code))
