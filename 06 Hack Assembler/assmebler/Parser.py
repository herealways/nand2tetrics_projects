class Parser(object):

    def parse(self, asm_codes: str):
        parsed_code = []
        for line in asm_codes.split('\n'):
            # ignore white space and comments
            comment_begin_at = line.find('//')
            if comment_begin_at != -1:
                line = line[:comment_begin_at]
            line = line.strip()
            if line == '':
                pass
            else:
                parsed_code.append(line)
        return parsed_code


if __name__ == "__main__":
    p = Parser()
    test_code = [
        "   @R0 //1234",
        "                                                  ",
        "(LOOP)",
        "//009933",
        "D=M //set data register to M",
        "   D;JGT",
    ]

    test_code2 = """
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/06/add/Add.asm

// Computes R0 = 2 + 3  (R0 refers to RAM[0])

@2
D=A
@3
D=D+A
@0
M=D
"""

    p.parse(test_code2)
