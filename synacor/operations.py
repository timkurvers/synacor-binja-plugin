from binaryninja.enums import BranchType

from .operation import Operation
from .utils import (
    ADDRESS_SIZE as size,
    ADDRESS, CHAR, REGISTER, VALUE
)

# halt: 0
#   stop execution and terminate the program
class HaltOperation(Operation):
    opcode = 0
    label = 'halt'

    def branching(self, ii):
        ii.add_branch(BranchType.UnresolvedBranch)

    def low_level_il(self, il):
        il.append(il.no_ret())

# set: 1 a b
#   set register <a> to the value of <b>
class SetOperation(Operation):
    opcode = 1
    label = 'set'
    operand_types = [REGISTER, VALUE]

    def low_level_il(self, il):
        a, b = self.operands_to_il(il)
        il.append(il.set_reg(size, a, b))

# push: 2 a
#   push <a> onto the stack
class StackPushOperation(Operation):
    opcode = 2
    label = 'push'
    operand_types = [VALUE]

    def low_level_il(self, il):
        a, = self.operands_to_il(il)
        il.append(il.push(size, a))

# pop: 3 a
#   remove the top element from the stack and write it into <a>; empty stack = error
class StackPopOperation(Operation):
    opcode = 3
    label = 'pop'
    operand_types = [REGISTER]

    def low_level_il(self, il):
        reg, = self.operands_to_il(il)
        il.append(il.set_reg(size, reg, il.pop(size)))

# eq: 4 a b c
#   set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
class EqualityOperation(Operation):
    opcode = 4
    label = 'eq'
    operand_types = [REGISTER, VALUE, VALUE]

    def low_level_il(self, il):
        a, b, c = self.operands_to_il(il)
        il.append(il.set_reg(size, a, il.compare_equal(size, b, c)))

# gt: 5 a b c
#   set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
class GreaterThanOperation(Operation):
    opcode = 5
    label = 'gt'
    operand_types = [REGISTER, VALUE, VALUE]

    def low_level_il(self, il):
        a, b, c = self.operands_to_il(il)
        il.append(il.set_reg(size, a, il.compare_signed_greater_than(size, b, c)))

# jmp: 6 a
#   jump to <a>
class JumpOperation(Operation):
    opcode = 6
    label = 'jmp'
    operand_types = [ADDRESS]

    def branching(self, ii):
        target, = self.operands
        if target.is_literal:
            ii.add_branch(BranchType.UnconditionalBranch, target.value * size)
        else:
            ii.add_branch(BranchType.UnresolvedBranch)

    def low_level_il(self, il):
        a, = self.operands_to_il(il)
        il.append(il.jump(a))

# jt: 7 a b
#   if <a> is nonzero, jump to <b>
class JumpIfNonzeroOperation(Operation):
    opcode = 7
    label = 'jt'
    operand_types = [VALUE, ADDRESS]

    def branching(self, ii):
        _, target = self.operands
        if target.is_literal:
            ii.add_branch(BranchType.TrueBranch, target.value * size)
        else:
            ii.add_branch(BranchType.UnresolvedBranch)
        ii.add_branch(BranchType.FalseBranch, self.next_operation)

    def low_level_il(self, il):
        a, b = self.operands_to_il(il)
        true_branch = il.get_label_for_address(il.arch, il[b].constant)
        false_branch = il.get_label_for_address(il.arch, self.next_operation)
        il.append(il.if_expr(a, true_branch, false_branch))

# jf: 8 a b
#   if <a> is zero, jump to <b>
class JumpIfZeroOperation(Operation):
    opcode = 8
    label = 'jf'
    operand_types = [VALUE, ADDRESS]

    def branching(self, ii):
        _, target = self.operands
        if target.is_literal:
            ii.add_branch(BranchType.TrueBranch, target.value * size)
        else:
            ii.add_branch(BranchType.UnresolvedBranch)
        ii.add_branch(BranchType.FalseBranch, self.next_operation)

    def low_level_il(self, il):
        a, b = self.operands_to_il(il)
        true_branch = il.get_label_for_address(il.arch, self.next_operation)
        false_branch = il.get_label_for_address(il.arch, il[b].constant)
        il.append(il.if_expr(a, true_branch, false_branch))

# add: 9 a b c
#   assign into <a> the sum of <b> and <c> (modulo 32768)
class AddOperation(Operation):
    opcode = 9
    label = 'add'
    operand_types = [REGISTER, VALUE, VALUE]

    def low_level_il(self, il):
        a, b, c = self.operands_to_il(il)
        il.append(il.set_reg(size, a, il.add(size, b, c)))

