#!/usr/bin/env python3
# ------------------------------------------------------------
# 32-bit ISA Simulator - Input Version (Full Operand Support)
# ------------------------------------------------------------
# Supports:
#   mov r1 234
#   mov r2 r1
#   add r1 r2 5
#   sub r1 r2
#   mul r1 43
#   div r4 23
#   end
# ------------------------------------------------------------
from isa32_sim import CPU32
import sys

def parse_operand(token):
    """Return (value, is_register, reg_index)"""
    token = token.strip().lower().rstrip(',')
    if token.startswith('r') and token[1:].isdigit():
        idx = int(token[1:])
        return None, True, idx
    else:
        return int(token), False, None

def get_value(cpu, token):
    val, is_reg, idx = parse_operand(token)
    return cpu.R[idx] if is_reg else val

def execute_instruction(cpu, line):
    parts = line.strip().split()
    if not parts or parts[0].startswith(('#',';')):
        return
    op = parts[0].upper()

    try:
        # MOV supports register or immediate
        if op == 'MOV':
            rd_val, _, rd = parse_operand(parts[1])
            src_val = get_value(cpu, parts[2])
            cpu.MOV(rd, src_val)

        # ADD and SUB accept 2 or 3 operands
        elif op in ('ADD','SUB'):
            _, _, rd = parse_operand(parts[1])
            val2 = get_value(cpu, parts[2])
            if len(parts) > 3:
                val3 = get_value(cpu, parts[3])
            else:
                val3 = val2
            if op == 'ADD':
                cpu.ADD(rd, rd, val3)
            else:
                cpu.SUB(rd, rd, val3)

        # MUL and DIV now accept register or immediate
        elif op == 'MUL':
            _, _, rd = parse_operand(parts[1])
            val = get_value(cpu, parts[2])
            temp_idx = 6  # temp reg
            cpu.MOV(temp_idx, val)
            cpu.MUL(rd, temp_idx)

        elif op == 'DIV':
            _, _, rd = parse_operand(parts[1])
            val = get_value(cpu, parts[2])
            temp_idx = 6  # temp reg
            cpu.MOV(temp_idx, val)
            cpu.DIV(rd, temp_idx)

        elif op in ('END','EXIT'):
            return 'EXIT'

        else:
            print(f"❌ Unknown instruction: {op}")

    except Exception as e:
        print(f"⚠️ Error executing '{line.strip()}': {e}")

def run_interactive():
    print("🧠 32-bit ISA Simulator (Interactive Mode)")
    print("Type 'END' or 'EXIT' to stop.\n")
    cpu = CPU32()
    while True:
        line = input(">> ").strip()
        if not line:
            continue
        if line.upper() in ('EXIT','END'):
            break
        execute_instruction(cpu, line)
    cpu.dump_registers()
    cpu.report()

def run_file(filename):
    print(f"📘 Running from file: {filename}")
    cpu = CPU32()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if execute_instruction(cpu, line) == 'EXIT':
                break
    cpu.dump_registers()
    cpu.report()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_interactive()
