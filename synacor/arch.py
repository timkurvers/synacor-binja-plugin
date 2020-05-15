import struct

from binaryninja.architecture import Architecture
from binaryninja.enums import BranchType
from binaryninja.function import InstructionInfo, RegisterInfo

from .operations import lookup, operations
from .utils import ADDRESS_SIZE, is_literal

class Synacor(Architecture):
    name = 'Synacor'

    address_size = ADDRESS_SIZE
    default_int_size = 2
    instr_alignment = 1
    max_instr_length = max([op.size for op in operations])

    regs = {
        'R0': RegisterInfo('R0', 2),
        'R1': RegisterInfo('R1', 2),
        'R2': RegisterInfo('R2', 2),
        'R3': RegisterInfo('R3', 2),
        'R4': RegisterInfo('R4', 2),
        'R5': RegisterInfo('R5', 2),
        'R6': RegisterInfo('R6', 2),
        'R7': RegisterInfo('R7', 2),

        # Not sure if used, but required by Binary Ninja
        'SP': RegisterInfo('SP', 1)
    }
    stack_pointer = 'SP'

    def decode(self, data, offset, count):
        start = offset * ADDRESS_SIZE
        end = start + count * ADDRESS_SIZE
        return struct.unpack('<%iH' % count, data[start:end])

    def get_instruction_info(self, data, addr):
        opcode = self.decode(data, 0, 1)[0]
        op = lookup.get(opcode)
        if op is None:
            return None

        result = InstructionInfo()
        result.length = op.size

        if op.name == 'jmp':
            address = self.decode(data, 1, 1)[0]
            if is_literal(address):
                result.add_branch(BranchType.UnconditionalBranch, address * ADDRESS_SIZE)
            else:
                result.add_branch(BranchType.UnresolvedBranch)
        elif op.name == 'jt':
            _, address = self.decode(data, 1, 2)
            if is_literal(address):
                result.add_branch(BranchType.TrueBranch, address * ADDRESS_SIZE)
            else:
                result.add_branch(BranchType.UnresolvedBranch)
            result.add_branch(BranchType.FalseBranch, addr + op.size)
        elif op.name == 'jf':
            _, address = self.decode(data, 1, 2)
            if is_literal(address):
                result.add_branch(BranchType.TrueBranch, addr + op.size)
            else:
                result.add_branch(BranchType.UnresolvedBranch)
            result.add_branch(BranchType.FalseBranch, address * ADDRESS_SIZE)
        elif op.name == 'call':
            address = self.decode(data, 1, 1)[0]
            if is_literal(address):
                result.add_branch(BranchType.CallDestination, address * ADDRESS_SIZE)
            else:
                result.add_branch(BranchType.UnresolvedBranch)
        elif op.name == 'halt':
            result.add_branch(BranchType.UnresolvedBranch)
        elif op.name == 'ret':
            result.add_branch(BranchType.FunctionReturn)

        return result

    def get_instruction_text(self, data, addr):
        opcode = self.decode(data, 0, 1)[0]
        op = lookup.get(opcode)
        if op is None:
            return None

        values = self.decode(data, 1, len(op.operands))
        tokens = []
        op.tokenize(self, data, addr, tokens, *values)
        return tokens, op.size

    def get_instruction_low_level_il(self, data, addr, il):
        opcode = self.decode(data, 0, 1)[0]
        op = lookup.get(opcode)
        if op is None:
            return None

        values = self.decode(data, 1, len(op.operands))
        op.to_llil(self, data, addr, il, *values)
        return op.size
