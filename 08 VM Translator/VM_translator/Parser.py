class Parser:

    def __init__(self, CodeWriter_instance, input_file_obj, current_vm_file_name):
        self.c = CodeWriter_instance
        setattr(self.c, 'vm_file_name', current_vm_file_name)
        self.constructor(input_file_obj)
    
    def constructor(self, file_obj):
        for line in file_obj:
            #strip comments and white spaces
            comment_begin_at=line.find('//')
            if comment_begin_at == -1:
                line = line
            elif comment_begin_at == 0:
                continue    #ignore comment line
            else:
                line = line[:comment_begin_at]
            line = line.strip()
            if line == '':
                continue

            cmd_type, cmd = self.command_type(line)
            if cmd_type != 'C_RETURN':
                arg1 = self.parse_argument1(cmd_type, cmd)
            else:
                arg1 = None

            if cmd_type in ['C_POP', 'C_PUSH', 'C_FUNCTION', 'C_CALL']:
                arg2 = self.parse_argument2(cmd)
            else:
                arg2 = None
            self.c.constructor(cmd_type, arg1, arg2)

    def command_type(self, line):
        print(line)
        cmd = line.split()
        first_cmd = cmd[0]
        cmd_type = ''
        if first_cmd in self.arithmetic_cmd:
            cmd_type = 'C_ARITHMETIC'
        elif first_cmd == 'push':
            cmd_type = 'C_PUSH'
        elif first_cmd == 'pop':
            cmd_type = 'C_POP'
        elif first_cmd == 'label':
            cmd_type = 'C_LABEL'
        elif first_cmd == 'goto':
            cmd_type = 'C_GOTO'
        elif first_cmd == 'if-goto':
            cmd_type = 'C_IF'
        elif first_cmd == 'function':
            cmd_type = 'C_FUNCTION'
        elif first_cmd == 'return':
            cmd_type = 'C_RETURN'
        elif first_cmd == 'call':
            cmd_type = 'C_CALL'
        return cmd_type, cmd
        



    def parse_argument1(self, cmd_type, cmd):
        if cmd_type == 'C_ARITHMETIC':
            arg1 = cmd[0]
        else:
            arg1 = cmd[1]
        return arg1
    
    def parse_argument2(self, cmd):
        arg2 = int(cmd[2])
        return arg2


    arithmetic_cmd = [
        'add',
        'sub',
        'neg',
        'eq',
        'gt',
        'lt',
        'and',
        'or',
        'not',
    ]

    # memory_access_cmd = [
    #     'push',
    #     'pop',
    # ]

    # branching_cmd = [
    #     'label',
    #     'goto',
    #     'if-goto',
    # ]

    # function_cmd = [
    #     'function',
    #     'call',
    #     'return',
    # ]