from binaryninja import CallingConvention

# See: https://github.com/ubuntor/synacor_challenge/blob/main/binja_plugin/__init__.py#L240
class SynacorCallingConvention(CallingConvention):
    caller_saved_regs = ['R0', 'R1', 'R2', 'R3']
    callee_saved_regs = ['R4', 'R5', 'R6', 'R7']
    int_arg_regs = ['R0', 'R1', 'R2', 'R3']
    int_return_reg = 'R0'
