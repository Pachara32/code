#!/usr/bin/env python3
# ------------------------------------------------------------
# 32-bit Instruction Set Architecture (ISA) Simulator
# ------------------------------------------------------------
# Requirements satisfied:
# • 32-bit integer operations with two’s complement arithmetic
# • 8 General Purpose Registers (GPRs), each 32-bit
# • Supports opcodes: MOV, ADD, SUB, MUL, DIV
# • Includes simple CPI (Clocks Per Instruction) tracking
# • Improved safety, structure, and readability
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
    """Simulates a minimal 32-bit CPU with 8 registers and basic arithmetic ISA."""

    def __init__(self):
        # 8 general purpose 32-bit registers (r0–r7)
        self.R = [0] * 8
        # r7 serves as HI/REM register for MUL/DIV
        self.cycles = 0
        self.instruction_count = 0

        # CPI (Clock Cycles Per Instruction)
        self.CPI = {
            "MOV": 1,
            "ADD": 1,
            "SUB": 1,
            "MUL": 3,
            "DIV": 4,
        }

    # -------------------- Core Instructions --------------------

    def MOV(self, rd, imm):
        """Move immediate or register value to rd."""
        self.R[rd] = wrap32(imm)
        self._count("MOV")

    def ADD(self, rd, rs, imm):
        """Add signed 32-bit values."""
        result = to_signed32(self.R[rs]) + to_signed32(imm)
        self.R[rd] = wrap32(result)
        self._count("ADD")

    def SUB(self, rd, rs, imm):
        """Subtract signed 32-bit values."""
        result = to_signed32(self.R[rs]) - to_signed32(imm)
        self.R[rd] = wrap32(result)
        self._count("SUB")

    def MUL(self, rd, rs):
        """Multiply 32-bit signed integers (store HI in r7)."""
        a = to_signed32(self.R[rd])
        b = to_signed32(self.R[rs])
        product = a * b
        self.R[rd] = wrap32(product)
        self.R[7] = wrap32(product >> 32)
        self._count("MUL")

    def DIV(self, rd, rs):
        """Divide 32-bit signed integers (store remainder in r7)."""
        dividend = to_signed32(self.R[rd])
        divisor = to_signed32(self.R[rs])
        if divisor == 0:
            print("⚠️ Division by zero ignored.")
            return
        quotient = int(dividend / divisor)
        remainder = dividend % divisor
        self.R[rd] = wrap32(quotient)
        self.R[7] = wrap32(remainder)
        self._count("DIV")

    # -------------------- Utility Methods --------------------

    def _count(self, op):
        """Increment instruction counters and cycles."""
        self.instruction_count += 1
        self.cycles += self.CPI.get(op, 1)

    def dump_registers(self):
        """Display register contents in signed, unsigned, and hex."""
        print("\nREGISTER STATE (Signed / Unsigned / Hex):")
        for i, val in enumerate(self.R):
            print(f"r{i}: {to_signed32(val):>12} / {val:>12} / 0x{val:08X}")

    def report(self):
        """Display performance summary."""
        print("\n--- Performance ---")
        print(f"Instructions executed: {self.instruction_count}")
        print(f"Total cycles:          {self.cycles}")
        if self.instruction_count:
            print(f"Average CPI:           {self.cycles / self.instruction_count:.2f}")


# -------------------- Example Program --------------------

if __name__ == "__main__":
    cpu = CPU32()

    # Example code similar to assignment sheet
    cpu.MOV(1, 3)          # mov r1, 3
    cpu.ADD(1, 1, 3)       # add r1, r1, 3
    cpu.MOV(2, 2)          # mov r2, 2
    cpu.MUL(2, 1)          # mul r2, r1
    cpu.MOV(3, 2)          # mov r3, 2
    cpu.DIV(3, 2)          # div r3, r2

    cpu.dump_registers()
    cpu.report()
