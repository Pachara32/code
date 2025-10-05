#!/usr/bin/env python3
# ------------------------------------------------------------
# 32-bit Instruction Set Architecture (ISA) Simulator
# ------------------------------------------------------------
# Requirements satisfied:
# • 32-bit integer operations with two’s complement arithmetic
# • 8 General Purpose Registers (GPRs), each 32-bit
# • Supports opcodes: MOV, ADD, SUB, MUL, DIV
# • Includes simple CPI (Clocks Per Instruction) tracking
# ------------------------------------------------------------
# Author: GPT-5
# ------------------------------------------------------------

MASK32 = 0xFFFFFFFF

def to_signed32(x):
    """Convert unsigned 32-bit to signed 32-bit integer."""
    x &= MASK32
    return x if x < 0x80000000 else x - 0x100000000

def wrap32(x):
    """Wrap integer into 32-bit two’s complement range."""
    return x & MASK32


class CPU32:
    def __init__(self):
        # 8 general purpose 32-bit registers (r0–r7)
        self.R = [0] * 8
        # r7 will serve as HI/REM register for MUL/DIV
        self.cycles = 0
        self.instruction_count = 0

        # CPI per instruction
        self.CPI = {
            "MOV": 1,
            "ADD": 1,
            "SUB": 1,
            "MUL": 3,
            "DIV": 4,
        }

    # -------------------- Core Instructions --------------------

    def MOV(self, rd, imm):
        """Move immediate value to register."""
        self.R[rd] = wrap32(imm)
        self._count("MOV")

    def ADD(self, rd, rs, imm):
        """Add immediate to register."""
        self.R[rd] = wrap32(to_signed32(self.R[rs]) + to_signed32(imm))
        self._count("ADD")

    def SUB(self, rd, rs, imm):
        """Subtract immediate from register."""
        self.R[rd] = wrap32(to_signed32(self.R[rs]) - to_signed32(imm))
        self._count("SUB")

    def MUL(self, rd, rs):
        """Multiply rd * rs → store low 32 bits in rd, high in r7."""
        a = to_signed32(self.R[rd])
        b = to_signed32(self.R[rs])
        result = a * b
        self.R[rd] = wrap32(result)
        self.R[7] = wrap32(result >> 32)
        self._count("MUL")

    def DIV(self, rd, rs):
        """Divide rd by rs → quotient in rd, remainder in r7."""
        dividend = to_signed32(self.R[rd])
        divisor = to_signed32(self.R[rs])
        if divisor == 0:
            raise ZeroDivisionError("Division by zero")
        quotient = int(dividend / divisor)
        remainder = dividend % divisor
        self.R[rd] = wrap32(quotient)
        self.R[7] = wrap32(remainder)
        self._count("DIV")

    # -------------------- Utility Methods --------------------

    def _count(self, op):
        self.cycles += self.CPI[op]
        self.instruction_count += 1

    def dump_registers(self):
        print("\nREGISTER STATE (Signed / Unsigned / Hex):")
        for i, val in enumerate(self.R):
            print(f"r{i}: {to_signed32(val):>12} / {val:>12} / 0x{val:08X}")

    def report(self):
        print("\n--- Performance ---")
        print(f"Instructions executed: {self.instruction_count}")
        print(f"Total cycles:          {self.cycles}")
        if self.instruction_count:
            print(f"Average CPI:           {self.cycles / self.instruction_count:.2f}")


# -------------------- Example Program --------------------

if __name__ == "__main__":
    cpu = CPU32()

    # Example code similar to assignment sheet
    # mov r1, 3
    cpu.MOV(1, 3)

    # add r1, r1, 3
    cpu.ADD(1, 1, 3)

    # mov r2, 2
    cpu.MOV(2, 2)

    # mul r2, r1
    cpu.MUL(2, 1)

    # mov r3, 2
    cpu.MOV(3, 2)

    # div r3, r2
    cpu.DIV(3, 2)

    # Display results
    cpu.dump_registers()
    cpu.report()
