import sys
from threading import Timer

from .patches import patch_debugger
from .synacor import Synacor, SynacorView

Synacor.register()
SynacorView.register()

# Since plugin load order is undefined, postpone the patching by a few seconds
patch_timeout = Timer(2.0, patch_debugger)
patch_timeout.start()
