class SymbolTable(object):

    def add_symbol(self, symbol, label_address=0):
        if label_address == 0:
            self.symbol_table[symbol] = str(self.init_address)
            self.init_address += 1
        else:
            self.symbol_table[symbol] = str(label_address)

    def get_symbol(self, symbol):
        return self.symbol_table[symbol]

    init_address = 16

    symbol_table = {
        "R0": '0',
        "R1": '1',
        "R2": '2',
        "R3": '3',
        "R4": '4',
        "R5": '5',
        "R6": '6',
        "R7": '7',
        "R8": '8',
        "R9": '9',
        "R10": '10',
        "R11": '11',
        "R12": '12',
        "R13": '13',
        "R14": '14',
        "R15": '15',
        "R16": '16',

        "SCREEN": '16384',
        "KBD": '24576',

        "SP": '0',
        "LCL": '1',
        "ARG": '2',
        "THIS": '3',
        "THAT": '4',
    }
