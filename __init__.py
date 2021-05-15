import sys
from threading import Timer

from binaryninja import Architecture

from .patches import patch_debugger
from .synacor import Synacor, SynacorCallingConvention, SynacorView

Synacor.register()

# Register calling convention
arch = Architecture[Synacor.name]
cc = SynacorCallingConvention(arch, 'default')
arch.register_calling_convention(cc)
arch.standalone_platform.default_calling_convention = cc

SynacorView.register()

# Since plugin load order is undefined, postpone the patching by a few seconds
patch_timeout = Timer(2.0, patch_debugger)
patch_timeout.start()
