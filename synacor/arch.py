import struct

from binaryninja.architecture import Architecture
from binaryninja.function import InstructionInfo, RegisterInfo

from .operand import Operand
from .operations import lookup, operations
from .utils import ADDRESS_SIZE as size

class Synacor(Architecture):
    name = 'Synacor'

    address_size = size
    default_int_size = 2
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
        'SP': RegisterInfo('SP', size)
    }
    stack_pointer = 'SP'

    def decode(self, data, count, offset=0):
        start = offset * size
        end = start + count * size
        return struct.unpack('<%iH' % count, data[start:end])

    def decode_operation(self, data, addr):
        opcode = self.decode(data, count=1)[0]
        op_cls = lookup.get(opcode)
        if op_cls is None:
            return None

        types = op_cls.operand_types
        values = self.decode(data, count=len(types), offset=1)
        operands = [Operand(flags, values[i]) for (i, flags) in enumerate(types)]
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
