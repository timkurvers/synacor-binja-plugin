# pylint: disable = bad-whitespace

ADDRESS_SIZE   = 2
LITERAL_MAX    = 32767
LITERAL_MODULO = 32768
REGISTER_MIN   = 32768
REGISTER_MAX   = 32775

# These operand types are for convenience and not Synacor architecture specific
VALUE    = 'value'
ADDRESS  = 'address'
CHAR     = 'char'
REGISTER = 'register'

def display(value, optype = VALUE, pad_bytes = 2):
    if optype == CHAR:
        return repr(chr(value))
    return '0x{0:0{1}X}'.format(value, pad_bytes * 2)

def safeint(value, base):
    try:
        return int(value, base)
    except ValueError:
        return None

class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)
