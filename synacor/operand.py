from binaryninja.enums import InstructionTextTokenType as TokenType
from binaryninja.function import InstructionTextToken as Token

from .utils import (
    ADDRESS_SIZE as size, LITERAL_MAX, REGISTER_MIN, REGISTER_MAX,
    ADDRESS, CHAR, REGISTER,
    display,
)

class Operand(object):
    def __init__(self, flags, value):
        self.flags = flags
        self.value = value

    @property
    def register_name(self):
        if not self.is_register:
            return None
        return 'R%i' % (self.value - REGISTER_MIN)

    @property
    def is_literal(self):
        return self.value <= LITERAL_MAX

    @property
    def is_register(self):
        return REGISTER_MIN <= self.value <= REGISTER_MAX

    def tokenize(self, tokens):
        if self.is_register:
            token = Token(TokenType.RegisterToken, self.register_name)
        elif self.is_literal:
            if self.flags & CHAR:
                token = Token(TokenType.CharacterConstantToken, display(self.value, CHAR))
            elif self.flags & ADDRESS:
                address = self.value * size
                token = Token(TokenType.PossibleAddressToken, display(address))
            else:
                token = Token(TokenType.TextToken, display(self.value, pad_bytes=0))
        if token:
            tokens.append(token)

    def to_il(self, il):
        if self.flags & REGISTER:
            if self.is_register:
                return self.register_name
            return None
        elif self.flags & ADDRESS:
            if self.is_register:
                reg = il.reg(size, self.register_name)
                return il.mult(size, reg, il.const(size, size))
            elif self.is_literal:
                return il.const_pointer(size, self.value * size)
            return None
        if self.is_register:
            return il.reg(size, self.register_name)
        elif self.is_literal:
            return il.const(size, self.value)
        return None
