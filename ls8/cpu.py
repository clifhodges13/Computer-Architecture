"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        self.ops = {
            "LDI": 0b10000010,
            "PRN": 0b01000111,
            "MUL": 0b10100010,
            "HLT": 0b00000001,
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        program = []

        if len(sys.argv) != 2:
            print('Please add a filename as a second argument.')
            sys.exit()

        # get the raw instructions
        unformatted_program = []
        with open(sys.argv[1], 'r') as file:
            unformatted_program = file.readlines()

        # format the instructions (remove comments and \n flags)
        for instruction in unformatted_program:
            formatted = instruction.split()
            # print(formatted)

            # if the line is empty or the line is a comment
            if len(formatted) < 1 or formatted[0] == '#':
                continue # just continue to the next loop

            program.append(int(formatted[0], 2))

        # load instructions into the program
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, pc): # read from memory at the pc location
        return self.ram[pc]

    def ram_write(self, pc, value): # write to memory at the pc location
        self.ram[pc] = value
        return self.ram[pc]

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            
            instruction = self.ram_read(self.pc)
            
            if instruction == self.ops["LDI"]: # LDI
                register_number = self.ram_read(self.pc + 1) # get the Register
                value = self.ram_read(self.pc + 2) # get the value to be stored
                self.reg[register_number] = value # set the register to that value
                self.pc += 3 # increment the program counter

            elif instruction == self.ops["PRN"]: # PRN
                register_number = self.ram_read(self.pc + 1) # get the Register
                print(self.reg[register_number]) # print the value in the register
                self.pc += 2 # increment the program counter

            elif instruction == self.ops["MUL"]: # MUL
                reg_a = self.ram_read(self.pc + 1) # get register a
                reg_b = self.ram_read(self.pc + 2) # get register b
                self.alu("MUL", reg_a, reg_b) # multiply value of reg_a times reg_b
                self.pc += 3

            elif instruction == self.ops["HLT"]: # HLT
                self.running = False

            else:
                print(f'Unknown instruction: {instruction}')
                self.pc += 1

