import re
import struct

from binaryninja import (
    Architecture, InstructionInfo, RegisterInfo
)

from .operand import Operand
from .operations import NoopOperation, lookup, operations
from .utils import ADDRESS_SIZE as size, safeint

class Synacor(Architecture):
    name = 'Synacor'

    address_size = size
    default_int_size = size
    instr_alignment = 1
    max_instr_length = max([op.size for op in operations])

    regs = {
        'R0': RegisterInfo('R0', size),
        'R1': RegisterInfo('R1', size),
        'R2': RegisterInfo('R2', size),
        'R3': RegisterInfo('R3', size),
        'R4': RegisterInfo('R4', size),
        'R5': RegisterInfo('R5', size),
        'R6': RegisterInfo('R6', size),
        'R7': RegisterInfo('R7', size),

        # Not sure if used, but required by Binary Ninja
        'sp': RegisterInfo('sp', size)
    }
    stack_pointer = 'sp'

    def assemble(self, code, _addr):
        parts = re.split('[ ,]+', code.decode().strip())
        instr = parts.pop(0)
        op_cls = lookup.get(instr) or lookup.get(safeint(instr, 0))
        if op_cls is None:
            raise ValueError("No operation found for '%s'" % instr)

        types = op_cls.operand_types
        if len(parts) != len(types):
            raise ValueError(
                "'%s' requires exactly %d operands" % (op_cls.label, len(types))
            )

        values = [op_cls.opcode]
        for (i, optype) in enumerate(types):
            values.append(Operand.assemble(i, optype, parts[i]))
        return struct.pack('<%iH' % len(values), *values)

    def convert_to_nop(self, data, _addr):
        nop = struct.pack('<1H', NoopOperation.opcode)
        return nop * (len(data) // size)

    def decode(self, data, count, offset=0):
        start = offset * size
        end = start + count * size
        if len(data) < end - start:
            return [None] * count
        return struct.unpack('<%iH' % count, data[start:end])

    def decode_operation(self, data, addr):
        opcode, = self.decode(data, count=1)
        op_cls = lookup.get(opcode)
        if op_cls is None:
            return None

        types = op_cls.operand_types
        values = self.decode(data, count=len(types), offset=1)
        if values is None:
            return None

        operands = [Operand(i, optype, values[i]) for (i, optype) in enumerate(types)]
        return op_cls(self, addr, operands)

    def get_instruction_info(self, data, addr):
        op = self.decode_operation(data, addr)
        if op is None:
            return None

        ii = InstructionInfo()
        ii.length = op.size
        op.branching(ii)
        return ii

    def get_instruction_text(self, data, addr):
        op = self.decode_operation(data, addr)
        if op is None:
            return None

        tokens = []
        op.tokenize(tokens)
        return tokens, op.size

    def get_instruction_low_level_il(self, data, addr, il):
        op = self.decode_operation(data, addr)
        if op is None:
            return None

        op.low_level_il(il)
        return op.size
