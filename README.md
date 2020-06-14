# Synacor plugin for Binary Ninja

![Python Version](https://badgen.net/badge/python/2.x%20&amp;%203.x/green)
[![MIT License](https://badgen.net/github/license/timkurvers/synacor-binja-plugin)](LICENSE.md)
[![CI](https://github.com/timkurvers/synacor-binja-plugin/workflows/ci/badge.svg)](https://github.com/timkurvers/synacor-binja-plugin/actions?query=workflow%3Aci)

![Synacor Binja Plugin](https://user-images.githubusercontent.com/378235/84187615-99c51a80-aa92-11ea-8da1-b9e569e11b5f.png)

[Binary Ninja] architecture plugin supporting Synacor programs from https://challenge.synacor.com.

The [architecture spec] is bundled in this repository.

See [synacor-challenge] for a JavaScript / ES6+ virtual machine capable of running Synacor programs.

# Installation

Clone the plugin to the [Binary Ninja plugin folder] for your platform:

```shell
git clone https://github.com/timkurvers/synacor-binja-plugin.git <binja-plugin-folder>/synacor-binja-plugin
```

Optionally install development dependencies:

```shell
pip install -r requirements.txt
```

# Usage

Soon.

# Debugging

Soon.

[Binary Ninja]: https://binary.ninja/
[Binary Ninja plugin folder]: https://docs.binary.ninja/guide/plugins.html#using-plugins
[GDB Remote Protocol]: https://sourceware.org/gdb/current/onlinedocs/gdb/Remote-Protocol.html
[architecture spec]: https://github.com/timkurvers/synacor-binja-plugin/blob/master/ARCH-SPEC.txt
[synacor-challenge]: https://github.com/timkurvers/synacor-challenge/
