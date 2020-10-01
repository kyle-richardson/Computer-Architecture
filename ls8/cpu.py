"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        pass
        self.pc = 0
        self.ram = {}
        self.reg = [0] * 8

    def load(self):
        """Load a program into memory."""

        address = 0
        arg = sys.argv[1]
        with open(arg, "r") as f:
            for line in f:
                line = line.partition('#')[0]
                line = line.rstrip()
                if line:
                    # print(line)
                    self.ram_write(address, int(line, 2))
                    address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     LDI,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     PRN,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
            self.increment(3)
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
            self.increment(3)
        elif op == LDI:
            self.reg[reg_a] = reg_b
            self.increment(3)
        elif op == PRN:
            print(self.reg[reg_a])
            self.increment(2)
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
            self.increment(3)

        else:
            raise Exception("Unsupported ALU operation")

    def increment(self, num):
        self.pc += num

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, value):
        self.ram[pc] = value

    def run(self):
        while self.ram_read(self.pc) != HLT:
            command = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            # print(f'command: {command},opa: {operand_a}, opb: {operand_b}')
            self.alu(command, operand_a, operand_b)
