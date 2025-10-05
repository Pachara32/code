#!/usr/bin/env python3
# ------------------------------------------------------------
# 32-bit ISA Simulator - Input Version
# ------------------------------------------------------------
# Reads assembly-like instructions from a file or keyboard input
# and executes them using the CPU32 class from isa32_sim.py
# ------------------------------------------------------------
# Author: GPT-5
# ------------------------------------------------------------

from isa32_sim import CPU32
import sys

def parse_operand(operand):
    """Parse register or immediate (e.g., 'r1' or '5')."""
    operand = operand.strip().lower()
    if operand.startswith('r') and operand[1:].isdigit():
        return int(operand[1:]), True  # (register index, is_register)
    else:
        return int(operand), False     # (immediate value, not register)


def execute_instruction(cpu, line):
    """Decode and execute a single line of code."""
    parts = line.strip().split()
    if not parts or parts[0].startswith(('#', ';')):
        return  # comment or blank line

    op = parts[0].upper()

    try:
        if op == 'MOV':
            rd, _ = parse_operand(parts[1].replace(',', ''))
            imm, _ = parse_operand(parts[2])
            cpu.MOV(rd, imm)

        elif op == 'ADD':
            rd, _ = parse_operand(parts[1].replace(',', ''))
            rs, _ = parse_operand(parts[2].replace(',', ''))
            imm, _ = parse_operand(parts[3])
            cpu.ADD(rd, rs, imm)

        elif op == 'SUB':
            rd, _ = parse_operand(parts[1].replace(',', ''))
            rs, _ = parse_operand(parts[2].replace(',', ''))
            imm, _ = parse_operand(parts[3])
            cpu.SUB(rd, rs, imm)

        elif op == 'MUL':
            rd, _ = parse_operand(parts[1].replace(',', ''))
            rs, _ = parse_operand(parts[2])
            cpu.MUL(rd, rs)

        elif op == 'DIV':
            rd, _ = parse_operand(parts[1].replace(',', ''))
            rs, _ = parse_operand(parts[2])
            cpu.DIV(rd, rs)

        elif op == 'EXIT':
            return 'EXIT'

        else:
            print(f"❌ Unknown instruction: {op}")

    except Exception as e:
        print(f"⚠️ Error executing '{line.strip()}': {e}")


def run_interactive():
    """Run in interactive mode (keyboard input)."""
    print("🧠 32-bit ISA Simulator (Interactive Mode)")
    print("Type instructions like: MOV r1, 3 | ADD r1, r1, 5 | MUL r2, r1")
    print("Type EXIT to finish and show results.\n")

    cpu = CPU32()

    while True:
        line = input(">> ").strip()
        if not line:
            continue
        if line.upper() == 'EXIT':
            break
        execute_instruction(cpu, line)

    cpu.dump_registers()
    cpu.report()


def run_file(filename):
    """Run from a file."""
    print(f"📘 Running instructions from file: {filename}")
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cpu = CPU32()
    for line in lines:
        if execute_instruction(cpu, line) == 'EXIT':
            break

    cpu.dump_registers()
    cpu.report()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_interactive()
