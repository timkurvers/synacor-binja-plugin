# pylint: disable = too-many-return-statements

from binaryninja import (
    InstructionTextToken as Token,
    InstructionTextTokenType as TokenType
)

from .utils import (
    ADDRESS_SIZE as size, LITERAL_MAX, REGISTER_MIN, REGISTER_MAX,
    ADDRESS, CHAR, REGISTER,
    display, safeint
)

class Operand(object):
    def __init__(self, index, optype, value):
        self.index = index
        self.type = optype
        self.value = value

    @staticmethod
    def assemble(index, optype, value):
        if optype == REGISTER and not value.startswith('R'):
            raise ValueError("Operand %d expects a register" % index)
        if value.startswith('R'):
            reg = safeint(value[1], 10)
            return REGISTER_MIN + reg
        nr = safeint(value, 0)
        if optype == CHAR and nr is None:
            char = value.strip('"\'')
            if len(char) != 1:
                raise ValueError("Operand %d expects a single char" % index)
            return ord(char)
        if optype == ADDRESS:
            nr /= 2
        return nr

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
            if self.type == CHAR:
                token = Token(TokenType.CharacterConstantToken, display(self.value, CHAR))
            elif self.type == ADDRESS:
                address = self.value * size
                token = Token(TokenType.PossibleAddressToken, display(address))
            else:
                token = Token(TokenType.TextToken, display(self.value, pad_bytes=0))
        if token:
            tokens.append(token)

    def to_il(self, il):
        if self.type == REGISTER:
            if self.is_register:
                return self.register_name
            return None
        if self.type == ADDRESS:
            if self.is_register:
                reg = il.reg(size, self.register_name)
                return il.mult(size, reg, il.const(size, size))
            if self.is_literal:
                return il.const(size, self.value * size)
            return None
        if self.is_register:
            return il.reg(size, self.register_name)
        if self.is_literal:
            return il.const(size, self.value)
        return None
