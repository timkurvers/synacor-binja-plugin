from binaryninja.enums import InstructionTextTokenType as TokenType
from binaryninja.function import InstructionTextToken as Token

from .utils import ADDRESS_SIZE as size, classproperty

class Operation(object):
    opcode = None
    label = None
    operand_types = []

    @classproperty
    def size(self):
        return size + len(self.operand_types) * size

    def __init__(self, arch, addr, operands):
        self.arch = arch
        self.addr = addr
        self.operands = operands

    @property
    def next_operation(self):
        return self.addr + self.size

    def branching(self, ii):
        pass

    def low_level_il(self, il):
        il.append(il.unimplemented())

    def operands_to_il(self, il):
        return [operand.to_il(il) for operand in self.operands]

    def tokenize(self, tokens):
        tokens.append(Token(TokenType.AddressDisplayToken, '0x{0:0{1}X}'.format(self.addr, 4)))
        tokens.append(Token(TokenType.TextToken, '  '))
        tokens.append(Token(TokenType.InstructionToken, '{:6}'.format(self.label)))

        for (i, operand) in enumerate(self.operands):
            operand.tokenize(tokens)
            if i < len(self.operands) - 1:
                tokens.append(Token(TokenType.OperandSeparatorToken, ', '))
