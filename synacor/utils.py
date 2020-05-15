ADDRESS_SIZE = 2
LITERAL_MAX = 32767
LITERAL_MODULO = 32768
REGISTER_MAX = 32775

# These flags are for convenience and not Synacor architecture specific
ADDRESS = 0b00000001
CHAR = 0b00000010
NUMBER = 0b00000100
REGISTER = 0b00001000
DYNAMIC = 0b00010000

NOOP = lambda *a, **k: None

def is_literal(value):
    return value <= LITERAL_MAX

def is_register(value):
    return LITERAL_MAX < value <= REGISTER_MAX
