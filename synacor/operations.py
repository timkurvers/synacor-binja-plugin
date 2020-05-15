from binaryninja.enums import InstructionTextTokenType as TokenType
from binaryninja.function import InstructionTextToken as Token

from .utils import (
    ADDRESS_SIZE, LITERAL_MAX, NOOP,
    ADDRESS, CHAR, DYNAMIC, REGISTER,
    is_literal, is_register
)

class Operation(object):
    def __init__(self, opcode, name, operands=None, to_llil=NOOP):
        self.opcode = opcode
        self.name = name
        if operands is None:
            operands = []
        self.operands = operands
        self.to_llil = to_llil

    @property
    def size(self):
        return 2 + len(self.operands) * 2

    def tokenize(self, _arch, _data, addr, tokens, *values):
        tokens.append(Token(TokenType.AddressDisplayToken, '0x{0:0{1}X}'.format(addr, 4)))
        tokens.append(Token(TokenType.TextToken, '  '))
        tokens.append(Token(TokenType.InstructionToken, '{:7}'.format(self.name)))

        for (i, value) in enumerate(values):
            operand = self.operands[i]

            if i != 0:
                tokens.append(
                    Token(TokenType.OperandSeparatorToken, ', ')
                )

            if is_register(value):
                register = 'R%i' % (value - LITERAL_MAX)
                tokens.append(
                    Token(TokenType.RegisterToken, register)
                )
            elif is_literal(value):
                if operand & CHAR:
                    tokens.append(
                        Token(TokenType.CharacterConstantToken, repr(chr(value)))
                    )
                elif operand & ADDRESS:
                    address = value * ADDRESS_SIZE
                    tokens.append(
                        Token(TokenType.PossibleAddressToken, '0x{0:0{1}X}'.format(address, 4))
                    )
                else:
                    tokens.append(
                        Token(TokenType.IntegerToken, str(value))
                    )
            else:
                tokens.append(Token(TokenType.TextToken, '%i (unknown type)' % value))

operations = [
    # halt: 0
    #   stop execution and terminate the program
    Operation(
        opcode=0,
        name='halt',
        to_llil=lambda arch, data, addr, il, *values: (
            il.append(il.no_ret())
        ),
    ),

    # set: 1 a b
    #   set register <a> to the value of <b>
    Operation(
        opcode=1,
        name='set',
        operands=[REGISTER, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # push: 2 a
    #   push <a> onto the stack
    Operation(
        opcode=2,
        name='push',
        operands=[DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # pop: 3 a
    #   remove the top element from the stack and write it into <a>; empty stack = error
    Operation(
        opcode=3,
        name='pop',
        operands=[REGISTER],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # eq: 4 a b c
    #   set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
    Operation(
        opcode=4,
        name='eq',
        operands=[REGISTER, DYNAMIC, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # gt: 5 a b c
    #   set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
    Operation(
        opcode=5,
        name='gt',
        operands=[REGISTER, DYNAMIC, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # jmp: 6 a
    #   jump to <a>
    Operation(
        opcode=6,
        name='jmp',
        operands=[DYNAMIC | ADDRESS],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # jt: 7 a b
    #   if <a> is nonzero, jump to <b>
    Operation(
        opcode=7,
        name='jt',
        operands=[DYNAMIC, DYNAMIC | ADDRESS],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # jf: 8 a b
    #   if <a> is zero, jump to <b>
    Operation(
        opcode=8,
        name='jf',
        operands=[DYNAMIC, DYNAMIC | ADDRESS],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # add: 9 a b c
    #   assign into <a> the sum of <b> and <c> (modulo 32768)
    Operation(
        opcode=9,
        name='add',
        operands=[REGISTER, DYNAMIC, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # mult: 10 a b c
    #   store into <a> the product of <b> and <c> (modulo 32768)
    Operation(
        opcode=10,
        name='mult',
        operands=[REGISTER, DYNAMIC, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # mod: 11 a b c
    #   store into <a> the remainder of <b> divided by <c>
    Operation(
        opcode=11,
        name='mod',
        operands=[REGISTER, DYNAMIC, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # and: 12 a b c
    #   stores into <a> the bitwise and of <b> and <c>
    Operation(
        opcode=12,
        name='and',
        operands=[REGISTER, DYNAMIC, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # or: 13 a b c
    #   stores into <a> the bitwise or of <b> and <c>
    Operation(
        opcode=13,
        name='or',
        operands=[REGISTER, DYNAMIC, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # not: 14 a b
    #   stores 15-bit bitwise inverse of <b> in <a>
    Operation(
        opcode=14,
        name='not',
        operands=[REGISTER, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # rmem: 15 a b
    #   read memory at address <b> and write it to <a>
    Operation(
        opcode=15,
        name='rmem',
        operands=[REGISTER | ADDRESS, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # wmem: 16 a b
    #   write the value from <b> into memory at address <a>
    Operation(
        opcode=16,
        name='wmem',
        operands=[DYNAMIC | ADDRESS, DYNAMIC],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # call: 17 a
    #   write the address of the next Operation to the stack and jump to <a>
    Operation(
        opcode=17,
        name='call',
        operands=[DYNAMIC | ADDRESS],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # ret: 18
    #   remove the top element from the stack and jump to it; empty stack = halt
    Operation(
        opcode=18,
        name='ret',
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # out: 19 a
    #   write the character represented by ascii code <a> to the terminal
    Operation(
        opcode=19,
        name='print',
        operands=[DYNAMIC | CHAR],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # in: 20 a
    #   read a character from the terminal and write its ascii code to <a>;
    #   it can be assumed that once input starts, it will continue until a newline
    #   is encountered; this means that you can safely read whole lines from the
    #   keyboard and trust that they will be fully read
    Operation(
        opcode=20,
        name='prompt',
        operands=[REGISTER],
        to_llil=lambda arch, data, addr, il, *values: (
            il.no_ret()
        ),
    ),

    # noop: 21
    #   no operation
    Operation(
        opcode=21,
        name='noop',
        to_llil=lambda arch, data, addr, il, *values: (
            il.append(il.nop())
        ),
    ),
]

lookup = {op.opcode : op for op in operations}
