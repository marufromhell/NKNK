import os
import readline
import re
import stat
import files
"""
Complib
This module provides a very basic command line completion library for Python.
GPLv3
email: maru@lithium-dev.xyz (pgp attached)
signal: maru.222
BTC: 16innLYQtz123HTwNLY3vScPmEVP7tob8u
ETH: 0x48994D78B7090367Aa20FD5470baDceec42cAF62 
XMR: 49dNpgP5QSpPDF1YUVuU3ST2tUWng32m8crGQ4NuM6U44CG1ennTvESWbwK6epkfJ6LuAKYjSDKqKNtbtJnU71gi6GrF4Wh
"""
def compile():  # list is the command list if not use globals()
    list = files.read('/home/maru/prog/nknk/cmdlist.txt').splitlines()
    global commands
    commands = list
    comp = Completer()
    readline.set_completer_delims('\t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.complete)
    return commands

RE_SPACE = re.compile('.*\\s+$', re.M)

class Completer(object):

    def _listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            res.append(name)
        return res

    def _complete_path(self, path=None):
        "Perform completion of filesystem path."
        if not path:
            return self._listdir('.')
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
                for p in self._listdir(tmp) if p.startswith(rest)]
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        # exact file match terminates this completion
        return [path + '']

    def complete_extra(self, args):
        "Completions for the 'extra' command."
        if not args:
            # Complete from the current directory if no arguments are provided
            return self._complete_path('.')
        # Treat the last argument as a path and complete it
        return self._complete_path(args[-1])

    def complete(self, text, state):
        "Generic readline completion entry point."
        buffer = readline.get_line_buffer()
        line = buffer.split()
        
        # Show all commands if no input
        if not line:
            matches = [c for c in commands]
            return matches[state] if state < len(matches) else None

        # Handle space at the end of the buffer
        if RE_SPACE.match(buffer):
            line.append('')

        # Resolve command to the implementation function
        cmd = line[0].strip()
        if cmd in commands:
            impl = getattr(self, f'complete_{cmd}', None)
            if impl:
                args = line[1:]  # Pass remaining arguments to the command-specific completer
                matches = impl(args)
                return matches[state] if state < len(matches) else None

        # Fallback: Match commands starting with the input
        if len(line) == 1:  # Only complete directory names if no additional input exists
            matches = [c for c in commands if c.startswith(cmd)]
            if not matches:
                # If no command matches, treat as a path and complete it
                matches = self._complete_path(text)
        else:
            # If additional input exists, only complete based on the last word
            partial_path = line[-1]
            matches = self._complete_path(partial_path)
            # Prepend the rest of the input to the match
            matches = [buffer[:buffer.rfind(partial_path)] + match for match in matches]

        return matches[state] if state < len(matches) else None
