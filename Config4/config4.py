import argparse
import yaml

def assembler(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        code = [eval(line.strip()) for line in f.readlines()]
    bc = []
    log_entries = []
    for line_num, (op, *args) in enumerate(code, start=1):
        try:
            if op == 'loadc':
                if len(args) != 2:
                    raise ValueError(f"Line {line_num}: Expected 2 arguments for 'loadc', got {len(args)}")
                a, b = args
                bc += serializer(55, ((b, 6),), 3)
                log_entries.append(f"loadc a={a} b={b}")

            elif op == 'read':
                if len(args) != 1:
                    raise ValueError(f"Line {line_num}: Expected 1 argument for 'read', got {len(args)}")
                a = args[0]
                bc += serializer(57, ((a, 0),), 3)
                log_entries.append(f"read a={a}")

            elif op == 'write':
                if len(args) != 2:
                    raise ValueError(f"Line {line_num}: Expected 2 arguments for 'write', got {len(args)}")
                a, b = args
                bc += serializer(61, ((b, 6),), 3)
                log_entries.append(f"write a={a} b={b}")

            elif op == 'bswap':
                if len(args) != 1:
                    raise ValueError(f"Line {line_num}: Expected 1 argument for 'bswap', got {len(args)}")
                a = args[0]
                bc += serializer(33, ((a, 0),), 3)
                log_entries.append(f"bswap a={a}")
            else:
                raise ValueError(f"Line {line_num}: Unknown operation '{op}'")
        except ValueError as e:
            print(f"Error in input file: {e}")
            return

    # Write binary output
    with open(output_file, 'wb') as f:
        f.write(bytearray(bc))

    # Write log file as YAML
    with open(log_file, 'w') as f:
        yaml.dump({"log": log_entries}, f, default_flow_style=False)

def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, 'little')

def interpreter(input_file, output_file, mem_range):
    with open(input_file, 'rb') as f:
        bc = f.read()

    memory = [0] * 100  # Увеличенный размер памяти
    accumulator = 0  # Регистр-аккумулятор

    pc = 0
    while pc < len(bc):
        instruction = int.from_bytes(bc[pc:pc+3], 'little')
        pc += 3

        opcode = instruction & 0b111111  # Первые 6 бит — код операции
        # a = (instruction >> 6) & 0b111111
        b = (instruction >> 6) & 0xFFFFF  # Поле B (20 бит)

        if opcode == 55:  # LOADC
            accumulator = b
        elif opcode == 57:  # READ
            if 0 <= accumulator < len(memory):
                accumulator = memory[accumulator]
            else:
                raise ValueError(f"Invalid memory read address: {accumulator}")
        elif opcode == 61:  # WRITE
            if 0 <= b < len(memory):
                memory[b] = accumulator
            else:
                raise ValueError(f"Invalid memory write address: {b}")
        elif opcode == 33:  # BSWAP
            accumulator = ((accumulator & 0xFF) << 24) | \
                          ((accumulator & 0xFF00) << 8) | \
                          ((accumulator & 0xFF0000) >> 8) | \
                          ((accumulator >> 24) & 0xFF)

    memory_output = {f"address_{addr}": memory[addr] for addr in range(mem_range[0], mem_range[1] + 1)}
    with open(output_file, 'w') as f:
        yaml.dump({"memory": memory_output}, f, default_flow_style=False)


def main():
    parser = argparse.ArgumentParser(description='Assembler and Interpreter for a custom VM.')
    subparsers = parser.add_subparsers(dest='command')

    # Assembler arguments
    asm_parser = subparsers.add_parser('assemble', help='Assemble source code into binary')
    asm_parser.add_argument('input_file', help='Path to the input source file')
    asm_parser.add_argument('output_file', help='Path to the output binary file')
    asm_parser.add_argument('log_file', help='Path to the log YAML file')

    # Interpreter arguments
    int_parser = subparsers.add_parser('interpret', help='Interpret binary file')
    int_parser.add_argument('input_file', help='Path to the input binary file')
    int_parser.add_argument('output_file', help='Path to the output YAML file')
    int_parser.add_argument('mem_range', type=int, nargs=2, help='Range of memory to output (start end)')

    args = parser.parse_args()
    if args.command == 'assemble':
        assembler(args.input_file, args.output_file, args.log_file)
    elif args.command == 'interpret':
        interpreter(args.input_file, args.output_file, args.mem_range)


if __name__ == "__main__":
    main()