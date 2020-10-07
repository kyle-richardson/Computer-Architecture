"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
JMP = 0b01010100
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001


class CPU:

    def __init__(self):
        self.pc = 0
        self.mutated_pc = False
        self.ram = {}
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.ram[self.reg[7]] = 0
        self.branchtable = {}
        self.branchtable[ADD] = self.handle_add
        self.branchtable[SUB] = self.handle_sub
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_ret

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

    def handle_push(self, a):
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.reg[a]

    def handle_pop(self, a):
        self.reg[a] = self.ram[self.reg[7]]
        self.reg[7] += 1

    def handle_add(self, a, b):
        self.reg[a] += self.reg[b]

    def handle_sub(self, a, b):
        self.reg[a] -= self.reg[b]

    def handle_ldi(self, a, b):
        self.reg[a] = b

    def handle_prn(self, a):
        print(self.reg[a])

    def handle_mul(self, a, b):
        self.reg[a] *= self.reg[b]

    def handle_jmp(self, a):
        self.pc = self.reg[a]

        # prevent auto pc increment
        self.mutated_pc = True

    def handle_call(self, a):
        # push next instruction on stack to return to
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.pc+2

        # change pc to called location
        self.pc = self.reg[a]

        # prevent auto pc increment
        self.mutated_pc = True

    def handle_ret(self):
        self.pc = self.ram[self.reg[7]]
        self.reg[7] += 1

        # prevent auto pc increment
        self.mutated_pc = True

    def alu(self, op):

        if op in self.branchtable:
            num_args = op >> 6
            if num_args == 1:
                self.branchtable[op](self.ram_read(self.pc+1))
            elif num_args == 2:
                self.branchtable[op](self.ram_read(
                    self.pc+1), self.ram_read(self.pc+2))
            else:
                self.branchtable[op]()
            if not self.mutated_pc:
                self.increment(num_args + 1)
            self.mutated_pc = False

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

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, value):
        self.ram[pc] = value

    def run(self):
        while self.ram_read(self.pc) != HLT:
            command = self.ram_read(self.pc)
            self.alu(command)
