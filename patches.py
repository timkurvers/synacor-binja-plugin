# pylint: disable = line-too-long

import os
import sys

# Patch Synacor support into Vector35's debugger plugin
def patch_debugger():
    # Do nothing if the debugger plugin is not installed
    plugin = sys.modules.get('Vector35_debugger.binjaplug')
    if not plugin:
        return

    def get_module_for_addr(self, remote_address):
        # Synacor programmes start at address 0
        closest_modaddr = -1
        closest_modpath = None
        for (modpath, modaddr) in self:
            if closest_modaddr < modaddr <= remote_address:
                closest_modaddr = modaddr
                closest_modpath = modpath
        return closest_modpath

    def relative_addr_to_absolute(self, rel_addr):
        module = rel_addr['module']
        relative_address = rel_addr['offset']

        if module is not None:
            if self[module] is not None:
                address = self[module] + relative_address
            elif self[os.path.abspath(module)] is not None:
                address = self[os.path.abspath(module)] + relative_address
            elif self[os.path.basename(module)] is not None:
                address = self[os.path.basename(module)] + relative_address
            else:
                raise Exception("Cannot resolve relative address: module {} not loaded".format(module))
        else:
            address = relative_address
        return address

    @property
    def ip(self):
        if not self.connected:
            raise Exception('Cannot read ip when disconnected')
        if self.remote_arch.name == 'x86_64':
            return self.registers['rip']
        if self.remote_arch.name == 'x86':
            return self.registers['eip']
        if self.remote_arch.name in ['aarch64', 'arm', 'armv7', 'Z80']:
            return self.registers['pc']
        if self.remote_arch.name == 'Synacor':
            return self.registers['ip']
        raise NotImplementedError('unimplemented architecture %s' % self.remote_arch.name)

    @property
    def stack_pointer(self):
        if not self.connected:
            raise Exception('Cannot read stack pointer when disconnected')
        if self.remote_arch.name == 'x86_64':
            return self.registers['rsp']
        if self.remote_arch.name == 'x86':
            return self.registers['esp']
        if self.remote_arch.name in ['aarch64', 'arm', 'armv7', 'Z80']:
            return self.registers['sp']
        if self.remote_arch.name == 'Synacor':
            return self.registers['sp']
        raise NotImplementedError('unimplemented architecture %s' % self.remote_arch.name)

    plugin.DebuggerModules.get_module_for_addr = get_module_for_addr
    plugin.DebuggerModules.relative_addr_to_absolute = relative_addr_to_absolute
    plugin.DebuggerState.ip = ip
    plugin.DebuggerState.stack_pointer = stack_pointer