# mult: 10 a b c
#   store into <a> the product of <b> and <c> (modulo 32768)
class MultiplyOperation(Operation):
    opcode = 10
    label = 'mult'
    operand_types = [REGISTER, VALUE, VALUE]

    def low_level_il(self, il):
        a, b, c = self.operands_to_il(il)
        il.append(il.set_reg(size, a, il.mult(size, b, c)))

# mod: 11 a b c
#   store into <a> the remainder of <b> divided by <c>
class ModuloOperation(Operation):
    opcode = 11
    label = 'mod'
    operand_types = [REGISTER, VALUE, VALUE]

    def low_level_il(self, il):
        a, b, c = self.operands_to_il(il)
        il.append(il.set_reg(size, a, il.mod_unsigned(size, b, c)))

# and: 12 a b c
#   stores into <a> the bitwise and of <b> and <c>
class AndOperation(Operation):
    opcode = 12
    label = 'and'
    operand_types = [REGISTER, VALUE, VALUE]

    def low_level_il(self, il):
        a, b, c = self.operands_to_il(il)
        il.append(il.set_reg(size, a, il.and_expr(size, b, c)))

# or: 13 a b c
#   stores into <a> the bitwise or of <b> and <c>
class OrOperation(Operation):
    opcode = 13
    label = 'or'
    operand_types = [REGISTER, VALUE, VALUE]

    def low_level_il(self, il):
        a, b, c = self.operands_to_il(il)
        il.append(il.set_reg(size, a, il.or_expr(size, b, c)))

# not: 14 a b
#   stores 15-bit bitwise inverse of <b> in <a>
class NotOperation(Operation):
    opcode = 14
    label = 'not'
    operand_types = [REGISTER, VALUE]

    def low_level_il(self, il):
        a, b = self.operands_to_il(il)
        il.append(il.set_reg(size, a, il.not_expr(size, b)))

# rmem: 15 a b
#   read memory at address <b> and write it to <a>
class ReadMemoryOperation(Operation):
    opcode = 15
    label = 'rmem'
    operand_types = [REGISTER | ADDRESS, VALUE]

# wmem: 16 a b
#   write the value from <b> into memory at address <a>
class WriteMemoryOperation(Operation):
    opcode = 16
    label = 'wmem'
    operand_types = [ADDRESS, VALUE]

# call: 17 a
#   write the address of the next operation to the stack and jump to <a>
class CallOperation(Operation):
    opcode = 17
    label = 'call'
    operand_types = [ADDRESS]

    def branching(self, ii):
        target, = self.operands
        if target.is_literal:
            ii.add_branch(BranchType.CallDestination, target.value * size)
        else:
            ii.add_branch(BranchType.UnresolvedBranch)

    def low_level_il(self, il):
        a, = self.operands_to_il(il)
        il.append(il.call(a))

# ret: 18
#   remove the top element from the stack and jump to it; empty stack = halt
class StackReturnOperation(Operation):
    opcode = 18
    label = 'ret'

    def branching(self, ii):
        ii.add_branch(BranchType.FunctionReturn)

    def low_level_il(self, il):
        il.append(il.ret(il.pop(size)))

# out: 19 a
#   write the character represented by ascii code <a> to the terminal
class OutOperation(Operation):
    opcode = 19
    label = 'out'
    operand_types = [CHAR]

# in: 20 a
#   read a character from the terminal and write its ascii code to <a>;
#   it can be assumed that once input starts, it will continue until a newline
#   is encountered; this means that you can safely read whole lines from the
#   keyboard and trust that they will be fully read
class InOperation(Operation):
    opcode = 20
    label = 'in'
    operand_types = [REGISTER]

# noop: 21
#   no operation
class NoopOperation(Operation):
    opcode = 21
    label = 'noop'

    def low_level_il(self, il):
        il.append(il.nop())

operations = [
    HaltOperation,
    SetOperation,
    StackPushOperation,
    StackPopOperation,
    EqualityOperation,
    GreaterThanOperation,
    JumpOperation,
    JumpIfNonzeroOperation,
    JumpIfZeroOperation,
    AddOperation,
    MultiplyOperation,
    ModuloOperation,
    AndOperation,
    OrOperation,
    NotOperation,
    ReadMemoryOperation,
    WriteMemoryOperation,
    CallOperation,
    StackReturnOperation,
    OutOperation,
    InOperation,
    NoopOperation,
]

lookup = lookup = {op.opcode : op for op in operations}
